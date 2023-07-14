import tkinter as tk
from tkinter import scrolledtext
import scripts
from PyPDF2 import PdfFileReader
import os
import subprocess
import webbrowser
import csv

def abrir_pdf():
    pdf_path = "front.html"
    webbrowser.open(pdf_path)

#Função para obter o valor da caixa de texto do terra
def obter_terra():
    global terra
    terra = campo_terra.get()

#Função para alternar entre os domínios do tempo e da frequência


def alternar_dominio():
    global tempo_frequencia
    if var_dominio.get() == 0:
        tempo_frequencia = True
    else:
        tempo_frequencia = False


def exibir_tensoes(tensoes_texto):
    #Criar uma nova janela para exibir as tensões
    janela_tensoes = tk.Toplevel()
    janela_tensoes.title("Tensões nos NÓS")

    #Criar um widget de texto com rolagem para exibir as tensões
    texto_tensoes = scrolledtext.ScrolledText(
        janela_tensoes, width=80, height=30)
    texto_tensoes.insert(tk.END, tensoes_texto)
    texto_tensoes.pack()

    #Configurar o widget de texto como somente leitura
    texto_tensoes.config(state=tk.DISABLED)


def alterar_circuito():

    terra = campo_terra.get()
    if len(terra) == 0:
        texto_saida.config(state="normal")
        texto_saida.delete("1.0", tk.END)
        texto_saida.insert(
            tk.END, "Por favor, indique o NÓ Terra para poder alterar o circuito")
        texto_saida.config(state="disabled")

        return

    def atualizar_texto():
        nome_arquivo = 'saida.txt'
        terra = campo_terra.get()
        configuracoes = funcoes.ler_dados_arquivo(nome_arquivo, terra)

        texto_entrada2.config(state="normal")
        texto_entrada2.delete("1.0", tk.END)
        texto_entrada2.insert(tk.END, "\t\t ")
        for i in range(7):
            cor = "red"  #Definir a cor para as linhas de 0 a 7
            #Aplicar a tag de estilo
            texto_entrada2.insert(tk.END, f"{i}\t\t", f"linha-{i}")
            #Configurar a cor da tag
            texto_entrada2.tag_config(f"linha-{i}", foreground=cor)
        texto_entrada2.insert(tk.END, "\n")
        for linha_idx, linha in enumerate(configuracoes):
            linha_formatada = '\t\t'.join(str(valor) for valor in linha)
            if linha_idx % 2 == 1:  #Verificar se o índice da linha é ímpar
                cor = "#8b0000"  #Definir a cor vermelha
            else:
                cor = "black"  #Definir a cor padrão (preta)
            #Aplicar a tag de estilo
            texto_entrada2.insert(
                tk.END, f"{linha_idx} -\t\t {linha_formatada}\n", f"linha-{linha_idx}")
            #Configurar a cor da tag
            texto_entrada2.tag_config(f"linha-{linha_idx}", foreground=cor)

        texto_entrada2.config(state="disabled")

    def alterar_valor():
        linha = int(entrada_linha.get())
        coluna = int(entrada_coluna.get())
        valor = None if entrada_novo_valor.get() == '' else entrada_novo_valor.get()

        with open('saida.txt', 'r', newline='') as arquivo:
            linhas = list(csv.reader(arquivo, delimiter='\t'))

        #Atualizar o valor na linha e coluna especificadas
        linhas[linha][coluna] = str(valor)

        #Salvar as alterações de volta no arquivo
        with open('saida.txt', 'w', newline='') as arquivo:
            writer = csv.writer(arquivo, delimiter='\t')
            writer.writerows(linhas)

        atualizar_texto()

    janela2 = tk.Tk()
    janela2.title("ALTERAR CIRCUITO")

    texto_entrada2 = scrolledtext.ScrolledText(janela2, width=120, height=30)
    texto_entrada2.grid(row=5, padx=1, pady=10)  #Definindo sticky="w"
    texto_entrada2.config(state="disabled")

    texto_entrada2.config(state="normal")
    texto_entrada2.delete("1.0", tk.END)

    #Criar widgets
    label_linha = tk.Label(janela2, text="Linha:")
    label_linha.grid(row=1, column=0)

    entrada_linha = tk.Entry(janela2)
    entrada_linha.grid(row=1, column=1, padx=10)

    label_coluna = tk.Label(janela2, text="Coluna:")
    label_coluna.grid(row=2, column=0)

    entrada_coluna = tk.Entry(janela2)
    entrada_coluna.grid(row=2, column=1)

    label_novo_valor = tk.Label(janela2, text="Novo Valor:")
    label_novo_valor.grid(row=3, column=0)

    entrada_novo_valor = tk.Entry(janela2)
    entrada_novo_valor.grid(row=3, column=1)

    botao_alterar = tk.Button(
        janela2, text="Alterar Valor", command=alterar_valor)

    botao_alterar.grid(row=4, columnspan=2, pady=10)

    atualizar_texto()
    janela2.mainloop()


def exibir_correntes(correntes_texto):
    #Criar uma nova janela para exibir as correntes
    janela_correntes = tk.Toplevel()
    janela_correntes.title("Corrente nos RAMOS")

    #Criar um widget de texto com rolagem para exibir as correntes
    texto_correntes = scrolledtext.ScrolledText(
        janela_correntes, width=80, height=30)
    texto_correntes.insert(tk.END, correntes_texto)
    texto_correntes.pack()

    #Configurar o widget de texto como somente leitura
    texto_correntes.config(state=tk.DISABLED)


def ordenar_linhas():
    with open("saida.txt", "r") as arquivo:
        linhas = arquivo.readlines()

    linhas_ordenadas = sorted(linhas, key=lambda linha: linha.split('\t')[0])

    with open("saida.txt", "w") as arquivo:
        arquivo.writelines(linhas_ordenadas)


def adicionar_linha():
    listaAr1 = []
    entrada_linhas.append([])
    for i in range(7):
        valor = campos_entrada[i].get() or "None"
        listaAr1.append(valor)
        entrada_linhas[-1].append(valor)

    #Adiciona o ramo no arquivo
    with open("saida.txt", "a") as arquivo:
        arquivo.write("\t".join(listaAr1) + "\n")

        #Verifica se é necessário adicionar a linha duplicada
        if listaAr1[0] != listaAr1[1]:
            listaAr2 = [listaAr1[1], listaAr1[0]] + listaAr1[2:]
            arquivo.write("\t".join(listaAr2) + "\n")

    ordenar_linhas()
    atualizar_texto()


def excluirdados():
    texto_entrada.config(state="normal")
    texto_entrada.delete("1.0", tk.END)
    with open("saida.txt", "w") as arquivo:
        arquivo.write("")


def gerar_dados():
    terra = campo_terra.get()
    valor_w = campo_w.get()

    tempo_frequencia = var_dominio.get() == 0

    #print(tempo_frequencia)

    if tempo_frequencia == True and len(valor_w) == 0:
        texto_saida.config(state="normal")
        texto_saida.delete("1.0", tk.END)
        texto_saida.insert(
            tk.END, "Está no Dominio do Tempo, indique um Omega, ou mude para o dominio da frequencia.")
        texto_saida.config(state="disabled")
    elif len(terra) == 1:

        texto_saida.config(state="normal")
        texto_saida.delete("1.0", tk.END)
        texto_saida.insert(tk.END, "Arquivo gerado com sucesso: saida.txt")
        texto_saida.config(state="disabled")

        configuracoes = funcoes.ler_dados_arquivo2("saida.txt", terra)
        nos = sorted(funcoes.obter_nos(configuracoes))
        ramos = funcoes.obter_ramos(configuracoes)

        valor_w = campo_w.get()
        if valor_w:
            w = float(valor_w)
        else:
            w = None
    else:
        texto_saida.config(state="normal")
        texto_saida.delete("1.0", tk.END)
        texto_saida.insert(tk.END, "Por favor, indique o NÓ Terra")
        texto_saida.config(state="disabled")

    try:
        equacoes, tensoes_nos, correntes, tensao_unica = funcoes.montar_sistema_equacoes(
            nos, configuracoes, w, tempo_frequencia)
        tensoes_nos_ = funcoes.calcular_sistema(
            equacoes, tensoes_nos, terra, tensao_unica)
        resultado_correntes = funcoes.calcular_correntes(
            correntes, tensoes_nos_)

        texto_tensoes = funcoes.Tensoes(tensoes_nos_, w)
        texto_correntes = funcoes.Correntes(
            resultado_correntes, ramos, w, configuracoes)

        #Exibir os resultados das tensões em uma nova janela
        exibir_tensoes(texto_tensoes)

        #Exibir os resultados das correntes em uma nova janela
        exibir_correntes(texto_correntes)

        #Atualizar as labels com os textos das tensões e correntes
        #label_tensoes.config(text=texto_tensoes)
        #label_correntes.config(text=texto_correntes)
    except Exception as e:
        #Tratamento de erro
        print("Ocorreu um erro:", str(e))
    atualizar_texto()


def atualizar_texto():
    texto_entrada.config(state="normal")
    texto_entrada.delete("1.0", tk.END)
    for linha in entrada_linhas:
        descricao = formatar_descricao(linha)
        texto_entrada.insert(tk.END, descricao + "\n")
    texto_entrada.config(state="disabled")


def formatar_descricao(linha):
    no_origem, no_saida, resistor, indutor, capacitor, fonte_tensao, fonte_corrente = linha

    descricao = f"Do nó {no_origem} para o Nó {no_saida} contém "

    if resistor != "None":
        descricao += f"um resistor de {resistor} ohms "
    if indutor != "None":
        descricao += f"um indutor de {indutor}H "
    if capacitor != "None":
        descricao += f"um capacitor de {capacitor}F "
    if fonte_tensao != "None":
        descricao += f"uma fonte de tensão de {fonte_tensao}V "
    if fonte_corrente != "None":
        descricao += f"uma fonte de corrente de {fonte_corrente}A"

    return descricao


janela = tk.Tk()
janela.title("Simulador de Circuitos")


#Campos de entrada
rotulos_campos = ["Nó de Origem", "Nó de Saída",
                  "Resistor (ohms)", "Indutor (H)", "Capacitor (F)", "Fonte de Tensão (V)", "Fonte de Corrente (A)"]
campos_entrada = []

for i in range(7):
    rotulo = tk.Label(janela, text=rotulos_campos[i])
    rotulo.grid(row=0, column=i, padx=10, pady=10)
    campo = tk.Entry(janela)
    campo.grid(row=1, column=i, padx=10)
    campos_entrada.append(campo)

#Botões
botao_adicionar = tk.Button(
    janela, text="Adicionar Linha", command=adicionar_linha)
botao_adicionar.grid(row=2, column=0, pady=10)

botao_gerar = tk.Button(janela, text="Calcular", command=gerar_dados)
botao_gerar.grid(row=2, column=1, pady=10)

botao_excluir = tk.Button(
    janela, text="Excluir circuito", command=excluirdados)
botao_excluir.grid(row=3, column=6, pady=10)

#Caixa de texto para o valor do terra
rotulo_terra = tk.Label(janela, text="Valor do terra:")
rotulo_terra.grid(row=2, column=2, pady=10)
campo_terra = tk.Entry(janela)
campo_terra.grid(row=2, column=3)

#Caixas de seleção para alternar entre os domínios do tempo e da frequência
#rotulo_dominio = tk.Label(janela, text="Domínio:")
#rotulo_dominio.grid(row=2, column=4, pady=10)
var_dominio = tk.IntVar()
check_tempo = tk.Checkbutton(janela, text="Domínio do Tempo",
                             variable=var_dominio, onvalue=0, offvalue=1, command=alternar_dominio)
check_tempo.grid(row=2, column=4, pady=5, sticky="w")
check_frequencia = tk.Checkbutton(janela, text="Domínio da Frequência",
                                  variable=var_dominio, onvalue=1, offvalue=0, command=alternar_dominio)
check_frequencia.grid(row=2, column=5, pady=5, sticky="w")

#Caixa de texto para o valor de w
rotulo_w = tk.Label(janela, text="Valor de w:")
rotulo_w.grid(row=2, column=6, pady=10)
campo_w = tk.Entry(janela)
campo_w.grid(row=2, column=7, columnspan=7)

#Texto de entrada
texto_entrada = scrolledtext.ScrolledText(janela, width=50, height=20)
texto_entrada.grid(row=3, columnspan=3, padx=1, pady=10,
                   sticky="w")  #Definindo sticky="w"
texto_entrada.config(state="disabled")

#Texto de saída
texto_saida = scrolledtext.ScrolledText(janela, width=50, height=2)
texto_saida.grid(row=4, columnspan=3, padx=1, pady=10, sticky="w")
texto_saida.config(state="disabled")

#Label para exibir as tensões
#rotulo_tensoes = tk.Label(janela, text="Valores das tensões em cada NÓ")
#rotulo_tensoes.grid(row=4, column=4, pady=10)
#label_tensoes = tk.Label(janela, text="", width=60, height=20, anchor="nw", justify="left", relief=tk.SUNKEN)
#label_tensoes.grid(row=3, pady=10, column=3, columnspan=4, sticky="w")

#Label para exibir as correntes
#rotulo_correntes = tk.Label(janela, text="Valores das correntes em cada ramo")
#rotulo_correntes.grid(row=4, column=7, pady=10)
#label_correntes = tk.Label(janela, text="", width=60, height=20, anchor="nw", justify="left", relief=tk.SUNKEN)
#label_correntes.grid(row=3, column=6, pady=10, columnspan=4, sticky="w")


botao_pdf = tk.Button(
    janela, text="Duvidas? Clique aqui para entender como colocar os dados", command=abrir_pdf)
botao_pdf.grid(row=7, column=3, columnspan=3)

botao_alterar = tk.Button(
    janela, text="Alterar linhas", command=alterar_circuito)
botao_alterar.grid(row=8, column=1)

#Lista para armazenar os dados de entrada
entrada_linhas = []

#Iniciar a janela principal
janela.mainloop()
