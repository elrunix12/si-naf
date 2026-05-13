# 📖 Guia de Atualização e Publicação (Deploy)

Como o Dashboard NAF é uma aplicação hospedada diretamente nos servidores do Google, existe um processo específico para que as alterações feitas no código (seja no `index.html` ou no `Código.gs`) fiquem visíveis para os usuários finais. **Apenas clicar em "Salvar" não atualiza o Dashboard.**



## 1. Versão ≠ Arquivo Salvo

No Google Apps Script, o link que você compartilha (a URL do Web App) aponta para uma **versão específica** e "congelada" do seu código.

* **Salvar (Ctrl+S):** Apenas guarda o seu rascunho no editor.
* **Implantar (Deploy):** Cria uma nova "foto" do código e a publica na internet.

Sempre que você fizer qualquer mudança visual ou lógica, você **precisa** gerar uma nova implantação para que os usuários vejam a mudança.



## 2. Passo a Passo para Atualizar o Dashboard

Siga este procedimento sempre que editar o código:

1. No topo do editor do Apps Script, clique no botão azul **Implantar**.
2. Selecione a opção **Gerenciar implantações**.
3. No menu lateral, clique no ícone de **Lápis (Editar)** da implantação ativa (geralmente chamada de "Web App").
4. Na caixa de seleção chamada **Versão**, escolha obrigatoriamente **"Nova versão"**.
* *Opcional:* Você pode escrever um breve comentário sobre o que mudou (ex: "Ajuste nas cores das abas").


5. Clique no botão azul **Implantar**.
6. O link (URL) continuará o mesmo, mas agora ele carregará o código atualizado.



## 3. Como Testar sem Afetar o Dashboard Público

Para evitar que os usuários vejam erros enquanto você ainda está testando novas funcionalidades:

1. Clique em **Implantar > Testar implantações**.
2. O Google fornecerá um link que termina em `/dev`.
3. Este link **sempre** mostra a versão mais recente do código que foi salva (Ctrl+S), sem precisar de um novo deploy.
4. **Atenção:** Apenas você (o desenvolvedor) consegue acessar o link `/dev`. Use-o para validar se os gráficos estão funcionando antes de publicar para todos.



## 4. Resolução de Problemas (Troubleshooting)

### "Atualizei o código, mas o erro continua"

* Verifique se você selecionou **"Nova Versão"** no Gerenciador de Implantações. Se você apenas clicar em "Implantar" sem mudar a versão, o Google reutiliza a versão anterior (o código antigo).

### "O Dashboard pede autorização toda hora"

* Isso acontece se você alterou quem pode acessar o app ou se adicionou uma nova funcionalidade no `Código.gs` que exige novas permissões do Google Drive. Clique em **Revisar Permissões** e aceite os termos para liberar o acesso.