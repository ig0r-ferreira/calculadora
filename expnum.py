import re as regex
import operacoes_mat as opmat
import sys


def obter_exp_prioritaria(exp_num):
    div = r'-?\s?\d*\.?\d+\s?/\s?-?\s?\d*\.?\d+'
    mult = r'-?\s?\d*\.?\d+\s?\*\s?-?\s?\d*\.?\d+'
    soma = r'-?\s?\d*\.?\d+\s?\+\s?-?\d*\.?\d+'
    sub = r'-?\s?\d*\.?\d+\s?-\s?-?\d*\.?\d+'

    # Busca por operações de divisão
    divisoes = regex.findall(div, exp_num)
    # Busca por operações de multiplicação
    multiplicacoes = regex.findall(mult, exp_num)
    # Busca por operações de soma
    somas = regex.findall(soma, exp_num)
    # Busca por operações de subtração
    substracoes = regex.findall(sub, exp_num)

    # Se não for encontrada mais nenhuma operação para ser realizada então 'None'
    # é retornado
    if len(divisoes) == len(multiplicacoes) == len(somas) == len(substracoes) == 0:
        return None

    # Retorna a primeira operação de divisão encontrada, caso ela se encontre antes
    # da multiplicação
    if len(divisoes) > 0 and \
            (len(multiplicacoes) == 0 or exp_num.find(divisoes[0]) < exp_num.find(multiplicacoes[0])):
        return divisoes[0]
    # Retorna a primeira operação de multiplicação encontrada, caso ela se encontre
    # antes da divisão
    if len(multiplicacoes) > 0 and \
            (len(divisoes) == 0 or exp_num.find(multiplicacoes[0]) < exp_num.find(divisoes[0])):
        return multiplicacoes[0]
    # Retorna a primeira operação de soma encontrada, caso ela se encontre antes da
    # subtração
    if len(somas) > 0 and \
            (len(substracoes) == 0 or exp_num.find(somas[0]) < exp_num.find(substracoes[0])):
        return somas[0]
    # Retorna a primeira operação de subtração encontrada, caso ela se encontre antes
    # da soma
    if len(substracoes) > 0 and \
            (len(somas) == 0 or exp_num.find(substracoes[0]) < exp_num.find(somas[0])):
        return substracoes[0]

    return None


def calc_exp_simples(exp_num):
    # Remove os espaços antes e depois da expressão numérica
    exp_num = exp_num.strip()

    while True:
        # Obtém a próxima expressão a ser calculada, seguindo a prioridade
        # das operações matemáticas
        prox_exp = obter_exp_prioritaria(exp_num)

        # Caso não tenha mais nenhuma expressão para calcular retorna o resultado
        if prox_exp is None:
            # Realiza o jogo de sinais
            exp_num = exp_num.replace('--', '')
            return exp_num

        print(f'=> Calculando por prioridade: {prox_exp}', end=' = ')

        if '/' in prox_exp:
            # Valores envolvidos na divisão
            elementos = regex.split(r'/', prox_exp)
            resultado = opmat.dividir(*[float(e.replace(' ', '')) for e in elementos])

        elif '*' in prox_exp:
            # Valores envolvidos na multiplicação
            elementos = regex.split(r'\*', prox_exp)
            resultado = opmat.multiplicar(*[float(e.replace(' ', '')) for e in elementos])

        elif '+' in prox_exp:
            # Valores envolvidos na soma
            elementos = regex.split(r'\+', prox_exp)
            resultado = opmat.somar(*[float(e.replace(' ', '')) for e in elementos])

        elif '-' in prox_exp:
            # Valores envolvidos na subtração
            elementos = regex.findall(r'-?\s?\d*\.?\d+\s?', prox_exp)
            resultado = opmat.somar(*[float(e.replace(' ', '')) for e in elementos])
        else:
            resultado = None

        print(resultado)

        # Na expressão original, substitui a expressão identificada como prioritária
        # pelo resultado dela
        exp_num = exp_num.replace(prox_exp, str(resultado))


def calc_exp(exp_num):
    # Remove os espaços antes e depois da expressão numérica
    exp_num = exp_num.strip()
    agrupadores = [
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

    print(f'\n-- Expressão original: {exp_num}')

    # Para cada agrupador, são eles: () [] {}
    for agrup in agrupadores:
        quant_abre = exp_num.count(agrup.get('abre'))
        quant_fecha = exp_num.count(agrup.get('fecha'))

        # Verifica se há algum agrupador que não foi aberto ou fechado corretamente
        if quant_abre != quant_fecha:
            sys.exit('Erro: Expressão inválida!')
        elif quant_abre == quant_fecha == 0:
            # Se o agrupador não for encontrado, pula para o próximo seguindo
            # a ordem de prioridade
            continue
        else:
            # Para cada par de agrupadores encontrados
            for i in range(0, quant_abre):
                abre_agrupador = exp_num.rfind(agrup.get('abre'))
                fecha_agrupador = exp_num.find(agrup.get('fecha'), abre_agrupador)

                # Obtém a expressão dentro do agrupador
                exp_no_agrupador = exp_num[abre_agrupador:fecha_agrupador + 1]

                # Calcula o resultado da expressão
                result = calc_exp_simples(exp_no_agrupador[1:-1])
                # Na expressão original substitui a expressão contida no agrupador
                # pelo resultado dela
                exp_num = exp_num.replace(exp_no_agrupador, str(result))

                print(f'\n-- Expressão simplificada: {exp_num}')

    # Retorna a expressão numérica simplificada após ter calculado as expressões
    # de todos os agrupadores
    return float(calc_exp_simples(exp_num))
