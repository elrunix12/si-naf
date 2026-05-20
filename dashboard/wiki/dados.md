# 📖 Gerenciamento de Dados (Planilhas e IDs)

O "Banco de Dados" deste dashboard é composto por uma ou mais planilhas do Google (Google Sheets). Esta arquitetura permite que o painel seja alimentado por diversos formulários simultaneamente, centralizando a gestão do NAF em um único lugar.



## 1. Como encontrar o ID de uma Planilha

Para conectar qualquer nova fonte de dados ao sistema, você precisará do seu **ID**. O ID é o código alfanumérico exclusivo presente na URL (endereço) da planilha, localizado entre `/d/` e `/edit`.

**Exemplo de URL:**
`https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2up30/edit`

**O ID desta planilha seria:**
`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2up30`



## 2. Conectando novas fontes (Propriedades do Script)

O Dashboard foi desenhado para que você não precise mexer no código principal para adicionar ou remover planilhas. Tudo é gerido através das **Propriedades do Script**.

### Passo a passo para adicionar uma planilha:

1. No editor do Apps Script, clique no ícone de **Engrenagem** (Configurações do projeto).
2. Vá até **Propriedades do script** e clique em **Adicionar propriedade do script**.
3. Siga o padrão de nomenclatura:
* **Propriedade:** `PLANILHA_ID_X` (substitua o X pelo próximo número disponível, ex: `PLANILHA_ID_4`).
* **Valor:** Cole o ID da planilha.


4. Clique em **Salvar**.



## 3. Gestão de Abas (Páginas)

Por padrão, o sistema é otimizado para formulários do Google, que costumam gerar as respostas na primeira página do arquivo.

* **Comportamento Padrão:** Se você cadastrar apenas o `PLANILHA_ID_X`, o script buscará automaticamente os dados na **primeira aba à esquerda (índice 0)**.
* **Aba Específica:** Se os dados estiverem em uma aba com nome específico (ex: "Consolidado 2025"), você deve adicionar uma nova propriedade chamada `TAB_NOME_X` com o nome exato da aba.

**Dica de Manutenção:** Caso o nome da aba mude, você só precisa atualizar a Propriedade do Script, sem necessidade de gerar uma nova versão (deploy) do sistema.



## 4. Segurança

Uma das maiores vantagens desta arquitetura é que o **Firewall de Privacidade** é global. Isso significa que:

1. Assim que você conecta um novo ID de planilha, o backend automaticamente passa a monitorar essa fonte.
2. Se a planilha contiver colunas contendo Nomes, Telefones ou E-mails, o sistema as bloqueará sumariamente.
3. **Criptografia de CPF:** Se a planilha possuir uma coluna de CPF, o sistema repara zeros à esquerda perdidos e aplica um algoritmo Hash irreversível (SHA-256) somado a um "Salt" (Chave de Segurança das propriedades do script). O Dashboard receberá apenas um código alfanumérico (ex: `e3b0c442...`), permitindo gerar estatísticas de fidelização.



## 5. Consistência de Dados entre Planilhas

Para que a união de várias planilhas funcione perfeitamente, os cabeçalhos não precisam estar na mesma ordem, mas precisam manter os mesmos **nomes (palavras-chave)**.

* **Exemplo:** Se a Planilha 1 chama a cidade de "Município" e a Planilha 2 chama de "Cidade", o sistema pode não conseguir cruzar os dados geográficos.
* **Solução:** Certifique-se de que as perguntas críticas do formulário (Data, Município, Idade, Sexo, Tipo de Atendimento) mantenham termos em comum conforme detalhado na página de [Mapeamento de Colunas].