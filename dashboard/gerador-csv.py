import csv
import random
import os
import hashlib
from datetime import datetime, timedelta

# ==============================================================================
# CONFIGURAÇÕES E DICIONÁRIOS
# ==============================================================================
QTD_ARQUIVOS = 3 # Quantidade de arquivos CSV a serem gerados
NUM_LINHAS = 5000
PASTA_TESTE = 'test'

CABECALHO = [
    "Carimbo de data/hora", "NOME DO CONTRIBUINTE", "CPF", "Telefone do Titular",
    "E-mail para contato", "Endereço Completo", "Carga Horária", "Data de Atendimento",
    "Tipo de usuário dos serviços", "O atendimento prestado foi conclusivo?",
    "Tipo de Atendimento", "Se respondeu outro, especifique aqui", "Pontuação",
    "Se houver, quantas folhas foram impressas:", "IDADE", "SEXO", "MUNICÍPIO DE RESIDÊNCIA"
]

CATEGORIAS_DICIONARIO = {
    "Imposto de Renda (IRPF)": ["AUXÍLIO À ELABORAÇÃO E ORIENTAÇÕES SOBRE A DECLARAÇÃO DE AJUSTE ANUAL DO IRPF", "INFORMAÇÕES E AUXÍLIO À ELABORAÇÃO DE PEDIDO DE ISENÇÃO DE IRPF PARA PORTADORES DE MOLÉSTIAS GRAVES", "INFORMAÇÕES GERAIS SOBRE ITR"],
    "Cadastros (CPF e CNPJ)": ["AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES CADASTRAIS DE CPF", "AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES CADASTRAIS DO CNPJ", "INFORMAÇÕES E AUXÍLIO À REGULARIZAÇÃO DE CPF SUSPENSO", "AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES CADASTRAIS DA MATRÍCULA CEI"],
    "Certidões e Situação Fiscal": ["AUXÍLIO À EMISSÃO E INFORMAÇÕES SOBRE CERTIDÕES NEGATIVAS DE DÉBITOS PF E PJ", "AUXÍLIO À CONSULTA À SITUAÇÃO FISCAL", "AGENDAMENTO ON-LINE DE ATENDIMENTOS NA RFB"],
    "MEI e Simples Nacional": ["AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES GERAIS SOBRE O MICROEMPREENDEDOR INDIVIDUAL", "AUXÍLIO À INSCRIÇÃO E INFORMAÇÕES GERAIS SOBRE O SIMPLES NACIONAL"],
    "Restituições e Isenções": ["AUXÍLIO À APRESENTAÇÃO DE PEDIDOS DE RESTITUIÇÃO DE PAGAMENTOS INDEVIDOS E/OU A MAIOR (PERDCOMPS)", "ORIENTAÇÕES E AUXÍLIO À ELABORAÇÃO DE PEDIDOS DE ISENÇÃO DE IPI/IOF NA COMPRA DE VEÍCULOS POR PORTADORES DE DEFICIÊNCIA FÍSICA, MENTAL OU VISUAL"],
    "Previdência e eSocial": ["INFORMAÇÕES E AUXÍLIO NO ESOCIAL DO EMPREGADOR DOMÉSTICO", "AUXÍLIO À EMISSÃO E INFORMAÇÕES SOBRE GUIAS PARA O RECOLHIMENTO DA CONTRIBUIÇÃO PREVIDENCIÁRIA DE PRODUTORES RURAIS PESSOA FÍSICA, SEGURADO ESPECIAL, CONTRIBUINTE INDIVIDUAL E OBRAS DE PESSOAS FÍSICAS"],
    "Apoio e Sistemas": ["ORIENTAÇÕES E AUXÍLIO AO CUMPRIMENTO DE OBRIGAÇÕES TRIBUTÁRIAS ACESSÓRIAS PARA ASSOCIAÇÕES E DEMAIS ENTIDADES SEM FINS LUCRATIVOS", "INFORMAÇÕES E AUXILIO PARA A OBTENÇÃO DE CERTIFICADO DIGITAL;", "INFORMAÇÕES E AUXILIO PARA REALIZAR A OPÇÃO PELO DOMICÍLIO TRIBUTÁRIO ELETRÔNICO - DTE;"],
    "Comércio Exterior": ["AUXÍLIO À HABILITAÇÃO NOS SISTEMAS RADAR E SISCOMEX;", "INFORMAÇÕES SOBRE REGRAS DE IMPORTAÇÃO E EXPORTAÇÃO ATRAVÉS DOS CORREIOS;", "INFORMAÇÕES SOBRE REGRAS DE BAGAGEM."]
}

TODOS_SERVICOS = []
MAPA_SERVICO_CATEGORIA = {}

for categoria_pai, lista_servicos in CATEGORIAS_DICIONARIO.items():
    for servico_especifico in lista_servicos:
        TODOS_SERVICOS.append(servico_especifico)
        MAPA_SERVICO_CATEGORIA[servico_especifico] = categoria_pai

TEXTOS_OUTROS = ["recuperar senha gov", "gov.br ouro", "esqueci a senha do ecac", "malha fina", "retificadora", "darf sicalc", "multa", "parcelamento", "ajuda inss", "pgfn"]
MUNICIPIOS = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Guarulhos"]
PERFIS_USUARIO = ["Pessoa Física", "Pessoa Jurídica", "Empresa Optante pelo Simples Nacional", "Microempresa Optante pelo Simples Nacional", "Entidades sem fins lucrativos"]

# Funções auxiliares
def gerar_data_aleatoria(inicio, fim):
    delta = fim - inicio
    segundos = random.randint(0, int(delta.total_seconds()))
    return inicio + timedelta(seconds=segundos)

def gerar_pool_cpfs(quantidade):
    pool = []
    for _ in range(quantidade):
        base = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
        if random.random() < 0.10: base = base[1:]
        pool.append(base)
    return pool

def gerar_hash_arquivo(caminho_arquivo):
    sha256_hash = hashlib.sha256()
    with open(caminho_arquivo, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def formatar_kpis_texto(titulo, arquivo_nome, hash_csv, num_linhas, carimbos_vazios, perfis, cpf_contagem, folhas_impressas, datas_estimadas, idade_soma, idade_qtd, genero, faixas, municipios, servicos):
    """Função para gerar o bloco de texto de um relatório (individual ou consolidado)"""
    pessoas_recorrentes = sum(1 for datas in cpf_contagem.values() if len(datas) > 1)
    total_cpfs_unicos = len(cpf_contagem)
    taxa_retorno = (pessoas_recorrentes / total_cpfs_unicos) * 100 if total_cpfs_unicos > 0 else 0
    publico_majoritario = max(perfis, key=perfis.get) if perfis else "N/A"
    media_idade = idade_soma / idade_qtd if idade_qtd > 0 else 0

    texto = f"\n==================================================\n"
    texto += f"📋 {titulo}\n"
    texto += f"==================================================\n"
    if arquivo_nome:
        texto += f"Ficheiro: {arquivo_nome}\n"
        texto += f"Hash (SHA-256): {hash_csv}\n"

    texto += f"\n📊 KPIs - ABA GERAL:\n"
    texto += f"  - Atendimentos Válidos: {num_linhas - carimbos_vazios}\n"
    texto += f"  - Público Majoritário: {publico_majoritario}\n"
    texto += f"  - Total de Pessoas Únicas (Hashes): {total_cpfs_unicos}\n"
    texto += f"  - Taxa de Retorno: {taxa_retorno:.1f}% ({pessoas_recorrentes} pessoas retornaram)\n"
    texto += f"  - Total Folhas Impressas: {folhas_impressas}\n"
    texto += f"  - Datas Estimadas Esperadas: {datas_estimadas}\n"
    texto += f"  - Linhas Ignoradas (Carimbo Inválido): {carimbos_vazios}\n"

    texto += f"\n🧠 PERFIL DO CONTRIBUINTE:\n"
    texto += f"  - Média de Idade Exata: {media_idade:.1f} anos\n"
    texto += f"  - Distribuição de Gênero:\n"
    for k, v in genero.items(): texto += f"    - {k}: {v}\n"

    texto += "\n📈 FAIXAS ETÁRIAS:\n"
    for k, v in faixas.items(): texto += f"  - {k}: {v}\n"

    texto += "\n🏢 PERFIL DO USUÁRIO:\n"
    for k, v in perfis.items(): texto += f"  - {k}: {v}\n"

    texto += "\n🌎 MUNICÍPIOS:\n"
    for k, v in municipios.items(): texto += f"  - {k.title()}: {v}\n"

    texto += "\n⚙️ SERVIÇOS OPERACIONAIS (CATEGORIAS PRINCIPAIS):\n"
    for k, v in servicos.items(): texto += f"  - {k}: {v}\n"
    return texto

# ==============================================================================
# LÓGICA PRINCIPAL
# ==============================================================================
def main():
    data_inicio = datetime(2022, 1, 1)
    data_fim = datetime(2026, 5, 1)
    cpfs_recorrentes = gerar_pool_cpfs(500)

    # 1. INICIAR VARIÁVEIS CONSOLIDADAS (TOTAIS)
    tot_genero = {"Masculino": 0, "Feminino": 0, "Não Informado": 0}
    tot_idade_soma = 0
    tot_idade_qtd = 0
    tot_faixas = {"Até 25": 0, "26 a 40": 0, "41 a 60": 0, "Acima de 60": 0, "Não Informado": 0}
    tot_perfis = {p: 0 for p in PERFIS_USUARIO}
    tot_municipios = {m.lower(): 0 for m in MUNICIPIOS}
    tot_servicos = {cat: 0 for cat in CATEGORIAS_DICIONARIO.keys()}
    tot_servicos["NÃO ESPECIFICADO"] = 0
    tot_datas_estimadas = 0
    tot_carimbos_vazios = 0
    tot_cpf_contagem = {}
    tot_folhas_impressas = 0
    tot_linhas_geradas = 0

    texto_log_final = f"Data da Geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    os.makedirs(PASTA_TESTE, exist_ok=True)

    # 2. CICLO PARA GERAR MÚLTIPLOS ARQUIVOS CSV
    for num_arquivo in range(1, QTD_ARQUIVOS + 1):
        arquivo_saida_atual = os.path.join(PASTA_TESTE, f'dados_naf_auditoria_{num_arquivo}.csv')
        print(f"A gerar arquivo {num_arquivo} de {QTD_ARQUIVOS}: {arquivo_saida_atual}...")

        # Reiniciar variáveis individuais para o arquivo atual
        ind_genero = {"Masculino": 0, "Feminino": 0, "Não Informado": 0}
        ind_idade_soma = 0
        ind_idade_qtd = 0
        ind_faixas = {"Até 25": 0, "26 a 40": 0, "41 a 60": 0, "Acima de 60": 0, "Não Informado": 0}
        ind_perfis = {p: 0 for p in PERFIS_USUARIO}
        ind_municipios = {m.lower(): 0 for m in MUNICIPIOS}
        ind_servicos = {cat: 0 for cat in CATEGORIAS_DICIONARIO.keys()}
        ind_servicos["NÃO ESPECIFICADO"] = 0
        ind_datas_estimadas = 0
        ind_carimbos_vazios = 0
        ind_cpf_contagem = {}
        ind_folhas_impressas = 0

        registros_preliminares = [{"carimbo_dt": gerar_data_aleatoria(data_inicio, data_fim), "id": i} for i in range(NUM_LINHAS)]
        registros_preliminares.sort(key=lambda x: x["carimbo_dt"])

        linhas_csv = []

        for reg in registros_preliminares:
            carimbo_dt = reg["carimbo_dt"]
            i = reg["id"]

            carimbo_str = carimbo_dt.strftime("%d/%m/%Y %H:%M:%S")
            data_atendimento_str = (carimbo_dt - timedelta(days=random.randint(0, 5))).strftime("%d/%m/%Y")
            roleta_data = random.random()

            if roleta_data < 0.05:
                carimbo_str = "Sem Carimbo"
                data_atendimento_str = ""
                ind_carimbos_vazios += 1
                tot_carimbos_vazios += 1
            elif roleta_data < 0.15:
                if carimbo_dt > (data_inicio + timedelta(days=30)):
                    data_atendimento_str = random.choice([
                        "31/02/2026", "99/99/2025", "00/13/2026", "ErroDigitação",  # calendário inexistente
                        "15/03/1969", "10/07/2016", "20/11/2019",                    # datas reais, mas antes do NAF existir
                        "01/01/2099"                                                  # data real, mas no futuro
                    ])
                    ind_datas_estimadas += 1
                    tot_datas_estimadas += 1

            datas_zuadas_possiveis = ["31/02/2026", "99/99/2025", "00/13/2026", "ErroDigitação"]
            data_atendimento_valida = bool(data_atendimento_str) and data_atendimento_str not in datas_zuadas_possiveis
            data_efetiva = data_atendimento_str if data_atendimento_valida else carimbo_dt.strftime("%d/%m/%Y")

            nome = f"Contribuinte {i+1}"
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}" if random.random() < 0.80 else random.choice(cpfs_recorrentes)

            if carimbo_str != "Sem Carimbo":
                ind_cpf_contagem.setdefault(cpf, set()).add(data_efetiva)
                tot_cpf_contagem.setdefault(cpf, set()).add(data_efetiva)

            telefone = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            email = f"contato{i}@teste.com"
            endereco = "Rua das Flores, 123"
            carga_horaria = f"{random.randint(10, 40)} horas"

            perfil = random.choice(PERFIS_USUARIO)
            if carimbo_str != "Sem Carimbo":
                ind_perfis[perfil] += 1
                tot_perfis[perfil] += 1

            conclusivo = random.choice(["SIM", "NÃO", ""])

            qtd_servicos = random.choices([0, 1, 2], weights=[0.05, 0.75, 0.2])[0]
            if qtd_servicos == 0:
                tipo_atendimento_str = random.choice(["", "Outros"])
                texto_outros = random.choice(["", "-", "."])
                if carimbo_str != "Sem Carimbo":
                    ind_servicos["NÃO ESPECIFICADO"] += 1
                    tot_servicos["NÃO ESPECIFICADO"] += 1
            else:
                servicos = random.sample(TODOS_SERVICOS, qtd_servicos)
                tipo_atendimento_str = ", ".join(servicos)
                texto_outros = random.choice(TEXTOS_OUTROS) if random.random() < 0.2 else ""
                if carimbo_str != "Sem Carimbo":
                    for s in servicos:
                        categoria_pai = MAPA_SERVICO_CATEGORIA[s]
                        ind_servicos[categoria_pai] += 1
                        tot_servicos[categoria_pai] += 1

            idade_raw = random.choices(["", "25", "26", "40", "41", "60", "61", str(random.randint(18, 80))], weights=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.65])[0]
            if carimbo_str != "Sem Carimbo":
                if not idade_raw:
                    ind_faixas["Não Informado"] += 1
                    tot_faixas["Não Informado"] += 1
                else:
                    v_idade = int(idade_raw)
                    ind_idade_soma += v_idade
                    tot_idade_soma += v_idade
                    ind_idade_qtd += 1
                    tot_idade_qtd += 1

                    if v_idade <= 25:
                        ind_faixas["Até 25"] += 1; tot_faixas["Até 25"] += 1
                    elif v_idade <= 40:
                        ind_faixas["26 a 40"] += 1; tot_faixas["26 a 40"] += 1
                    elif v_idade <= 60:
                        ind_faixas["41 a 60"] += 1; tot_faixas["41 a 60"] += 1
                    else:
                        ind_faixas["Acima de 60"] += 1; tot_faixas["Acima de 60"] += 1


            sexo_escolha = random.choice([("masculino", "Masculino"), ("FEMININO", "Feminino"), ("Não Informar", "Não Informado"), (" ", "Não Informado")])
            if carimbo_str != "Sem Carimbo":
                ind_genero[sexo_escolha[1]] += 1
                tot_genero[sexo_escolha[1]] += 1

            mun_base = random.choice(MUNICIPIOS)
            municipio = mun_base.lower() if random.random() < 0.5 else mun_base.upper()
            if carimbo_str != "Sem Carimbo":
                ind_municipios[mun_base.lower()] += 1
                tot_municipios[mun_base.lower()] += 1

            folhas_int = random.randint(0, 10)
            if carimbo_str != "Sem Carimbo":
                ind_folhas_impressas += folhas_int
                tot_folhas_impressas += folhas_int

            pontuacao = str(random.randint(1, 5))

            linha = [
                carimbo_str, nome, cpf, telefone, email, endereco, carga_horaria,
                data_atendimento_str, perfil, conclusivo, tipo_atendimento_str,
                texto_outros, pontuacao, str(folhas_int), idade_raw, sexo_escolha[0], municipio
            ]
            linhas_csv.append(linha)
            tot_linhas_geradas += 1

        # Salvar CSV Individual
        with open(arquivo_saida_atual, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(CABECALHO)
            writer.writerows(linhas_csv)

        hash_csv = gerar_hash_arquivo(arquivo_saida_atual)

        # Adicionar log individual à variável de texto final
        texto_log_final += formatar_kpis_texto(
            titulo=f"RELATÓRIO INDIVIDUAL - ARQUIVO {num_arquivo}",
            arquivo_nome=arquivo_saida_atual,
            hash_csv=hash_csv,
            num_linhas=NUM_LINHAS,
            carimbos_vazios=ind_carimbos_vazios,
            perfis=ind_perfis,
            cpf_contagem=ind_cpf_contagem,
            folhas_impressas=ind_folhas_impressas,
            datas_estimadas=ind_datas_estimadas,
            idade_soma=ind_idade_soma,
            idade_qtd=ind_idade_qtd,
            genero=ind_genero,
            faixas=ind_faixas,
            municipios=ind_municipios,
            servicos=ind_servicos
        )

    # 3. CONSTRUIR E ADICIONAR O RELATÓRIO CONSOLIDADO
    texto_log_final += formatar_kpis_texto(
        titulo="RELATÓRIO CONSOLIDADO GERAL",
        arquivo_nome=None,
        hash_csv=None,
        num_linhas=tot_linhas_geradas,
        carimbos_vazios=tot_carimbos_vazios,
        perfis=tot_perfis,
        cpf_contagem=tot_cpf_contagem,
        folhas_impressas=tot_folhas_impressas,
        datas_estimadas=tot_datas_estimadas,
        idade_soma=tot_idade_soma,
        idade_qtd=tot_idade_qtd,
        genero=tot_genero,
        faixas=tot_faixas,
        municipios=tot_municipios,
        servicos=tot_servicos
    )

    # 4. IMPRIMIR E SALVAR O TEXTO FINAL NUM ÚNICO FICHEIRO TXT
    print(texto_log_final)

    diretorio_log = os.path.join("test", "log")
    os.makedirs(diretorio_log, exist_ok=True)
    caminho_arquivo_log = os.path.join(diretorio_log, f"log-{datetime.now().strftime('%Y-%m-%d-%Hh%Mm%Ss')}.txt")

    with open(caminho_arquivo_log, "w", encoding="utf-8") as f_log:
        f_log.write(texto_log_final)

    print(f"\nSucesso! {QTD_ARQUIVOS} ficheiros CSV foram gerados.")
    print(f"O registo de auditoria com dados individuais e consolidados foi guardado em: {caminho_arquivo_log}")

if __name__ == "__main__":
    main()
