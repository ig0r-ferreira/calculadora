import PySimpleGUI as sg

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


def criar_display():
    config_display = {
        'text': '0',
        'key': 'display',
        'justification': 'right',
        'size': (20, 1),
        'expand_x': True,
        'font': f'{FAMILIA_PADRAO_FONTE} 20',
        'border_width': 1,
        'relief': sg.RELIEF_GROOVE,
        'background_color': COR_BRANCA,
        'text_color': COR_PRETA
    }

    display = sg.Text(**config_display)
    return display


def config_botao_numerico(**kwargs):
    config_botao = {
        'size': (LARGURA_PADRAO_BOTAO, 2),
        'button_color': (COR_PRETA, COR_TEMA),
        'pad': PAD_PADRAO_BOTAO
    }

    if kwargs:
        config_botao.update(kwargs)

    return config_botao


def config_botao_aux(**kwargs):
    config_botao = {
        'size': (LARGURA_PADRAO_BOTAO, 2),
        'button_color': (COR_BRANCA, COR_AZUL_ESCURO),
        'pad': PAD_PADRAO_BOTAO
    }

    if kwargs:
        config_botao.update(kwargs)

    return config_botao


def config_botao_operacao(**kwargs):
    config_botao = {
        'size': (LARGURA_PADRAO_BOTAO * 2, 2),
        'button_color': (COR_BRANCA, COR_AZUL_ESCURO),
        'pad': PAD_PADRAO_BOTAO
    }

    if kwargs:
        config_botao.update(kwargs)

    return config_botao


def montar_painel_superior():
    elementos_painel = [
        [
            criar_display()
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
    elementos_painel = [
        [
            sg.Button('(', **config_botao_aux()),
            sg.Button(')', **config_botao_aux()),
            sg.Button('<-', key='BackSpace:8', **config_botao_aux()),
            sg.Button('C', key='Delete:46', **config_botao_aux(
                size=(LARGURA_PADRAO_BOTAO * 2, 2),
                button_color=(COR_BRANCA, COR_VERMELHA)))
        ],
        [
            sg.Button('7', **config_botao_numerico()),
            sg.Button('8', **config_botao_numerico()),
            sg.Button('9', **config_botao_numerico()),
            sg.Button('+', **config_botao_operacao())
        ],
        [
            sg.Button('4', **config_botao_numerico()),
            sg.Button('5', **config_botao_numerico()),
            sg.Button('6', **config_botao_numerico()),
            sg.Button('-', **config_botao_operacao())
        ],
        [
            sg.Button('1', **config_botao_numerico()),
            sg.Button('2', **config_botao_numerico()),
            sg.Button('3', **config_botao_numerico()),
            sg.Button('x', key='*', **config_botao_operacao())
        ],
        [
            sg.Button('0', **config_botao_numerico(size=(LARGURA_PADRAO_BOTAO * 2 + 2, 2))),
            sg.Button(',', **config_botao_numerico()),
            sg.Button('/', **config_botao_operacao())
        ],
        [
            sg.Button(button_text='=', size=(0, 2), expand_x=True, button_color=(COR_BRANCA, COR_VERDE),
                      pad=PAD_PADRAO_BOTAO)
        ]
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
        'use_default_focus': False,
        'return_keyboard_events': True,
        'finalize': True,
        'background_color': COR_TEMA,
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


if __name__ == "__main__":
    janela = gerar_interface()

    while True:
        evento, valores = janela.read()

        print(f'{evento}: {valores}')

        if evento == sg.WINDOW_CLOSED:
            break

    janela.close()
