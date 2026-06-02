/**
 * Backend do Visualizador NAF
 * Lê as planilhas e envia os dados brutos (incluindo dados nominais) para o frontend.
 */
function doGet() {
  return HtmlService.createTemplateFromFile('index')
      .evaluate()
      .setTitle('Visualizador de Contribuintes NAF')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function obterDadosPlanilha() {
  const propriedades = PropertiesService.getScriptProperties();
  const fontes = [
    { id: propriedades.getProperty('PLANILHA_ID_1'), aba: propriedades.getProperty('TAB_NOME_1') },
    { id: propriedades.getProperty('PLANILHA_ID_2'), aba: propriedades.getProperty('TAB_NOME_2') },
    { id: propriedades.getProperty('PLANILHA_ID_3'), aba: propriedades.getProperty('TAB_NOME_3') },
    { id: propriedades.getProperty('PLANILHA_ID_4'), aba: propriedades.getProperty('TAB_NOME_4') },
    { id: propriedades.getProperty('PLANILHA_ID_5'), aba: propriedades.getProperty('TAB_NOME_5') }
  ].filter(f => f.id !== null);

  let registrosConsolidados = [];

  fontes.forEach((fonte) => {
    try {
      const ss = SpreadsheetApp.openById(fonte.id);
      let sheet;
      
      if (fonte.aba && fonte.aba.trim() !== "") {
        sheet = ss.getSheetByName(fonte.aba.trim());
      } else {
        sheet = ss.getSheets()[0]; 
      }

      if (!sheet) return;

      const values = sheet.getDataRange().getValues();
      if (values.length <= 1) return; // Pula se só tiver o cabeçalho

      const cabecalhoLocal = values[0]; 
      const linhasDeDados = values.slice(1); 

      linhasDeDados.forEach((linha) => {
        let registro = {};
        let linhaTemDado = false;

        cabecalhoLocal.forEach((nomeColuna, i) => {
          const nomeLimpo = nomeColuna.toString().trim();
          if (!nomeLimpo) return;

          let valor = linha[i];
          if (valor !== "" && valor !== null) linhaTemDado = true;

          // Formatação de Datas
          if (valor instanceof Date) {
            registro[nomeLimpo] = valor.toLocaleDateString('pt-BR');
          } else {
            registro[nomeLimpo] = valor;
          }
        });

        if (linhaTemDado) {
          registrosConsolidados.push(registro);
        }
      });

    } catch (e) {
      console.error(`Erro ao processar planilha ${fonte.id}: ${e.message}`);
    }
  });

  return registrosConsolidados;
}