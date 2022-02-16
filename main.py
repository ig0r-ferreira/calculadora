import PySimpleGUI as sg
from interface import gerar_interface


def carregar_restricoes():
    seq = display.conteudo()

    if len(seq) == 0:
        return

    if seq == ESTADO_INICIAL:

        janela['('].update(disabled=False)
        janela[','].update(disabled=not INICIO_ZERO)

        for _botao in ['+', '*', '/', ')']:
            janela[_botao].update(disabled=True)

    elif seq == '-':

        janela['('].update(disabled=False)
        janela['-'].update(disabled=True)

        for _botao in ['+', '*', '/', ',', ')']:
            janela[_botao].update(disabled=True)

    else:
        ultima_tecla = seq[-1]

        match ultima_tecla:

            case ('0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'):
                janela['('].update(disabled=True)

                for _botao in ['+', '-', '*', '/', ',', ')']:
                    janela[_botao].update(disabled=False)

            case ('+' | '-' | 'x' | '/'):
                janela['('].update(disabled=False)
                janela[')'].update(disabled=True)

            case ',':
                for _botao in ['+', '-', '*', '/', ',', '(', ')']:
                    janela[_botao].update(disabled=True)

            case '(':
                janela['-'].update(disabled=False)

                for _botao in ['+', '*', '/', ',']:
                    janela[_botao].update(disabled=True)

            case ')':
                janela['('].update(disabled=True)
                janela[','].update(disabled=True)


def obter_botao_compativel(_evento):
    if _evento == '\r':
        return Funcoes.CALCULAR

    if type(janela.find_element(_evento, silent_on_error=True)) is sg.Button:
        return _evento
    return None


def mostrar_erro(msg):
    sg.PopupError(msg, modal=True)
    janela.read(timeout=1000)


class Funcoes:
    LIMPAR = 'Delete:46'
    BACKSPACE = 'BackSpace:8'
    CALCULAR = '='


class Display:
    display = None

    def __init__(self, _display):
        self.display = _display

    def conteudo(self):
        return self.display.get()

    def mostrar(self, info):
        self.display(info)

    def reset(self):
        self.display('0')

    def backspace(self):
        self.display(self.display.get()[:-1])
        return self.display.get()

    def calcular(self):
        from opcalc import calcular_exp

        exp = self.display.get().replace(',', '.').replace('x', '*')

        try:
            result_exp = calcular_exp(exp)
        except Exception as erro:
            raise erro
        else:
            self.mostrar(str(result_exp).replace('.', ','))


janela = gerar_interface()
display = Display(janela['display'])

ESTADO_INICIAL = '0'
SAIR = sg.WINDOW_CLOSED
INICIO_ZERO = False

while True:

    carregar_restricoes()

    evento, valores = janela.read()

    if evento == SAIR:
        break

    botao = obter_botao_compativel(evento)

    if botao is None:
        continue

    match botao:
        case Funcoes.BACKSPACE:

            if display.backspace() == '':
                display.reset()

        case Funcoes.LIMPAR:
            display.reset()

        case Funcoes.CALCULAR:
            try:
                display.calcular()
            except Exception as erro_calcular:
                mostrar_erro(erro_calcular)

        case _:

            if janela[botao].Disabled:
                continue

            sequencia = display.conteudo()

            if sequencia == ESTADO_INICIAL:

                if botao == '0':
                    INICIO_ZERO = True
                    continue

                elif not INICIO_ZERO:
                    sequencia = ''

                else:
                    INICIO_ZERO = False

            elif botao in ['+', '-', '*', '/', ','] and sequencia[-1] in ['+', '-', 'x', '/', ',']:
                sequencia = display.backspace()

            display.mostrar(sequencia + janela[botao].ButtonText)

janela.close()
