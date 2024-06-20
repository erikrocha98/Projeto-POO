import pygame
import pickle
from pygame.locals import *
from player import Player
from world import World
from button import Button
from portal import Portal
from os import path
from coin import Coin
from audio import AudioManager  # Importar a classe AudioManager

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

# Instanciando o gerenciador de áudio e score
audio_manager = AudioManager()

# Mais inicializações...
base_font = pygame.font.Font(None, 30)
user_text = ''
input_rect = pygame.Rect(screen_width // 2 - 90, screen_height // 2 - 2, 175, 45)
input_rect2 = pygame.Rect(screen_width // 2 - 92, screen_height // 2 - 5, 180, 50)
rect_color = (80, 80, 80)

active = False
nickname_entered = False
main_menu = True
game_over = 0
level = 1

# load images...
bg_img = pygame.image.load('assets/background_start.png')
startbtn_img = pygame.image.load('assets/start.png')
exitbtn_img = pygame.image.load('assets/exit.png')
submitbtn_img = pygame.image.load('assets/submit.png')
music_on_img = pygame.image.load('assets/music_on.png')
music_off_img = pygame.image.load('assets/music_off.png')
restartbtn_img = pygame.image.load('assets/restart.png')

# load sounds removido, gerenciado por AudioManager
audio_manager.play_music('assets/desafio.mp3')  # Iniciar a música de fundo

player = Player(100, screen_height - 130)

portal_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

def load_level(level):
    if path.exists(f'level{level}_data'):
        with open(f'level{level}_data', 'rb') as pickle_in:
            world_data = pickle.load(pickle_in)
        world = World(world_data, portal_group)  # Passa portal_group para World
        portal_group.empty()
        portal_positions = world.get_portal_positions()
        for pos in portal_positions:
            new_portal = Portal(pos[0], pos[1])
            portal_group.add(new_portal)
        return world
    else:
        print("No more levels!")
        return None

# Carregando o nível inicial
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = load_level(level)

start_button = Button(screen_width // 2 - 98, screen_height // 2 - 5, startbtn_img)
exit_button = Button(screen_width // 2 - 98, screen_height // 2 + 55, exitbtn_img)
submit_button = Button(screen_width // 2 - 20, screen_height // 2 + 50, submitbtn_img)
music_on_button = Button(screen_width // 2 + 362, screen_height // 2 + 280, music_on_img)
music_off_button = Button(screen_width // 2 + 362, screen_height // 2 + 320, music_off_img)
restart_button = Button(screen_width // 2 - 98, screen_height // 2, restartbtn_img)

running = True
while running:
    clock.tick(fps)
    screen.blit(bg_img, (0, -25))

    if main_menu:
        if not nickname_entered:
            if start_button.drawbutton():
                audio_manager.play_sound('button')  # Tocar som do botão
                nickname_entered = True
            if exit_button.drawbutton():
                audio_manager.play_sound('button')
                running = False
        else:
            pygame.draw.rect(screen, (200, 200, 200), input_rect, 0, 90)
            pygame.draw.rect(screen, rect_color, input_rect2, 5, 90)
            text_surface = base_font.render(user_text, True, (0, 0, 0))
            screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 12))

            if user_text and submit_button.drawbutton():
                audio_manager.play_sound('button')
                main_menu = False
                audio_manager.stop_music()
                audio_manager.play_music('assets/level1.mp3')  # Muda a música para o nível 1
                bg_img = pygame.image.load('assets/background.jpg')

    else:
        world.update_enemies()
        
        # Desenhar os elementos do mundo diretamente no loop principal
        for tile in world.get_tile_list():
            screen.blit(tile[0], tile[1])
        
        portal_group.draw(screen)

        # Desenhar os inimigos (fantasmas e lava)
        world.ghost_group.draw(screen)
        world.lava_group.draw(screen)
        world.coin_group.draw(screen)

        game_over = player.update(screen, screen_height, world, game_over)  # Passa 'world' como argumento para o método update()

        for portal in portal_group:
            if player.rect.colliderect(portal.rect):
                level += 1
                new_world = load_level(level)
                if new_world:
                    world = new_world
                    player = Player(100, screen_height - 130)  # Reseta o jogador para a posição inicial
                else:
                    running = False

        if game_over == -1:
            pygame.mixer.music.stop()
            if restart_button.drawbutton():
                audio_manager.play_sound('button')
                player = Player(100, screen_height - 130)  # Reseta o jogador
                world = load_level(level)  # Reseta o mundo
                game_over = 0
                pygame.mixer.music.play(-1)
            else:
                game_over_text = base_font.render('Game Over', True, (255, 0, 0))
                screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 20))

    if music_on_button.drawbutton():
        audio_manager.play_sound('button')
        pygame.mixer.music.play(-1)  # Supondo que level1.mp3 é sua música de nível
    if music_off_button.drawbutton():
        audio_manager.play_sound('button')
        audio_manager.stop_music()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
                rect_color = (56, 56, 56)
            else:
                active = False
                rect_color = (70, 110, 119)

        if event.type == pygame.KEYDOWN:
            if active and nickname_entered:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if base_font.size(user_text + event.unicode)[0] < input_rect.width - 20:
                        user_text += event.unicode

    pygame.display.update()

pygame.quit()
