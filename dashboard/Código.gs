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

/**
 * Função obrigatória para servir o Web App.
 */
function doGet() {
  return HtmlService.createTemplateFromFile('index')
      .evaluate()
      .setTitle('Dashboard Analítico NAF')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Extrai dados de várias planilhas e cria uma base de objetos consolidada.
 * Esta função é "inteligente": ela mapeia o cabeçalho de cada planilha 
 * individualmente antes de processar as linhas.
 * * @return {Array<Object>} Lista de registros higienizados para o frontend.
 */
function obterDadosPlanilha() {
  const propriedades = PropertiesService.getScriptProperties();
  
  // 1. Configuração das fontes (Busca nas Propriedades do Script)
  const fontes = [
    { id: propriedades.getProperty('PLANILHA_ID_1'), aba: propriedades.getProperty('TAB_NOME_1') },
    { id: propriedades.getProperty('PLANILHA_ID_2'), aba: propriedades.getProperty('TAB_NOME_2') },
    { id: propriedades.getProperty('PLANILHA_ID_3'), aba: propriedades.getProperty('TAB_NOME_3') }
  ].filter(f => f.id !== null);

  let registrosConsolidados = [];

  // 2. Loop de Processamento por Planilha
  fontes.forEach((fonte) => {
    try {
      const ss = SpreadsheetApp.openById(fonte.id);
      let sheet;

      // Seleção da aba: Nome específico ou primeira da esquerda [0]
      if (fonte.aba && fonte.aba.trim() !== "") {
        sheet = ss.getSheetByName(fonte.aba);
      } else {
        sheet = ss.getSheets()[0]; 
      }

      if (!sheet) return;

      const values = sheet.getDataRange().getValues();
      if (values.length <= 1) return; // Pula planilhas sem dados

      const cabecalhoLocal = values[0]; // Pega o cabeçalho desta planilha específica
      const linhasDeDados = values.slice(1); // Pega apenas o conteúdo

      /**
       * MAPEAMENTO INTELIGENTE:
       * Transformamos cada linha em um objeto { "Nome da Coluna": "Valor" }
       * baseando-se no cabeçalho desta planilha atual.
       * Isso permite que as colunas estejam em ordens diferentes em cada ID.
       */
      linhasDeDados.forEach((linha) => {
        let registro = {};
        
        cabecalhoLocal.forEach((nomeColuna, i) => {
          // 1. Prevenção: Ignora se a coluna for nula ou vazia
          if (!nomeColuna) return;

          const nomeOriginal = nomeColuna.toString();
          
          // 2. Normalização para o FIREWALL
          const nomeTratado = nomeOriginal.toLowerCase()
            .trim()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

          // 3. FIREWALL COM REGEX (Mais seguro contra falsos positivos)
          // O \b garante que ele procura a palavra exata (ex: " rg "), não pedaços de palavras (ex: "carga")
          const regexProibido = /\b(cpf|cnpj|contribuinte|telefone|celular|email|e-mail|rg|identidade|nascimento|endereco|senha)\b/;

          // Testa se o nome da coluna bate com alguma das palavras proibidas
          if (regexProibido.test(nomeTratado)) {
            return; // Bloqueia e avança para a próxima coluna
          }

          let valor = linha[i];

          // 4. Formatação de Dados
          if (valor instanceof Date) {
            registro[nomeOriginal] = valor.toLocaleDateString('pt-BR');
          } else {
            registro[nomeOriginal] = valor;
          }
        });

        // Só adiciona se o objeto não estiver vazio (garante que temos dados)
        if (Object.keys(registro).length > 0) {
          registro["rowId"] = registrosConsolidados.length + 2;
          registrosConsolidados.push(registro);
        }
      });

    } catch (e) {
      console.error(`Erro ao processar planilha ${fonte.id}: ${e.message}`);
    }
  });

  // Retorna o "pacotão" de objetos prontos para os filtros do seu index.html
  return registrosConsolidados;
}