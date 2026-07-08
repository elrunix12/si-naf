# 📖 Regras de Negócio e Lógicas Internas

Este documento detalha as lógicas que estão "chumbadas" (hardcoded) no código do Dashboard. Estas regras são cruciais para o funcionamento dos gráficos e filtros, e devem ser consultadas caso a estrutura das perguntas do Google Forms seja alterada.


## 1. Identificação de Gênero
O sistema não exige uma resposta exata, mas sim a presença de termos-chave na coluna de sexo/gênero para evitar erros de preenchimento.

* **Lógica:** O código transforma a resposta em minúsculas e remove acentos antes de verificar.
* **Masculino:** Identificado se o texto contiver a palavra `masculino`.
* **Feminino:** Identificado se o texto contiver a palavra `feminino`.
* **Não Informado:** Caso a resposta não contenha nenhum dos dois termos acima (ou esteja vazia).

> **Atenção:** Se o formulário for alterado para opções como "Homem / Mulher", o código no `index.html` precisará ser atualizado para procurar por esses novos termos.


## 2. Faixas Etárias (Brackets)
A idade numérica capturada é automaticamente agrupada em blocos para facilitar a leitura do gráfico de barras. As faixas atuais são:

| Faixa | Regra Lógica |
| :--- | :--- |
| **Até 25** | Idade menor ou igual a 25 anos |
| **26 a 40** | Idade entre 26 e 40 anos |
| **41 a 60** | Idade entre 41 e 60 anos |
| **Acima de 60** | Idade maior que 60 anos |
| **Não Informado** | Quando o campo está vazio ou contém texto não numérico |


## 3. Inteligência de Padronização (Campo "Outros")
Para evitar que o gráfico de serviços fique poluído com erros de digitação (ex: "irpf", "imposto de renda", "declaração de ir"), a função `padronizarOutros()` agrupa termos semelhantes.

### Exemplos de Agrupamento Automático:
* **CONTA GOV.BR (CRIAÇÃO/NÍVEIS):** Agrupa termos como "Gov", "Ouro", "Prata", "Bronze".
* **RECUPERAÇÃO DE SENHA / ACESSO:** Agrupa "Senha", "Acesso", "eCAC".
* **DECLARAÇÃO RETIFICADORA (IRPF):** Agrupa "Retificadora".
* **RESTITUIÇÃO / PERDCOMP:** Agrupa "Restitui" (restituição, restituir) e "Perdcomp".
* **MALHA FINA / REGULARIZAÇÃO:** Agrupa "Malha", "Pendência", "Regulariza".
* **IMPOSTO DE RENDA (DÚVIDAS/DECLARAÇÃO):** Agrupa "IRPF", "IR", "Imposto de Renda", "IRRF".
* **EMISSÃO DE DARF / GUIA:** Agrupa "DARF", "Guia", "Sicalc".
* **COMPENSAÇÃO / MULTAS:** Agrupa "Compensa" (compensação) e "Multa".
* **PARCELAMENTO DE DÉBITOS:** Agrupa "Parcelamento", "Parcela".
* **SERVIÇOS INSS:** Agrupa "INSS", "Previdência".
* **SERVIÇOS MEI (GERAL):** Agrupa "MEI", "DASN".
* **CNPJ (BAIXA/ALTERAÇÃO):** Agrupa "CNPJ", "Baixa", "Alteração".

> **Nota:** essa lista reflete as regras atuais em `padronizarOutros()` no `index.html`. Se você adicionar uma nova regra no código, lembre de atualizar esta lista também — ela já ficou desatualizada uma vez.

**Manutenção:** Se uma nova demanda recorrente aparecer com nomes variados, adicione uma nova regra `if (t.includes('termo'))` dentro da função no `index.html`.


## 4. Cálculos de Crescimento (KPIs)
Os indicadores no topo da aba "Geral" comparam o desempenho atual com o período anterior imediatamente anterior.

* **Se o filtro "Mês" estiver em "Todos":** O sistema compara o **Ano Selecionado** com o **Ano Anterior**.
* **Se um "Mês" específico estiver selecionado:** O sistema compara aquele mês com o **Mês Anterior** (ex: Março/2026 vs Fevereiro/2026).
* **Sinalização:**
    * 🟢 **Verde (↑):** Aumento no volume em relação ao período passado.
    * 🔴 **Vermelho (↓):** Queda no volume em relação ao período passado.
    * ⚪ **Cinza (S/ Base):** Não existem dados no ano/mês anterior para realizar a comparação.


## 5. Validação de Datas, Estimativa por Mediana e Fallback

O sistema possui regras de consistência para garantir que a linha do tempo do dashboard não seja distorcida por erros humanos, como datas inexistentes, anos muito antigos ou datas futuras.

A data usada no dashboard segue uma ordem de prioridade:

* **Prioridade 1 (Data Oficial):** o sistema tenta usar primeiro a coluna **"Data de Atendimento"**.
* **Validação de Calendário:** a data precisa existir de verdade no calendário. Exemplos inválidos, como `31/02/2024`, `99/99/2025` ou `00/13/2026`, são rejeitados.
* **Trava de Data Mínima:** datas anteriores a **01/01/2021** são consideradas inválidas para proteger o gráfico histórico.
* **Trava de Data Máxima:** datas posteriores ao dia atual também são consideradas inválidas, pois o formulário registra apenas atendimentos já realizados.
* **Consistência com o Carimbo:** quando o Carimbo é válido, uma Data de Atendimento posterior a ele também é tratada como inválida — isso indicaria que o atendimento foi lançado no formulário antes de ter acontecido.
* **Estimativa por Mediana:** quando a **"Data de Atendimento"** foi preenchida, mas é inválida, o sistema tenta estimar a provável data do atendimento usando o **Carimbo de Data/Hora** menos a mediana histórica de atraso no lançamento.
* **Revalidação da Estimativa:** a data estimada pela mediana também precisa cair dentro do intervalo aceito (entre a Data Mínima e hoje). Se cair fora desse intervalo, a estimativa é descartada mesmo que a mediana em si seja considerada confiável, e o sistema usa o Carimbo como fallback.
* **Fallback Automático:** se a mediana não for confiável, não houver amostra suficiente, ou a Data de Atendimento estiver em branco, o sistema utiliza o **"Carimbo de Data/Hora"**, que é o timestamp automático gerado pelo Google Forms.
* **Descarte Seguro:** se nem a **"Data de Atendimento"** nem o **"Carimbo"** forem datas válidas, a linha é ignorada no processamento.

Essa regra evita que datas digitadas incorretamente prejudiquem os filtros de ano/mês, o gráfico de evolução histórica e os cálculos comparativos do dashboard.

---

### 5.1. Como a mediana é calculada

A mediana mede o atraso típico entre a data real do atendimento e o momento em que o atendimento foi lançado no formulário.

> **Nota:** o Carimbo do Google Forms registra data e hora, mas o sistema descarta o horário e compara apenas dia, mês e ano. Isso é feito na leitura de cada data, antes de qualquer comparação.

> **Atenção:** a estimativa por mediana só é tentada quando a Data de Atendimento **foi preenchida, mas é inválida** (fora do calendário, fora do intervalo aceito, ou posterior ao Carimbo). Se o campo estiver **em branco**, o sistema pula direto para o Carimbo, sem tentar estimar.

O cálculo usa a diferença:

```text
Carimbo de Data/Hora - Data de Atendimento
```

Exemplo:

```text
Data de Atendimento: 10/05/2026
Carimbo: 12/05/2026
Atraso: 2 dias
```

Quando uma linha possui **Data de Atendimento inválida**, mas possui **Carimbo válido**, o sistema estima:

```text
Data estimada = Carimbo - mediana de atraso
```

Exemplo:

```text
Carimbo: 20/05/2026
Mediana histórica: 2 dias
Data estimada: 18/05/2026
```

---

### 5.2. Janela móvel de 365 dias

A mediana não é calculada com base na data atual.

Para cada linha problemática, o sistema usa os **365 dias anteriores ao Carimbo daquela própria linha**.

Exemplo:

```text
Linha problemática:
Carimbo = 10/08/2025

Janela usada para calcular a mediana:
10/08/2024 até 10/08/2025
```

Essa regra é importante porque o padrão de lançamento pode mudar ao longo do tempo, especialmente em ambientes com rotatividade de voluntários.

---

### 5.3. Critérios para a mediana ser considerada confiável

A mediana só é usada quando existe uma base mínima de registros válidos.

O sistema considera confiável apenas a mediana calculada com:

* pelo menos **30 registros válidos** na janela de 365 dias;
* registros com **Data de Atendimento válida**;
* registros com **Carimbo válido**;
* registros em que a Data de Atendimento seja igual ou anterior ao Carimbo;
* atrasos entre **0 e 90 dias**;
* dados reais, sem usar datas já estimadas para gerar novas estimativas.

Se esses critérios não forem atendidos, a mediana é considerada não confiável e o sistema usa o Carimbo como fallback.

Além disso, mesmo com a mediana confiável, a **data estimada resultante** (Carimbo − mediana) precisa cair dentro do intervalo de datas aceito pelo sistema (entre a Data Mínima e hoje). Se a conta resultar em uma data fora desse intervalo, o sistema descarta a estimativa e usa o Carimbo diretamente — essa é a última verificação antes de aceitar uma data estimada.

O limite de **90 dias** foi adotado porque o período de declaração do Imposto de Renda costuma durar pouco mais de dois meses. Assim, o sistema aceita atrasos operacionais maiores durante períodos de alta demanda, sem considerar automaticamente esses registros como extremos.

---

#### Exemplos de mediana confiável

A mediana é considerada confiável quando existe uma quantidade suficiente de registros válidos e coerentes dentro da janela de 365 dias.

Exemplo:

```text
Linha problemática:
Data de Atendimento = 31/02/2026
Carimbo = 20/05/2026
```

O sistema procura registros válidos entre:

```text
20/05/2025 e 20/05/2026
```

Suponha que ele encontre 45 registros válidos com atrasos como:

```text
0, 1, 1, 1, 2, 2, 2, 3, 3, 4...
```

Como há pelo menos 30 registros válidos, todos com atraso entre 0 e 90 dias, a mediana pode ser usada.

Se a mediana for:

```text
2 dias
```

A data estimada será:

```text
20/05/2026 - 2 dias = 18/05/2026
```

Nesse caso, o atendimento entra no dashboard com:

```text
origemData = ESTIMADA_MEDIANA
medianaDias = 2
```

#### Exemplos de mediana não confiável

A mediana não é usada quando a base de comparação não é suficiente ou contém dados incoerentes.

Exemplo 1 — poucos registros válidos:

```text
Linha problemática:
Data de Atendimento = 99/99/2026
Carimbo = 20/05/2026
```

Na janela de 365 dias, o sistema encontra apenas:

```text
12 registros válidos
```

Como o mínimo exigido é 30 registros válidos, a mediana é considerada não confiável.

Nesse caso, o sistema usa o Carimbo como fallback:

```text
dataStr = 20/05/2026
origemData = CARIMBO
medianaDias = null
```

Exemplo 2 — registros com atraso negativo:

```text
Data de Atendimento = 25/05/2026
Carimbo = 20/05/2026
```

Esse registro indica que o formulário teria sido enviado antes do atendimento acontecer. Por isso, ele não entra no cálculo da mediana.

Exemplo 3 — atraso extremo:

```text
Data de Atendimento = 01/01/2026
Carimbo = 20/05/2026
```

A diferença é maior que 90 dias. Como esse atraso foge do padrão esperado, o registro não entra no cálculo da mediana.

Se, depois de remover atrasos negativos e extremos, sobrarem menos de 30 registros válidos, a mediana não é usada e o sistema mantém o fallback pelo Carimbo.


### 5.4. Como alterar os parâmetros de validação

Alguns limites da regra de datas podem ser ajustados diretamente nas constantes do `index.html`.

#### Alterar a data mínima aceita

A data mínima aceita pelo dashboard é definida nesta constante:

```javascript
const DATA_MINIMA_ATENDIMENTO = new Date(2021, 0, 1); // 01/01/2021
```

Para alterar o ano mínimo, ajuste o primeiro número.

Exemplo: para aceitar datas a partir de 01/01/2020:

```javascript
const DATA_MINIMA_ATENDIMENTO = new Date(2020, 0, 1); // 01/01/2020
```

Observação: em JavaScript, os meses começam em zero. Por isso:

```text
0 = janeiro
1 = fevereiro
2 = março
...
11 = dezembro
```

#### Alterar o limite máximo de atraso da mediana

O atraso máximo aceito no cálculo da mediana é definido nesta constante:

```javascript
const ATRASO_MAXIMO_MEDIANA_DIAS = 90;
```

Esse valor indica o maior intervalo permitido entre a **Data de Atendimento** e o **Carimbo de Data/Hora** para que um registro entre no cálculo da mediana.

Exemplo: para aceitar apenas atrasos de até 60 dias:

```javascript
const ATRASO_MAXIMO_MEDIANA_DIAS = 60;
```

Exemplo: para aceitar atrasos de até 120 dias:

```javascript
const ATRASO_MAXIMO_MEDIANA_DIAS = 120;
```

Aumentar esse valor torna a mediana mais tolerante a lançamentos tardios. Reduzir esse valor torna o cálculo mais rígido e remove mais registros considerados fora do padrão.

#### Alterar a quantidade mínima de registros para confiar na mediana

A quantidade mínima de registros válidos é definida nesta constante:

```javascript
const AMOSTRA_MINIMA_MEDIANA = 30;
```

Se houver menos registros válidos do que esse limite dentro da janela de 365 dias, o sistema não usa a mediana e mantém o fallback pelo Carimbo.

#### Alterar a janela histórica da mediana

A janela usada para calcular a mediana é definida nesta constante:

```javascript
const JANELA_MEDIANA_DIAS = 365;
```

Esse valor representa os 365 dias anteriores ao Carimbo da própria linha problemática.

Exemplo: para usar uma janela de 180 dias:

```javascript
const JANELA_MEDIANA_DIAS = 180;
```

Exemplo: para usar uma janela de 730 dias:

```javascript
const JANELA_MEDIANA_DIAS = 730;
```

A janela não é calculada a partir da data atual. Ela sempre usa como referência o **Carimbo de Data/Hora** da linha que precisa ser corrigida.


### 5.5. Origem da data usada

Cada atendimento tratado recebe um campo interno chamado `origemData`, que indica de onde veio a data usada no dashboard.

Os valores possíveis são:

```text
DATA_ATENDIMENTO
CARIMBO
ESTIMADA_MEDIANA
```

Significado:

* **DATA_ATENDIMENTO:** a data oficial foi considerada válida e usada diretamente.
* **CARIMBO:** a Data de Atendimento estava vazia ou inválida, e o sistema usou o timestamp do Google Forms.
* **ESTIMADA_MEDIANA:** a Data de Atendimento estava inválida, e o sistema estimou a data usando a mediana histórica de atraso.

Esse campo permite auditoria e também viabiliza o botão de ocultar/exibir datas estimadas no dashboard.

---

### 5.6. Botão para ocultar ou exibir datas estimadas

Quando existem registros com `origemData = "ESTIMADA_MEDIANA"`, o dashboard exibe um botão para controlar a visualização dessas datas.

* **Ocultar estimadas:** remove temporariamente os registros estimados dos KPIs e gráficos.
* **Exibir estimadas:** inclui novamente os registros estimados no dashboard.

Esse controle permite comparar os indicadores com e sem registros estimados.

---

### 5.7. Trecho principal do código responsável pela escolha da data

```javascript
// 1. Localização Inteligente de Colunas (Prioriza "Data de Atendimento")
const keyAtendimento = colunas.find(k => limparTexto(k).includes('data de atendimento'));
const keyCarimbo = colunas.find(k => limparTexto(k).includes('carimbo'));

const dataAtendimentoStr = keyAtendimento ? String(row[keyAtendimento] || "").trim() : "";
const carimboStr = keyCarimbo ? String(row[keyCarimbo] || "").trim() : "";

const dataResolvida = resolverDataAtendimento(dataAtendimentoStr, carimboStr, contextoMediana);

// Se nem Data de Atendimento nem Carimbo forem datas válidas, ignora a linha
if (!dataResolvida) return;

const dateParsed = dataResolvida.dataStr;
```

---

### 5.8. Resumo da regra

```text
1. Se o Carimbo for inválido, ignora a linha (ver seção 5.9).
2. Tenta usar a Data de Atendimento.
3. Se a Data de Atendimento for válida e não for posterior ao Carimbo, usa essa data.
4. Se a Data de Atendimento estiver em branco, pula direto para o Carimbo (não tenta estimar).
5. Se a Data de Atendimento foi preenchida, mas é inválida (ou é posterior ao Carimbo), tenta estimar por mediana.
6. A mediana usa os 365 dias anteriores ao Carimbo da própria linha.
7. Se a mediana for confiável e a data estimada cair dentro do intervalo aceito, usa Carimbo - mediana.
8. Se a mediana não for confiável, ou a data estimada cair fora do intervalo aceito, usa o Carimbo.
```

### 5.9 Trava Data de Carimbo

O Sistema pressupõe que você esteja usando o Google Forms para registrar o atendimento. Por isso, linhas que não contenham o Carimbo não são reconhecidas. Caso você use apenas colunas com Data de Atendimento, altere a seguinte linha para `FALSE`:

```
// true = Exige que a linha tenha um carimbo válido do Forms para ser lida.
// false = Funciona como o sistema antigo (lê apenas pela Data de Atendimento).
const EXIGIR_CARIMBO = true;
```

**ATENÇÃO:** Caso você não use o Google Forms ou Data de Carimbo, a aproximação por mediana **NÃO** irá funcionar, pois ela precisa de uma data de referência para fazer a estimativa.

## 6. Cálculo da Taxa de Retorno (Fidelização)

A Taxa de Retorno, visível na aba "Geral", mede quantos contribuintes usaram o NAF mais de uma vez em dias distintos.

* **Lógica Base:** Como o frontend não recebe CPF — apenas o `usuarioHash` — o sistema usa esse hash como identificador indireto do contribuinte.
* **Cálculo:** O código agrupa todos os atendimentos feitos pelo mesmo `usuarioHash`. Em seguida, ele analisa a `Data de Atendimento`. Se o mesmo Hash possuir registros em duas ou mais datas diferentes, ele é contabilizado como "Pessoa Recorrente".
* **Fórmula:** `(Total de Pessoas Recorrentes / Total de Hashes Únicos) * 100`.
* **Atenção:** Se uma pessoa fizer três serviços *no mesmo dia*, ela **não** será considerada recorrente, apenas gerará mais volume operacional.
