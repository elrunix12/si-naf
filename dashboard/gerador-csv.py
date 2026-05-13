import csv
import random
from datetime import datetime, timedelta

# Configurações do teste
NUM_LINHAS = 10000
ARQUIVO_SAIDA = 'dados_naf_10000.csv'

CABECALHO = [
    "Carimbo de data/hora", "NOME DO CONTRIBUINTE", "CPF", "Data de Atendimento", 
    "Tipo de usuário dos serviços", "O atendimento prestado foi conclusivo?", 
    "Tipo de Atendimento", "Se respondeu outro, especifique aqui", "Pontuação", 
    "Se houver, quantas folhas foram impressas:", "IDADE", "SEXO", "MUNICÍPIO DE RESIDÊNCIA"
]

TIPOS_ATENDIMENTO_OFICIAIS = [
    "Auxílio à elaboração e orientações sobre a Declaração de Ajuste Anual do IRPF",
    "Auxílio à inscrição e Informações cadastrais de CPF",
    "Auxílio à inscrição e Informações cadastrais do CNPJ",
    "Auxílio à emissão e informações sobre Certidões Negativas de Débitos PF e PJ",
    "Auxílio à consulta à situação fiscal",
    "Agendamento on-line de atendimentos na RFB",
    "Informações e auxílio à regularização de CPF Suspenso",
    "Informações e auxílio à elaboração de pedido de isenção de IRPF para portadores de moléstias graves",
    "Orientações e auxílio à elaboração de pedidos de isenção de IPI/IOF na compra de veículos por portadores de deficiência física, mental ou visual",
    "Auxílio à apresentação de pedidos de restituição de pagamentos indevidos e/ou a maior (Perdcomps)",
    "Informações gerais sobre ITR",
    "Auxílio à inscrição e Informações gerais sobre o Microempreendedor Individual",
    "Auxílio à inscrição e Informações gerais sobre o Simples Nacional",
    "Auxílio à inscrição e informações cadastrais da matrícula CEI",
    "Informações e auxílio no eSocial do empregador doméstico",
    "Auxílio à emissão e informações sobre guias para o recolhimento da contribuição previdenciária de Produtores Rurais Pessoa Física, Segurado Especial, Contribuinte Individual e obras de pessoas físicas",
    "Orientações e auxílio ao cumprimento de obrigações tributárias acessórias para associações e demais entidades sem fins lucrativos",
    "Informações e auxilio para a obtenção de Certificado Digital;",
    "Informações e auxilio para realizar a opção pelo Domicílio Tributário Eletrônico - DTE;",
    "Auxílio à habilitação nos sistemas RADAR e Siscomex;",
    "Informações sobre regras de importação e exportação através dos Correios;",
    "Informações sobre Regras de Bagagem."
]

TEXTOS_OUTROS = [
    "recuperar senha gov", "gov.br ouro", ".", "nada", "nao lembro",
    "esqueci a senha do ecac", "malha fina", "pendencia na receita",
    "retificadora", "imposto de renda atrasado", "darf sicalc", "multa", 
    "parcelamento", "ajuda inss", "cancelar mei", "alterar cnpj",
    "queria saber sobre o cpf", "asdfasdfasdf", "-", "12345"
]

MUNICIPIOS = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Campinas", "Guarulhos", "Osasco", "Niterói", "Contagem"]

def gerar_data_aleatoria(inicio, fim):
    delta = fim - inicio
    segundos_aleatorios = random.randint(0, int(delta.total_seconds()))
    return inicio + timedelta(seconds=segundos_aleatorios)

def main():
    data_inicio = datetime(2024, 1, 1)
    data_fim = datetime(2026, 5, 1)

    print(f"Gerando {NUM_LINHAS} registros...")

    with open(ARQUIVO_SAIDA, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        # Usa o padrão do Google Sheets para o Brasil: delimitador de vírgula, com aspas em campos contendo vírgulas
        writer = csv.writer(arquivo_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(CABECALHO)

        for i in range(NUM_LINHAS):
            # 1. Datas (Carimbo e Atendimento)
            carimbo_dt = gerar_data_aleatoria(data_inicio, data_fim)
            carimbo_str = carimbo_dt.strftime("%d/%m/%Y %H:%M:%S")
            
            # Simulando que a data de atendimento pode ser do mesmo dia, de dias anteriores, ou vazia (10% de chance)
            if random.random() < 0.10:
                data_atendimento_str = ""
            else:
                dias_atraso = random.randint(0, 5)
                atendimento_dt = carimbo_dt - timedelta(days=dias_atraso)
                data_atendimento_str = atendimento_dt.strftime("%d/%m/%Y")

            # 2. Dados Sensíveis / Básicos
            nome = f"Contribuinte Teste {i+1}"
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            
            # 3. Perfis
            tipo_usuario = random.choice(["PESSOA FÍSICA", "PESSOA JURÍDICA"])
            conclusivo = random.choice(["SIM", "NÃO"])
            
            # 4. Serviços (Simulando múltiplas escolhas separadas por vírgula)
            qtd_servicos = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
            servicos_escolhidos = random.sample(TIPOS_ATENDIMENTO_OFICIAIS, qtd_servicos)
            
            # Adiciona "Outros" em 15% dos casos
            texto_outros = ""
            if random.random() < 0.15:
                servicos_escolhidos.append("Outros")
                texto_outros = random.choice(TEXTOS_OUTROS)
            
            tipo_atendimento_str = ", ".join(servicos_escolhidos)
            
            # 5. Outros Dados
            pontuacao = str(random.randint(1, 5))
            folhas = str(random.choices([0, 1, 2, 5, 10, 20], weights=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])[0])
            
            # Idade (5% de chance de vir em branco ou com texto inválido para testar o fallback de NaN)
            if random.random() < 0.05:
                idade = random.choice(["", "não informou", "idade"])
            else:
                idade = str(random.randint(18, 75))
                
            sexo = random.choice(["MASCULINO", "FEMININO", "NÃO INFORMAR"])
            municipio = random.choice(MUNICIPIOS)

            # Escreve a linha
            linha = [
                carimbo_str, nome, cpf, data_atendimento_str, tipo_usuario, 
                conclusivo, tipo_atendimento_str, texto_outros, pontuacao, 
                folhas, idade, sexo, municipio
            ]
            writer.writerow(linha)

    print(f"Sucesso! Arquivo '{ARQUIVO_SAIDA}' gerado e pronto para importação.")

if __name__ == "__main__":
    main()
