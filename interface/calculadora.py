import PySimpleGUI as sg
import json


class Calculadora:

    def __init__(self):
        self.janela = None
        self.config = self.__carregar_config()

        self.INICIO_ZERO = False
        self.ESTADO_INICIAL = '0'

        self.__criar_area_display()
        self.__criar_area_botoes()

    @staticmethod
    def __carregar_config():
        with open('./config/config.json', 'r') as arquivo:
            config_interface = json.load(arquivo)

        return config_interface

    @staticmethod
    def __mostrar_msg_erro(erro):
        sg.PopupError(erro, modal=True)

    def __criar_area_display(self):

        self.display = sg.Text(**self.config['DISPLAY'])

        self.config['AREA_DISPLAY']['layout'].append(
            [self.display]
        )

        area_display = sg.Frame(**self.config['AREA_DISPLAY'])

        layout = self.config['JANELA']['layout']
        layout.append(
            [area_display]
        )

    def __criar_area_botoes(self):

        botoes = [
            [
                sg.Button('(', key='(', **self.config['BOTOES_AUX'], **self.config['TODOS_BOTOES']),
                sg.Button(')', key=')', **self.config['BOTOES_AUX'], **self.config['TODOS_BOTOES']),
                sg.Button('<-', key='BackSpace:8', **self.config['BOTOES_AUX'], **self.config['TODOS_BOTOES']),
                sg.Button('C', key='Delete:46', **self.config['BOTAO_LIMPAR'], **self.config['TODOS_BOTOES']),
            ],
            [
                sg.Button('7', key='7', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('8', key='8', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('9', key='9', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('+', key='+', **self.config['BOTOES_OP'], **self.config['TODOS_BOTOES']),
            ],
            [
                sg.Button('4', key='4', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('5', key='5', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('6', key='6', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('-', key='-', **self.config['BOTOES_OP'], **self.config['TODOS_BOTOES']),
            ],
            [
                sg.Button('1', key='1', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('2', key='2', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('3', key='3', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('x', key='*', **self.config['BOTOES_OP'], **self.config['TODOS_BOTOES']),
            ],
            [
                sg.Button('0', key='0', **self.config['BOTAO_ZERO'], **self.config['TODOS_BOTOES']),
                sg.Button(',', key=',', **self.config['BOTOES_NUM'], **self.config['TODOS_BOTOES']),
                sg.Button('/', key='/', **self.config['BOTOES_OP'], **self.config['TODOS_BOTOES']),
            ],
            [
                sg.Button('=', key='=', **self.config['BOTAO_CALCULAR'], **self.config['TODOS_BOTOES']),
            ]
        ]

        self.config['AREA_BOTOES']['layout'].extend(botoes)

        area_botoes = sg.Frame(**self.config['AREA_BOTOES'])

        self.config['JANELA']['layout'].append(
            [area_botoes]
        )

    def __obter_botao_compativel(self, evento):
        if evento == '\r':
            return "="

        if type(self.janela.find_element(evento, silent_on_error=True)) is sg.Button:
            return evento
        return None

    def __carregar_restricoes(self):
        seq = self.display.get()

        if len(seq) == 0:
            return

        if seq == self.ESTADO_INICIAL:

            self.janela['('].update(disabled=False)
            self.janela[','].update(disabled=not self.INICIO_ZERO)

            for botao in ['+', '*', '/', ')']:
                self.janela[botao].update(disabled=True)

        elif seq == '-':

            self.janela['('].update(disabled=False)
            self.janela['-'].update(disabled=True)

            for botao in ['+', '*', '/', ',', ')']:
                self.janela[botao].update(disabled=True)

        else:
            ultima_tecla = seq[-1]

            match ultima_tecla:

                case ('0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'):
                    self.janela['('].update(disabled=True)

                    for botao in ['+', '-', '*', '/', ',', ')']:
                        self.janela[botao].update(disabled=False)

                case ('+' | '-' | 'x' | '/'):
                    self.janela['('].update(disabled=False)
                    self.janela[')'].update(disabled=True)

                case ',':
                    for botao in ['+', '-', '*', '/', ',', '(', ')']:
                        self.janela[botao].update(disabled=True)

                case '(':
                    self.janela['-'].update(disabled=False)

                    for botao in ['+', '*', '/', ',']:
                        self.janela[botao].update(disabled=True)

                case ')':
                    self.janela['('].update(disabled=True)
                    self.janela[','].update(disabled=True)

    def reset_display(self):
        self.display('0')

    def backspace_display(self):
        self.display(self.display.get()[:-1])

    def atualizar_display(self, info):
        self.display(info)

    def calcular(self):
        from calculo.calcexpress import calcular_exp

        exp = self.display.get().replace(',', '.').replace('x', '*')

        try:
            result_exp = calcular_exp(exp)
        except Exception as erro:
            raise erro
        else:
            self.atualizar_display(str(result_exp).replace('.', ','))

    def finalizar(self):
        self.janela.close()

    def iniciar(self):

        self.janela = sg.Window(**self.config['JANELA'])

        while True:

            self.__carregar_restricoes()

            evento, valores = self.janela.read()

            if evento == sg.WINDOW_CLOSED:
                break

            botao = self.__obter_botao_compativel(evento)

            if botao is None:
                continue

            match botao:
                case 'BackSpace:8':

                    self.backspace_display()

                    if self.display.get() == '':
                        self.reset_display()

                case 'Delete:46':
                    self.reset_display()

                case '=':
                    try:
                        self.calcular()
                    except Exception as erro_calcular:
                        self.__mostrar_msg_erro(erro_calcular)
                        self.janela.read(timeout=1000)

                case _:

                    if self.janela[botao].Disabled:
                        continue

                    sequencia = self.display.get()

                    if sequencia == self.ESTADO_INICIAL:

                        if botao == '0':
                            self.INICIO_ZERO = True
                            continue

                        elif not self.INICIO_ZERO:
                            sequencia = ''

                        else:
                            self.INICIO_ZERO = False

                    elif botao in ['+', '-', '*', '/', ','] and sequencia[-1] in ['+', '-', 'x', '/', ',']:
                        self.backspace_display()
                        sequencia = self.display.get()

                    self.atualizar_display(sequencia + self.janela[botao].ButtonText)

        self.finalizar()
