function doGet() {
  return HtmlService.createTemplateFromFile('index')
      .evaluate()
      .setTitle('Dashboard NAF - Analytics')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// A função que o seu front-end (HTML) chama para puxar os dados
function obterDadosPlanilha() {
  // 1. Chama o serviço de "cofre" do Google
  const propriedades = PropertiesService.getScriptProperties();
  
  // 2. Pega o valor secreto que você salvou nas configurações
  const idSecreto = propriedades.getProperty('PLANILHA_ID');
  
  // 3. Abre a planilha usando a variável (sem chumbamento no código!)
  const ss = SpreadsheetApp.openById(idSecreto);
  // Substitua o nome entre aspas pelo nome exato que está na aba da sua planilha
  const sheet = ss.getSheetByName("Página2"); 
  const values = sheet.getDataRange().getValues();
  
  if (values.length <= 1) return []; 
  
  const cabecalho = values[0];
  
  // Firewall (Lista de Proibição)
  const colunasProibidas = ["NOME DO CONTRIBUINTE", "CPF"];
  const indicesProibidos = colunasProibidas
    .map(nome => cabecalho.indexOf(nome))
    .filter(indice => indice !== -1);
  
  const rows = values.slice(1);
  
  return rows.map(function(row, index) {
    let novaLinha = {};
    cabecalho.forEach(function(colNome, i) {
      if (!indicesProibidos.includes(i)) { 
        if (row[i] instanceof Date) {
          novaLinha[colNome] = row[i].toLocaleDateString('pt-BR');
        } else {
          novaLinha[colNome] = row[i];
        }
      }
    });
    
    novaLinha["rowId"] = index + 2; 
    return novaLinha;
  });
}