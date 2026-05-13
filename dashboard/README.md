# 📊 Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

Dashboard interativo de alta performance desenvolvido como uma *Single Page Application* (SPA) para consolidar, tratar e visualizar dados de atendimentos do NAF provenientes do Google Forms.

O sistema utiliza uma **Arquitetura Serverless**, operando de forma independente como um Web App através do Google Apps Script.

## 📂 Estrutura do Projeto

* **Frontend:** [index.html](index.html) — Interface em HTML5/JS com Tailwind CSS e Chart.js.
* **Backend:** [Código.gs](Código.gs) — Motor de processamento em Google Apps Script (GAS).

* **Ferramentas de Dados:**
* [gerador-csv.py](gerador-csv.py) — Script Python para geração de dados sintéticos para testes.


* **Documentação:** [wiki](wiki) — Manuais detalhados de manutenção e configuração.



## 🚀 Funcionalidades Principais

* **Consolidação Multi-Planilhas:** Une dados de múltiplos formulários automaticamente.
* **Firewall LGPD:** Bloqueia dados sensíveis (Nome e CPF) no servidor antes do envio ao navegador.
* **Mapeamento Inteligente:** Localiza dados por palavras-chave, ignorando a ordem das colunas na planilha.
* **Desmembramento de Serviços:** Contabiliza individualmente múltiplos serviços marcados em um único atendimento.
* **Filtros Dinâmicos:** Cruzamento de dados por Ano, Mês, Município, Gênero e Status de Atendimento.



## ⚙️ Configuração e Instalação

O processo de instalação é feito diretamente no portal do Google Apps Script. Para um passo a passo completo, consulte:

👉 **[Guia de Instalação e Deploy](wiki/atualizaçao.md)**

### Resumo de Configuração (Propriedades do Script)

No portal GAS, configure as IDs das suas planilhas em "Configurações do Projeto":

* `PLANILHA_ID_1`: ID da planilha principal.
* `TAB_NOME_1`: (Opcional) Nome da aba específica.



## 📖 Documentação Técnica (Wiki)

Para garantir a manutenção de longo prazo e a escalabilidade do projeto, consulte os manuais específicos abaixo:

* **[Gestão do Dicionário de Categorias](wiki/dicionario.md)** — Como alterar ou adicionar novos tipos de serviços no Dashboard.
* **[Mapeamento de Cabeçalhos](wiki/cabecalho.md)** — Como o script identifica as colunas da planilha através de palavras-chave.
* **[Conexão de Dados e IDs](wiki/dados.md)** — Tutorial de como encontrar IDs e conectar novas planilhas.
* **[Consolidação de Múltiplas Abas](wiki/multiplas-abas.md)** — Como somar dados de diferentes páginas de um mesmo arquivo.
* **[Guia de Atualização (Deploy)](wiki/atualizaçao.md)** — Como publicar novas versões do código sem quebrar o link público.
* **[Guia de Atualização (Deploy)](wiki/gerador-python.md)** — Tutorial de como usar o `gerador-csv.py`.


## 🔒 Segurança e Privacidade (Privacy by Design)

O sistema foi construído para ser resiliente a vazamentos de dados:

1. **Backend (GAS):** Filtra e remove colunas de identificação pessoal (CPF, Nome) antes da transmissão.
2. **Acesso:** O controle de acesso aos dados brutos permanece sob a gestão das permissões de compartilhamento do Google Drive do proprietário.



## ⚡ Stack Tecnológica

* **Linguagem:** JavaScript (ES6+), Google Apps Script (V8).
* **Frontend:** [Tailwind CSS](https://tailwindcss.com/) (Estilização) e [Chart.js](https://www.chartjs.org/) (Gráficos).
* **Dados:** JSON dinâmico via `google.script.run`.
* **Testes:** Python para geração de volumes massivos de dados sintéticos.



### 🔄 Como atualizar o código?

Sempre que editar o [index.html](index.html) ou o [Código.gs](Código.gs), você deve criar uma **Nova Versão** em `Implantar > Gerenciar implantações` para que as mudanças fiquem públicas.