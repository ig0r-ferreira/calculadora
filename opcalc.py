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


def formatar_exp(exp_num):
    exp_num = exp_num.replace(' ', '')

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


def buscar_prioridade(exp_num):

    exp_num = formatar_exp(exp_num)

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


def simplificar_exp(exp_num):

    while True:
        # Obtém a próxima expressão a ser calculada, seguindo a prioridade
        # das operações matemáticas
        exp_num = formatar_exp(exp_num)
        prox_exp = buscar_prioridade(exp_num)

        # Caso não tenha mais nenhuma expressão para calcular retorna o resultado
        if prox_exp is None:
            # Realiza o jogo de sinais
            exp_num = exp_num.replace('-(-', '').replace(')', '').replace('(', '')

            return exp_num

        if '/' in prox_exp:
            separador_div = r'/'
            # Valores envolvidos na divisão
            elementos = regex.split(separador_div, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            try:
                result = dividir(*elementos)
            except ZeroDivisionError as erro_divisao:
                raise erro_divisao

        elif '*' in prox_exp:
            separador_mult = r'\*'
            # Valores envolvidos na multiplicação
            elementos = regex.split(separador_mult, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            result = multiplicar(*elementos)

        elif '+' in prox_exp:
            separador_soma = r'\+'
            # Valores envolvidos na soma
            elementos = regex.split(separador_soma, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            result = somar(*elementos)

        elif '-' in prox_exp:
            separador_sub = r'(?<=\))-(?=\()|(?<=\d)-(?=\()|(?<=\))-(?=\d)|(?<=\d)-(?=\d)'
            # Valores envolvidos na subtração
            elementos = regex.split(separador_sub, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            result = subtrair(*elementos)

        else:
            result = None

        result = str(result)

        # Se o resultado for negativo adiciona os parênteses ao redor
        if regex.search(r'-\d*\.?\d+', result):
            result = f'({result})'

        # Na expressão original, substitui a expressão identificada como prioritária
        # pelo resultado dela
        exp_num = exp_num.replace(prox_exp, result)


def calcular_exp(exp_num):
    conjuntos = [
        {
            'abre': '(',
            'fecha': ')'
        },
        {
            'abre': '[',
            'fecha': ']'
        },
        {
            'abre': '{',
            'fecha': '}'
        }
    ]

    # Para cada conjunto, são eles: () [] {}
    for conjunto in conjuntos:
        quant_abre = exp_num.count(conjunto.get('abre'))
        quant_fecha = exp_num.count(conjunto.get('fecha'))

        # Verifica se há algum conjunto que não foi aberto ou fechado corretamente
        if quant_abre != quant_fecha:
            erro_sintaxe = 'Expressão inválida!'

            if quant_abre > quant_fecha:
                erro_sintaxe += f' Há um \'{conjunto.get("fecha")}\' faltando.'
            else:
                erro_sintaxe += f' Há um \'{conjunto.get("abre")}\' faltando.'

            raise SyntaxError(erro_sintaxe)

        elif quant_abre == quant_fecha == 0:
            # Se o conjunto não for encontrado, pula para o próximo seguindo
            # a ordem de prioridade
            continue
        else:
            # Para cada par de conjuntos encontrados
            while True:
                abre_conjunto = exp_num.rfind(conjunto.get('abre'))
                fecha_conjunto = exp_num.find(conjunto.get('fecha'), abre_conjunto)

                if abre_conjunto == fecha_conjunto == -1:
                    break

                # Obtém a expressão no conjunto
                exp_no_conjunto = exp_num[abre_conjunto:fecha_conjunto + 1]

                # Calcula o resultado da expressão
                try:
                    resultado = simplificar_exp(exp_no_conjunto)
                except ZeroDivisionError as erro_divisao:
                    raise erro_divisao

                # Na expressão original substitui a expressão contida no conjunto
                # pelo resultado dela
                exp_num = exp_num.replace(exp_no_conjunto, str(resultado))

    # Retorna a expressão numérica simplificada após ter calculado as expressões
    # de todos os conjuntos
    try:
        resultado_final = float(simplificar_exp(exp_num))

        if resultado_final.is_integer():
            # Se não é um número "quebrado" elimina as casas decimais
            resultado_final = int(resultado_final)

        return resultado_final

    except ValueError:
        raise ValueError('Expressão inválida!')

    except ZeroDivisionError as erro_divisao:
        raise erro_divisao


if __name__ == "__main__":
    print(calcular_exp('5 + 6 * 20'))
