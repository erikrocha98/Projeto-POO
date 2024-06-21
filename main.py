import pygame
import pickle
from pygame.locals import *
from player import Player
from world import World
from button import Button
from portal import Portal
from os import path
from audio import AudioManager
from score import ScoreManager

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

# Instanciando o gerenciador de áudio e score
audio_manager = AudioManager()
score_manager = ScoreManager()

# Font para exibir o score
font = pygame.font.Font('assets/game_font.ttf', 20)

# Utilitários para entrada de texto
base_font = pygame.font.Font('assets/game_font.ttf', 24)
user_text = ''
input_rect = pygame.Rect(screen_width // 2 - 90, screen_height // 2 - 2, 175, 45)
input_rect2 = pygame.Rect(screen_width // 2 - 92, screen_height // 2 - 5, 180, 50)
rect_color = (80, 80, 80)

active = False
nickname_entered = False
main_menu = True
show_high_scores_screen = False
game_over = 0
current_level = 1
final_level = 5  # Defina o nível final aqui
show_final_screen = False
level = 1

# Load images
bg_img = pygame.image.load('assets/background_start.png')
startbtn_img = pygame.image.load('assets/start.png')
exitbtn_img = pygame.image.load('assets/exit.png')
submitbtn_img = pygame.image.load('assets/submit.png')
music_on_img = pygame.image.load('assets/music_on.png')
music_off_img = pygame.image.load('assets/music_off.png')
restartbtn_img = pygame.image.load('assets/restart.png')
quitbtn_img = pygame.image.load('assets/quit.png')
recordesbtn_img = pygame.image.load('assets/recordes.png')
backbtn_img = pygame.image.load('assets/back.png')

audio_manager.play_music('assets/desafio.mp3') 

player = Player(100, screen_height - 130)

portal_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Função para carregar os dados do nível e criar o mundo
def load_level(level):
    level_path = f'level/level{level}_data'  # Atualiza o caminho para a pasta level
    if path.exists(level_path):
        with open(level_path, 'rb') as pickle_in:
            world_data = pickle.load(pickle_in)
        world = World(world_data, portal_group, coin_group)  # Passa portal_group para World
        portal_group.empty()
        portal_positions = world.get_portal_positions()
        for pos in portal_positions:
            new_portal = Portal(pos[0], pos[1])
            portal_group.add(new_portal)
        return world
    else:
        print(f"Level {level} data not found!")
        return None

# Carregando o nível inicial
world = load_level(current_level)

# Criação dos botões
start_button = Button(screen_width // 2 - 98, screen_height // 2 - 60, startbtn_img)
exit_button = Button(screen_width // 2 - 98, screen_height // 2, exitbtn_img)
submit_button = Button(screen_width // 2 - 20, screen_height // 2 + 50, submitbtn_img)
music_on_button = Button(screen_width // 2 + 350, screen_height // 2 + 280, music_on_img)
music_off_button = Button(screen_width // 2 + 350, screen_height // 2 + 320, music_off_img)
restart_button = Button(screen_width // 2 - 98, screen_height // 2, restartbtn_img)
quit_button = Button(screen_width // 2 - 98, screen_height // 2 - 60, quitbtn_img)
records_button = Button(screen_width // 2 - 98, screen_height // 2 + 60, recordesbtn_img)
back_button = Button(screen_width // 2 - 100, 480, backbtn_img)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

running = True
while running:
    clock.tick(fps)
    screen.blit(bg_img, (0, -25))
    top_scores = score_manager.get_top_scores(1)  # Obtém apenas o high score
    high_score = top_scores[0][1] if top_scores else 0
    name_score = top_scores[0][0] if top_scores else 0

    if main_menu:
        if not nickname_entered:
            if start_button.drawbutton():
                audio_manager.play_sound('button')  # Tocar som do botão
                nickname_entered = True
                current_level = 1  # Reinicia o nível para 1 ao iniciar um novo jogo
                world = load_level(current_level)  # Carrega o nível 1
                player.score = 0  # Reseta o score
                user_text = ''  # Limpa o nome do usuário
                player.rect.x = 100  # Posiciona o jogador no início da fase
                player.rect.y = screen_height - 130
            if exit_button.drawbutton():
                audio_manager.play_sound('button')
                running = False
            if records_button.drawbutton():
                audio_manager.play_sound('button')
                show_high_scores_screen = True
                main_menu = False
                
        else:
            pygame.draw.rect(screen, (200, 200, 200), input_rect, 0, 90)
            pygame.draw.rect(screen, rect_color, input_rect2, 5, 90)
            text_surface = font.render(user_text, True, (0, 0, 0))
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 5))
            draw_text(f'QUAL O SEU NOME?', font, (0,0,0), screen, 300, 360)

            if user_text and submit_button.drawbutton():
                nickname_entered = False
                audio_manager.play_sound('button')
                main_menu = False
                audio_manager.stop_music()
                audio_manager.play_music('assets/level1.mp3') 
                bg_img = pygame.image.load('assets/background.jpg')

    elif show_high_scores_screen:
        score_manager.draw_high_scores(screen, font, font, (255,255,255), (255,255,255), screen_width, screen_height)
        if back_button.drawbutton():
             audio_manager.play_sound('button')
             main_menu = True
             show_high_scores_screen = False

    elif show_final_screen:
        # Desenhar a tela final
        screen.fill((0, 0, 0))  # Preenche a tela com preto
        draw_text('Parabéns, você concluiu todos os desafios do jogo!!', font, (255, 255, 255), screen, 100, screen_height // 2 - 50)
        draw_text('E venceu essa batalha', font, (255, 255, 255), screen, 100, screen_height // 2)
        
        if back_button.drawbutton():
            audio_manager.play_sound('button')
            show_final_screen = False
            show_high_scores_screen = True
            main_menu = False

    else:
        world.update_enemies()
        nickname_entered = False

        # Desenhar os elementos do mundo diretamente no loop principal
        for tile in world.get_tile_list():
            screen.blit(tile[0], tile[1])
        
        portal_group.draw(screen)

        # Desenhar os inimigos (fantasmas e lava)
        world.ghost_group.draw(screen)
        world.lava_group.draw(screen)
        world.coin_group.draw(screen)

        game_over, player_score = player.update(screen, screen_height, world, game_over) # Passa 'world' como argumento para o método update()

        # Desenha o score na tela
        draw_text(f'Score: {player.score} ({user_text})', font, (255, 255, 255), screen, 45, 6)
        draw_text(f'High Score: {high_score}', font, (255, 255, 255), screen, 600, 6)

        for portal in portal_group:
            if player.rect.colliderect(portal.rect):
                if current_level < final_level:
                    current_level += 1
                    world = load_level(current_level)
                    player.rect.x = 100
                    player.rect.y = screen_height - 130  # Reseta a posição do jogador
                else:
                    # Nível final completado, exibe a tela final
                    show_final_screen = True
                    score_manager.add_score(user_text, player.score)
                    score_manager.save_scores()
                    game_over = 0
                    player = Player(100, screen_height - 130)  # Reseta o jogador
                    current_level = 1  # Reinicia o nível para 1 ao concluir o jogo
                    world = load_level(current_level)  # Carrega o nível 1
                    audio_manager.stop_music()
                    audio_manager.play_music('assets/desafio.mp3')
                    bg_img = pygame.image.load('assets/background_start.png')
                    break

        if game_over == -1:
            pygame.mixer.music.stop()

            if restart_button.drawbutton():
                audio_manager.play_sound('button')
                player = Player(100, screen_height - 130)  # Reseta o jogador
                world = load_level(current_level)  # Carrega o nível atual
                game_over = 0
                pygame.mixer.music.play(-1)

            elif quit_button.drawbutton():
                score_manager.add_score(user_text, player.score)
                score_manager.save_scores()                
                audio_manager.play_sound('button')  # Tocar som do botão ao clicar
                show_high_scores_screen = True  # Retorna para a tela inicial
                game_over = 0  # Reseta o estado de fim de jogo
                player = Player(100, screen_height - 130)  # Reseta o jogador
                world = load_level(level)  # Carrega novamente o nível inicial ou reset
                audio_manager.stop_music()
                audio_manager.play_music('assets/desafio.mp3')  # Toca a música da tela inicial
                bg_img = pygame.image.load('assets/background_start.png')  # Retorna a imagem de fundo inicial


        if music_on_button.drawbutton():
            audio_manager.toggle_music(True)
        if music_off_button.drawbutton():
            audio_manager.toggle_music(False)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                active = False
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    pygame.display.update()

pygame.quit()
