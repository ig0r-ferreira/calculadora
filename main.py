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
COR_LARANJA = '#ff6700'

COR_BOTAO_CALCULAR = (COR_BRANCA, COR_VERDE)
COR_BOTAO_LIMPAR = (COR_BRANCA, COR_VERMELHA)
COR_BOTOES_NUM = (COR_PRETA, COR_TEMA)


TAMANHO_BOTOES_NUM = (LARGURA_PADRAO_BOTAO, 2)
TAMANHO_BOTOES_ESPECIAIS = (LARGURA_PADRAO_BOTAO, 2)
TAMANHO_BOTAO_GRANDE = (LARGURA_PADRAO_BOTAO * 2 + 2, 2)


TAMANHO_FONTE_VISOR = 20
ESP_EXT_VISOR = ((5, 20), (7, 7))

CONFIG_VISOR = {
    'text': '',
    'key': 'visor',
    'size': (16, 2),
    'expand_x': True,
    'justification': 'right',
    'font': f'{FAMILIA_PADRAO_FONTE} {TAMANHO_FONTE_VISOR}',
    'relief': sg.RELIEF_GROOVE,
    'border_width': 1,
    'background_color': COR_BRANCA,
    'text_color': COR_PRETA,
    'pad': ESP_EXT_VISOR
}

CONFIG_BOTAO_CALCULAR = {
    'button_text': '=',
    'size': TAMANHO_BOTAO_GRANDE,
    'button_color': COR_BOTAO_CALCULAR,
    'pad': PAD_PADRAO_BOTAO
}

CONFIG_JANELA = {
    'title': 'Calculadora',
    'background_color': COR_TEMA,
    'use_default_focus': False,
    'element_justification': 'center',
    'font': f'{FAMILIA_PADRAO_FONTE} {TAMANHO_PADRAO_FONTE} bold',
    'margins': (20, 30)
}

layout_principal = [
    [
        sg.Frame('', [
            [
                sg.Text(**CONFIG_VISOR),
                sg.Button(**CONFIG_BOTAO_CALCULAR)
            ]
        ],
                 expand_x=True,
                 pad=((7, 7), (25, 25)),
                 element_justification='center',
                 background_color=COR_TEMA,
                 border_width=0)
    ],
    [
        sg.Frame('', [
            [
                sg.Button(**{
                    'button_text': botao,
                    'size': TAMANHO_BOTOES_ESPECIAIS if botao != 'C' else TAMANHO_BOTAO_GRANDE,
                    'button_color': (COR_BRANCA, COR_AZUL_ESCURO) if botao != 'C' else COR_BOTAO_LIMPAR,
                    'pad': PAD_PADRAO_BOTAO
                }) for botao in ['(', ')', '<-', 'C']

            ],
            [
                sg.Button(**{
                    'button_text': str(i),
                    'size': TAMANHO_BOTOES_ESPECIAIS,
                    'button_color': COR_AZUL_ESCURO,
                    'pad': PAD_PADRAO_BOTAO
                }) for i in ['+', '-', '/', 'x', ',']
            ],
            [
                sg.Button(**{
                    'button_text': str(i),
                    'size': TAMANHO_BOTOES_NUM,
                    'button_color': COR_BOTOES_NUM,
                    'pad': PAD_PADRAO_BOTAO
                }) for i in range(0, 5)
            ],
            [
                sg.Button(**{
                    'button_text': str(i),
                    'size': TAMANHO_BOTOES_NUM,
                    'button_color': COR_BOTOES_NUM,
                    'pad': PAD_PADRAO_BOTAO
                }) for i in range(5, 10)
            ]
        ], expand_x=True, element_justification='center', background_color=COR_TEMA, border_width=0)
    ],
]

CONFIG_JANELA['layout'] = layout_principal


janela = sg.Window(**CONFIG_JANELA)

while True:
    evento, valores = janela.read()

    if evento == sg.WINDOW_CLOSED:
        break

    if evento not in ['C', '<-', '=']:
        janela['visor'](janela['visor'].get() + evento)
    elif evento == 'C':
        janela['visor']('')
    elif evento == '<-':
        janela['visor'](janela['visor'].get()[:-1])
    elif evento == '=':
        from opcalc import calcular_exp

        conteudo_visor = janela['visor']

        exp_num = conteudo_visor.get().replace(',', '.').replace('x', '*')
        try:
            resultado = calcular_exp(exp_num)
        except Exception as erro:
            sg.PopupError(erro)
        else:
            conteudo_visor(str(resultado).replace('.', ','))

janela.close()
