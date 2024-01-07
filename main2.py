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

surface = pygame.Surface((LARGURA_JANELA,ALTURA_JANELA), pygame.SRCALPHA)

# Definindo cores
PRETO = (0,0,0,)
BRANCO = (255,255,255)

# Constantes
Ms = 1.98847e30
G = 1.9853516e-29
GM = G*Ms
UA = 1.496e11
escala = 350

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
T = 0.1 # 1 ano
N = T/h

while True:

    clock.tick(120)
    janela.fill(PRETO)
    janela.blit(surface, (0,0))

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

    if len(orbita) > N:
        orbita.pop(0)

    for j in range(len(orbita)-1):
        pygame.draw.line(janela,BRANCO,
            (x_c + orbita[j][0]*escala, y_c + orbita[j][1]*escala),
            (x_c + orbita[j+1][0]*escala, y_c + orbita[j+1][1]*escala),2            
        )

    pygame.draw.circle(janela,BRANCO,(r[0]*escala + x_c,r[1]*escala + y_c),4)

    pygame.draw.circle(janela,BRANCO,(x_c,y_c),4)

    pygame.draw.line(janela,(255,255,255,0),(x_c,y_c),(r[0]*escala + x_c,r[1]*escala + y_c))

    pygame.display.update()

