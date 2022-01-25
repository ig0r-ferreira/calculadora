import re as regex
import operacoes_mat as opmat


def formatar_exp(exp_num):
    exp_num = exp_num.replace(' ', '')

    # negativos_sem_parenteses = r'(?:^|(?<=[^(]))-\d+|(?<=[(])-\d+(?=\*|\+|-|\/)'
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


def obter_exp_prioritaria(exp_num):

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


def calc_exp_simples(exp_num):

    while True:
        # Obtém a próxima expressão a ser calculada, seguindo a prioridade
        # das operações matemáticas
        exp_num = formatar_exp(exp_num)
        prox_exp = obter_exp_prioritaria(exp_num)

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
                result = opmat.dividir(*elementos)
            except ZeroDivisionError as erro:
                raise erro

        elif '*' in prox_exp:
            separador_mult = r'\*'
            # Valores envolvidos na multiplicação
            elementos = regex.split(separador_mult, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            result = opmat.multiplicar(*elementos)

        elif '+' in prox_exp:
            separador_soma = r'\+'
            # Valores envolvidos na soma
            elementos = regex.split(separador_soma, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            result = opmat.somar(*elementos)

        elif '-' in prox_exp:
            separador_sub = r'(?<=\))-(?=\()|(?<=\d)-(?=\()|(?<=\))-(?=\d)|(?<=\d)-(?=\d)'
            # Valores envolvidos na subtração
            elementos = regex.split(separador_sub, prox_exp)
            elementos = [e.replace('(', '').replace(')', '') for e in elementos]
            result = opmat.subtrair(*elementos)

        else:
            result = None

        result = str(result)

        # Se o resultado for negativo adiciona os parênteses ao redor
        if regex.search(r'-\d*\.?\d+', result):
            result = f'({result})'

        # Na expressão original, substitui a expressão identificada como prioritária
        # pelo resultado dela
        exp_num = exp_num.replace(prox_exp, result)


def calc_exp(exp_num):
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

    print(f'\n<-- \033[1mExpressão inicial:\033[m {exp_num}')

    # Para cada conjunto, são eles: () [] {}
    for conjunto in conjuntos:
        quant_abre = exp_num.count(conjunto.get('abre'))
        quant_fecha = exp_num.count(conjunto.get('fecha'))

        # Verifica se há algum conjunto que não foi aberto ou fechado corretamente
        if quant_abre != quant_fecha:
            raise Exception('\nOperação inválida!')

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
                print(f'--- \033[1mExpressão prioritária:\033[m {exp_no_conjunto}', end=' = ')

                # Calcula o resultado da expressão
                try:
                    result = calc_exp_simples(exp_no_conjunto)
                except ZeroDivisionError as erro:
                    raise erro

                print(result)

                # Na expressão original substitui a expressão contida no conjunto
                # pelo resultado dela
                exp_num = exp_num.replace(exp_no_conjunto, str(result))

                print(f'--- \033[1mExpressão simplificada:\033[m {exp_num}')

    # Retorna a expressão numérica simplificada após ter calculado as expressões
    # de todos os conjuntos
    try:
        resultado_final = float(calc_exp_simples(exp_num))
        resultado_final = int(resultado_final) if resultado_final.is_integer() else resultado_final

        print(f'--> \033[1mResultado final:\033[m {resultado_final}')
        return resultado_final

    except ValueError:
        raise ValueError('\nOperação inválida!')

    except ZeroDivisionError as erro:
        raise erro
