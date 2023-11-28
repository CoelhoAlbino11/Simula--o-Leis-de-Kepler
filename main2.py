# Importando bibliotecas
import pygame
import numpy as np
from sys import exit

# Inicializa o game
pygame.init()

# Define dimensões da janela 
LARGURA_JANELA = 1500
ALTURA_JANELA = 800
x_c = LARGURA_JANELA / 2
y_c = ALTURA_JANELA / 2

# Cria uma janela
janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
clock = pygame.time.Clock() # Define um tick

# Definindo cores
PRETO = (0,0,0,)
BRANCO = (255,255,255)

# Constantes
Ms = 1.98847e30
G = 1.9853516e-29
GM = G*Ms
UA = 1.496e11

def f(r):
    
    x,y,vx,vy = r

    R = np.sqrt(x**2 + y**2)

    dx = vx
    dy = vy
    fvx = -GM*x/(R**3)
    fvy = -GM*y/(R**3)

    return np.array([dx,dy,fvx,fvy])

h = 1/1000
r = [1,0,0,-1*np.pi]
orbita = []

while True:

    clock.tick(120)
    janela.fill(PRETO)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            exit()

    k1 = h * f(r)
    k2 = h * f(r + k1/2)
    k3 = h * f(r + k2/2)
    k4 = h * f(r + k3)

    r = r + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
    orbita.append(r)

    for j in range(len(orbita)-1):
        pygame.draw.line(janela,BRANCO,
            (x_c + orbita[j][0]*250, y_c + orbita[j][1]*250),
            (x_c + orbita[j+1][0]*250, y_c + orbita[j+1][1]*250),2            
        )

    pygame.draw.circle(janela,BRANCO,(r[0]*250 + x_c,r[1]*250 + y_c),4)

    pygame.draw.circle(janela,BRANCO,(x_c,y_c),4)

    pygame.draw.line(janela,BRANCO,(x_c,y_c),(r[0]*250 + x_c,r[1]*250 + y_c))

    pygame.display.update()

