#Importando Bibliotecas
import pygame
import math
from sys import exit

# Inicializa o jogo
pygame.init()

# Define dimensões da janela 
LARGURA_JANELA = 1500
ALTURA_JANELA = 800
x_centro = LARGURA_JANELA / 2
y_centro = ALTURA_JANELA / 2

# Cria uma janela
janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("As leis de Kepler")
clock = pygame.time.Clock()

# Define cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (150,20,50)

# Define Constantes
UA = 1.496e11  # Unidade Astronômica em metros
ESCALA_DIST = 250 / UA  # 100 pixels = 1 UA
GM_Sol = 1.334e20
TEMPO_ESCALA = 24 * 3600

# Define fonte
FONTE = pygame.font.Font("font.ttf", 9)

##
## Classes
##
class Star():
    def __init__(self, x:float, y:float, GM:float, sprite:str):
        self.x = x  # Center of mass
        self.y = y  # Center of mass
        self.GM = GM
        self.image = pygame.transform.smoothscale(pygame.image.load(sprite), (30, 30))

    def renderStar(self): # Renderiza a imagem da propria estrela
        x_image = self.x - self.image.get_width() / 2
        y_image = self.y - self.image.get_height() / 2
        janela.blit(self.image, (x_image, y_image))
StandarStar = Star(x_centro, y_centro, GM_Sol, "imagens/sol2.png") # O nosso sol :)

class Planet():
    def __init__(self, nome_planeta:str, escala:tuple, a:float, b:float, e:float, dist:float = 0, star:Star = StandarStar):
        self.nome_planeta = nome_planeta  # Nome do Planeta
        self.escala = escala  # Escala tamanho da imagem do planeta
        self.a = a  # Semi eixo maior [m]
        self.b = b  # Semi eixo menor [m]
        self.e = e  # Excentricidade
        self.dist = dist
        self.star = star
        self.tick_planeta = 0

        self.c = self.e * self.a * ESCALA_DIST # Calcula distância do centro ao foco em escala
        self.vp = math.sqrt(GM_Sol*((1+self.e)/(self.a*(1-self.e)))) # Calcula velocidade no períelio
        self.rp = self.a*(1-self.e) # Calcula distância do planeta ao periélio

        self.x_planeta = x_centro + self.a * ESCALA_DIST
        self.y_planta = y_centro
        self.v = 0

        self.AREA_PERC = 0
        self.K = 10 # quantida de subdivisões da órbita [2ª lei]
        self.sec_A = (math.pi * self.a * self.b * (ESCALA_DIST)**2)/(self.K)
        self.pos = [[self.x_planeta,self.y_planta]]

        # Carrega a imagem do referido planeta ajustando sua escala para a desejada
        self.image = pygame.transform.smoothscale(
            pygame.image.load(f"imagens/{self.nome_planeta}.png"), 
            self.escala)

    def mov_circular(self, angulo:float) -> None:

        r = self.dist * ESCALA_DIST
        self.renderCircularOrbit(r)

        velocidade = math.sqrt(GM_Sol / r)
        omega = velocidade / r
        omega = omega / 10e6

        self.x_planeta = int(r * math.cos(math.radians(angulo * omega))) + x_centro
        self.y_planta = int(r * math.sin(math.radians(angulo * omega))) + y_centro
 
        dist = (self.a * (1 - (self.e) ** 2)) / (1 + self.e * math.cos(math.radians(angulo * omega)))
        dist_texto = FONTE.render(f"{round(dist / 1000, 1)} km", 1, BRANCO) # Renderiza a distância como texto
        janela.blit(dist_texto, (self.x_planeta - self.image.get_width() * 2, self.y_planta - self.image.get_height() * 2)) # Mostra as distâncias na tela, atualizando a cada laço

        self.renderLineStarPlanet(self.x_planeta,self.y_planta)
        self.renderPlanet()

    def mov_eliptico(self, angulo:float, esc:bool = False, line:bool = False, area:bool = False) -> None:

        a_esc = self.a * ESCALA_DIST
        b_esc = self.b * ESCALA_DIST
        
        self.renderEllipticalOrbit(a_esc,b_esc)

        r = (self.a*(1 - (self.e)**2)) / (1 + self.e*math.cos(math.radians(angulo)))
        self.v = math.sqrt(GM_Sol*((2/r)-(1/self.a))) # Calcula a velocidade para uma órbita elíptica
        self.v = 3600 * self.v # Coloca a velocidade em Km/h
        
        X = int(math.cos(math.radians(angulo)) * a_esc) + x_centro
        Y = int(math.sin(math.radians(angulo)) * b_esc) + y_centro
        
        if len(self.pos) < self.K:
            self.AREA_PERC += calcArea(self.x_planeta, self.y_planta, X, Y)
            if self.AREA_PERC >= self.sec_A:
                self.AREA_PERC = 0
                self.pos.append([self.x_planeta, self.y_planta])

        self.x_planeta = X
        self.y_planta = Y

        if area:
            self.renderLineArea()
        if esc:
            self.renderVelocity(angulo, a_esc, b_esc)
        if line:
            pygame.draw.line(janela, BRANCO, (self.star.x, self.star.y), (self.x_planeta, self.y_planta))
        self.renderPlanet()

        self.renderLineStarPlanet(self.x_planeta,self.y_planta)

    
    #
    # Renderizações
    #
    def renderPlanet(self) -> None: # Renderiza o proprio planeta
        x_image = self.x_planeta - self.image.get_width() / 2
        y_image = self.y_planta - self.image.get_height() / 2
        janela.blit(self.image, (x_image, y_image))

    def renderLineStarPlanet(self,x_planet,y_planet) -> None:
        pygame.draw.line(janela,BRANCO,(self.star.x,self.star.y),(x_planet,y_planet))
    
    def renderCircularOrbit(self, r:int) -> None: # Renderiza uma orbita circular de raio "r"
        pygame.draw.circle(janela, BRANCO, (x_centro,y_centro), r, 1)

    def renderEllipticalOrbit(self,a_esc:float,b_esc:float) -> None: # Renderiza uma órbita elíptica com semi-eixo maior = a_esc e semi-eixo menor = b_esc
        pygame.draw.ellipse(janela, BRANCO, (x_centro - a_esc, y_centro - b_esc, 2 * a_esc, 2 * b_esc), (1))

    def renderVelocity(self, angulo:float, a_esc:float, b_esc:float) -> None: # Renderiza o vetor velocidade com o valor em cima do planeta
        v_texto = FONTE.render(f"{round(self.v,1)} km/h", 1, BRANCO)
        janela.blit(v_texto, (self.x_planeta + self.image.get_width(), self.y_planta + self.image.get_height()))

        # Deriva as funções x e y
        dx_dtheta = int(-math.sin(math.radians(angulo)) * a_esc)
        dy_dtheta = int(math.cos(math.radians(angulo)) * b_esc)

        # Calcula os pontos iniciais do vetor velocidade
        vx = self.x_planeta + dx_dtheta
        vy = self.y_planta + dy_dtheta

        comprimento_v = (self.v/10**12) # Mede o comprimento da velocidade multiplicando v por uma escala = 10^6
        
        # Determina os pontos finais do vetor velocidade
        x_v_final = self.x_planeta + dx_dtheta * comprimento_v
        y_v_final = self.y_planta + dy_dtheta * comprimento_v

        pygame.draw.line(janela, VERMELHO, (vx, vy), (x_v_final, y_v_final), 2)

    def renderLineArea(self) -> None: # Renderiza todas as subdivisões da orbita segundo a 2ª lei
        for linha in self.pos:
                #print(self.K)
                #print(len(self.pos))
                pygame.draw.line(janela, (0,0,255),(self.star.x, self.star.y),(linha[0],linha[1]))
             
class Button():
	def __init__(self, imagem, pos, escala):
        
		self.imagem = pygame.transform.scale(imagem, (int(imagem.get_width()/2 * escala), int(imagem.get_height()/2 * escala)))
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		
		self.rect = self.imagem.get_rect(center=(self.x_pos, self.y_pos))

	def atualiza(self) -> None:
		
		if self.imagem is not None:
			
			janela.blit(self.imagem, self.rect)
			
	def checaEntrada(self, position) -> bool:
		
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		
		return False

##
## Funções
##
def calcArea(Xi,Yi,Xf,Yf) -> float:
    return abs(-Yi*Xf + Xi*Yf + Yi*x_centro - Yf*x_centro - Xi*y_centro + Xf*y_centro)/2

def get_font(tamanho):
    return pygame.font.Font("font.ttf", tamanho)

##
## Cenas
##
def PRIMEIRA_LEI():
    Sol = Star(x_centro+50, y_centro, GM_Sol, "imagens/sol2.png")
    Terra = Planet("terra", (20, 20), 1.2*UA, 0.9978 * UA, 0.555,1.00 * UA, Sol)

    theta = 0
    pygame.display.set_caption("Primeira Lei de Kepler - Lei das Órbitas")

    while True:
         
        clock.tick(60)
        janela.fill(PRETO)

        PRIM_MOUSE_POS = pygame.mouse.get_pos()

        BOTAO_VOLTAR = Button(imagem=pygame.image.load("botões/botaoSemEscrita.png"), pos= (1400,40), escala= 3)
        BOTAO_VOLTAR.atualiza()

        PERIELIO_TEXTO = get_font(30).render("Periélio", True, BRANCO)
        PERIELIO_RECT = PERIELIO_TEXTO.get_rect(center = (x_centro * 1.7, y_centro))
        
        AFELIO_TEXTO = get_font(30).render("Afélio", True, BRANCO)
        AFELIO_RECT = AFELIO_TEXTO.get_rect(center = (x_centro/3.4, y_centro))

        janela.blit(PERIELIO_TEXTO,PERIELIO_RECT)
        janela.blit(AFELIO_TEXTO,AFELIO_RECT)

        # Desenha o planeta
        Terra.mov_eliptico(theta,True)
        Sol.renderStar()
        
        theta += 1

        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                 
                if BOTAO_VOLTAR.checaEntrada(PRIM_MOUSE_POS):
                    
                    MENU_PRINCIPAL()
        
        pygame.display.update()

def SEGUNDA_LEI():
    Sol = Star(x_centro+50, y_centro, GM_Sol, "imagens/sol2.png")
    Terra = Planet("terra", (20, 20), 1.2*UA, 0.9978 * UA, 0.5555, 1.00 * UA, Sol)
    
    theta = 0
    pygame.display.set_caption("Segunda Lei de Kepler - Leis das Áreas")

    while True:

        janela.fill(PRETO)
        clock.tick(60)

        MOUSE_SEC_POS = pygame.mouse.get_pos()

        BOTAO_VOLTAR = Button(imagem=pygame.image.load("botões/botaoSemEscrita.png"), pos= (1400,40), escala= 3)
        BOTAO_VOLTAR.atualiza()

        # Desenha o planeta Marte descrevendo um movimento elíptico
        Terra.mov_eliptico(theta,False,True, True)
        Sol.renderStar()

        theta += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if BOTAO_VOLTAR.checaEntrada(MOUSE_SEC_POS):

                    MENU_PRINCIPAL()    
        
        pygame.display.update()

def TERCEIRA_LEI():

    Focus_Sun = 4.30 # Distância do sol (localizado no foco) ao centro
    Sol = Star(x_centro + Focus_Sun, y_centro, GM_Sol, "imagens/sol2.png")
    # Instanciando os planetas
    Mercurio = Planet("mercurio", (12, 12), 0.38700 * UA, 0.37870 * UA, 0.2056, 0.39 * UA, Sol)
    Venus = Planet("venus", (18, 18), 0.72300 * UA, 0.72298 * UA, 0.0067, 0.72 * UA, Sol)
    Terra = Planet("terra", (20, 20), UA, 0.9978 * UA, 0.0167, 1.00 * UA, Sol)
    Marte = Planet("marte", (16, 16), 1.52400 * UA, 1.51740 * UA, 0.0934, 1.52 * UA, Sol)

    theta = 0
    pygame.display.set_caption("Terceia Lei de Kepler - Lei Harmônica")

    while True:

        clock.tick(60)
        janela.fill(PRETO)

        TERC_MOUSE_POS = pygame.mouse.get_pos()
        
        BOTAO_VOLTAR = Button(imagem=pygame.image.load("botões/botaoSemEscrita.png"), pos= (1400,40), escala= 3)
        BOTAO_VOLTAR.atualiza()

        # Desenha os planetas descrevendo movimento circular
        Mercurio.mov_circular(theta)
        Venus.mov_circular(theta)
        Terra.mov_circular(theta)
        Marte.mov_circular(theta)

        Sol.renderStar()
        
        # Cálculo e exibição dos períodos
        Mercurio_periodo = round(math.sqrt((4 * math.pi ** 2 * Mercurio.dist ** 3) / GM_Sol), 2)
        Venus_periodo = round(math.sqrt((4 * math.pi ** 2 * Venus.dist ** 3) / GM_Sol), 2)
        Terra_periodo = round(math.sqrt((4 * math.pi ** 2 * Terra.dist ** 3) / GM_Sol), 2)
        Marte_periodo = round(math.sqrt((4 * math.pi ** 2 * Marte.dist ** 3) / GM_Sol), 2)

        Periodo_texto = FONTE.render(f"Período (Dias)", 1, BRANCO)
        Mercurio_periodo_texto = FONTE.render(f"Mercúrio: {Mercurio_periodo / TEMPO_ESCALA :.2f}", 1, BRANCO)
        Venus_periodo_texto = FONTE.render(f"Vênus: {Venus_periodo / TEMPO_ESCALA :.2f}", 1, BRANCO)
        Terra_periodo_texto = FONTE.render(f"Terra: {Terra_periodo / TEMPO_ESCALA :.2f}", 1, BRANCO)
        Marte_periodo_texto = FONTE.render(f"Marte: {Marte_periodo / TEMPO_ESCALA :.2f}", 1, BRANCO)

        janela.blit(Periodo_texto, (20,10))
        janela.blit(Mercurio_periodo_texto, (20, 30))
        janela.blit(Venus_periodo_texto, (20, 50))
        janela.blit(Terra_periodo_texto, (20, 70))
        janela.blit(Marte_periodo_texto, (20, 90))

        theta += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                 
                if BOTAO_VOLTAR.checaEntrada(TERC_MOUSE_POS):
                    
                    MENU_PRINCIPAL()
        
        pygame.display.update()  # Atualiza a tela a cada laço rodado

def MENU_PRINCIPAL():
    pygame.display.set_caption("As três leis de Kepler")
    while True:
	    
        janela.fill(PRETO)
        clock.tick(60)

        MOUSE_MENU_POS = pygame.mouse.get_pos()

        TEXTO_MENU = get_font(50).render("LEIS DE KEPLER", True, BRANCO)
        MENU_RECT = TEXTO_MENU.get_rect(center = (750,100))

        BOTAO_PRIMEIRA_LEI = Button(imagem=pygame.image.load("botões/leiDasOrbitas.png"), pos= (750,250), escala= 7)
        BOTAO_SEGUNDA_LEI = Button(imagem=pygame.image.load("botões/leiDasAreas.png"), pos= (750,400), escala= 7)
        BOTAO_TERCEIRA_LEI = Button(imagem=pygame.image.load("botões/leiHarmonica.png"), pos= (750,550), escala= 7)

        janela.blit(TEXTO_MENU, MENU_RECT)

        BOTAO_PRIMEIRA_LEI.atualiza()
        BOTAO_SEGUNDA_LEI.atualiza()
        BOTAO_TERCEIRA_LEI.atualiza()

        for event in pygame.event.get():
              
            if event.type == pygame.QUIT:
                    
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                  
                if BOTAO_PRIMEIRA_LEI.checaEntrada(MOUSE_MENU_POS):
                    PRIMEIRA_LEI()
                
                if BOTAO_SEGUNDA_LEI.checaEntrada(MOUSE_MENU_POS):
                    SEGUNDA_LEI()

                if BOTAO_TERCEIRA_LEI.checaEntrada(MOUSE_MENU_POS):
                    TERCEIRA_LEI()
            
        pygame.display.update()

## Main()
MENU_PRINCIPAL()
