from decimal import *
import re as regex

getcontext().prec = 9
getcontext().rounding = ROUND_HALF_UP


REGEX_NUM_REAL = r'\d*\.?\d+'
REGEX_NUM_REAL_CIENTIFICO = r'\d*\.?\d+[Ee]\+\d+|\d*\.?\d+[Ee]\-\d+|\d*\.?\d+[Ee]\d+'


def somar(*elementos):
    soma = 0
    for e in elementos:
        soma += Decimal(f'{e}')

    return soma


def subtrair(*elementos):
    result = None
    for i, e in enumerate(elementos):
        e = Decimal(f'{e}')
        if i == 0:
            result = e
            continue
        result -= e

    return result


def multiplicar(*elementos):
    result = 1
    for e in elementos:
        result *= Decimal(f'{e}')

    return result


def dividir(*elementos):
    result = None
    try:
        for i, e in enumerate(elementos):
            e = Decimal(f'{e}')
            if i == 0:
                result = e
                continue

            result /= e

    except ZeroDivisionError:
        raise ZeroDivisionError('Não é possível efetuar uma divisão por zero!')
    else:
        return result


def _obter_sinais_associacao():
    return [
        {
            'abre': '(',
            'fecha': ')',
        },
        {
            'abre': '[',
            'fecha': ']',
        },
        {
            'abre': '{',
            'fecha': '}',
        }
    ]


def _validar_uso_sinais_associacao(exp_num):
    for sinal in _obter_sinais_associacao():
        quant_abre = exp_num.count(sinal.get('abre'))
        quant_fecha = exp_num.count(sinal.get('fecha'))

        # Verifica se há algum sinal que não foi aberto ou fechado corretamente
        if quant_abre != quant_fecha:
            erro_sintaxe = 'Expressão inválida.'

            if quant_abre > quant_fecha:
                erro_sintaxe += f' Há um \'{sinal.get("abre")}\' que não foi fechado.'
            else:
                erro_sintaxe += f' Há um \'{sinal.get("fecha")}\' sobrando.'

            raise SyntaxError(erro_sintaxe)


def _buscar_caracteres_nao_permitidos(exp_num):
    REGEX_CARACTERES_INCOMUNS = r'[^.+\-*/()\[\]{}\d\sEe]'

    result = regex.findall(REGEX_CARACTERES_INCOMUNS, exp_num)
    if len(result) > 0:
        caracteres = ' '.join(result)
        raise SyntaxError(f'Expressão inválida. Não use o(s) caracter(es): {caracteres}.')


def _validar_exp(exp_num):
    _buscar_caracteres_nao_permitidos(exp_num)
    _validar_uso_sinais_associacao(exp_num)


def _aplicar_parenteses_em_negativos(exp_num):
    REGEX_NUM_NEGATIVO = fr'(?:(?<=^)|(?<=[(\[{{]))-({REGEX_NUM_REAL}|{REGEX_NUM_REAL_CIENTIFICO})(?=[+\-\/*])|' \
                         fr'(?<=[^(\[}}Ee])-({REGEX_NUM_REAL}|{REGEX_NUM_REAL_CIENTIFICO})' \
                         r'(?:(?=[+\-\/*])|(?=[)\]}])|(?=$))'

    while True:

        result = regex.search(REGEX_NUM_NEGATIVO, exp_num)

        if result is None:
            break

        pos_ini = result.span()[0]
        pos_fim = result.span()[1]

        exp_lista = list(exp_num)

        exp_lista.insert(pos_fim, ')')

        if pos_ini > 0 and (exp_num[pos_ini - 1].isdigit() or exp_num[pos_ini - 1] == ')'):
            exp_lista.insert(pos_ini, '+(')
        else:
            exp_lista.insert(pos_ini, '(')

        exp_num = ''.join(exp_lista)

    return exp_num


def _aplicar_jogo_de_sinais(exp_num):
    REGEX_DUPLA_NEGACAO = fr'-[(\[{{]-({REGEX_NUM_REAL}|{REGEX_NUM_REAL_CIENTIFICO})[)\]}}]'

    elementos = regex.findall(REGEX_DUPLA_NEGACAO, exp_num)

    if len(elementos) > 0:
        for e in elementos:
            exp_num = exp_num.replace(f'-(-{e})', f'+{e}')

    return exp_num


def _formatar_exp(exp_num):
    exp_num = exp_num.replace(' ', '')

    exp_num = _aplicar_parenteses_em_negativos(exp_num)

    exp_num = _aplicar_jogo_de_sinais(exp_num)

    return exp_num


def _montar_regex_para_operacao(operacao):
    return r'(?:(?<=^)|(?<=[+\-\/\*\(]))' \
           fr'({REGEX_NUM_REAL}|\(-{REGEX_NUM_REAL}\)|{REGEX_NUM_REAL_CIENTIFICO}|\(-({REGEX_NUM_REAL_CIENTIFICO})\))' \
           fr'{operacao}' \
           fr'({REGEX_NUM_REAL}|\(-{REGEX_NUM_REAL}\)|{REGEX_NUM_REAL_CIENTIFICO}|\(-({REGEX_NUM_REAL_CIENTIFICO})\))' \
           r'(?:(?=$)|(?=[+\-\/\*\)]))'


def _buscar_prioridade(exp_num):

    REGEX_DIVISAO = _montar_regex_para_operacao(r'\/')
    REGEX_MULTIPLICACAO = _montar_regex_para_operacao(r'\*')
    REGEX_SOMA = _montar_regex_para_operacao(r'\+')
    REGEX_SUBTRACAO = _montar_regex_para_operacao(r'-')

    # Busca por operações de divisão
    prox_div = regex.search(REGEX_DIVISAO, exp_num)
    # Busca por operações de multiplicação
    prox_mult = regex.search(REGEX_MULTIPLICACAO, exp_num)
    # Busca por operações de soma
    prox_soma = regex.search(REGEX_SOMA, exp_num)
    # Busca por operações de subtração
    prox_sub = regex.search(REGEX_SUBTRACAO, exp_num)

    # Se não for encontrada mais nenhuma operação para ser realizada então 'None'
    # é retornado
    if prox_div == prox_mult == prox_soma == prox_sub is None:
        return None

    # Retorna a primeira operação de divisão encontrada, caso ela se encontre antes
    # da multiplicação
    if prox_div and (prox_mult is None or prox_div.span()[0] < prox_mult.span()[0]):
        return prox_div.group()
    # Retorna a primeira operação de multiplicação encontrada, caso ela se encontre
    # antes da divisão
    if prox_mult and (prox_div is None or prox_mult.span()[0] < prox_div.span()[0]):
        return prox_mult.group()
    # Retorna a primeira operação de soma encontrada, caso ela se encontre antes da
    # subtração
    if prox_soma and (prox_sub is None or prox_soma.span()[0] < prox_sub.span()[0]):
        return prox_soma.group()
    # Retorna a primeira operação de subtração encontrada, caso ela se encontre antes
    # da soma
    if prox_sub and (prox_soma is None or prox_sub.span()[0] < prox_soma.span()[0]):
        return prox_sub.group()

    return None


def _simplificar_exp(exp_num):
    while True:
        exp_num = _formatar_exp(exp_num)
        # Obtém a próxima expressão a ser calculada, seguindo a prioridade das operações matemáticas
        exp_prioridade = _buscar_prioridade(exp_num)
        # Caso não tenha mais nenhuma expressão para calcular, retorna o resultado

        if exp_prioridade is None:
            REGEX_RESULTADO = fr'-?({REGEX_NUM_REAL}|{REGEX_NUM_REAL_CIENTIFICO})(?:(?=[)\]}}])|(?=$))'

            result = regex.search(REGEX_RESULTADO, exp_num)

            if result is None:
                raise InvalidOperation('Operação inválida!')

            result = result.group()

            return result

        REGEX_OPERADOR = r'(?<=\))[^\w\s\.](?=\()|' \
                         r'(?<=\))[^\w\s\.](?=\d)|' \
                         r'(?<=\d)[^\w\s\.](?=\()|' \
                         r'(?<=\d)[^\w\s\.](?=\d)'

        busca_operador = regex.search(REGEX_OPERADOR, exp_prioridade)
        operador = None

        if busca_operador is not None:
            operador = busca_operador.group()

        elementos = regex.split(REGEX_OPERADOR, exp_prioridade)
        elementos = [e.replace('(', '').replace(')', '') for e in elementos]

        if operador == '/':
            try:
                result = dividir(*elementos)
            except ZeroDivisionError as erro_divisao_por_zero:
                raise erro_divisao_por_zero

        elif operador == '*':
            result = multiplicar(*elementos)

        elif operador == '+':
            result = somar(*elementos)

        elif operador == '-':
            result = subtrair(*elementos)

        else:
            result = None

        result = str(result)

        # Substitui a expressão prioritária pelo resultado dela
        exp_num = exp_num.replace(exp_prioridade, result)


def _formatar_resultado(result):
    try:
        result = Decimal(result)
    except InvalidOperation:
        raise InvalidOperation('Operação inválida!')
    else:
        result = result.to_integral() if result == result.to_integral() else result.normalize()

        return result


def calcular_exp(exp_num):

    _validar_exp(exp_num)

    REGEX_CONTEUDO_APENAS_NUMERO = fr'^-?({REGEX_NUM_REAL}|{REGEX_NUM_REAL_CIENTIFICO})$'

    # Para cada sinal de associação: () [] {}
    for sinal in _obter_sinais_associacao():
        quant_abre = exp_num.count(sinal.get('abre'))
        quant_fecha = exp_num.count(sinal.get('fecha'))

        # Pula caso não encontre expressões entre os sinais
        if quant_abre == quant_fecha == 0:
            continue

        # Para cada par de sinais encontrados
        while True:
            abre_sinal = exp_num.rfind(sinal.get('abre'))
            fecha_sinal = exp_num.find(sinal.get('fecha'), abre_sinal)

            if abre_sinal == fecha_sinal == -1:
                break

            # Obtém a expressão entre os sinais de associação
            exp_prioridade = exp_num[abre_sinal+1:fecha_sinal]

            # Verifica se a expressão é apenas um número
            if regex.match(REGEX_CONTEUDO_APENAS_NUMERO, exp_prioridade):
                resultado = exp_prioridade
            else:
                try:
                    # Calcula o resultado da expressão
                    resultado = _simplificar_exp(exp_prioridade)
                except ZeroDivisionError as erro_divisao_por_zero:
                    raise erro_divisao_por_zero

            # Substitui a expressão prioritária pelo resultado dela
            exp_num = exp_num.replace(f'{sinal.get("abre")}{exp_prioridade}{sinal.get("fecha")}', str(resultado))

    # Verifica se o que sobrou da expressão é o próprio resultado
    if regex.match(REGEX_CONTEUDO_APENAS_NUMERO, exp_num):
        result_exp = exp_num
    else:
        # Calcula o resultado da expressão final após ter calculado todas as expressões
        # entre os sinais de associação
        result_exp = _simplificar_exp(exp_num)

    result_exp = _formatar_resultado(result_exp)

    return result_exp


if __name__ == "__main__":

    expressoes = [
        '-5 - {-[-7]}',
        '2 + 8 - 3 - 5 + 15',
        '-5 - (-(-10 + 8 - 5))',
        '(-10 / 2.5 * (-3.8))',
        '12 + [35 - (10 + 2) +2]',
        '[(18 + 3 * 2) / 8 + 5 * 3] / 6',
        '37 + [-25 - (-11 + 19 - 4)]',
        '60 / {2 * [-7 + 18 / (-3 + 12)]} - [7 * (-3) - 18 / (-2) + 1]',
        '-8 + {-5 + [(8 - 12) + (13 + 12)] - 10}',
        '3 - {2 + (11 - 15) - [5 + (-3 + 1)] + 8}',
        '{[(8 * 4 + 3) / 7 + (3 + 15 / 5) * 3] * 2 - (19 - 7) / 6} * 2 + 12',
        '((1111111111 + 1111111111) * (1111111111 + 1111111111)) * 2',
        '9.87654320e18 * (-5)',
        '(-2.22222222e9 - (-3.33333333e9)) * 4.44444444e11'
    ]

    for exp in expressoes:
        print(f'{expressoes.index(exp) + 1})\t{exp} = {calcular_exp(exp)}')
