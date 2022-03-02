from time import sleep
import PySimpleGUI as sg
import json


class Calculadora:

    def __init__(self):
        self._janela = None
        self._display = None
        self._config = self._carregar_config()

        self._INICIO_ZERO = False
        self._ESTADO_INICIAL = '0'

        self._criar_area_display()
        self._criar_area_botoes()

    @staticmethod
    def _carregar_config():
        with open('./config/config.json', 'r') as arquivo:
            config_interface = json.load(arquivo)

        return config_interface

    @staticmethod
    def _mostrar_msg_erro(erro):
        sg.PopupError(erro, modal=True)

    def _criar_area_display(self):

        self._display = sg.Text(**self._config['DISPLAY'])

        self._config['AREA_DISPLAY']['layout'].append(
            [self._display]
        )

        area_display = sg.Frame(**self._config['AREA_DISPLAY'])

        layout = self._config['JANELA']['layout']
        layout.append(
            [area_display]
        )

    def _criar_area_botoes(self):

        self._BACKSPACE = '\u232b'
        self._LIMPAR = 'C'
        self._CALCULAR = '='

        self._SOMA = '\u002B'
        self._SUBTRACAO = '\u2212'
        self._MULTIPLICACAO = '\u00D7'
        self._DIVISAO = '\u00F7'
        self._PARENTESE_ESQUERDO = '('
        self._PARENTESE_DIREITO = ')'
        self._VIRGULA = ','

        botoes = [
            [
                sg.Button(self._PARENTESE_ESQUERDO, **self._config['BOTOES_AUX'], **self._config['TODOS_BOTOES']),
                sg.Button(self._PARENTESE_DIREITO, **self._config['BOTOES_AUX'], **self._config['TODOS_BOTOES']),
                sg.Button(self._BACKSPACE, **self._config['BOTOES_AUX'], **self._config['TODOS_BOTOES']),
                sg.Button(self._LIMPAR, **self._config['BOTAO_LIMPAR'], **self._config['TODOS_BOTOES']),
            ],
            [
                sg.Button('7', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button('8', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button('9', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button(self._SOMA, **self._config['BOTOES_OP'], **self._config['TODOS_BOTOES']),
            ],
            [
                sg.Button('4', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button('5', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button('6', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button(self._SUBTRACAO, **self._config['BOTOES_OP'], **self._config['TODOS_BOTOES']),
            ],
            [
                sg.Button('1', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button('2', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button('3', **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button(self._MULTIPLICACAO, **self._config['BOTOES_OP'], **self._config['TODOS_BOTOES']),
            ],
            [
                sg.Button('0', **self._config['BOTAO_ZERO'], **self._config['TODOS_BOTOES']),
                sg.Button(self._VIRGULA, **self._config['BOTOES_NUM'], **self._config['TODOS_BOTOES']),
                sg.Button(self._DIVISAO, **self._config['BOTOES_OP'], **self._config['TODOS_BOTOES']),
            ],
            [
                sg.Button(self._CALCULAR, **self._config['BOTAO_CALCULAR'], **self._config['TODOS_BOTOES']),
            ]
        ]

        self._config['AREA_BOTOES']['layout'].extend(botoes)

        area_botoes = sg.Frame(**self._config['AREA_BOTOES'])

        self._config['JANELA']['layout'].append(
            [area_botoes]
        )

    def _obter_botao_compativel(self, evento):

        match evento:
            case '+':
                return self._SOMA
            case '-':
                return self._SUBTRACAO
            case '*':
                return self._MULTIPLICACAO
            case '/':
                return self._DIVISAO
            case 'BackSpace:8':
                return self._BACKSPACE
            case 'Delete:46':
                return self._LIMPAR
            case '\r':
                return self._CALCULAR
            case _:
                if type(self._janela.find_element(evento, silent_on_error=True)) is sg.Button:
                    return evento
                return None

    def _carregar_restricoes(self):
        seq = self._display.get()

        if len(seq) == 0:
            return

        janela = self._janela

        if seq == self._ESTADO_INICIAL:

            janela[self._SUBTRACAO].update(disabled=False)
            janela[self._PARENTESE_ESQUERDO].update(disabled=False)
            janela[self._VIRGULA].update(disabled=not self._INICIO_ZERO)

            for botao in [
                self._SOMA, self._MULTIPLICACAO, self._DIVISAO, self._PARENTESE_DIREITO
            ]:
                janela[botao].update(disabled=True)

        elif seq == self._SUBTRACAO:

            janela[self._PARENTESE_ESQUERDO].update(disabled=False)
            janela[self._SUBTRACAO].update(disabled=True)

            for botao in [
                self._SOMA, self._MULTIPLICACAO, self._DIVISAO, self._VIRGULA, self._PARENTESE_DIREITO
            ]:
                janela[botao].update(disabled=True)

        elif len(seq) > 2 and ('e' in seq[-2:] or 'E' in seq[-2:]):

            for botao in [
                self._SOMA, self._SUBTRACAO, self._MULTIPLICACAO, self._DIVISAO,
                self._VIRGULA, self._PARENTESE_DIREITO, self._PARENTESE_ESQUERDO
            ]:
                janela[botao].update(disabled=True)

            for num in range(0, 10):
                janela[f'{num}'].update(disabled=True)

        else:

            ultima_tecla = seq[-1]

            match ultima_tecla:

                case ('0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'):

                    if janela[ultima_tecla].Disabled:
                        for num in range(0, 10):
                            janela[f'{num}'].update(disabled=False)

                    janela[self._PARENTESE_ESQUERDO].update(disabled=True)

                    for botao in [
                        self._SOMA, self._SUBTRACAO, self._MULTIPLICACAO, self._DIVISAO,
                        self._VIRGULA, self._PARENTESE_DIREITO
                    ]:
                        janela[botao].update(disabled=False)

                case (self._SOMA | self._SUBTRACAO | self._MULTIPLICACAO | self._DIVISAO):

                    if janela[ultima_tecla].Disabled:
                        for botao in [
                            self._SOMA, self._SUBTRACAO, self._MULTIPLICACAO, self._DIVISAO,
                        ]:
                            janela[botao].update(disabled=False)

                    for num in range(0, 10):
                        janela[f'{num}'].update(disabled=False)

                    janela[self._PARENTESE_ESQUERDO].update(disabled=False)
                    janela[self._PARENTESE_DIREITO].update(disabled=True)
                    janela[self._VIRGULA].update(disabled=True)

                case self._VIRGULA:

                    for botao in [
                        self._SOMA, self._SUBTRACAO, self._MULTIPLICACAO, self._DIVISAO,
                        self._VIRGULA, self._PARENTESE_ESQUERDO, self._PARENTESE_DIREITO
                    ]:
                        janela[botao].update(disabled=True)

                case self._PARENTESE_ESQUERDO:

                    janela[self._SUBTRACAO].update(disabled=False)

                    for botao in [
                        self._SOMA, self._MULTIPLICACAO, self._DIVISAO, self._VIRGULA
                    ]:
                        janela[botao].update(disabled=True)

                case self._PARENTESE_DIREITO:

                    janela[self._PARENTESE_ESQUERDO].update(disabled=True)
                    janela[self._VIRGULA].update(disabled=True)

                    for num in range(0, 10):
                        janela[f'{num}'].update(disabled=True)

    def _reset_display(self):
        self._display(self._ESTADO_INICIAL)

    def _backspace_display(self):
        self._display(self._display.get()[:-1])

    def _atualizar_display(self, info):
        self._display(info)

    def _calcular(self):
        from calculo.calcexpress import calcular_exp

        exp = self._display.get().\
            replace(self._VIRGULA, '.'). \
            replace(self._SOMA, '+'). \
            replace(self._SUBTRACAO, '-').\
            replace(self._MULTIPLICACAO, '*').\
            replace(self._DIVISAO, '/')

        try:
            result_exp = calcular_exp(exp)
        except Exception as erro:
            raise erro
        else:
            result_exp = str(result_exp).\
                replace('.', self._VIRGULA).\
                replace('-', self._SUBTRACAO)
            self._atualizar_display(result_exp)

    def _simular_clique(self, botao):
        cor_padrao = self._janela[botao].ButtonColor
        self._janela[botao].update(button_color=('white', 'black'))
        self._janela.refresh()
        sleep(0.05)
        self._janela[botao].update(button_color=cor_padrao)
        self._janela.refresh()

    def finalizar(self):
        self._janela.close()

    def iniciar(self):

        self._janela = sg.Window(**self._config['JANELA'])

        while True:

            self._carregar_restricoes()

            evento, valores = self._janela.read()

            if evento == sg.WINDOW_CLOSED:
                break

            botao = self._obter_botao_compativel(evento)

            if botao is None:
                continue

            match botao:
                case self._BACKSPACE:
                    self._simular_clique(botao)
                    self._backspace_display()

                    if self._display.get() == '':
                        self._reset_display()

                case self._LIMPAR:
                    self._simular_clique(botao)
                    self._reset_display()

                case self._CALCULAR:
                    self._simular_clique(botao)
                    try:
                        self._calcular()
                    except Exception as erro_calcular:
                        self._mostrar_msg_erro(erro_calcular)
                        self._janela.read(timeout=1000)

                case _:
                    if self._janela[botao].Disabled:
                        continue

                    self._simular_clique(botao)

                    sequencia = self._display.get()

                    if sequencia == self._ESTADO_INICIAL:

                        if botao == '0':
                            self._INICIO_ZERO = True
                            continue

                        elif not self._INICIO_ZERO:
                            sequencia = ''

                        else:
                            self._INICIO_ZERO = False

                    elif botao in [
                        self._SOMA, self._SUBTRACAO, self._MULTIPLICACAO, self._DIVISAO, self._VIRGULA
                    ] and sequencia[-1] in [
                        self._SOMA, self._SUBTRACAO, self._MULTIPLICACAO, self._DIVISAO, self._VIRGULA
                    ]:
                        self._backspace_display()
                        sequencia = self._display.get()

                    self._atualizar_display(sequencia + self._janela[botao].ButtonText)

        self.finalizar()
