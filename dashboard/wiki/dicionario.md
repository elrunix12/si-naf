# 📖 Gestão do Dicionário de Categorias

O **Dicionário de Categorias** é o "cérebro" da aba Operacional do Dashboard. Ele é responsável por transformar as respostas longas, técnicas e muitas vezes combinadas do Google Forms em rótulos (*labels*) curtos e fáceis de ler nos gráficos.

---

## 1. Localização no Código

O dicionário reside no arquivo `index.html`, logo no início da tag `<script>`, armazenado na constante:

```javascript
const categoriasDicionario = { ... };
```

---

## 2. Anatomia e Lógica de Funcionamento

O dicionário funciona como um mapeamento de **Chaves** e **Valores**:

* **Chave (Rótulo do Gráfico):** É o nome consolidado que aparecerá na legenda do gráfico (ex: `"Imposto de Renda (IRPF)"`).
* **Valores (Array de Termos):** É a lista contendo os textos exatos (ou fragmentos estratégicos) gerados pelo Google Forms.

### 🔍 Correspondência Exata (Como o sistema lê as frases)

O sistema utiliza um comando JavaScript chamado `.includes()`. Isso significa que ele procura por uma **frase exata (ou fragmento exato)** que você colocou entre as aspas, e não palavra por palavra.

**Importante: a comparação acontece nos dois sentidos.** O código real é:

```javascript
chaves.some(chave => termo.includes(chave) || chave.includes(termo))
```

Ou seja, dá *match* tanto se o texto do Forms contém a frase cadastrada no dicionário, quanto se a frase cadastrada contém o texto do Forms. Na prática, isso significa que mesmo um termo digitado de forma truncada ou ligeiramente diferente da opção original ainda pode ser reconhecido — o que reforça a importância de usar frases longas e específicas no dicionário (ver Checklist, item 2).

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

---

## 3. Tratamento de Múltiplos Serviços (Caixas de Seleção)

No Google Forms, se a pergunta "Tipo de Atendimento" for de múltipla escolha (caixas de seleção), o usuário pode marcar 3 serviços ao mesmo tempo. A planilha do Google exporta isso em uma única célula, separado por vírgulas:

> *Exemplo na planilha:* `AUXÍLIO À INSCRIÇÃO MEI, INFORMAÇÕES GERAIS SOBRE ITR`

**Você não precisa se preocupar com isso no dicionário.**
A lógica do Dashboard já está programada para separar essa célula por vírgulas em termos individuais e testar **cada termo separadamente** contra as chaves do seu dicionário. Se ele encontrar o texto do MEI em um termo e o texto do ITR em outro, ele computará +1 para "MEI e Simples Nacional" e +1 para "Imposto de Renda", desmembrando o atendimento perfeitamente nos gráficos.

### ⚠️ Exceção: Textos do Dicionário com Vírgula Própria

Duas opções oficiais do NAF têm vírgula dentro do próprio texto (ex: "...PORTADORES DE DEFICIÊNCIA FÍSICA, MENTAL OU VISUAL", em "Restituições e Isenções"). Como a vírgula também é o separador de múltipla escolha, isso causava um bug real: ao separar a célula por vírgulas, esses textos eram fatiados em pedaços — e cada pedaço, por ser um trecho do texto original, ainda batia com a mesma categoria (graças à comparação bidirecional da Seção 2). Resultado: um único atendimento marcado era contado 2 ou 3 vezes em vez de 1, inflando os números de "Restituições e Isenções" e "Previdência e eSocial" nos gráficos.

**Isso já foi corrigido no código.** Antes de separar a célula por vírgula, o sistema primeiro varre o dicionário procurando textos completos que tenham vírgula própria e os extrai inteiros da célula. Só o que sobra depois disso é separado por vírgula normalmente.

**Você não precisa fazer nada de especial ao cadastrar uma nova categoria com vírgula no texto** — a varredura é automática e cobre qualquer entrada do dicionário, atual ou futura. Esse bloco de verificação fica isolado, calculado uma única vez (fora do loop de linhas, por performance), logo depois da definição de `categoriasDicionario` no `index.html`.

**Isso não afeta o campo "Especificar Outro".** Aquele campo nunca é separado por vírgula — o texto inteiro é tratado como uma resposta única. A consequência é diferente: se alguém digitar dois assuntos separados por vírgula ali (ex: "problema no CNPJ, dúvida sobre MEI"), os dois viram uma única entrada no drill-down de "Outros", categorizada pela primeira palavra-chave que bater — não é uma contagem a mais, é uma informação a menos.

> **Por que a marcação "Outros" sozinha é ignorada:** quando o usuário marca apenas a caixa "Outros" na múltipla escolha, o Google Forms grava essa marcação genérica na própria coluna Tipo de Atendimento — mas o conteúdo real do serviço está na coluna Especificar Outro, tratada separadamente. Por isso o sistema descarta essa marcação genérica ao processar a múltipla escolha: se ela fosse contabilizada, o mesmo atendimento seria contado duas vezes (uma pela marcação genérica, outra pelo texto livre).

> **O total de pessoas atendidas não muda:** mesmo quando uma linha gera várias entradas na Aba Operacional (uma para cada serviço marcado), o KPI de Total de Pessoas Atendidas conta cada linha da planilha uma única vez, independentemente de quantos serviços ela tenha gerado.

---

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

---

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

---

## 6. A Categoria Especial: "Outros" e Textos Livres

A categoria `"Outros": []` no final do dicionário **deve permanecer sempre vazia**.

* **Como funciona:** O sistema processa primeiro todas as categorias definidas por você. Se um termo da múltipla escolha não encontrar correspondência em nenhuma das chaves, ele é jogado no balde "Outros" — com **exceção** descrita abaixo.

* ⚠️ **Atenção ao marcador genérico:** se o termo não reconhecido for **apenas** a própria opção "Outro" ou "Outros" do checkbox (sem nenhum outro serviço válido junto), ele **não** vira uma entrada em "Outros" — ele é descartado silenciosamente. Isso é proposital: o conteúdo real desse "Outros" marcado deve vir do campo **Especificar Outro** (texto livre), que é processado separadamente. Ou seja, marcar só a caixinha "Outros" no formulário, sem preencher o texto livre com algo válido, não vai gerar nenhuma entrada no drill-down de Outros — e isso é o comportamento esperado, não um bug.

* **Drill-down (Detalhamento):** Na aba Operacional, ao clicar em **"Detalhar Outros"**, o sistema mostra exatamente o que os usuários digitaram na opção "Outros / Especifique" (mais os termos da múltipla escolha que não bateram com nenhuma categoria).

* **Trava Final (Nenhum Serviço Reconhecido):** o rótulo `"NÃO ESPECIFICADO"` só aparece quando, ao mesmo tempo, (1) a coluna Tipo de Atendimento não contiver nenhum termo real — esteja vazia ou contenha apenas a marcação genérica "Outros" — **e** (2) o campo Especificar Outro também estiver vazio ou contiver um termo inválido (como "." ou "-"). Nesse cenário, o atendimento continua sendo contabilizado nos KPIs gerais, só não aparece com um serviço identificável no gráfico de detalhamento.

### 🛠️ A Função `padronizarOutros()`
Como textos livres geram muita sujeira (erros de digitação, letras minúsculas, gírias), o sistema passa essas respostas por uma "lavanderia" chamada `padronizarOutros()` (localizada mais para o final do `index.html`).

Se os usuários começarem a usar muito uma sigla nova (ex: "PGFN" para parcelamento), você pode adicionar uma regra de aproximação dentro dessa função:

```javascript
// Exemplo dentro da função padronizarOutros(texto):
if (t.includes('PGFN') || t.includes('REGULARIZACAO GOV')) return 'PARCELAMENTO DE DÉBITOS';
```

Dessa forma, "PGFN", "pgfn", "Pgfn..." vão virar uma barra única e limpa no gráfico detalhado.

---

## 💡 Checklist de Boas Práticas para Manutenção a Longo Prazo

1. **Letras Maiúsculas (Caixa Alta):** O sistema transforma todas as respostas do Forms em MAIÚSCULAS antes de comparar. Portanto, escreva os textos no dicionário sempre em **CAIXA ALTA**.
2. **Fuja de Termos Muito Curtos:** Nunca cadastre palavras como `"IR"`, `"CPF"` ou `"MEI"` sozinhas no dicionário. Como a comparação funciona nos dois sentidos (ver Seção 2), termos curtos aumentam ainda mais o risco de *match* acidental — por exemplo, uma pessoa que digitar "PRI**MEI**RO" no campo "Outros" seria contabilizada como "Abertura de MEI". Use trechos maiores: `"INSCRIÇÃO DE MEI"`, `"AJUSTE ANUAL DO IRPF"`.
3. **Sincronização com o Forms:** Se a coordenação mudar a redação de uma pergunta no Google Forms (Ex: de "Informações de ITR" para "Dúvidas sobre ITR"), lembre-se de vir no código e atualizar o dicionário, caso contrário os novos atendimentos cairão na aba "Outros".
4. **Backup Rápido:** Antes de mexer nas chaves e vírgulas do dicionário, copie o código original e cole num Bloco de Notas. Se o painel quebrar após a sua edição, você tem como reverter em segundos.
5. **Vírgulas no Texto:** Se uma nova opção oficial do Forms tiver vírgula no próprio texto, não se preocupe — o sistema já detecta e trata isso automaticamente (ver Seção 3).

---

## 📌 Nota Técnica (para desenvolvedores)

Existe uma função `categorizar(texto)` no código (próximo à linha 1321) com uma lógica de comparação parecida, porém **unidirecional** (`txt.includes(chave)` apenas) e que atualmente **não é chamada em nenhum lugar** do sistema. Trata-se aparentemente de código residual de uma versão anterior. Ela não afeta o funcionamento atual do Dashboard, mas pode gerar confusão para quem estiver lendo o código e pensar que é essa a função usada na classificação real (que é a das linhas ~666-676, dentro do processamento principal das linhas da planilha).
