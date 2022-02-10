import PySimpleGUI as sg
from interface import gerar_interface


janela = gerar_interface()

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
