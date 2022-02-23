from decimal import *
import re as regex

getcontext().prec = 9
getcontext().rounding = ROUND_HALF_UP


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


def __obter_sinais_associacao():
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


def __validar_uso_sinais_associacao(exp_num):
    for sinal in __obter_sinais_associacao():
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


def __buscar_caracteres_nao_permitidos(exp_num):
    result = regex.findall(r'[^.+\-*/()\[\]{}\d\s]', exp_num)
    if len(result) > 0:
        caracteres = ' '.join(result)
        raise SyntaxError(f'Expressão inválida. Não use o(s) caracter(es): {caracteres}.')


def __validar_exp(exp_num):
    __buscar_caracteres_nao_permitidos(exp_num)
    __validar_uso_sinais_associacao(exp_num)


def __colocar_negativos_entre_parenteses(exp_num):
    negativos_sem_parenteses = r'(?:^|(?<=[^(]))-\d*\.?\d+|(?<=[(])-\d*\.?\d+(?=\*|\+|-|\/)'

    while True:

        result = regex.search(negativos_sem_parenteses, exp_num)

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


def __aplicar_jogo_de_sinais(exp_num):
    elementos = regex.findall(r'-\(-\d*\.?\d+\)', exp_num)
    if len(elementos) > 0:
        for e in elementos:
            exp_num = exp_num.replace(e, '+' + regex.search(r'\d*\.?\d+', e).group())

    return exp_num


def __formatar_exp(exp_num):
    exp_num = exp_num.replace(' ', '')

    exp_num = __colocar_negativos_entre_parenteses(exp_num)

    exp_num = __aplicar_jogo_de_sinais(exp_num)

    return exp_num


def __buscar_prioridade(exp_num):

    div = r'\d*\.?\d+\/\d*\.?\d+|' \
          r'\(-\d*\.?\d+\)\/\(-\d*\.?\d+\)|' \
          r'\d*\.?\d+\/\(-\d*\.?\d+\)|' \
          r'\(-\d*\.?\d+\)\/\d*\.?\d+'
    mult = r'\d*\.?\d+\*\d*\.?\d+|' \
           r'\(-\d*\.?\d+\)\*\(-\d*\.?\d+\)|' \
           r'\d*\.?\d+\*\(-\d*\.?\d+\)|' \
           r'\(-\d*\.?\d+\)\*\d*\.?\d+'
    soma = r'\d*\.?\d+\+\d*\.?\d+|' \
           r'\(-\d*\.?\d+\)\+\(-\d*\.?\d+\)|' \
           r'\d*\.?\d+\+\(-\d*\.?\d+\)|' \
           r'\(-\d*\.?\d+\)\+\d*\.?\d+'
    sub = r'\d*\.?\d+-\d*\.?\d+|' \
          r'\(-\d*\.?\d+\)-\(-\d*\.?\d+\)|' \
          r'\d*\.?\d+-\(-\d*\.?\d+\)|' \
          r'\(-\d*\.?\d+\)-\d*\.?\d+'

    # Busca por operações de divisão
    prox_div = regex.search(div, exp_num)
    # Busca por operações de multiplicação
    prox_mult = regex.search(mult, exp_num)
    # Busca por operações de soma
    prox_soma = regex.search(soma, exp_num)
    # Busca por operações de subtração
    prox_sub = regex.search(sub, exp_num)

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


def __simplificar_exp(exp_num):
    while True:
        exp_num = __formatar_exp(exp_num)
        # Obtém a próxima expressão a ser calculada, seguindo a prioridade
        # das operações matemáticas
        exp_prioridade = __buscar_prioridade(exp_num)

        # Caso não tenha mais nenhuma expressão para calcular, retorna o resultado
        if exp_prioridade is None:

            result = regex.search(r'-?\d*\.?\d+', exp_num).group()

            return result

        identifica_operador = r'(?<=\))[^\w\s\.](?=\()|' \
                              r'(?<=\))[^\w\s\.](?=\d)|' \
                              r'(?<=\d)[^\w\s\.](?=\()|' \
                              r'(?<=\d)[^\w\s\.](?=\d)'

        busca_operador = regex.search(identifica_operador, exp_prioridade)
        operador = None

        if busca_operador is not None:
            operador = busca_operador.group()

        elementos = regex.split(identifica_operador, exp_prioridade)
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

        # Na expressão original, substitui a expressão prioritária pelo resultado dela
        exp_num = exp_num.replace(exp_prioridade, result)


def calcular_exp(exp_num):

    __validar_exp(exp_num)

    # Para cada sinal de associação: () [] {}
    for sinal in __obter_sinais_associacao():
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
            exp_interna = exp_num[abre_sinal:fecha_sinal + 1]

            # Calcula o resultado da expressão
            try:
                resultado = __simplificar_exp(exp_interna[1:-1])
            except ZeroDivisionError as erro_divisao_por_zero:
                raise erro_divisao_por_zero

            # Na expressão original, substitui a expressão contida entre os sinais pelo resultado dela
            exp_num = exp_num.replace(exp_interna, str(resultado))

    # Verifica se o que sobrou da expressão é o próprio resultado
    if regex.search(r'^-?\d*\.?\d+$', exp_num) is not None:
        resultado_final = exp_num
    else:
        # Calcula a expressão final após ter calculado todas as expressões entre os sinais de associação
        resultado_final = __simplificar_exp(exp_num)

    try:
        resultado_final = float(resultado_final)

        if resultado_final.is_integer():
            # Se não é um número "quebrado" elimina as casas decimais
            resultado_final = int(resultado_final)

        return resultado_final

    except ValueError:
        raise ValueError('Erro ao calcular o resultado.')

    except ZeroDivisionError as erro_divisao_por_zero:
        raise erro_divisao_por_zero


if __name__ == "__main__":

    expressoes = [
        '2 + 8 - 3 - 5 + 15',
        '12 + [35 - (10 + 2) +2]',
        '[(18 + 3 * 2) / 8 + 5 * 3] / 6',
        '37 + [-25 - (-11 + 19 - 4)]',
        '60 / {2 * [-7 + 18 / (-3 + 12)]} - [7 * (-3) - 18 / (-2) + 1]',
        '-8 + {-5 + [(8 - 12) + (13 + 12)] - 10}',
        '3 - {2 + (11 - 15) - [5 + (-3 + 1)] + 8}',
        '{[(8 * 4 + 3) / 7 + (3 + 15 / 5) * 3] * 2 - (19 - 7) / 6} * 2 + 12',
        '-(-5) - (-10)',
    ]

    for exp in expressoes:
        print(f'{expressoes.index(exp) + 1})\t{exp} = {calcular_exp(exp)}')
