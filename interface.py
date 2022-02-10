import PySimpleGUI as sg
from functools import partial


FAMILIA_PADRAO_FONTE = 'Tahoma'
TAMANHO_PADRAO_FONTE = 14
LARGURA_PADRAO_BOTAO = 6
PAD_PADRAO_BOTAO = (7, 7)

COR_TEMA = '#faf9f8'
COR_VERDE = '#009000'
COR_VERMELHA = '#cc0000'
COR_AZUL_ESCURO = '#0e2f44'
COR_PRETA = 'black'
COR_BRANCA = 'white'


def criar_botao(conteudo='', config=None):
    if config is None:
        config = {}
    if conteudo != '':
        config['button_text'] = str(conteudo)
    return sg.Button(**config)


def montar_painel_superior():

    config_visor = {
        'text': '',
        'key': 'visor',
        'size': (16, 2),
        'expand_x': True,
        'justification': 'right',
        'font': f'{FAMILIA_PADRAO_FONTE} 20',
        'relief': sg.RELIEF_GROOVE,
        'border_width': 1,
        'background_color': COR_BRANCA,
        'text_color': COR_PRETA,
        'pad': ((5, 20), (7, 7))
    }

    visor = sg.Text(**config_visor)

    config_botao_calcular = {
        'button_text': '=',
        'size': (LARGURA_PADRAO_BOTAO * 2 + 2, 2),
        'button_color': (COR_BRANCA, COR_VERDE),
        'pad': PAD_PADRAO_BOTAO
    }

    botao_calcular = criar_botao('=', config_botao_calcular)

    elementos_painel = [
        [
            visor,
            botao_calcular
        ]
    ]

    config_painel = {
        'title': '',
        'layout': elementos_painel,
        'expand_x': True,
        'pad': ((7, 7), (25, 25)),
        'element_justification': 'center',
        'background_color': COR_TEMA,
        'border_width': 0
    }

    return sg.Frame(**config_painel)


def montar_painel_botoes():

    config_botao_aux = {
        'size': (LARGURA_PADRAO_BOTAO, 2),
        'button_color': (COR_BRANCA, COR_AZUL_ESCURO),
        'pad': PAD_PADRAO_BOTAO
    }
    config_botao_num = {
        'size': (LARGURA_PADRAO_BOTAO, 2),
        'button_color': (COR_PRETA, COR_TEMA),
        'pad': PAD_PADRAO_BOTAO
    }

    # Botões da primeira fileira
    botoes_aux1 = list(map(partial(criar_botao, config=config_botao_aux), ['(', ')', '<-']))
    botoes_aux1.append(criar_botao('C', {
        'size': (LARGURA_PADRAO_BOTAO * 2 + 2, 2),
        'button_color': (COR_BRANCA, COR_VERMELHA),
        'pad': PAD_PADRAO_BOTAO
    }))

    # Botões da segunda fileira
    botoes_aux2 = list(map(partial(criar_botao, config=config_botao_aux), ['+', '-', '/', 'x', ',']))

    # Botões da terceira fileira - Botões numéricos de 0 a 4
    botoes_num1 = list(map(partial(criar_botao, config=config_botao_num), list(range(0, 5))))

    # Botões da quarta fileira - Botões numéricos de 5 a 9
    botoes_num2 = list(map(partial(criar_botao, config=config_botao_num), list(range(5, 10))))

    elementos_painel = [
        botoes_aux1,
        botoes_aux2,
        botoes_num1,
        botoes_num2
    ]

    config_painel = {
        'title': '',
        'layout': elementos_painel,
        'expand_x': True,
        'element_justification': 'center',
        'background_color': COR_TEMA,
        'border_width': 0
    }

    return sg.Frame(**config_painel)


def gerar_interface():
    
    config_janela = {
        'title': 'Calculadora',
        'layout': [],
        'background_color': COR_TEMA,
        'use_default_focus': False,
        'element_justification': 'center',
        'font': f'{FAMILIA_PADRAO_FONTE} {TAMANHO_PADRAO_FONTE} bold',
        'margins': (20, 30)
    }

    layout_janela = config_janela['layout']

    layout_janela.append([
        montar_painel_superior(),
    ])

    layout_janela.append([
        montar_painel_botoes()
    ])

    return sg.Window(**config_janela)
