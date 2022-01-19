import operacoes as opmat


def calc_exp_simples(exp):
    exp = exp.replace('(', '').replace(')', '')
    if '/' in exp:
        exp = exp.replace(' / ', ' ')
        operandos = [float(o) for o in exp.split(' ')]
        result = opmat.dividir(*operandos)
    elif '*' in exp:
        exp = exp.replace(' * ', ' ')
        operandos = [float(o) for o in exp.split(' ')]
        result = opmat.multiplicar(*operandos)
    elif '+' in exp:
        exp = exp.replace(' + ', ' ')
        operandos = [float(o) for o in exp.split(' ')]
        result = opmat.dividir(*operandos)
    else:
        exp = exp.replace(' - ', ' ')
        operandos = [float(o) for o in exp.split(' ')]
        result = opmat.dividir(*operandos)

    return result


expressao = '2 + 4 + 3 * 3 - (3 * (30 / 10))'
total_parenteses = expressao.count('(')

if total_parenteses > 0:
    abre_parenteses = []
    fecha_parenteses = []
    for i, c in enumerate(expressao):
        if c == '(':
            abre_parenteses.append(i)
        if c == ')':
            fecha_parenteses.append(i)

    for i in range(total_parenteses - 1, -1, -1):
        sub_exp = expressao[abre_parenteses[i]:(fecha_parenteses[::-1][i] + 1)]
        result_sub_exp = calc_exp_simples(sub_exp)
        expressao = expressao.replace(sub_exp, str(result_sub_exp))

    print(expressao)
