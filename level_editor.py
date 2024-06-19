import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Tamanho do tile e dimensões da tela
tile_size = 35
cols = 20
margin = 80
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Editor de Níveis')

# Carregamento de imagens
bg_img = pygame.image.load('assets/background.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('assets/ground_dirt.png')
grass_img = pygame.image.load('assets/ground2.png')
enemy_img = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
pygame.draw.rect(enemy_img, (255, 0, 0), enemy_img.get_rect())  # Quadrado vermelho
lava_img = pygame.image.load('assets/lava1.png')
portal_img = pygame.image.load('assets/portal.png')
save_img = pygame.image.load('assets/save_btn.png')
load_img = pygame.image.load('assets/load_btn.png')

# Definir variáveis do jogo
clicked = False
level = 1

# Criar lista de tiles vazia
world_data = []
for row in range(cols):
    r = [0] * cols
    world_data.append(r)

# Criar bordas
for tile in range(0, cols):
    world_data[cols - 1][tile] = 2
    world_data[0][tile] = 1
    world_data[tile][0] = 1
    world_data[tile][cols - 1] = 1

# Função para exibir texto na tela
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_grid():
    for c in range(cols + 1):
        # Linhas verticais
        pygame.draw.line(screen, (255, 255, 255), (c * tile_size, 0), (c * tile_size, screen_height - margin))
        # Linhas horizontais
        pygame.draw.line(screen, (255, 255, 255), (0, c * tile_size), (screen_width, c * tile_size))

def draw_world():
    for row in range(cols):
        for col in range(cols):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 3:
                    img = pygame.transform.scale(enemy_img, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                elif world_data[row][col] == 4:
                    img = pygame.transform.scale(portal_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
                elif world_data[row][col] == 6:
                    img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

# Criar botões de carregar e salvar
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

# Loop principal do jogo
running = True
while running:

    clock.tick(fps)

    screen.fill((144, 201, 120))
    screen.blit(bg_img, (0, 0))

    draw_grid()
    draw_world()

    draw_text(f'Nível: {level}', pygame.font.SysFont('Futura', 24), (255, 255, 255), tile_size, screen_height - 60)
    draw_text('Pressione UP ou DOWN para mudar de nível', pygame.font.SysFont('Futura', 24), (255, 255, 255), tile_size, screen_height - 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            if x < cols and y < cols:
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 6:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 6
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    if save_button.draw():
        with open(f'level{level}_data', 'wb') as pickle_out:
            pickle.dump(world_data, pickle_out)
    if load_button.draw():
        if path.exists(f'level{level}_data'):
            with open(f'level{level}_data', 'rb') as pickle_in:
                world_data = pickle.load(pickle_in)

    pygame.display.update()

pygame.quit()
