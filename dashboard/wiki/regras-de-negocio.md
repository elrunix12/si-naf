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
O sistema possui regras de consistência para garantir que nenhum dado seja perdido e que a linha do tempo não seja distorcida por erros humanos (como o preenchimento de anos absurdos).

* **Prioridade 1 (Data Oficial):** O sistema tenta buscar primeiro a coluna "Data de Atendimento".
* **Regra de Consistência (Trava de 2021):** Se a "Data de Atendimento" foi preenchida, mas o ano for **anterior a 2021** (ex: digitação errada como 2015 ou 2010), o sistema invalida essa entrada para proteger o gráfico histórico.
* **Prioridade 2 (Fallback Automático):** Caso a "Data de Atendimento" esteja vazia **ou** tenha sido invalidada pela trava de 2021, o sistema utiliza o "Carimbo de Data/Hora" (Timestamp automático e inalterável do Google Forms) como a data oficial daquele atendimento.

**Trecho do código (`index.html`) responsável por essa regra:**
```javascript
// 1. Localização Inteligente de Colunas (Prioriza "Data de Atendimento")
const keyAtendimento = colunas.find(k => limparTexto(k).includes('data de atendimento'));
const keyCarimbo = colunas.find(k => limparTexto(k).includes('carimbo'));

let rawDate = "";
const dataAtendimentoStr = keyAtendimento ? String(row[keyAtendimento] || "").trim() : "";
const carimboStr = keyCarimbo ? String(row[keyCarimbo] || "").trim() : "";

if (dataAtendimentoStr !== "") {
    // Extrai o ano da Data de Atendimento para fazer a checagem
    const anoInformado = parseInt(extrairAno(extractDateString(dataAtendimentoStr)));
    
    // TRAVA: Se o ano for reconhecido e for menor que 2021, ignora e usa o Carimbo
    if (!isNaN(anoInformado) && anoInformado < 2021) {
        rawDate = carimboStr;
    } else {
        rawDate = dataAtendimentoStr; // Data válida e >= 2021
    }
} else if (carimboStr !== "") {
    rawDate = carimboStr; // Plano B: se atendimento estiver vazio, usa carimbo
}

// --- TRAVA DE DATA VAZIA E CABEÇALHOS ---
// Se a data estiver vazia, não tiver números ou for o cabeçalho, pula a linha
if (!rawDate || !/\d/.test(rawDate) || rawDate.toLowerCase().includes('carimbo')) return;