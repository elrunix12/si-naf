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
* **CONTA GOV.BR:** Agrupa termos como "Gov", "Ouro", "Prata", "Bronze".
* **RECUPERAÇÃO DE SENHA:** Agrupa "Senha", "Acesso", "eCAC".
* **SERVIÇOS MEI:** Agrupa "MEI", "DASN", "Inscrição MEI".
* **IMPOSTO DE RENDA:** Agrupa "IRPF", "IR", "Imposto de Renda", "Declaração".

**Manutenção:** Se uma nova demanda recorrente aparecer com nomes variados, adicione uma nova regra `if (t.includes('termo'))` dentro da função no `index.html`.


## 4. Cálculos de Crescimento (KPIs)
Os indicadores no topo da aba "Geral" comparam o desempenho atual com o período anterior imediatamente anterior.

* **Se o filtro "Mês" estiver em "Todos":** O sistema compara o **Ano Selecionado** com o **Ano Anterior**.
* **Se um "Mês" específico estiver selecionado:** O sistema compara aquele mês com o **Mês Anterior** (ex: Março/2026 vs Fevereiro/2026).
* **Sinalização:**
    * 🟢 **Verde (↑):** Aumento no volume em relação ao período passado.
    * 🔴 **Vermelho (↓):** Queda no volume em relação ao período passado.
    * ⚪ **Cinza (S/ Base):** Não existem dados no ano/mês anterior para realizar a comparação.


## 5. Prioridade e Trava de Datas (Fallback)

O sistema possui regras de consistência para garantir que a linha do tempo do dashboard não seja distorcida por erros humanos, como datas inexistentes, anos muito antigos ou datas futuras.

A data usada no dashboard segue uma ordem de prioridade:

* **Prioridade 1 (Data Oficial):** o sistema tenta usar primeiro a coluna **"Data de Atendimento"**.
* **Validação de Calendário:** a data precisa existir de verdade no calendário. Exemplos inválidos, como `31/02/2024`, `99/99/2025` ou `00/13/2026`, são rejeitados.
* **Trava de Data Mínima:** datas anteriores a **01/01/2021** são consideradas inválidas para proteger o gráfico histórico.
* **Trava de Data Máxima:** datas posteriores ao dia atual também são consideradas inválidas, pois o formulário registra apenas atendimentos já realizados.
* **Prioridade 2 (Fallback Automático):** se a **"Data de Atendimento"** estiver vazia ou for inválida, o sistema tenta usar o **"Carimbo de Data/Hora"**, que é o timestamp automático gerado pelo Google Forms.
* **Descarte Seguro:** se nem a **"Data de Atendimento"** nem o **"Carimbo"** forem datas válidas, a linha é ignorada no processamento.

Essa regra evita que datas digitadas incorretamente prejudiquem os filtros de ano/mês, o gráfico de evolução histórica e os cálculos comparativos do dashboard.

**Trecho principal do código (`index.html`) responsável pela escolha da data:**

```javascript
// 1. Localização Inteligente de Colunas (Prioriza "Data de Atendimento")
const keyAtendimento = colunas.find(k => limparTexto(k).includes('data de atendimento'));
const keyCarimbo = colunas.find(k => limparTexto(k).includes('carimbo'));

const dataAtendimentoStr = keyAtendimento ? String(row[keyAtendimento] || "").trim() : "";
const carimboStr = keyCarimbo ? String(row[keyCarimbo] || "").trim() : "";

const dataResolvida = resolverDataAtendimento(dataAtendimentoStr, carimboStr);

// Se nem Data de Atendimento nem Carimbo forem datas válidas, ignora a linha
if (!dataResolvida) return;

const dateParsed = dataResolvida.dataStr;
```

**Funções auxiliares responsáveis pela validação real da data:**

```javascript
const DATA_MINIMA_ATENDIMENTO = new Date(2021, 0, 1); // 01/01/2021

function obterHojeSemHorario() {
    const hoje = new Date();
    return new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
}

function parseDataBrasileira(raw) {
    if (!raw) return null;

    const texto = String(raw).trim();

    // Aceita datas no padrão DD/MM/AAAA ou DD-MM-AAAA
    // Mantém ano com 4 dígitos para evitar ambiguidade.
    const match = texto.match(/(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})/);
    if (!match) return null;

    const dia = Number(match[1]);
    const mes = Number(match[2]);
    const ano = Number(match[3]);

    const data = new Date(ano, mes - 1, dia);

    // Confirma se o JavaScript não "corrigiu" uma data inválida.
    // Ex.: 31/02/2024 viraria março se não houvesse esta trava.
    const dataExiste =
        data.getFullYear() === ano &&
        data.getMonth() === mes - 1 &&
        data.getDate() === dia;

    if (!dataExiste) return null;

    return data;
}

function dataDentroDoIntervalo(data) {
    if (!data) return false;

    const hoje = obterHojeSemHorario();

    return data >= DATA_MINIMA_ATENDIMENTO && data <= hoje;
}

function formatarDataDashboard(data) {
    const dia = String(data.getDate()).padStart(2, '0');
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const ano = data.getFullYear();

    return `${dia}/${mes}/${ano}`;
}

function resolverDataAtendimento(dataAtendimentoRaw, carimboRaw) {
    const dataAtendimento = parseDataBrasileira(dataAtendimentoRaw);

    if (dataDentroDoIntervalo(dataAtendimento)) {
        return {
            dataStr: formatarDataDashboard(dataAtendimento),
            origem: "DATA_ATENDIMENTO"
        };
    }

    const dataCarimbo = parseDataBrasileira(carimboRaw);

    if (dataDentroDoIntervalo(dataCarimbo)) {
        return {
            dataStr: formatarDataDashboard(dataCarimbo),
            origem: "CARIMBO"
        };
    }

    return null;
}
```

**Resumo da regra:**

```text
1. Tenta usar Data de Atendimento.
2. Se a data existir no calendário e estiver entre 01/01/2021 e hoje, usa essa data.
3. Se a Data de Atendimento for inválida, tenta usar o Carimbo.
4. Se o Carimbo também for inválido, a linha é ignorada.
```
> Observação: o campo interno `origemData` registra se a data usada veio da coluna `DATA_ATENDIMENTO` ou do fallback `CARIMBO`, facilitando auditoria e futuras melhorias.

## 6. Cálculo da Taxa de Retorno (Fidelização)

A Taxa de Retorno, visível na aba "Geral", mede quantos contribuintes usaram o NAF mais de uma vez em dias distintos.

* **Lógica Base:** Como o sistema é protegido pela LGPD, o frontend não recebe CPFs, apenas o `usuarioHash`.
* **Cálculo:** O código agrupa todos os atendimentos feitos pelo mesmo `usuarioHash`. Em seguida, ele analisa a `Data de Atendimento`. Se o mesmo Hash possuir registros em duas ou mais datas diferentes, ele é contabilizado como "Pessoa Recorrente".
* **Fórmula:** `(Total de Pessoas Recorrentes / Total de Hashes Únicos) * 100`.
* **Atenção:** Se uma pessoa fizer três serviços *no mesmo dia*, ela **não** será considerada recorrente, apenas gerará mais volume operacional.