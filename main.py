import tkinter.font
from tkinter import *
from functools import partial


def digitar(e):
    tela_exibicao['text'] = tela_exibicao['text'] + str(e)


def apagar():
    tela_exibicao['text'] = tela_exibicao['text'][:-1]


def limpar_visor():
    tela_exibicao['text'] = ''


def calcular():
    from expnum import calc_exp

    expressao_numerica = tela_exibicao['text'].replace(',', '.')
    resultado = calc_exp(expressao_numerica)
    if resultado is not None:
        tela_exibicao['text'] = str(resultado).replace('.', ',')


def criar_botao(local, config):

    botao = Button(local,
                   width=config.get('width'),
                   height=config.get('height'),
                   text=config.get('text'),
                   command=config.get('command')
                   )

    botao.grid(row=config.get('row'), column=config.get('column'), padx=6, pady=8)

    if config.get('font'):
        font_family = config.get('font').get('family')
        font_size = config.get('font').get('size')
        font_weight = config.get('font').get('weight')

        botao.config(font=tkinter.font.Font(
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
            {'identificador': '1', 'acao': partial(digitar, '1'), 'font': {'weight': 'bold'}},
            {'identificador': '2', 'acao': partial(digitar, '2'), 'font': {'weight': 'bold'}},
            {'identificador': '3', 'acao': partial(digitar, '3'), 'font': {'weight': 'bold'}},
            {'identificador': '+', 'acao': partial(digitar, '+'), 'font': {}},
        ],
        [
            {'identificador': '4', 'acao': partial(digitar, '4'), 'font': {'weight': 'bold'}},
            {'identificador': '5', 'acao': partial(digitar, '5'), 'font': {'weight': 'bold'}},
            {'identificador': '6', 'acao': partial(digitar, '6'), 'font': {'weight': 'bold'}},
            {'identificador': '-', 'acao': partial(digitar, '-'), 'font': {}},
        ],
        [
            {'identificador': '7', 'acao': partial(digitar, '7'), 'font': {'weight': 'bold'}},
            {'identificador': '8', 'acao': partial(digitar, '8'), 'font': {'weight': 'bold'}},
            {'identificador': '9', 'acao': partial(digitar, '9'), 'font': {'weight': 'bold'}},
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


janela = Tk()
janela.title('Calculadora')
janela.resizable(height=False, width=False)
janela.minsize(400, 610)

tela_exibicao = Label(master=janela, width=23, height=3, font=18, bg='white', fg='black')
tela_exibicao.pack(pady=40)
tela_exibicao.config(font=tkinter.font.Font(
    family='Lucida Console',
    size=16,
    weight='bold'
))

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
