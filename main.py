import PySimpleGUI as sg
from interface import gerar_interface


def obter_botao_compativel(_janela, _evento):
    if _evento == '\r':
        return Funcoes.CALCULAR

    if type(_janela.find_element(_evento, silent_on_error=True)) is sg.Button:
        return _evento
    return None


def mostrar_erro(_janela, msg):
    sg.PopupError(msg, modal=True)
    _janela.read(timeout=1000)


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

IDs_BOTOES_NAO_INICIAIS = ['+', '/', '*', ',', ')']
IDs_BOTOES_NAO_CONSECUTIVOS = ['+', '-', '/', '*', ',']
BOTOES_NAO_CONSECUTIVOS = [janela[botao].ButtonText for botao in IDs_BOTOES_NAO_CONSECUTIVOS]

JANELA_FECHADA = sg.WINDOW_CLOSED
INICIOU_COM_ZERO = False

while True:
    evento, valores = janela.read()

    if evento == JANELA_FECHADA:
        break

    id_botao = obter_botao_compativel(janela, evento)

    if id_botao is None:
        continue

    match id_botao:
        case Funcoes.BACKSPACE:
            if display.backspace() == '':
                display.reset()

        case Funcoes.LIMPAR:
            display.reset()

        case Funcoes.CALCULAR:
            try:
                display.calcular()
            except Exception as erro_calcular:
                mostrar_erro(janela, erro_calcular)

        case _:

            sequencia = display.conteudo()

            if sequencia == '0':

                if id_botao == '0':
                    INICIOU_COM_ZERO = True
                    continue
                elif not INICIOU_COM_ZERO:
                    if id_botao in IDs_BOTOES_NAO_INICIAIS:
                        continue

                    sequencia = ''
                else:
                    INICIOU_COM_ZERO = False
            else:
                if id_botao in IDs_BOTOES_NAO_CONSECUTIVOS:

                    if sequencia == '-':
                        continue

                    if sequencia[-1] in BOTOES_NAO_CONSECUTIVOS:
                        sequencia = display.backspace()
                    else:
                        janela[id_botao].Disabled = True
                else:
                    for id_botao_nc in IDs_BOTOES_NAO_CONSECUTIVOS:
                        janela[id_botao_nc].Disabled = False

            display.mostrar(sequencia + janela[id_botao].ButtonText)

janela.close()
