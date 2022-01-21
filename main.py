from expnum import calc_exp
from tkinter import *
from functools import partial


def digitar(e):
    visor['text'] = visor['text'] + str(e)


def limpar_visor():
    visor['text'] = ''


janela = Tk()
janela.title('Calculadora')

visor = Label(master=janela, width=40, height=3, bg='black', fg='white')
visor.pack()

botoes_frame = Frame(master=janela, width=100, height=100)
botoes_frame.pack()
botoes_frame.config(pady=30, padx=15)

cont = 1
for i in range(1, 4):
    for j in range(0, 3):
        botao = Button(botoes_frame, text=f'{cont}', font=16, command=partial(digitar, cont))
        botao.grid(row=i, column=j, padx=5, pady=8)
        botao.config(width=5, height=2)
        cont = cont + 1

operacoes = ['+', '-', '*', '/']
for i, operador in enumerate(operacoes):
    botao_op = Button(botoes_frame, text=operador, font=16, command=partial(digitar, f' {operador} '))
    botao_op.grid(row=i + 1, column=4, padx=5, pady=8)
    botao_op.config(width=6, height=2)


botao_virgl = Button(botoes_frame, text=',', font=16, command=partial(digitar, ','))
botao_virgl.grid(row=4, column=2, padx=5, pady=8)
botao_virgl.config(width=6, height=2)

botao_zero = Button(botoes_frame, text='0', font=16, command=partial(digitar, '0'))
botao_zero.grid(row=4, column=1, padx=5, pady=8)
botao_zero.config(width=6, height=2)

botao_limpar = Button(botoes_frame, text='C', font=16, command=limpar_visor)
botao_limpar.grid(row=4, column=0, padx=5, pady=8)
botao_limpar.config(width=6, height=2)

botao_result = Button(botoes_frame, text='=', font=16, command=f' = ')
botao_result.grid(row=5, column=4, padx=5, pady=8)
botao_result.config(width=6, height=2)

janela.mainloop()

# expressao_numerica = '-8 + ((- 20 / 5) * 16)'
# print(f'\nResultado da expressão: {calc_exp(expressao_numerica)}')
