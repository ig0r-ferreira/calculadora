import operacoes as opmat
import re as regex


def obter_exp_prioritaria(exp):
    div = exp.find('/')
    mult = exp.find('*')
    soma = exp.find('+')
    sub = exp.find('-')

    if div != -1 and (mult == -1 or div < mult):
        return regex.findall(r'-?\d*\.?\d+\s?/\s?-?\d*\.?\d+', exp)[0]
    if mult != -1 and (div == -1 or div > mult):
        return regex.findall(r'-?\d*\.?\d+\s?\*\s?-?\d*\.?\d+', exp)[0]
    if soma != -1 and (sub == -1 or soma < sub):
        return regex.findall(r'-?\d*\.?\d+\s?\+\s?-?\d*\.?\d+', exp)[0]
    if sub != -1 and (soma == -1 or soma > sub):
        return regex.findall(r'-?\d*\.?\d+\s?-\s?-?\d*\.?\d+', exp)[0]


def calc_exp_simples(exp):
    while True:
        exp_priort = obter_exp_prioritaria(exp)
        print(exp_priort, end=' = ')
        if exp_priort is None:
            return exp

        if '/' in exp_priort:
            elementos = regex.split(r'/', exp_priort)
            resultado = opmat.dividir(*[float(e) for e in elementos])

        elif '*' in exp_priort:
            elementos = regex.split(r'\*', exp_priort)
            resultado = opmat.multiplicar(*[float(e) for e in elementos])

        elif '+' in exp_priort:
            elementos = regex.split(r'\+', exp_priort)
            resultado = opmat.somar(*[float(e) for e in elementos])

        elif '-' in exp_priort:
            elementos = regex.split(r'-', exp_priort)
            resultado = opmat.subtrair(*[float(e) for e in elementos])
        else:
            resultado = None

        print(resultado)
        exp = exp.replace(exp_priort, str(resultado))


def calc_exp_complex(exp):
    if exp.count('(') != exp.count(')'):
        print('Erro: Expressão inválida!')
        return

    total_parenteses = exp.count('(')

    if total_parenteses > 0:

        for i in range(0, total_parenteses):
            abre_parentese = exp.rfind('(')
            fecha_parentese = exp.find(')', abre_parentese) + 1

            exp_prioritaria = exp[abre_parentese:fecha_parentese]
            result_exp = calc_exp_simples(exp_prioritaria[1:-1])

            exp = exp.replace(exp_prioritaria, str(result_exp))

    print(calc_exp_simples(exp))


separador = ' '
expressao = '2 + 4 + 3 * 3 - (3 * (30 / 10) * (8 - 2 * 2))'
# 2 + 4 + 3 * 3 - 36
# 2 + 4 + 9 - 36
# 15 - 36
# -21
calc_exp_complex(expressao)
