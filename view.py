import sys

import operacoes as opmat
import re as regex


def obter_exp_prioritaria(exp):
    div = r'-?\s?\d*\.?\d+\s?/\s?-?\s?\d*\.?\d+'
    mult = r'-?\s?\d*\.?\d+\s?\*\s?-?\s?\d*\.?\d+'
    soma = r'-?\s?\d*\.?\d+\s?\+\s?-?\d*\.?\d+'
    sub = r'-?\s?\d*\.?\d+\s?-\s?-?\d*\.?\d+'

    divisoes = regex.findall(div, exp)
    multiplicacoes = regex.findall(mult, exp)
    somas = regex.findall(soma, exp)
    substracoes = regex.findall(sub, exp)

    if len(divisoes) == len(multiplicacoes) == len(somas) == len(substracoes) == 0:
        return None

    if len(divisoes) > 0 and (len(multiplicacoes) == 0 or exp.find(divisoes[0]) < exp.find(multiplicacoes[0])):
        return divisoes[0]
    if len(multiplicacoes) > 0 and (len(divisoes) == 0 or exp.find(multiplicacoes[0]) < exp.find(divisoes[0])):
        return multiplicacoes[0]
    if len(somas) > 0 and (len(substracoes) == 0 or exp.find(somas[0]) < exp.find(substracoes[0])):
        return somas[0]
    if len(substracoes) > 0 and (len(somas) == 0 or exp.find(substracoes[0]) < exp.find(somas[0])):
        return substracoes[0]


def calc_exp_simples(exp):
    while True:
        exp_prioritaria = obter_exp_prioritaria(exp)

        if exp_prioritaria is None:
            return exp

        print(f'=> Calculando: {exp}', end=' = ')

        if '/' in exp_prioritaria:
            elementos = regex.split(r'/', exp_prioritaria)
            resultado = opmat.dividir(*[float(e.replace(' ', '')) for e in elementos])

        elif '*' in exp_prioritaria:
            elementos = regex.split(r'\*', exp_prioritaria)
            resultado = opmat.multiplicar(*[float(e.replace(' ', '')) for e in elementos])

        elif '+' in exp_prioritaria:
            elementos = regex.split(r'\+', exp_prioritaria)
            resultado = opmat.somar(*[float(e.replace(' ', '')) for e in elementos])

        elif '-' in exp_prioritaria:
            elementos = regex.findall(r'-?\s?\d*\.?\d+\s?', exp_prioritaria)
            resultado = opmat.somar(*[float(e.replace(' ', '')) for e in elementos])
        else:
            resultado = None

        print(resultado)

        exp = exp.replace(exp_prioritaria, str(resultado))


def calc_exp_complex(exp):
    if exp.count('(') != exp.count(')'):
        sys.exit('Erro: Expressão inválida!')

    parenteses = exp.count('(')

    if parenteses > 0:

        for i in range(0, parenteses):

            print(f'\n{i + 1}ª parte: {exp}')

            abre_parentese = exp.rfind('(')
            fecha_parentese = exp.find(')', abre_parentese)
            exp_em_parenteses = exp[abre_parentese:fecha_parentese + 1]

            result = calc_exp_simples(exp_em_parenteses[1:-1])

            exp = exp.replace(exp_em_parenteses, str(result))

    print(f'\n{parenteses + 1}ª parte: {exp}')

    return float(calc_exp_simples(exp))


expressao = '(((8 * 4 + 3) / 7 + (3 + 15 / 5) * 3) * 2 - (19 - 7) / 6) * 2 + 12'
calc_exp_complex(expressao)



