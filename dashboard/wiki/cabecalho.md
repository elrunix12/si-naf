# 📖 Mapeamento Dinâmico de Colunas

Diferente de sistemas rígidos que quebram se você mudar uma coluna de lugar, o Dashboard NAF utiliza um sistema de "caça-palavras" para ler o cabeçalho da sua planilha. A ordem das perguntas no Google Forms não importa; o que importa é que o título da pergunta contenha uma palavra-chave específica.



## 1. Onde isso acontece no código?

O mapeamento ocorre na função `processarDadosBrutos(rawData)`, logo no início do processo de leitura, através de constantes (`const`) que usam o comando `.find()` e `.includes()`.

```javascript
const folhasKey = colunas.find(k => limparTexto(k).includes('folhas'));
const tipoKey = colunas.find(k => limparTexto(k).includes('tipo de atendimento') && !limparTexto(k).includes('usuario'));
const outroKey = colunas.find(k => limparTexto(k).includes('respondeu outro'));
const sexoKey = colunas.find(k => limparTexto(k).includes('sexo'));
// ...

```



## 2. A Função `limparTexto()` (Anti-Erros)

Para evitar que erros de digitação no cabeçalho quebrem o sistema, o Dashboard passa os nomes das colunas por uma função de limpeza antes de procurá-las.
A função `limparTexto()` pega o cabeçalho e:

1. Transforma tudo em letras minúsculas.
2. Remove todos os acentos (ex: "MUNICÍPIO" vira "municipio").

Portanto, quando você for alterar as palavras-chave no código, **escreva sempre em letras minúsculas e sem acentos** dentro dos parênteses do `.includes('...')`.



## 3. Tabela de Palavras-Chave Obrigatórias

Esta é a lista de raízes de texto que o sistema procura atualmente. Se a pergunta no Google Forms não contiver esse texto exato, a coluna será ignorada e o dado não aparecerá no painel.

| Variável no Código | Texto Procurado (`.includes`) | Exemplo de Pergunta Aceita no Forms |
|  |  |  |
| `folhasKey` | `folhas` | *Se houver, quantas **folhas** foram impressas?* |
| `outroKey` | `respondeu outro` | *Se **respondeu outro**, especifique aqui:* |
| `sexoKey` | `sexo` | *Qual o seu **sexo** / gênero?* |
| `conclusivoKey` | `conclusivo` | *O atendimento prestado foi **conclusivo**?* |
| `municipioKey` | `municipio` | *Qual o **município** de residência?* |
| `tipoUserKey` | `tipo de usuario` | ***Tipo de usuário** dos serviços (PF ou PJ)?* |

### Regras de Exceção:

* **Tipo de Atendimento:** O sistema procura por `tipo de atendimento`, mas exclui colunas que também tenham a palavra `usuario`. Isso evita que ele confunda a coluna de "Tipo de usuário" com a coluna de serviços prestados.
* **Idade:** O código exige a correspondência exata para evitar confusões. A pergunta no Forms deve se chamar exatamente `IDADE` (o sistema limpa para `idade`). Se a pergunta for "Qual a sua idade?", o script não vai encontrar.



## 4. Como alterar uma palavra-chave?

Se a unidade do NAF decidir mudar a redação da pergunta no formulário, você precisará atualizar o código.

**Cenário:** O formulário mudou a pergunta de *"Se houver, quantas folhas foram impressas?"* para *"Número de cópias entregues"*.

**Passo a passo da correção:**

1. Abra o arquivo `index.html`.
2. Localize a linha: `const folhasKey = colunas.find(k => limparTexto(k).includes('folhas'));`
3. Troque a palavra `'folhas'` pela nova palavra-chave. Escolha uma palavra única, toda em minúscula e sem acento:

```javascript
// CÓDIGO CORRIGIDO:
const folhasKey = colunas.find(k => limparTexto(k).includes('copias'));

```



## 5. Hierarquia Temporal (A dupla verificação de Data)

O sistema possui uma inteligência específica para lidar com as datas, garantindo que nenhum atendimento fique órfão (sem mês/ano) caso o aluno esqueça de preencher.

```javascript
const keyAtendimento = colunas.find(k => limparTexto(k).includes('data de atendimento'));
const keyCarimbo = colunas.find(k => limparTexto(k).includes('carimbo'));

```

1. **Plano A:** Ele procura a coluna que contenha `data de atendimento` e tenta usá-la.
2. **Plano B:** Se o aluno deixou essa data em branco ou digitou um texto inválido, o sistema recua imediatamente e puxa a data do `carimbo` (Timestamp), que é gerado automaticamente pelo servidor do Google Forms no momento do envio e não pode ser apagado.