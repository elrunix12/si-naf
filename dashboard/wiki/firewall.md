# 📖 Documentação: Firewall de Dados Sensíveis (Dashboard NAF)


## 🛡️ Visão Geral

O "Firewall de Dados" é um mecanismo de segurança implementado no backend (`Código.gs`). Seu objetivo é impedir que Informações de Identificação Pessoal (PII) e dados sensíveis trafeguem do servidor do Google para o navegador do usuário.

A única exceção é o CPF: em vez de ser bloqueado sumariamente, ele é interceptado e transformado em um código anônimo irreversível (Hash SHA-256 com Salt). Isso permite que o Dashboard contabilize se um contribuinte retornou (fidelização), sem nunca saber quem ele é.

## ⚙️ Como Funciona (O Fluxo Lógico via Index Mapping)

Para garantir máxima velocidade, o firewall não analisa célula por célula. Ele lê o cabeçalho uma única vez e cria um "mapa de colunas permitidas":

1. **Higienização do Cabeçalho:** Converte os títulos para minúsculas e remove os acentos (ex: "E-mail" vira "e-mail").
2. **Interceptação do CPF:** Se a coluna for identificada como CPF, o sistema anota a posição dela para aplicar a criptografia posteriormente.
3. **Validação por Regex:** O texto normalizado das demais colunas é testado contra uma lista de palavras proibidas utilizando limites de palavra (`\b`), o que evita falsos positivos (ex: barra "rg" isolado, mas permite "carga"). As colunas aprovadas entram para a lista de `colunasPermitidas`.

## 💻 O Código-Fonte

Este é o bloco lógico da nova arquitetura de alta performance, executado antes de ler os dados:

```javascript
// O Regex é instanciado FORA do loop para economizar memória (Alta Performance)
const regexProibido = /\b(cpf|cnpj|contribuinte|telefone|celular|email|e-mail|rg|identidade|nascimento|endereco|senha)\b/;

let indiceCpf = -1;
const colunasPermitidas = [];

cabecalhoLocal.forEach((nomeColuna, i) => {
  if (!nomeColuna) return;
  
  const nomeTratado = nomeColuna.toString().toLowerCase().trim().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  // Intercepta o CPF
  if (nomeTratado === 'cpf' || nomeTratado.includes('cpf')) {
    indiceCpf = i;
    return;
  }

  // Se passar no firewall, entra no mapa de colunas permitidas
  if (!regexProibido.test(nomeTratado)) {
    colunasPermitidas.push({ nomeOriginal: nomeColuna.toString(), index: i });
  }
});
```

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