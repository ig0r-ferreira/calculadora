def somar(*elementos):
    return sum(elementos)


def subtrair(*elementos):
    result = None
    for i, e in enumerate(elementos):
        if i == 0:
            result = e
            continue
        result -= e
    return result


def multiplicar(*elementos):
    result = 1
    for e in elementos:
        result *= e
    return result


def dividir(*elementos):
    result = None
    try:
        for i, e in enumerate(elementos):
            if i == 0:
                result = e
                continue
            result /= e
    except ZeroDivisionError:
        raise ZeroDivisionError('\nNão é possível efetuar uma divisão por zero!')
    else:
        return result
