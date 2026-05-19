# 📊 Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

## 📂 Estrutura do Projeto

O projeto foi construído com foco em segurança e estabilidade, utilizando **zero dependências externas (CDNs)**. Todos os scripts e estilos são injetados localmente pelo servidor do Google.

* **Frontend:** [`index.html`](https://www.google.com/search?q=index.html) — Interface principal em HTML5/JS com Tailwind CSS embutido.
* **Backend:** [`Código.gs`](https://www.google.com/search?q=C%C3%B3digo.gs) — Motor de processamento, sanitização e consolidação de dados em Google Apps Script (GAS).
* **Dependências Locais (Injetadas no HTML):**
    * `Lib_ChartJS.html` — Biblioteca Chart.js (Renderização dos gráficos).
    * `Lib_DataLabels.html` — Plugin ChartDataLabels (Exibição dos números nas barras/pizzas).


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

* **[Manual do Usuário](wiki/guia-usuário.md)** — Guia do Dashboard para usuários finais.
* **[Gestão do Dicionário de Categorias](wiki/dicionario.md)** — Como alterar ou adicionar novos tipos de serviços no Dashboard.
* **[Mapeamento de Cabeçalhos](wiki/cabecalho.md)** — Como o script identifica as colunas da planilha através de palavras-chave.
* **[Conexão de Dados e IDs](wiki/dados.md)** — Tutorial de como encontrar IDs e conectar novas planilhas.
* **[Consolidação de Múltiplas Abas](wiki/multiplas-abas.md)** — Como somar dados de diferentes páginas de um mesmo arquivo.
* **[Guia de Atualização (Deploy)](wiki/atualizaçao.md)** — Como publicar novas versões do código sem quebrar o link público.
* **[Guia Gerador Python](wiki/gerador-python.md)** — Tutorial de como usar o `gerador-csv.py`.
* **[Firewall](wiki/firewall.md)** — Bloqueio de palavras chaves no Backend.
* **[Regras de negócio](wiki/regras-de-negocio.md)** — Este documento compila as "travas lógicas" do código, como a conversão de géneros, faixas etárias, aglomeração do campo "Outros" e o cálculo dos KPIs.


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