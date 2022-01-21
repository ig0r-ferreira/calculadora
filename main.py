import tkinter.font

from expnum import calc_exp
from tkinter import *
from functools import partial


def digitar(e):
    visor['text'] = visor['text'] + str(e)


def apagar():
    visor['text'] = visor['text'][:-1]


def limpar_visor():
    visor['text'] = ''


def calcular_resultado():
    expressao_numerica = visor['text'].replace(',', '.')
    visor['text'] = str(calc_exp(expressao_numerica)).replace('.', ',')


def criar_botao(local, texto, linha, coluna, acao):
    botao = Button(local, width=5, height=2, text=texto, command=acao)

    botao.grid(row=linha, column=coluna, padx=6, pady=8)

    config_font = tkinter.font.Font(family='Lucida Console', size=15)
    botao.config(font=config_font)

    return botao


def gerar_visor(local):
    visor = Label(master=local, width=23, height=3, font=18, bg='white', fg='black')
    visor.pack(pady=40)

    config_font = tkinter.font.Font(family='Lucida Console', size=16, weight='bold')
    visor.config(font=config_font)

    return visor


def gerar_painel_botoes(local):
    botoes_frame = Frame(master=local, width=100, height=100)
    botoes_frame.pack(padx=25)

    return botoes_frame


def gerar_botoes_numericos(local):
    num = 1
    config_font = tkinter.font.Font(family='Lucida Console', size=15, weight='bold')
    for i in range(1, 4):
        for j in range(0, 3):
            botao = criar_botao(local, texto=f'{num}', linha=i, coluna=j, acao=partial(digitar, num))
            botao.config(font=config_font)
            num = num + 1

    botao_zero = criar_botao(local, texto='0', linha=4, coluna=1, acao=partial(digitar, '0'))
    botao_zero.config(font=config_font)


def gerar_botoes_operacoes(local):
    operacoes_mat = ['+', '-', '*', '/']

    for i, operador in enumerate(operacoes_mat):
        criar_botao(local, texto=operador, linha=i + 1, coluna=3, acao=partial(digitar, f' {operador} '))

    criar_botao(local, texto='C', linha=0, coluna=2, acao=limpar_visor)
    criar_botao(local, texto='<=', linha=0, coluna=3, acao=apagar)
    criar_botao(local, texto='=', linha=5, coluna=3, acao=calcular_resultado)


def gerar_botoes_adicionais(local):
    criar_botao(local, texto='(', linha=0, coluna=0, acao=partial(digitar, '('))
    criar_botao(local, texto=')', linha=0, coluna=1, acao=partial(digitar, ')'))
    criar_botao(local, texto=',', linha=4, coluna=2, acao=partial(digitar, ','))


janela = Tk()
janela.title('Calculadora')
janela.resizable(height=False, width=False)
janela.minsize(400, 610)

visor = gerar_visor(janela)

painel_botoes = gerar_painel_botoes(janela)
gerar_botoes_numericos(painel_botoes)
gerar_botoes_operacoes(painel_botoes)
gerar_botoes_adicionais(painel_botoes)

janela.mainloop()
