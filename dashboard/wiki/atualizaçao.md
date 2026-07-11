# Guia de Instalação, Configuração e Publicação (Deploy)

Este guia orienta o processo de configuração inicial e atualização do **Dashboard NAF**. Como a aplicação é hospedada nos servidores do Google, o salvamento simples (Ctrl+S) não reflete as mudanças para os usuários; é necessário um processo de "Implantação".


## 1. Configuração Inicial (Instalação do Zero)

Antes de publicar, o ambiente precisa ser preparado com os arquivos corretos.

### A. Criação dos Arquivos

No editor do Google Apps Script, você deve ter exatamente esta estrutura de arquivos:

1. **`Código.gs`**: Onde fica a lógica do servidor.
2. **`index.html`**: A interface visual.
3. **`Lib_ChartJS.html`**: Crie um novo arquivo HTML, apague todo o conteúdo e cole o código da biblioteca Chart.js.
4. **`Lib_DataLabels.html`**: Crie um novo arquivo HTML e cole o código do plugin de rótulos de dados.

### B. Configuração das Fontes de Dados (Propriedades)

O backend busca os IDs das planilhas através de **Propriedades do Script**. Sem isso, o Dashboard não terá dados para ler.

1. No menu lateral esquerdo, clique na **Engrenagem (Configurações do Projeto)**.
2. Role até o final em **Propriedades do Script**.
3. Adicione as seguintes chaves (exatamente com esses nomes):
* `PLANILHA_ID_1`: O ID da planilha principal de dados.
* `TAB_NOME_1`: O nome da aba (ex: "Respostas ao Formulário 1").
* *(Repita para ID_2, ID_3 se houver mais fontes)*.


## 2. Versão ≠ Arquivo Salvo

No Google Apps Script, o link que você compartilha (a URL do Web App) aponta para uma **versão específica** e "congelada" do seu código.

* **Salvar (Ctrl+S):** Apenas guarda o seu rascunho no editor.
* **Implantar (Deploy):** Cria uma "foto" imutável do código e a publica na internet.

Sempre que você fizer qualquer mudança visual ou lógica, você **precisa** gerar uma nova implantação, caso contrário, o link continuará mostrando a versão antiga.


## 3. Passo a Passo para Atualizar o Dashboard

Siga este procedimento sempre que editar o código para que as mudanças "entrem no ar":

1. No topo do editor, clique no botão azul **Implantar > Gerenciar implantações**.
2. No menu lateral, clique no ícone de **Lápis (Editar)** da implantação ativa (tipo "Web App").
3. Na caixa de seleção chamada **Versão**, escolha obrigatoriamente **"Nova versão"**.
* *Dica:* No campo de descrição, escreva o que mudou (ex: "Corrigido filtro de gênero"). Isso ajuda no histórico.


4. Clique no botão azul **Implantar**.
5. **Importante:** O link (URL) continuará o mesmo. Basta atualizar a página do Dashboard no navegador.



## 4. Como Testar sem Afetar os Usuários

Para evitar que os usuários vejam erros enquanto você ainda está mexendo no código:

1. Clique em **Implantar > Testar implantações**.
2. O Google fornecerá um link que termina em `/dev`.
3. Este link **sempre** mostra a versão mais recente que foi salva (Ctrl+S), sem precisar de um novo deploy.
4. **Uso Recomendado:** Valide tudo no link `/dev`. Quando estiver perfeito, faça o processo de "Gerenciar Implantações" (item 3) para publicar a versão oficial.


## 5. Configurações de Acesso e Permissões

Na primeira vez que você implantar (ou se mudar quem pode acessar), verifique estas opções:

* **Executar como:** 
    * *Eu (sua conta):* O app usa as suas permissões para ler as planilhas. (Recomendado para NAF).
    * *Usuário que acessa o app:* Cada pessoa precisa ter acesso às planilhas originais.

> **Recomendação:** se o NAF tiver (ou puder criar) uma conta institucional do Google — não vinculada a uma pessoa específica, tipo `naf.suainstituicao@gmail.com` — prefira implantar e executar o Web App a partir dela, em vez da conta pessoal de um voluntário ou coordenador. Isso evita que o Dashboard fique dependente de uma única pessoa continuar com acesso à conta: se ela sair do núcleo, o projeto pode ficar sem ninguém capaz de editá-lo ou reimplantá-lo até que a propriedade do arquivo seja transferida no Google Drive.


* **Quem pode acessar:**
    * **Apenas eu:** só a sua própria conta Google consegue abrir o Dashboard. Serve para testar sozinho, mas não funciona para publicar o link para o NAF usar.
    * **Pessoas com conta institucional:** limita o acesso a quem tem uma conta da própria organização (ex: `@suainstituicao.edu.br`). Essa opção só existe se a instituição usa **Google Workspace**; com contas Gmail comuns, ela nem aparece como opção. É a mais restritiva de fato, porque distingue quem é da instituição de quem não é.
    * **Pessoas com conta Google:** qualquer pessoa com uma conta Google (Gmail ou não) consegue acessar, desde que tenha o link. Quando a instituição usa contas Gmail comuns (sem Workspace), essa é a opção mais restritiva disponível — mas ela não diferencia "alguém do NAF" de "qualquer pessoa no mundo com conta Google". Na prática, a única barreira adicional é o link não circular publicamente.
    * **Todo mundo (não recomendado):** libera o acesso sem exigir login nenhum. Além de não ter nenhum controle de quem acessa, deixa o link exposto a bots, crawlers e scanners automáticos — esse tráfego indesejado pode consumir a cota diária de execução do Apps Script (bem mais apertada em contas Gmail comuns do que em contas Workspace) e derrubar o Dashboard para os usuários reais.

**Independentemente da opção escolhida:** evite divulgar o link do Web App em canais públicos (grupos abertos, redes sociais, páginas indexadas por buscadores). Quanto mais gente tiver o link, maior a chance de ele circular além do público pretendido e gerar tráfego indesejado — e, no caso das opções sem exigência de conta institucional, esse tráfego conta contra a mesma cota diária do Apps Script.


## 6. Resolução de Problemas (Troubleshooting)

### "Atualizei o código, mas o erro ou a versão antiga continua"

* **Causa:** Você provavelmente esqueceu de selecionar **"Nova Versão"** no Gerenciador de Implantações. Se você apenas clicar em "Implantar" sem mudar para "Nova Versão", o Google apenas revalida a versão anterior.

### "O Dashboard pede autorização ou dá erro de 'Script Interrompido'"

* **Causa:** Sempre que você adiciona uma funcionalidade nova que acessa o Google Drive ou Planilhas, o Google exige um novo consentimento.
* **Solução:** Abra o link do Web App, clique em **Revisar Permissões**, selecione sua conta e clique em **Avançado > Ir para Dashboard NAF (não seguro)** e clique em **Permitir**.

### "Os gráficos estão em branco ou não carregam"

* **Causa:** Verifique se as IDs das planilhas nas **Propriedades do Script** estão corretas ou se o nome das colunas na planilha mudou e o sistema não conseguiu "pescar" as palavras-chave.
