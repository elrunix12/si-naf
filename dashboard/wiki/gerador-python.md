# Script Gerador de Dados Sintéticos e Auditoria (Python)

O arquivo `gerador-csv.py` é uma ferramenta desenvolvida para criar bases de dados sintéticas estruturadas para o Dashboard NAF. O script simula entradas do Google Forms, gera casos de borda (edge cases) para validação da limpeza de dados e cria um log de auditoria com os KPIs da base gerada.

## 1. Objetivo do Script

O gerador é utilizado para validar o comportamento do Dashboard com grandes volumes de dados. Ele aplica regras para testar:

* **Desmembramento de Serviços:** Múltiplos serviços selecionados em um único atendimento.
* **Higienização de Dados:** Datas inválidas, idades vazias e inconsistências textuais no campo "Outros".
* **Métricas de Recorrência:** Simulação estruturada de CPFs repetidos para validar o cálculo da taxa de retorno.

## 2. Configurações Básicas

No início do script, as variáveis definem o volume de dados e a quantidade de arquivos a serem gerados:

```python
QTD_ARQUIVOS = 4      # Quantidade de arquivos CSV a serem gerados
NUM_LINHAS = 5000     # Quantidade de atendimentos por arquivo
PASTA_TESTE = 'test'  # Diretório principal de saída

```

Os arquivos `.csv` gerados receberão numeração automática no nome (ex: `dados_naf_auditoria_1.csv`, `dados_naf_auditoria_2.csv`).

## 3. Lógicas de Simulação

O script aplica regras estatísticas para refletir cenários de produção:

### Regras Temporais e Datas

* **Período Base:** Os atendimentos são gerados aleatoriamente entre 1 de janeiro de 2024 e 1 de maio de 2026.


* **Inconsistências:** Em 5% dos registros, o carimbo de data/hora é omitido. Em outros 10% dos registros (cumulativamente, até 15% do total), são inseridas datas de atendimento inválidas (ex: "31/02/2026", "ErroDigitação") para validar o tratamento de erros do Dashboard. Essa substituição só ocorre para atendimentos com carimbo posterior aos primeiros 30 dias do período simulado, garantindo que já exista histórico suficiente para a estimativa por mediana.



### Distribuição de Serviços

* **Probabilidades:** Há 75% de chance de o atendimento ter 1 serviço, 20% de ter 2 serviços e 5% de não possuir serviço listado (vazio ou "Outros").


* **Campo "Outros":** Quando aplicável, preenche o campo com termos predefinidos (ex: "malha fina", "recuperar senha gov") para testar a categorização textual.



### Usuários e Inconsistências

* **Recorrência:** O script utiliza um conjunto restrito de 500 CPFs predefinidos para gerar retornos e testar a lógica de clientes recorrentes do dashboard. Esse pool é gerado uma única vez e compartilhado entre todos os arquivos CSV — por isso a mesma pessoa pode aparecer em arquivos diferentes, o que permite testar a detecção de recorrência entre fontes/abas distintas, não só dentro de um único arquivo.


* **Idade e Gênero:** Em 5% dos casos, a idade fica em branco. Nos demais casos, o script sorteia com peso igual os valores exatos nos limites de cada faixa etária (25, 26, 40, 41, 60, 61), para validar as bordas de `categorizarIdade()`, além de idades aleatórias entre 18 e 80 anos. Variáveis de sexo misturam padrões de preenchimento em maiúsculas, minúsculas ou vazios.



## 4. Como Executar e Saídas Geradas

1. Certifique-se de ter o Python instalado.


2. Abra o terminal na raiz do projeto e execute:

```bash
python gerador-csv.py

```

3. O script criará (se não existirem) os diretórios correspondentes e produzirá as seguintes saídas:
* **Bases de Dados:** Vários arquivos `.csv` (conforme definido na configuração) serão salvos na pasta `test/`.
* **Gabarito de Auditoria (Log):** Um único arquivo `.txt` será salvo na subpasta `test/log/`. Este documento contém o Hash SHA-256 de cada CSV, as métricas individuais de cada arquivo e um relatório consolidado geral.



## 5. Importação para o Dashboard

Para testar os dados no sistema atual:

1. Abra uma planilha do Google.


2. Acesse **Arquivo > Importar > Fazer upload** e selecione um dos arquivos gerados (ex: `dados_naf_auditoria_1.csv`) na pasta `test`.


3. Escolha a opção **"Substituir planilha atual"**.


4. Copie o ID da planilha na URL e configure-o nas propriedades ou scripts do seu Dashboard.

**Testando múltiplas fontes:** como o pool de CPFs recorrentes é compartilhado entre os arquivos gerados, vale a pena importar `dados_naf_auditoria_1.csv` e `dados_naf_auditoria_2.csv` como duas abas ou fontes diferentes (`PLANILHA_ID_1`/`TAB_NOME_1` e `PLANILHA_ID_2`/`TAB_NOME_2`), conforme descrito em [Consolidação de Múltiplas Abas](multiplas-abas.md). Nesse caso, o **"RELATÓRIO CONSOLIDADO GERAL"** do log é o gabarito correto a usar — ele já soma os dois arquivos e calcula a recorrência considerando pessoas que aparecem em ambos.



## 6. Manutenção de Categorias

Os serviços estão organizados no dicionário `CATEGORIAS_DICIONARIO` dentro do script. Caso novos serviços ou categorias sejam adicionados ao formulário oficial do NAF, este dicionário deve ser atualizado para garantir a equivalência durante os testes e a correta geração do gabarito de auditoria.
