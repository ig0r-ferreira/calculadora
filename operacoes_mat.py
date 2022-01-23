from decimal import *

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
        raise ZeroDivisionError('\nNão é possível efetuar uma divisão por zero!')
    else:
        return result
