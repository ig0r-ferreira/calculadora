from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
from functools import partial


def digitar(c):
    visor['text'] = visor['text'] + str(c)


def apagar():
    visor['text'] = visor['text'][:-1]


def limpar_visor():
    visor['text'] = ''


def calcular():
    from opcalc import calcular_exp

    exp_num = visor['text'].replace(',', '.')
    try:
        resultado = calcular_exp(exp_num)
    except Exception as erro:
        exibir_erro(erro)
        # limpar_visor()
    else:
        visor['text'] = str(resultado).replace('.', ',')


def exibir_erro(msg):
    messagebox.showerror('Erro', msg, parent=janela)


def criar_botao(local, config):

    botao = Button(local, width=config.get('width'), height=config.get('height'),
                   text=config.get('text'), command=config.get('command'))

    botao.grid(row=config.get('row'), column=config.get('column'), padx=6, pady=8)

    if config.get('font'):
        font_family = config.get('font').get('family')
        font_size = config.get('font').get('size')
        font_weight = config.get('font').get('weight')

        botao.config(font=tkfont.Font(
            family='Lucida Console' if not font_family else font_family,
            size=15 if not font_size else font_size,
            weight='normal' if not font_weight else font_weight
        ))

    return botao


def obter_config_botoes():
    return [
        [
            {'identificador': '(', 'acao': partial(digitar, '('), 'font': {}},
            {'identificador': ')', 'acao': partial(digitar, ')'), 'font': {}},
            {'identificador': 'C', 'acao': limpar_visor, 'font': {}},
            {'identificador': '<=', 'acao': apagar, 'font': {}},
        ],
        [
            {'identificador': '1', 'acao': partial(digitar, '1'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '2', 'acao': partial(digitar, '2'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '3', 'acao': partial(digitar, '3'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '+', 'acao': partial(digitar, '+'), 'font': {}},
        ],
        [
            {'identificador': '4', 'acao': partial(digitar, '4'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '5', 'acao': partial(digitar, '5'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '6', 'acao': partial(digitar, '6'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '-', 'acao': partial(digitar, '-'), 'font': {}},
        ],
        [
            {'identificador': '7', 'acao': partial(digitar, '7'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '8', 'acao': partial(digitar, '8'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '9', 'acao': partial(digitar, '9'), 'font': {'weight': tkfont.BOLD}},
            {'identificador': '*', 'acao': partial(digitar, '*'), 'font': {}},
        ],
        [
            None,
            {'identificador': '0', 'acao': partial(digitar, '0'), 'font': {}},
            {'identificador': ',', 'acao': partial(digitar, ','), 'font': {}},
            {'identificador': '/', 'acao': partial(digitar, '/'), 'font': {}},
        ],
        [
            None,
            None,
            None,
            {'identificador': '=', 'acao': calcular, 'font': {}},
        ]
    ]


# Janela principal
janela = Tk()
# Título da janela
janela.title('Calculadora')
# Não permite expandir a tela, mantendo-a em tamanho fixo
janela.resizable(height=False, width=False)
# Tamanho da janela
janela.minsize(400, 610)

# Visor da calculadora
visor = Label(master=janela, width=23, height=3, bg='white', fg='black')
visor.pack(pady=40)
visor.config(font=tkfont.Font(
    family='Lucida Console',
    size=16,
    weight=tkfont.BOLD
))

# Painel de botões da calculadora
painel_botoes = Frame(master=janela, width=100, height=100)
painel_botoes.pack(padx=25)

config_botoes = obter_config_botoes()

for i, fileira in enumerate(config_botoes):
    for j, botao in enumerate(fileira):

        if botao is None:
            continue

        criar_botao(painel_botoes, {
            'width': 5,
            'height': 2,
            'text': botao.get('identificador'),
            'command': botao.get('acao'),
            'row': i,
            'column': j,
            'font': {
                'family': botao.get('font').get('family'),
                'size': botao.get('font').get('size'),
                'weight': botao.get('font').get('weight')
            }
        })

janela.mainloop()
