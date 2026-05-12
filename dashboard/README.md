Aqui está o **README.md** consolidado. Reuni a estrutura detalhada e o passo a passo que você enviou no arquivo com os aprofundamentos técnicos e de segurança da nossa conversa anterior.

O resultado é uma documentação robusta, ideal para apresentar o projeto formalmente ou deixá-lo como legado para outros desenvolvedores/alunos.

---

# 📊 Dashboard Analítico NAF (Núcleo de Apoio Contábil e Fiscal)

Dashboard interativo de alta performance desenvolvido em *Single Page Application (SPA)* para analisar e visualizar os dados de atendimentos registrados nas planilhas do NAF.

A ferramenta foi construída com uma **Arquitetura Serverless (100% em Nuvem)**, integrando-se nativamente e em tempo real aos formulários do Google (Google Forms) através do Google Apps Script, atuando como um Web App independente.

---

## 🚀 Principais Funcionalidades e Diferenciais

* **Consolidação Inteligente Multi-Planilhas:** Capacidade de unir dados de múltiplos formulários (IDs diferentes) de forma transparente e automática em um único painel.
* **Firewall de Privacidade (Adequação LGPD):** Backend configurado para interceptar e bloquear o tráfego de dados sensíveis.
* **Mapeamento Inteligente de Colunas:** O sistema rastreia as respostas com base em palavras-chave no cabeçalho. A ordem das perguntas no formulário não importa, permitindo alterações no Forms sem quebrar o painel.
* **Hierarquia Temporal Inteligente:** Lógica de *fallback* que prioriza automaticamente a "Data de Atendimento" real inserida pelo aluno, utilizando o "Carimbo de data/hora" apenas como plano B de segurança para evitar dados órfãos.
* **Desmembramento de Atendimentos Múltiplos:** Identifica quando o usuário seleciona múltiplos serviços no formulário e os contabiliza de forma individualizada, sem distorcer o número total de pessoas físicas atendidas.
* **Filtros Dinâmicos Multi-nível:** Análise granular através de filtros combinados globais (`Ano`, `Mês`, `Município`) e locais (`Público`, `Conclusão`, `Serviço`, `Gênero`).
* **Resiliência de Abas:** O sistema prioriza a primeira aba de cada planilha automaticamente (padrão do Forms), mas permite a definição de abas específicas via configurações.

---

## 🔒 Segurança e Privacidade

Este projeto foi desenhado sob o princípio de *Privacy by Design*:

* **Zero Transmissão Sensível:** O loop de processamento no Google Apps Script identifica colunas de identificação pessoal (`CPF` e `NOME DO CONTRIBUINTE`) e as remove da memória antes de gerar o pacote JSON. Essas informações **jamais chegam ao navegador do usuário**.
* **Isolamento de Ambiente:** O acesso aos dados brutos continua sendo controlado estritamente pelas permissões de compartilhamento do Google Drive de quem implantou o script.

---

## ⚙️ Configuração e Implantação (Web App)

Diferente de scripts comuns vinculados a uma única planilha, este dashboard é um sistema independente. Siga os passos abaixo para configurá-lo:

### Passo 1: Criar o Projeto no Google Apps Script

1. Acesse o portal [script.google.com](https://script.google.com/).
2. Clique em **+ Novo Projeto**.
3. Renomeie o projeto para `Dashboard Analítico NAF`.

### Passo 2: Inserir o Código

1. No editor, você verá um arquivo chamado `Código.gs`. Apague o conteúdo existente e cole o código do **backend** (o "motor" que processa as planilhas).
2. Clique no ícone de **+** (ao lado de Arquivos) e escolha a opção **HTML**.
3. Nomeie este arquivo exatamente como `index` (o Google adicionará a extensão `.html` automaticamente).
4. Apague o conteúdo padrão e cole todo o código do seu **frontend** (HTML/CSS/JS).
5. Clique no ícone de **Salvar** (disquete).

### Passo 3: Configurar o "Banco de Dados" (Propriedades do Script)

Para que o dashboard saiba de onde puxar as informações sem que você precise editar o código fonte, usaremos as variáveis de ambiente:

1. No menu lateral esquerdo, clique no ícone de **Engrenagem** (Configurações do projeto).
2. Role até o final da página e clique em **Adicionar propriedade do script**.
3. Adicione os mapeamentos abaixo conforme a sua necessidade:

| Propriedade | Valor Sugerido | Descrição |
| --- | --- | --- |
| `PLANILHA_ID_1` | `1BxiMVs0XRA...` | O código longo encontrado na URL da sua planilha principal. |
| `TAB_NOME_1` | `Respostas 1` | **(Opcional)** Nome exato da aba. Se vazio, o script puxa a **1ª aba**. |
| `PLANILHA_ID_2` | `1xyz987abc...` | ID de um segundo formulário para consolidar os dados. |

4. Clique em **Salvar propriedades do script**.

### Passo 4: Implantação (Deploy)

1. No canto superior direito, clique em **Implantar > Nova implantação**.
2. Clique na engrenagem ao lado de "Selecione o tipo" e selecione **App da Web**.
3. **Descrição:** "Versão Inicial".
4. **Executar como:** "Eu" (sua conta).
5. **Quem tem acesso:** "Qualquer pessoa com uma conta do Google" (ou restrinja ao seu domínio institucional).
6. Clique em **Implantar**.
7. O Google solicitará que você autorize o acesso aos seus dados. Conceda as permissões necessárias.
8. Ao final, você receberá uma **URL do App da Web**. Este é o link oficial do seu Dashboard.

---

## 📋 Estrutura Exigida no Formulário (Forms)

O script busca palavras-chave específicas no cabeçalho das planilhas para cruzar os dados. O cabeçalho deve conter obrigatoriamente as seguintes raízes textuais (a ordem das colunas não importa):

| Informação Desejada | Palavra-chave obrigatória no cabeçalho | Exemplo de Pergunta no Forms |
| --- | --- | --- |
| **Data** | `Data de Atendimento` ou `Carimbo` | *Data de Atendimento* |
| **Idade** | `IDADE` | *Qual a sua idade?* |
| **Gênero/Sexo** | `SEXO` | *Sexo / Gênero* |
| **Município** | `MUNICÍPIO` | *Município de Residência* |
| **Tipo de Usuário** | `Tipo de usuário` | *Tipo de usuário dos serviços (PF ou PJ)?* |
| **Conclusão** | `conclusivo` | *O atendimento prestado foi conclusivo?* |
| **Volume de Folhas** | `folhas` | *Se houver, quantas folhas foram impressas?* |
| **Serviços Prestados** | `Tipo de Atendimento` | *Tipo de Atendimento (Múltipla escolha)* |
| **Serviço "Outros"** | `respondeu outro` | *Se respondeu outro, especifique aqui:* |

### Regras Essenciais e Lógica de Processamento:

1. A pergunta de **Tipo de Atendimento** deve ser do tipo "Caixas de seleção" (múltipla escolha) no Forms.
2. A coluna de **Idade** processa apenas números nativamente (textos acidentais são isolados pelo sistema).
3. Na coluna de **Folhas Impressas**, o sistema extrai o maior número digitado na célula (ex: "Foram 5 folhas" é computado como `5`).
4. **Nota sobre Atendimentos Múltiplos:** Caso o formulário permita selecionar vários serviços, o Dashboard desmembra os itens automaticamente no gráfico operacional para garantir que a volumetria por categoria seja exata.

---

## 📚 Dicionário de Categorização (Macro Serviços)

Como os formulários podem conter preenchimentos manuais não padronizados, o sistema utiliza um algoritmo de varredura para agrupar as demandas. Se nenhum termo for encontrado, a demanda cai na categoria "Outros", que possui uma visualização de "Drill-down" exclusiva na aba Operacional.

| Categoria Final Dashboard | Palavras-chave mapeadas pelo código |
| --- | --- |
| **DASN MEI** | DASN, DECLARAÇÃO ANUAL, FATURAMENTO MEI |
| **Parcelamento** | PARCELAMENTO, PARCELA, DIVIDIR, NEGOCIAÇÃO |
| **Imposto de Renda** | IRPF, DIRPF, AJUSTE ANUAL, DECLARAÇÃO DE AJUSTE, RENDIMENTO, RESTITUIÇÃO, IR |
| **Emissão de DARF** | DARF, GUIA, PAGAMENTO |
| **Abertura de MEI** | ABERTURA, ABRIR, FORMALIZAÇÃO, MEI, ABERTURA DE MEI |
| **Outros** | Qualquer entrada que não contenha os termos acima. |

---

## 💾 Exportação e Relatórios

O sistema foi desenhado para utilizar a exportação nativa e segura do seu navegador:

1. Clique no botão de **"Mostrar Números" (ícone de olho 👁️)** no menu superior direito para exibir os valores absolutos sobre as barras e fatias.
2. Clique com o botão direito do mouse sobre o gráfico desejado e selecione **"Salvar imagem como..."**.
3. A imagem será baixada em formato PNG de alta qualidade para uso em relatórios institucionais.

---

## ⚡ Stack Tecnológica

* **Processamento e Backend:** Google Apps Script (V8) API.
* **Interface e Estilização:** HTML5, CSS3, [Tailwind CSS](https://tailwindcss.com/).
* **Lógica e Dinâmica Frontend:** JavaScript (ES6+) Vanilla (Processamento de JSON via `google.script.run`).
* **Visualização de Dados:** [Chart.js](https://www.chartjs.org/) + `chartjs-plugin-datalabels`.

---

### 🔄 Como atualizar o Dashboard?

Sempre que você fizer uma alteração no código (`index.html` ou `Código.gs`), lembre-se de atualizar a versão em cache no Google:
Vá em **Implantar > Gerenciar implantações > Clique no ícone de Editar (lápis) > Em "Versão", selecione "Nova Versão" > Implantar**. Caso contrário, o link do dashboard continuará exibindo o código antigo.