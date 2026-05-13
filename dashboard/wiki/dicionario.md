# 📖 Wiki: Gestão do Dicionário de Categorias

O **Dicionário de Categorias** é o "cérebro" da aba Operacional do Dashboard. Ele é responsável por transformar as respostas longas, técnicas e muitas vezes combinadas do Google Forms em rótulos (*labels*) curtos e fáceis de ler nos gráficos.



## 1. Localização no Código

O dicionário reside no arquivo `index.html`, logo no início da tag `<script>`, armazenado na constante:

```javascript
const categoriasDicionario = { ... };

```



## 2. Anatomia e Lógica de Funcionamento

O dicionário funciona como um mapeamento de **Chaves** e **Valores**:

* **Chave (Rótulo do Gráfico):** É o nome consolidado que aparecerá na legenda do gráfico (ex: `"Imposto de Renda (IRPF)"`).
* **Valores (Array de Termos):** É a lista contendo os textos exatos (ou fragmentos estratégicos) gerados pelo Google Forms.

### 🔍 Correspondência Exata (Como o sistema lê as frases)

O sistema utiliza um comando JavaScript chamado `.includes()`. Isso significa que ele procura pela **frase exata (ou fragmento exato)** que você colocou entre as aspas, e não palavra por palavra.

**Exemplo prático:**
Se você tem duas categorias diferentes:

```javascript
"Cadastros (CPF e CNPJ)": [
    "AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES CADASTRAIS DE CPF"
],
"Comércio Exterior": [
    "AUXÍLIO À HABILITAÇÃO NOS SISTEMAS RADAR E SISCOMEX"
]

```

O sistema **não** vai se confundir apenas porque ambas começam com a palavra "AUXÍLIO". Ele exige que o bloco inteiro de texto dê *match*.

Isso é excelente porque evita **falsos positivos**. A única forma de o sistema misturar tudo seria se você configurasse o dicionário de forma muito genérica, colocando apenas a palavra isolada (ex: `"Comércio Exterior": ["AUXÍLIO"]`). Portanto, **use sempre frases completas ou trechos longos o suficiente para serem únicos.**



## 3. Tratamento de Múltiplos Serviços (Caixas de Seleção)

No Google Forms, se a pergunta "Tipo de Atendimento" for de múltipla escolha (caixas de seleção), o aluno pode marcar 3 serviços ao mesmo tempo. A planilha do Google exporta isso em uma única célula, separado por vírgulas:

> *Exemplo na planilha:* `AUXÍLIO À INSCRIÇÃO MEI, INFORMAÇÕES GERAIS SOBRE ITR`

**Você não precisa se preocupar com isso no dicionário.**
A lógica do Dashboard já está programada para ler essa célula gigante e testar **cada linha do seu dicionário** contra ela. Se ele encontrar o texto do MEI e o texto do ITR na mesma célula, ele computará +1 para "MEI e Simples Nacional" e +1 para "Imposto de Renda", desmembrando o atendimento perfeitamente nos gráficos.



## 4. Como Adicionar uma Nova Categoria (Novo Guarda-chuva)

Para criar um novo grupo de serviços no gráfico, adicione um novo bloco seguindo este padrão:

1. Escolha o nome curto que aparecerá no Dashboard.
2. Abra a sua planilha de respostas e copie o texto exato da opção do formulário.
3. Insira no código:

```javascript
"Nome da Nova Categoria": [
    "TEXTO EXATO DA OPÇÃO 1",
    "TEXTO EXATO DA OPÇÃO 2"
],

```



## 5. Como Adicionar um Serviço a uma Categoria Existente

Basta adicionar o novo texto dentro do "array" (os colchetes `[]`) da categoria desejada.

```javascript
"MEI e Simples Nacional": [
    "AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES GERAIS SOBRE O MICROEMPREENDEDOR INDIVIDUAL",
    "NOVA OPÇÃO QUE VOCÊ CRIOU NO FORMS" // Adicione aqui
],

```

### ⚠️ A Regra da Vírgula (Prevenção Crítica de Erros)

Ao modificar os serviços, respeite a sintaxe do JavaScript: **os itens de uma lista precisam ser separados por vírgulas**. Essa vírgula fica **sempre de fora das aspas**, no final da linha, indicando que "há mais um item abaixo".

❌ **O Jeito Errado (Vai quebrar o painel - Tela em branco):**

```javascript
"MEI e Simples Nacional": [
    "AUXÍLIO À INSCRIÇÃO MEI," // ERRO 1: A vírgula está DENTRO das aspas.
    "ALTERAÇÃO DE DADOS MEI"   // ERRO 2: Faltou a vírgula de fora separando esta linha da próxima.
    "BAIXA DE MEI"
],

```

✅ **O Jeito Certo:**

```javascript
"MEI e Simples Nacional": [
    "AUXÍLIO À INSCRIÇÃO MEI", // CORRETO: Terminou o texto, fechou aspas, colocou a vírgula.
    "ALTERAÇÃO DE DADOS MEI",  // CORRETO: Tem mais um item embaixo, então vai vírgula.
    "BAIXA DE MEI"             // CORRETO: Último item da lista NÃO leva vírgula no final.
],

```



## 6. A Categoria Especial: "Outros" e Textos Livres

A categoria `"Outros": []` no final do dicionário **deve permanecer sempre vazia**.

* **Como funciona:** O sistema processa primeiro todas as categorias definidas por você. Se uma célula da planilha não encontrar correspondência em nenhuma das chaves, ela é automaticamente jogada no balde "Outros".
* **Drill-down (Detalhamento):** Na aba Operacional, ao clicar em **"Detalhar Outros"**, o sistema mostra exatamente o que os alunos digitaram na opção "Outros / Especifique".

### 🛠️ A Função `padronizarOutros()`

Como textos livres geram muita sujeira (erros de digitação, letras minúsculas, gírias), o sistema passa essas respostas por uma "lavanderia" chamada `padronizarOutros()` (localizada mais para o final do `index.html`).

Se os alunos começarem a usar muito uma sigla nova (ex: "PGFN" para parcelamento), você pode adicionar uma regra de aproximação dentro dessa função:

```javascript
// Exemplo dentro da função padronizarOutros(texto):
if (t.includes('PGFN') || t.includes('REGULARIZACAO GOV')) return 'PARCELAMENTO DE DÉBITOS';

```

Dessa forma, "PGFN", "pgfn", "Pgfn..." vão virar uma barra única e limpa no gráfico detalhado.



## 💡 Checklist de Boas Práticas para Manutenção a Longo Prazo

1. **Letras Maiúsculas (Caixa Alta):** O sistema transforma todas as respostas do Forms em MAIÚSCULAS antes de comparar. Portanto, escreva os textos no dicionário sempre em **CAIXA ALTA**.
2. **Fuja de Termos Muito Curtos:** Nunca cadastre palavras como `"IR"`, `"CPF"` ou `"MEI"` sozinhas no dicionário. Uma pessoa que digitar "PRI**MEI**RO" no campo "Outros" vai ser contabilizada como "Abertura de MEI" acidentalmente. Use trechos maiores: `"INSCRIÇÃO DE MEI"`, `"AJUSTE ANUAL DO IRPF"`.
3. **Sincronização com o Forms:** Se a coordenação mudar a redação de uma pergunta no Google Forms (Ex: de "Informações de ITR" para "Dúvidas sobre ITR"), lembre-se de vir no código e atualizar o dicionário, caso contrário os novos atendimentos cairão na aba "Outros".
4. **Backup Rápido:** Antes de mexer nas chaves e vírgulas do dicionário, copie o código original e cole num Bloco de Notas. Se o painel quebrar após a sua edição, você tem como reverter em segundos.