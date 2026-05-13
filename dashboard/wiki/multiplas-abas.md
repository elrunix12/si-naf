# 📖 Consolidação de Múltiplas Abas (Páginas) da Mesma Planilha

Pode haver casos em que todos os dados de que necessita estão dentro do mesmo ficheiro de Google Sheets, mas distribuídos por abas diferentes (por exemplo: "Respostas 1", "Respostas 2", etc.). O Dashboard permite consolidar estas abas como se fossem fontes de dados independentes.



## 1. O Conceito de "Fonte de Dados"

Para o Dashboard, cada aba de uma planilha é considerada uma "Fonte de Dados" única. Se quiser puxar duas abas do mesmo ficheiro, terá de configurar duas entradas nas **Propriedades do Script**, repetindo o ID da planilha mas mudando o nome da aba.



## 2. Passo a Passo da Configuração

Imagine que a sua planilha com o ID `ABC123XXX` tem duas abas que deseja somar: uma chamada `Janeiro` e outra chamada `Fevereiro`.

Deverá configurar as Propriedades do Script da seguinte forma:

| Propriedade | Valor | Explicação |
| --- | --- | --- |
| `PLANILHA_ID_1` | `ABC123XXX` | O ID da planilha. |
| `TAB_NOME_1` | `Janeiro` | O nome exato da primeira aba. |
| `PLANILHA_ID_2` | `ABC123XXX` | **O mesmo ID** da planilha anterior. |
| `TAB_NOME_2` | `Fevereiro` | O nome exato da segunda aba. |

---

## 3. Regras Cruciais para Múltiplas Abas

### Obrigatoriedade do `TAB_NOME_X`

Se configurar dois IDs iguais (`PLANILHA_ID_1` e `PLANILHA_ID_2`) mas **não** preencher as propriedades `TAB_NOME`, o script irá ler duas vezes a primeira aba da planilha. Isto fará com que os seus dados apareçam duplicados no Dashboard. Exemplos:


**Cenário A:** Duplicação Acidental (Risco)

Se repetir o ID e deixar as propriedades `TAB_NOME_X` em branco, o script lerá a primeira aba da planilha em ambas as chamadas.

* **Resultado:** Os dados serão **duplicados**. Se a planilha tem 100 registos, o Dashboard mostrará 200. Todos os gráficos e KPIs (total de pessoas, MEIs, folhas) exibirão o dobro do valor real.

**Cenário B:** Consolidação Legítima (Uso Correto)

Se repetir o ID, mas definir nomes de abas diferentes para cada entrada.

* **Exemplo de Configuração:**
* `PLANILHA_ID_1`: `ID_DA_PLANILHA_A` | `TAB_NOME_1`: `Respostas 2023`
* `PLANILHA_ID_2`: `ID_DA_PLANILHA_A` | `TAB_NOME_2`: `Respostas 2024`


* **Resultado:** O Dashboard funcionará perfeitamente. Ele entenderá que deve aceder ao mesmo ficheiro, mas extrair dados de "gavetas" (abas) diferentes, somando-os no painel final.

| Configuração | ID Repetido? | Abas Diferentes? | Resultado no Dashboard |
| --- | --- | --- | --- |
| **Cenário A** | Sim | Não | **Erro:** Dados duplicados (clonados). |
| **Cenário B** | Sim | Sim | **Sucesso:** Consolidação correta de abas. |


**Sempre que repetir um ID de planilha**, o uso da propriedade `TAB_NOME_X` torna-se obrigatório para distinguir as páginas.

### Nomes Exatos

O Google Apps Script é sensível a letras maiúsculas e espaços. Se a aba se chamar `Respostas 1` (com espaço) e escrever `Respostas1` (sem espaço) na propriedade, o sistema não encontrará os dados. Verifique sempre se o nome está idêntico ao que aparece na parte inferior da sua folha de cálculo.

---

## 4. Vantagens desta Abordagem

* **Histórico Consolidado:** Permite manter abas separadas por ano ou semestre no Google Sheets (para organização interna) enquanto o Dashboard mostra o volume total acumulado de todas elas.
* **Performance:** O script faz chamadas separadas para cada aba, garantindo que o processamento dos dados seja feito de forma organizada antes da união final.

## 💡 Dica de Organização

Se a sua planilha tiver muitas abas mas apenas uma for a "oficial" (a que recebe as respostas do formulário), não precisa de configurar o `TAB_NOME_X`. O Dashboard irá sempre ler a primeira aba por padrão. Utilize esta configuração de múltiplas abas apenas quando precisar realmente de somar dados de páginas diferentes de um mesmo ficheiro.