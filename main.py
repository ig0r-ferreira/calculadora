import PySimpleGUI as sg


sg.theme('DefaultNoMoreNagging')
font_family = 'Tahoma'

layout_botoes = [
    [
        sg.Button('('),
        sg.Button(')'),
        sg.Button('C'),
        sg.Button('<-')
    ],
    [
        sg.Button('1'),
        sg.Button('2'),
        sg.Button('3'),
        sg.Button('+')
    ],
    [
        sg.Button('4'),
        sg.Button('5'),
        sg.Button('6'),
        sg.Button('-')
    ],
    [
        sg.Button('7'),
        sg.Button('8'),
        sg.Button('9'),
        sg.Button('x'),
    ],
    [
        sg.Button('', disabled=True),
        sg.Button('0'),
        sg.Button(','),
        sg.Button('/'),
    ],
    [
        sg.Button('=', size=(25, 2))
    ]
]

layout_janela = [
    [
        sg.Frame('', [
            [
                sg.Text(text='',
                        key='visor',
                        justification='right',
                        text_color='black',
                        font=(font_family, 14, 'bold'),
                        background_color='white',
                        size=(22, 1),
                        pad=(10, 25))
            ]
        ], pad=(10, 10), element_justification='center', background_color='white')
    ],
    [
        sg.Frame('', layout_botoes, pad=(10, 20), element_justification='center', border_width=0)
    ]
]

janela = sg.Window('Calculadora', layout_janela)

for botao in list(filter(lambda e: type(e) == sg.Button, janela.element_list())):
    font_size = 12
    font_weight = 'bold'
    botao.Font = (font_family, font_size, font_weight)

    if botao.Size == (None, None):
        botao.Size = (5, 2)

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
