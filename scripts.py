import math
import cmath
import math
import os
from itertools import combinations
from sympy import symbols, Eq, solve
import ast
from itertools import groupby
import sympy
import csv
import re
from sympy import I, re, im


def calcular_complexo(expressao):
    expressao = expressao.replace(' ', '')  # Remover espaços em branco
    if 'sen' in expressao:
        expressao = sen_para_cos(expressao)

    inicio_parenteses = expressao.find('(')
    fim_parenteses = expressao.find(')')
    dentro_parenteses = expressao[inicio_parenteses+1:fim_parenteses]

    if '-' in dentro_parenteses:
        angulo_graus = - \
            float(dentro_parenteses[dentro_parenteses.rfind('-')+1:])
    elif '+' in dentro_parenteses:
        angulo_graus = float(
            dentro_parenteses[dentro_parenteses.rfind('+')+1:])
    else:
        angulo_graus = 0

    angulo_radianos = math.radians(angulo_graus)
    magnitude = float(expressao[:expressao.find('cos')])
    complexo = cmath.rect(magnitude, angulo_radianos)

    return complexo


def excluir_linhas_repetidas(nome_arquivo):
    linhas = []

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha not in linhas:
                linhas.append(linha)

    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)


def ler_dados_arquivo3(nome_arquivo):
    configuracoes = []

    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            valores = linha.strip().split('\t')
            configuracao = []

            for val in valores:
                if val.isdigit():
                    configuracao.append(int(val))
                elif val == 'None':
                    configuracao.append(None)
                else:
                    try:
                        complex_val = ast.literal_eval(val)
                        if isinstance(complex_val, complex):
                            configuracao.append(complex_val)
                        else:
                            configuracao.append(float(val))
                    except (ValueError, SyntaxError):
                        configuracao.append(val)

            configuracoes.append(configuracao)

    return configuracoes


def excluir_linhas_tensao_isolada(nome_arquivo, terra):
    linhas = ler_dados_arquivo3(nome_arquivo)

    grupos = groupby(linhas, key=lambda x: x[0])

    for no_origem, grupo in grupos:
        for linha in grupo:
            no_origem, no_destino, R, L, C, V, I = linha
            if all(val is None for val in (R, L, C, I)) and V is not None and terra in no_destino:
                #print("FONTE ISOLADA LIGADO AO TERRA")
                tensao_isolada = linha
                linhas = list(
                    filter(lambda x: not x[0].startswith(no_origem), linhas))
                linhas.append(tensao_isolada)
                linhas = sorted(linhas, key=lambda x: x[0])
                with open(nome_arquivo, 'w') as arquivo:
                    for linha in linhas:
                        arquivo.write('\t'.join(str(item)
                                      for item in linha) + '\n')
                break
    return


def ler_dados_arquivo(nome_arquivo, terra=None):
    configuracoes = []
    excluir_linhas_repetidas(nome_arquivo)
    excluir_linhas_tensao_isolada(nome_arquivo, terra)

    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            valores = linha.strip().split('\t')

            #Verifica se a linha começa com o valor do parâmetro 'terra'
            if terra is not None and valores[0] == terra:
                continue  # Ignora a linha

            configuracao = []

            for val in valores:
                if val.isdigit():
                    configuracao.append(int(val))
                elif val == 'None':
                    configuracao.append(None)
                else:
                    try:
                        complex_val = ast.literal_eval(val)
                        if isinstance(complex_val, complex):
                            configuracao.append(complex_val)
                        else:
                            configuracao.append(float(val))
                    except (ValueError, SyntaxError):
                        configuracao.append(val)

            configuracoes.append(configuracao)

    return configuracoes


def ler_dados_arquivo2(nome_arquivo, terra=None):
    configuracoes = []
    excluir_linhas_repetidas(nome_arquivo)
    excluir_linhas_tensao_isolada(nome_arquivo, terra)

    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            valores = linha.strip().split('\t')

            #Verifica se a linha começa com o valor do parâmetro 'terra'
            if terra is not None and valores[0] == terra:
                continue  # Ignora a linha

            configuracao = []

            for val in valores:
                if val.isdigit():
                    configuracao.append(int(val))
                elif val == 'None':
                    configuracao.append(None)
                elif 'cos' in val or 'sen' in val:
                    complexo = calcular_complexo(val)
                    configuracao.append(complexo)
                else:
                    try:
                        complex_val = ast.literal_eval(val)
                        if isinstance(complex_val, complex):
                            configuracao.append(complex_val)
                        else:
                            configuracao.append(float(val))
                    except (ValueError, SyntaxError):
                        configuracao.append(val)

            configuracoes.append(configuracao)

    return configuracoes

#Calcula a impedancia dos Resistores, Indutores e Capacitores


def Zl(w, L):
    return (w*L)*1j


def Zc(w, C):
    return 1 / ((w*C)*1j)


def Zr(R):
    return R


def fasor(complex):
    modulo, fase = cmath.polar(complex)
    fase = math.degrees(fase)
    return str(modulo) + " fase " + str(fase) + "º"


'''
#Está parte do circuito comentada se refe-re a uma outra abordagem para organizar um circuito em 
#Um circuito série equivalente, devido ao tempo eu fiz outras abordagem como fazer a analise
#Nodal, devido a isso, deixei está parte comentada como uma forma de retomar
#Esse projeto de simulador de circuitos senoidais

def paralelo(z_values):
    return 1 / sum(1 / z for z in z_values)

def serie(z1, z2):
    return z1+z2

def encontrar_linhas_em_paralelo(configuracoes):
    linhas_em_paralelo = []

    for i in range(len(configuracoes)):
        linha1 = configuracoes[i]
        no1_l1 = linha1[0]
        no2_l1 = linha1[1]
        v_l1 = linha1[5]
        i_l1 = linha1[6]

        #Verificar se a linha possui fonte de tensão ou corrente
        if v_l1 is not None or i_l1 is not None:
            continue

        #Verificar se a linha possui apenas um único componente
        if sum(x is not None for x in linha1[2:5]) != 1:
            continue

        for j in range(i + 1, len(configuracoes)):
            linha2 = configuracoes[j]
            no1_l2 = linha2[0]
            no2_l2 = linha2[1]
            v_l2 = linha2[5]
            i_l2 = linha2[6]

            #Verificar se a linha possui fonte de tensão ou corrente
            if v_l2 is not None or i_l2 is not None:
                continue

            #Verificar se a linha possui apenas um único componente
            if sum(x is not None for x in linha2[2:5]) != 1:
                continue

            if (no1_l1 == no1_l2) and (no2_l1 == no2_l2):
                if linha1 not in linhas_em_paralelo:
                    linhas_em_paralelo.append(linha1)
                if linha2 not in linhas_em_paralelo:
                    linhas_em_paralelo.append(linha2)

    return linhas_em_paralelo


def encontrar_linhas_em_serie(configuracoes):
    linhas_em_serie = []

    for linha in configuracoes:
        componentes = linha[2:5]
        componentes_validos = [c for c in componentes if c is not None]

        if len(componentes_validos) > 1:
            linhas_em_serie.append(linha)

    return linhas_em_serie


def z_equivalente_paralelo(linhas_paralelo):
    #Inicializa com a primeira linha em paralelo
    z_equivalente = linhas_paralelo[0].copy()

    for linhas in linhas_paralelo[1:]:
        z_equivalente[2] = None
        z_equivalente[3] = None
        z_equivalente[4] = None
        z_equivalente[5] = None
        z_equivalente[6] = None

        for linha in linhas:
            for i in range(2, 7):
                if linha[i] is not None:
                    if z_equivalente[i] is None:
                        z_equivalente[i] = linha[i]
                    else:
                        z_equivalente[i] = paralelo(z_equivalente[i], linha[i])
                        z_equivalente[i] = paralelo(z_equivalente[i], linha[i])

    return z_equivalente


def MontarCircuito(configuracoes):

    linhas_paralelo = encontrar_linhas_em_paralelo(configuracoes)
    linhas_em_serie = encontrar_linhas_em_serie(configuracoes)

    print("Linhas em paralelo")
    for linha1 in linhas_paralelo:
        print(linha1)

    print("Linhas em series")
    for linha in linhas_em_serie:
        print(linha)
'''


def encontrar_listas_nos_iguais(configuracoes):
    listas_nos_iguais = []

    for i in range(len(configuracoes)):
        linha1 = configuracoes[i]
        no1_l1 = linha1[0]
        no2_l1 = linha1[1]

        for j in range(i + 1, len(configuracoes)):
            linha2 = configuracoes[j]
            no1_l2 = linha2[0]
            no2_l2 = linha2[1]

            if (no1_l1 == no1_l2) and (no2_l1 == no2_l2):
                listas_nos_iguais.append((linha1, linha2))

    return listas_nos_iguais


def obter_nos(componentes):
    nos = set()
    for comp in componentes:
        no_origem, no_destino, *_ = comp
        nos.add(no_origem)
        nos.add(no_destino)
    return list(nos)


def obter_nos_origem(configuracoes):
    nos_origem = set()

    for config in configuracoes:
        no_origem = config[0]
        nos_origem.add(no_origem)

    return list(nos_origem)


def obter_ramos(lista):
    primeiros_valores = []
    for linha in lista:
        primeiros_valores.append(linha[:2])
    return primeiros_valores


def identifica_tensao_dependente(v):
    text = 'I_'
    for i in range(100):
        if text+str(i) in str(v):
            return True
    return False
#Separa o numero da tensão de sua corrente


def fonte_t_dependente(v):
    #Encontrar o número usando expressão regular
    numero = float(re.findall(r'\d+(?:\.\d+)?', v)[0])
    #Encontrar o índice usando expressão regular
    indice = re.findall(r'[A-Za-z]_\d+', v)[0]

    return numero, symbols(indice)


def montar_sistema_equacoes(nos, componentes, omega, t_or_f):
    #Criação das variáveis simbólicas para as tensões nos nós
    tensoes_nos = symbols(' '.join(nos))

    #Lista para armazenar as equações do sistema
    equacoes = []
    sistema_eq = []
    correntes = []
    resultados_dict = {}

    #Ordenar a lista de componentes pelo nó de origem
    componentes_ordenados = sorted(componentes, key=lambda x: x[0])

    #Agrupar os componentes pelo nó de origem
    grupos = groupby(componentes_ordenados, key=lambda x: x[0])
    tensao_unica = {}

    #Iterar sobre os grupos
    for no_origem, grupo in grupos:
        for comp in grupo:
            no_origem, no_destino, R, L, C, V, I = comp

            if t_or_f:
                Zr_value = Zr(R) if R is not None else 0
                Zl_value = Zl(omega, L) if L is not None else 0
                Zc_value = Zc(omega, C) if C is not None else 0
                soma_componentes = sum((Zr_value, Zl_value, Zc_value))
                #print(soma_componentes)
            else:
                soma_componentes = sum(valor for valor in (
                    R, L, C) if valor is not None)
                #print("Soma Componentes: ", soma_componentes)

            indice_origem = nos.index(no_origem)
            indice_destino = nos.index(no_destino)

            print("SOMA", soma_componentes)

            if identifica_tensao_dependente(V):
                ganho_tensao, correnteET = fonte_t_dependente(V)
                ganho_tensao *= -1
                eq = (((tensoes_nos[indice_origem] - tensoes_nos[indice_destino] -
                      (ganho_tensao*correnteET)) / (soma_componentes)))
                print("Ganho de tensão:", ganho_tensao)
            elif all(x is None for x in (R, L, C)) and V is not None:
                tensao_unica[tensoes_nos[indice_origem]] = V
                eq = (
                    ((tensoes_nos[indice_origem] - tensoes_nos[indice_destino] - (V))))
            elif I is not None:
                eq = I
            elif V is not None:
                eq = (
                    ((tensoes_nos[indice_origem] - tensoes_nos[indice_destino] - (V)) / (soma_componentes)))
            else:
                eq = (
                    ((tensoes_nos[indice_origem] - tensoes_nos[indice_destino]) / (soma_componentes)))
                #print("EQUAÇÃO: ", eq)

            #print(str(tensoes_nos[indice_origem]), "->", str(tensoes_nos[indice_destino]), eq)
            resultado = str(tensoes_nos[indice_origem]) + \
                " -> " + str(tensoes_nos[indice_destino])
            resultados_dict[resultado] = eq
            equacoes.append(eq)
            correntes.append(eq)
            #print(eq)
            #print("Linha: ", comp, "No: ", no_origem)

        sistema_eq.append(Eq(sum(equacoes), 0))
        equacoes.clear()
    print("CORRENTES____________-")
    print(correntes)
    print("____________________")

    return sistema_eq, tensoes_nos, correntes, tensao_unica


def calcular_sistema(sistema, tensoes_nos, terra, tensao_unica):
    sistema = [eq.subs(terra, 0) for eq in sistema]
    '''
    print("Tensao unica:", tensao_unica)
    if len(tensao_unica) > 0:
        for chave, valor in tensao_unica.items():
            sistema = [eq.subs(chave, valor) for eq in sistema]

    print("SISTEMA", sistema)
    print("tensoes_nos", tensoes_nos)
    '''
    solucao = solve(sistema, tensoes_nos)
    if len(tensao_unica) > 0:
        for chave, valor in tensao_unica.items():
            solucao[chave] = valor
        solucao = dict(sorted(solucao.items(), key=lambda x: str(x[0])))
        solucao[terra] = 0
    else:
        solucao[terra] = 0

    print("SOLUCAO", solucao)
    return solucao


def Tensoes(tensoes_nos, w):
    #print("Tensoes nos nós")
    Texto = ''
    print("#######")
    print(tensoes_nos)
    for chave, valor in tensoes_nos.items():
        if valor == 0:
            Texto += f"{chave} {valor}\n"
            #print(chave, valor)
            continue
        magnitude, angulo_rad = cmath.polar(valor)
        angulo_graus = math.degrees(angulo_rad)  # Converter para graus

        Texto += f"Para o nó: {chave}\n"

        if im(valor) != 0:
            Texto += "Complexo:\n"
            Texto += f"{valor}\n"
            Texto += "Dominio da frequencia:\n"
            Texto += f"{round(magnitude, 3)} < {round(angulo_graus, 3)}º V\n"
            Texto += "Dominio do Tempo:\n"
            Texto += f"{chave}(t) = {round(magnitude, 3)}cos({w}t + ({round(angulo_graus, 3)}º))V\n\n"
        else:
            Texto += f"{chave} = {round(magnitude, 3)}V\n\n"
        #print("----------------------------------------------------------")
    return Texto


def obter_descricao_ramo(dados):
    descricao = ""
    componentes = []

    for i in range(2, len(dados)):
        if dados[i] is not None:
            if i == 2:
                componentes.append(f"Resistor {dados[i]}Ω")
            elif i == 3:
                componentes.append(f"Indutor {dados[i]}H")
            elif i == 4:
                componentes.append(f"Capacitor {dados[i]}F")

    if componentes:
        descricao = f"Ramo {dados[0]} -> {dados[1]} que contém: "
        descricao += ", ".join(componentes)

    return descricao


def Correntes(correntes_ramos, ramo, w, configuracoes):
    #print("Corrente nos ramos")
    Texto = ''
    for i in range(len(correntes_ramos)):
        if correntes_ramos[i] == 0:
            #print(ramo[i], correntes_ramos[i])
            Texto += f"{ramo[i]}, {correntes_ramos[i]}"
            continue
        #print("teste: ", correntes_ramos[i])
        if isinstance(correntes_ramos[i], sympy.Expr) and sympy.re(correntes_ramos[i]) < 0:
            correntes_ramos[i] = -correntes_ramos[i]

        magnitude, angulo_rad = cmath.polar(correntes_ramos[i])
        angulo_graus = math.degrees(angulo_rad)  # Converter para graus
        #angulo_graus += 180 if angulo_graus < 0 else 0

        #Texto += obter_descricao_ramo(configuracoes[i])
        if im(correntes_ramos[i]) != 0:
            Texto += f"Para a corrente do {obter_descricao_ramo(configuracoes[i])}\n"
            Texto += "Complexo:\n"
            Texto += f"{correntes_ramos[i]}\n"
            Texto += "Dominio da frequencia:\n"
            Texto += f"{round(magnitude, 4)} < {round(angulo_graus, 4)}º A\n"
            Texto += "Dominio do Tempo:\n"
            Texto += f"i_{i+1}(t) = {round(magnitude, 4)}cos({w}t + ({round(angulo_graus, 4)}º))A\n\n"
        else:
            Texto += f"Para a corrente do {obter_descricao_ramo(configuracoes[i])}\n"
            Texto += f"I_{i+1} = {round(magnitude, 4)}A\n\n"
    return Texto


def calcular_correntes(correntes, valores_subs):
    correntes_calculadas = []

    print("___________________________")
    print(correntes)
    print(valores_subs)
    print("___________________________")
    for i in correntes:
        if isinstance(i, sympy.Expr):
            correntes_calculadas.append(i.subs(valores_subs))
        else:
            correntes_calculadas.append(i)
            continue

    return correntes_calculadas

#Converte de sen para cos, caso o usuario passe um valor do tipo 30sen(5t + 50)
def sen_para_cos(expressao):
    indice_sen = expressao.find('sen')
    magnitude = expressao[:indice_sen]
    angulo = expressao[indice_sen + 3:]
    parte1 = ''
    for char in angulo:
        if char in ['+', '-', ')']:
            break
        parte1 += char

    match = re.search(r'[-+]?\d+\b', angulo)
    numero = 0
    text = ''
    if match:
        numero = int(match.group()) if match else 0
    novo_angulo = float(numero - 90)
    if novo_angulo > 0:
        text = "+" + str(novo_angulo)
    else:
        text = str(novo_angulo)

    nova_expressao = magnitude + 'cos' + parte1 + text + ')'

    return nova_expressao


'''
#Testes preliminares
nome_arquivo = 'saida.txt'
configuracoes = ler_dados_arquivo2(nome_arquivo)
nos = sorted(obter_nos(configuracoes))
ramos = obter_ramos(configuracoes)
terra = 'b'
w = 5000
tempo_frequencia = True #True para entradas no dominio do tempo e False para entradas no dominio da frequencia

equacoes, tensoes_nos, correntes, tensao_unica = montar_sistema_equacoes(nos, configuracoes, w, tempo_frequencia)
tensoes_nos_ = calcular_sistema(equacoes, tensoes_nos, terra, tensao_unica)
resultado_correntes = calcular_correntes(correntes, tensoes_nos_)

print("Equações:")
print(equacoes)
print("Tensoes:")
print(tensoes_nos_)
print("Correntes:")
print(resultado_correntes)
'''
#Tensoes(tensoes_nos_, w)
#print("####################################################################################")
#Correntes(resultado_correntes, ramos, w)
