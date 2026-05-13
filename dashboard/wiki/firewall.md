# 📖 Documentação: Firewall de Dados Sensíveis (Dashboard NAF)


## 🛡️ Visão Geral

O "Firewall de Dados" é um mecanismo de segurança implementado no backend (`Código.gs`) do Dashboard NAF. Seu objetivo exclusivo é impedir que Informações de Identificação Pessoal (PII) e dados sensíveis dos contribuintes sejam trafegados do servidor do Google para o navegador do usuário.

Como o sistema lê dados brutos de planilhas de atendimento, ele atua como um filtro intermediário, garantindo que colunas contendo CPFs, nomes, telefones ou e-mails sejam sumariamente ignoradas durante a consolidação dos dados.


## ⚙️ Como Funciona (O Fluxo Lógico)

O firewall opera em três etapas sequenciais para cada coluna encontrada no cabeçalho da planilha:

### 1. Prevenção contra Nulos (Null Check)

O sistema verifica se a coluna realmente possui um título. Planilhas frequentemente possuem colunas vazias geradas por formatação. Se o título for nulo ou vazio, o sistema ignora a coluna imediatamente para evitar falhas de processamento.

### 2. Normalização Profunda (Higienização)

Para evitar que o filtro seja burlado por erros de digitação ou formatações diferentes (ex: "CPF", "Cpf", "cpf", "NOME", "Nome"), o título da coluna passa por uma esteira de limpeza:

* `toLowerCase()`: Converte todas as letras para minúsculas.
* `trim()`: Remove espaços em branco acidentais no início e no final.
* `normalize("NFD").replace(...)`: Remove completamente qualquer acentuação (ex: "E-mail" e "Endereço" viram "e-mail" e "endereco").

### 3. Validação por Expressão Regular (Regex)

O texto normalizado é testado contra uma lista de palavras proibidas utilizando Regex. O uso de **limites de palavra (`\b`)** garante precisão absoluta, evitando **falsos positivos**.

* *Exemplo prático:* A regra barra a palavra isolada `rg`. Se não houvesse o limite de palavra, uma coluna perfeitamente segura chamada `carga horária` ou `margem` seria bloqueada acidentalmente, pois contém as letras "r" e "g" juntas.


## 💻 O Código-Fonte

Este é o bloco lógico localizado dentro da função `obterDadosPlanilha()`, rodando no loop de mapeamento de cabeçalhos:

```javascript
// 1. Prevenção: Ignora se a coluna for nula ou vazia
if (!nomeColuna) return;

const nomeOriginal = nomeColuna.toString();

// 2. Normalização para o FIREWALL
const nomeTratado = nomeOriginal.toLowerCase()
  .trim()
  .normalize("NFD")
  .replace(/[\u0300-\u036f]/g, "");

// 3. FIREWALL COM REGEX (Proteção contra falsos positivos)
const regexProibido = /\b(cpf|cnpj|contribuinte|telefone|celular|email|e-mail|rg|identidade|nascimento|endereco|senha)\b/;

// Se o nome da coluna contiver alguma das palavras proibidas, bloqueia.
if (regexProibido.test(nomeTratado)) {
  return; 
}

```



## 🚫 Dicionário de Bloqueio Atual

A expressão regular atual bloqueia qualquer coluna cujo título contenha as seguintes palavras isoladas:

* `cpf` / `cnpj` (Identificação Fiscal)
* `contribuinte` (Geralmente atrelado ao "Nome do Contribuinte")
* `telefone` / `celular` (Contato direto)
* `email` / `e-mail` (Contato digital)
* `rg` / `identidade` (Documentos civis)
* `nascimento` (Geralmente atrelado à "Data de Nascimento")
* `endereco` (Localização física)
* `senha` (Credenciais)



## 🛠️ Como Atualizar / Adicionar Novas Palavras

O sistema foi desenhado para ser escalável. Para adicionar uma nova restrição (por exemplo, "CEP" ou "Passaporte"), não é necessário reescrever a lógica.

Basta localizar a variável `regexProibido` no `Código.gs` e adicionar a nova palavra dentro dos parênteses, separada por uma barra vertical (`|`).

**Exemplo de adição da palavra "cep":**

* **Antes:** `/\b(cpf|cnpj|contribuinte...)\b/`
* **Depois:** `/\b(cpf|cnpj|contribuinte|cep...)\b/`

*Nota de segurança: Não utilize acentos ou letras maiúsculas ao adicionar novas palavras na Regex, pois a etapa de normalização já converte tudo para minúsculas e remove os acentos antes da verificação.*