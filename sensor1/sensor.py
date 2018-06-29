## Simulador de dados.
## Reproduz situações reais nos dutos

import random
import math

''' O programa sensor é um meio que temos de simular os dados provenientes dos sensores de radiacao, ao qual nao temos recurso.
Ele utiliza um simples esquema de geração de valores de posicao e radiacao em funcao da coordenada de deslocamento transversal.
Como foi dito que nao tinhamos a possibilidade de ter um sensor e suas bibliotecas em maos, manipulamos os dados para que gerar situacoes
em que nossa solucao viria a agir.

segue abaixo as variveis utilizadas para o controle do programa

R = raio da tubulação
rad = radiação emitida pela particula
x = posição em x - deslocamento da particula em ralação a x
y = posição em y - deslocamento da particula em ralação a y
z = posição em z - deslocamento da particula em ralação a z
dx = variação do deslocamento em x
s = nome do arquivo - String
xv = quando dx varia - Boolean
rv = rad varia - Boolean
c = corrosão - Boolean
v = vazamento - Boolean
d = deslocamento condicional em x
r = raio condicional - lista
i = indeice da lista - int
r[i] = valor condiconal - float
'''
#Todas as operacoes matematicas a seguir visam a deixar as coordenadas que usaremos dentro das situacoes que estipulamos
def escreve(R, rad, x, dx, y, z, s, xv, rv, c, v): #Funcao que cria os arquivos .txt pra a futura plotagem e analise no programa principal
    f = open(s, "w")

    # Inicio das condicinais para a geracao de dados para cada situacao de comportamento do fluido no tubo
    while(x < 200):
        d = dx
        # situação onde muda velocidade do fluido. Causada por algum bloqueio no meio do trajeto
        if(xv and x >= 45 and x <= 150):
            d =dx*2.5

        # situação onde a radiacao é retida por substancias mais densas na mistura, paredes mais espessas devido a solidifacao do fluido,etc
        if(rv and x >= 40):
            rad = 0.5

        x += d

        # Situação onde há corrosão das paredes do tubo em determinado trajeto
        i=0
        if(c and x >= 40 and x <= 90):
            r=[0.3, 0.35, 0.45, 0.5, 0.5, 0.45, 0.35, 0.3]
            y = r[i]*math.cos(x)
            z = R*math.sin(x)
            i += 1
        else:
            # Situação onde há um vazamento de fluido por um orificio
            if(v and x >= 40 and x <= 70):
                z += 0.005
                y += 0.005
            else:
                z = R*math.sin(x)
                y = R*math.cos(x)

        st = "%.2f %.2f %.2f %.2f\n"
        f.write(st % (x, y, z, rad))
    f.close()
#Funcoes que chamam a funcao escreve com os paramentros de entrada especificados para a situcao descrita
'''@x_const: simula situaçõa fluido desloca-se normalmente'''
def x_const():
    escreve(0.25, 1.0, 0.0, 0.5, 0.0, 0.0, "dados1.txt", False, False, False, False)

'''@x_varia: O Simula radiacomponente dxo da particula sendo alterada'''
def x_varia():
    escreve(0.25, 1.0, 0.0, 0.5, 0.0, 0.0, "dados2.txt", True, False, False, False)

'''@rad_varia: Simula radiação da particula sendo alterada'''
def rad_varia():
    escreve(0.25, 1.0, 0.0, 0.5, 0.0, 0.0, "dados3.txt", False, True, False, False)

'''@corroi: Simula ubulação corroida'''
def corroi():
    escreve(0.25, 1.0, 0.0, 0.5, 0.0, 0.0, "dados4.txt", False, False, True, False)

'''@cvazamento: Simula tubulação rompida'''
def vazamento():
    escreve(0.25, 1.0, 0.0, 0.5, 0.0, 0.0, "dados5.txt", False, False, False, True)

'''Simula situação onde há torção no duto'''
def torce(R, rad, x, dx, y, z):
    f = open("dados6.txt", "w")

    # Inicio das condicinais para a geracao de dados para cada situacao de comportamento do fluido no tubo
    while(x < 200):
        d = dx

        x += d
        z = R*math.sin(x)
        y = R*math.cos(x)
        if(x >= 40):
             y-=1

        st = "%.2f %.2f %.2f %.2f\n"
        f.write(st % (x, y, z, rad))
    f.close()

## Chama as funções
x_const()
x_varia()
rad_varia()
corroi()
vazamento()
torce(0.25, 1.0, 0.0, 0.5, 0.0, 0.0)
