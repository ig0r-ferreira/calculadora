import PySimpleGUI as sg
from interface import gerar_interface


janela = gerar_interface()

LIMPAR_DISPLAY = 'Delete:46'
BACKSPACE_DISPLAY = 'BackSpace:8'
CALCULAR_EXPRESSAO = '='
INICIOU_COM_ZERO = False

while True:
    evento, valores = janela.read()

    if evento == sg.WINDOW_CLOSED:
        break

    if evento == '\r':
        evento = CALCULAR_EXPRESSAO

    if type(janela.find_element(evento, silent_on_error=True)) is sg.Button:

        display = janela['display']

        if evento not in [LIMPAR_DISPLAY, BACKSPACE_DISPLAY, CALCULAR_EXPRESSAO]:

            conteudo_display = display.get()

            if conteudo_display == '0':
                if evento == '0':
                    INICIOU_COM_ZERO = True
                    continue
                elif not INICIOU_COM_ZERO:
                    conteudo_display = ''
                else:
                    INICIOU_COM_ZERO = False

            display(conteudo_display + janela[evento].ButtonText)

        elif evento == LIMPAR_DISPLAY:
            display('0')

        elif evento == BACKSPACE_DISPLAY:
            display(display.get()[:-1])

        elif evento == CALCULAR_EXPRESSAO:
            from opcalc import calcular_exp

            exp_num = display.get().replace(',', '.').replace('x', '*')

            try:
                resultado = calcular_exp(exp_num)
            except Exception as erro:
                sg.PopupError(erro)
            else:
                display(str(resultado).replace('.', ','))

janela.close()
