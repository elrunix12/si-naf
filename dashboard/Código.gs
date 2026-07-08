/*
 * Dashboard NAF
 * Copyright (C) 2026  elrunix12
 *
 * Este programa é um software livre: você pode redistribuí-lo e/ou modificá-lo
 * sob os termos da GNU Affero General Public License, versão 3 (AGPLv3),
 * conforme publicada pela Free Software Foundation.
 *
 * Este programa é distribuído na esperança de que seja útil,
 * mas SEM NENHUMA GARANTIA; sem mesmo a garantia implícita de
 * COMERCIALIZAÇÃO ou ADEQUAÇÃO A UM DETERMINADO PROPÓSITO.
 *
 * Veja o arquivo LICENSE para mais detalhes.
 */

/**
 * @fileoverview Backend do Dashboard NAF (Google Apps Script)
 * Consolida múltiplas fontes de dados de forma inteligente e segura.
 */

function doGet() {
  return HtmlService.createTemplateFromFile('index')
      .evaluate()
      .setTitle('Dashboard Analítico NAF')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Extrai dados de várias planilhas e cria uma base de objetos consolidada.
 * Otimizada para alta performance usando filtragem prévia de colunas (Index Mapping).
 *
 * @return {Array<Object>} Lista de registros higienizados para o frontend.
 */
function obterDadosPlanilha() {
  const propriedades = PropertiesService.getScriptProperties();

  // 1. Configuração das fontes de dados
  const fontes = [
    { id: propriedades.getProperty('PLANILHA_ID_1'), aba: propriedades.getProperty('TAB_NOME_1') },
    { id: propriedades.getProperty('PLANILHA_ID_2'), aba: propriedades.getProperty('TAB_NOME_2') },
    { id: propriedades.getProperty('PLANILHA_ID_3'), aba: propriedades.getProperty('TAB_NOME_3') }
  ].filter(f => f.id !== null);

  const saltHash = propriedades.getProperty('SALT_HASH_CPF') || "Chave_Padrao_Temporaria_NAF_2026";
  let registrosConsolidados = [];

  const regexProibido = /\b(cpf|cnpj|contribuinte|telefone|celular|email|e-mail|rg|identidade|nascimento|endereco|senha|nome)\b/;

  // 2. Loop de Processamento por Planilha
  fontes.forEach((fonte) => {
    try {
      const ss = SpreadsheetApp.openById(fonte.id);
      let sheet = fonte.aba && fonte.aba.trim() !== "" ? ss.getSheetByName(fonte.aba) : ss.getSheets()[0];

      if (!sheet) return;

      const values = sheet.getDataRange().getValues();
      if (values.length <= 1) return;

      const cabecalhoLocal = values[0];
      const linhasDeDados = values.slice(1);

      // ==========================================
      // ESTRATÉGIA SEGURA: MAPEAMENTO DE INJEÇÃO
      // ==========================================
      // Descobrimos os índices das colunas uma única vez antes de ler as linhas.
      let indiceCpf = -1;
      const colunasPermitidas = [];

      cabecalhoLocal.forEach((nomeColuna, i) => {
        if (!nomeColuna) return;

        const nomeOriginal = nomeColuna.toString();
        const nomeTratado = nomeOriginal.toLowerCase().trim()
          .normalize("NFD").replace(/[\u0300-\u036f]/g, "");

        // Se for a coluna de CPF, memoriza o índice dela
        if (nomeTratado === 'cpf' || nomeTratado.includes('cpf')) {
          indiceCpf = i;
          return;
        }

        // Se não for uma coluna proibida pelo Filtro de Colunas Sensíveis, memoriza para leitura em lote
        if (!regexProibido.test(nomeTratado)) {
          colunasPermitidas.push({
            nomeOriginal: nomeOriginal,
            index: i
          });
        }
      });

      // 3. Processamento Ultra Rápido das Linhas
      linhasDeDados.forEach((linha) => {
        let registro = {};

        // Tratamento isolado e seguro do CPF (com correção de zero à esquerda)
        if (indiceCpf !== -1) {
          const valorCpf = linha[indiceCpf];
          const cpfLimpo = String(valorCpf || "").replace(/\D/g, '').padStart(11, '0');

          if (cpfLimpo.length === 11) {
            registro['usuarioHash'] = gerarHashAnonimo(cpfLimpo, saltHash);
          }
        }

        // Processa apenas as colunas previamente aprovadas pelo mapa
        colunasPermitidas.forEach((col) => {
          const valor = linha[col.index];

          if (valor instanceof Date) {
            registro[col.nomeOriginal] = valor.toLocaleDateString('pt-BR');
          } else {
            registro[col.nomeOriginal] = valor;
          }
        });

        // Adiciona o registro se ele contiver informações válidas
        if (Object.keys(registro).length > 0) {
          registro["rowId"] = registrosConsolidados.length + 2;
          registrosConsolidados.push(registro);
        }
      });

    } catch (e) {
      console.error(`Erro ao processar planilha ${fonte.id}: ${e.message}`);
    }
  });

  return registrosConsolidados;
}

/**
 * Gera um hash irreversível SHA-256 de forma segura (Pseudonimização).
 */
function gerarHashAnonimo(cpf, salt) {
  const textoParaHashear = cpf + salt;
  const signature = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, textoParaHashear);
  let hexString = '';
  for (let i = 0; i < signature.length; i++) {
    let byte = signature[i];
    if (byte < 0) byte += 256;
    let hex = byte.toString(16);
    if (hex.length === 1) hex = '0' + hex;
    hexString += hex;
  }
  return hexString;
}
