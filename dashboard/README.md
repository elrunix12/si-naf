# 📊 Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

Este projeto é uma aplicação web desenvolvida em Google Apps Script para transformar respostas de formulários do NAF em indicadores visuais de atendimento.

O Dashboard consolida dados vindos de Planilhas Google, aplica regras de padronização e privacidade, e apresenta os resultados em gráficos e KPIs interativos para apoio à gestão do núcleo.

Fluxo geral:

```text
Google Forms → Planilhas Google → Google Apps Script → Dashboard
```

## 📂 Estrutura do Projeto

O projeto foi construído com foco em segurança e estabilidade, utilizando **zero dependências externas (CDNs)**. Todos os scripts, estilos e bibliotecas são injetados localmente pelo servidor do Google Apps Script.

* **Frontend:** [`index.html`](index.html) — Interface principal em HTML5/JavaScript, responsável pela estrutura da página, filtros, abas, KPIs e renderização dos gráficos.

* **Estilos Locais:** [`style.html`](style.html) — Arquivo injetado no `index.html`, contendo o Tailwind CSS compilado localmente e regras visuais específicas do Dashboard.

* **Backend:** [`Código.gs`](Código.gs) — Motor de processamento, sanitização, consolidação e entrega dos dados em Google Apps Script (GAS).

* **Dependências Locais (Injetadas no HTML):**

  * `Lib_ChartJS.html` — Biblioteca Chart.js, usada para renderização dos gráficos.
  * `Lib_DataLabels.html` — Plugin ChartDataLabels, usado para exibição opcional dos valores nos gráficos.

* **Ferramentas de Dados:**

  * [`gerador-csv.py`](gerador-csv.py) — Script Python para geração de dados sintéticos para testes.

* **Documentação:** [`wiki`](wiki) — Manuais detalhados de uso, manutenção e configuração.

## 🚀 Funcionalidades Principais

* **Consolidação Multi-Planilhas:** Une dados de múltiplos formulários automaticamente.
* **Firewall LGPD:** Bloqueia dados sensíveis, como Nome e CPF, no servidor antes do envio ao navegador.
* **Anonimização de CPF:** Utiliza hash para permitir análise de retorno dos contribuintes sem expor o CPF original.
* **Mapeamento Inteligente:** Localiza dados por palavras-chave, ignorando a ordem das colunas na planilha.
* **Validação de Datas:** Rejeita datas inexistentes, futuras ou anteriores ao limite mínimo configurado.
* **Estimativa por Mediana:** Quando a Data de Atendimento está inválida, o sistema pode estimar uma data provável com base no histórico de atraso entre atendimento e lançamento no formulário.
* **Controle de Datas Estimadas:** Permite ocultar ou exibir registros com datas estimadas nos indicadores e gráficos.
* **Desmembramento de Serviços:** Contabiliza individualmente múltiplos serviços marcados em um único atendimento.
* **Filtros Dinâmicos:** Cruzamento de dados por Ano, Mês, Município, Gênero, Status de Atendimento e outros filtros específicos por aba.
* **Gráficos Interativos:** Exibição opcional de valores nos gráficos e detalhamento da categoria “Outros”.

## ⚙️ Configuração e Instalação

O processo de instalação é feito diretamente no portal do Google Apps Script. Para um passo a passo completo, consulte:

👉 **[Guia de Instalação e Deploy](wiki/atualizaçao.md)**

### Resumo de Configuração (Propriedades do Script)

No portal GAS, configure as IDs das suas planilhas em **Configurações do Projeto**:

* `PLANILHA_ID_1`: ID da planilha principal.
* `TAB_NOME_1`: nome da aba específica, se aplicável.
* `PLANILHA_ID_2` / `TAB_NOME_2`: usados caso exista uma segunda fonte de dados.
* `PLANILHA_ID_3` / `TAB_NOME_3`: usados caso exista uma terceira fonte de dados.
* `SALT_HASH_CPF`: chave usada para gerar o hash anonimizado dos CPFs.

## 📖 Documentação Técnica (Wiki)

Para garantir a manutenção de longo prazo e a escalabilidade do projeto, consulte os manuais específicos abaixo:

* **[Manual do Usuário](wiki/guia-usuário.md)** — Guia do Dashboard para usuários finais.
* **[Gestão do Dicionário de Categorias](wiki/dicionario.md)** — Como alterar ou adicionar novos tipos de serviços no Dashboard.
* **[Mapeamento de Cabeçalhos](wiki/cabecalho.md)** — Como o script identifica as colunas da planilha através de palavras-chave.
* **[Conexão de Dados e IDs](wiki/dados.md)** — Tutorial de como encontrar IDs e conectar novas planilhas.
* **[Consolidação de Múltiplas Abas](wiki/multiplas-abas.md)** — Como somar dados de diferentes páginas de um mesmo arquivo.
* **[Guia de Atualização (Deploy)](wiki/atualizaçao.md)** — Como publicar novas versões do código sem quebrar o link público.
* **[Guia Gerador Python](wiki/gerador-python.md)** — Tutorial de como usar o `gerador-csv.py`.
* **[Firewall](wiki/firewall.md)** — Bloqueio de palavras-chave e remoção de dados sensíveis no Backend.
* **[Regras de Negócio](wiki/regras-de-negocio.md)** — Documento com as travas lógicas do código, como validação de datas, estimativa por mediana, conversão de gêneros, faixas etárias, aglomeração do campo “Outros” e cálculo dos KPIs.

## 🔒 Segurança e Privacidade (Privacy by Design)

O sistema foi construído para ser resiliente a vazamentos de dados:

1. **Backend (GAS):** filtra e remove colunas de identificação pessoal, como Nome e CPF, antes da transmissão para o navegador.
2. **Anonimização:** o CPF não é enviado ao frontend. Em seu lugar, o sistema utiliza um hash para permitir a análise de retorno dos contribuintes sem expor o dado original.
3. **Acesso:** o controle de acesso aos dados brutos permanece sob a gestão das permissões de compartilhamento do Google Drive do proprietário.
4. **Dependências Locais:** o projeto não utiliza CDNs externas; bibliotecas, scripts e estilos são servidos localmente pelo Apps Script.

## ⚡ Stack Tecnológica

* **Linguagem:** JavaScript (ES6+) e Google Apps Script (V8).
* **Frontend:** HTML5, JavaScript Vanilla, Tailwind CSS compilado localmente e Chart.js.
* **Estilos:** `style.html`, injetado localmente no `index.html`.
* **Dados:** JSON dinâmico via `google.script.run`.
* **Testes:** Python para geração de volumes massivos de dados sintéticos.

## 🔄 Como atualizar o código?

Sempre que editar arquivos do projeto, publique uma nova versão no Google Apps Script para que as mudanças fiquem disponíveis no link público.

Arquivos que normalmente exigem nova versão após alteração:

* `index.html`
* `style.html`
* `Código.gs`
* `Lib_ChartJS.html`
* `Lib_DataLabels.html`

No Apps Script, acesse:

```text
Implantar > Gerenciar implantações > Editar > Nova versão
```

Depois, salve a implantação para publicar as alterações.
