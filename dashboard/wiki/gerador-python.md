# 📖 Script Gerador de Dados Sintéticos (Python)

O arquivo `gerador-csv.py` é uma ferramenta de suporte desenvolvida para criar bases de dados massivas e realistas. Ele permite testar a estabilidade do Dashboard, o desmembramento de serviços e as funções de limpeza de dados antes da aplicação em produção.



## 1. Objetivo do Script

Para validar se os gráficos e filtros funcionam corretamente com milhares de registros, utilizamos dados sintéticos. O script simula o comportamento real de preenchimento do Google Forms, incluindo:

* **Múltiplas Escolhas:** Atendimentos com um ou mais serviços marcados.
* **Dados Incompletos:** Datas de atendimento vazias e idades não informadas para testar as lógicas de *fallback*.
* **Sujeira no campo "Outros":** Inserção de termos aleatórios para validar a função de padronização.



## 2. Configurações Básicas

No topo do arquivo, você encontrará as variáveis de controle:

```python
NUM_LINHAS = 10000            # Quantidade de atendimentos a gerar
ARQUIVO_SAIDA = 'dados_naf.csv' # Nome do arquivo final

```



## 3. Lógicas de Simulação Realista

O script não gera apenas dados aleatórios, ele segue regras de negócio específicas do NAF:

### 🕒 Inteligência Temporal

* **Carimbo de data/hora:** Gerado aleatoriamente entre 2024 e 2026.
* **Data de Atendimento:** Em 10% dos casos, o script deixa este campo vazio para forçar o Dashboard a usar o Carimbo de data/hora como plano B.

### 📊 Serviços e "Outros"

* **Pesos de Probabilidade:** 70% dos atendimentos simulados possuem apenas 1 serviço, enquanto 30% simulam múltiplas escolhas (2 ou 3 serviços).
* **Campo "Outros":** Em 15% dos casos, o serviço "Outros" é adicionado, sorteando um texto da lista `TEXTOS_OUTROS` (ex: "recuperar senha gov", "malha fina").

### 🧹 Teste de Resiliência (Idade e Folhas)

* O script insere intencionalmente textos como "não informou" ou campos vazios na coluna de **IDADE** em 5% dos casos.
* Isso serve para garantir que o Dashboard não trave ao tentar calcular a média de idade com valores não numéricos.



## 4. Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Abra o terminal na pasta do projeto.
3. Execute o comando:
```bash
python gerador-csv.py

```


4. O arquivo `.csv` será gerado na mesma pasta, pronto para ser importado no Google Sheets.



## 5. Importação para o Dashboard

Para testar os dados gerados no seu sistema:

1. Abra uma planilha do Google.
2. Vá em **Arquivo > Importar > Fazer upload** e selecione o arquivo gerado.
3. Escolha a opção **"Substituir planilha atual"**.
4. Copie o ID desta nova planilha e cole nas **Propriedades do Script** do seu Dashboard.



## 💡 Dica para Desenvolvedores

Ao adicionar um novo serviço oficial ao Google Forms, lembre-se de incluí-lo também na lista `TIPOS_ATENDIMENTO_OFICIAIS` dentro deste script Python. Isso garante que seus testes de estresse sempre reflitam a estrutura atual do formulário.