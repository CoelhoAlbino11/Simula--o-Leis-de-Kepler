import pygame
import math

# Configurações da tela
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configurações do corpo orbital
a = 300  # Semi-eixo maior
b = 200  # Semi-eixo menor
periapsis_speed = 5  # Velocidade no periélio
min_distance = 1e-5  # Valor mínimo para a distância ao foco

# Cálculo da excentricidade
eccentricity = math.sqrt(1 - (b ** 2) / (a ** 2))

# Cálculo da distância do foco
focus_distance = a * eccentricity

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Função para calcular a posição do corpo na órbita elíptica
def calculate_orbit_position(angle):
    x = WIDTH // 2 + a * math.cos(angle)
    y = HEIGHT // 2 + b * math.sin(angle)
    return x, y

# Loop principal do jogo
def game_loop():
    angle = 0  # Ângulo inicial
    angle_increment = math.radians(0.5)  # Incremento angular

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLACK)

        # Calcula a posição do corpo na órbita
        x, y = calculate_orbit_position(angle)

        # Desenha a elipse
        pygame.draw.ellipse(screen, WHITE, (WIDTH // 2 - a, HEIGHT // 2 - b, 2 * a, 2 * b), 1)

        # Desenha o corpo
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), 10)

        # Calcula a distância do corpo ao foco
        distance_to_focus = math.sqrt((x - (WIDTH // 2 + focus_distance)) ** 2 + (y - HEIGHT // 2) ** 2)

        # Calcula a velocidade proporcional à distância
        if distance_to_focus > min_distance:
            if distance_to_focus < focus_distance:
                speed = periapsis_speed * (focus_distance / distance_to_focus)
            else:
                speed = periapsis_speed * (focus_distance / distance_to_focus)
        else:
            speed = periapsis_speed

        # Atualiza o ângulo para a próxima iteração
        angle += angle_increment * speed/2

        pygame.display.flip()
        clock.tick(FPS)

# Inicia o loop do jogo
game_loop()
