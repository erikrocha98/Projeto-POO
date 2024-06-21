import os
import pygame

class ScoreManager:
    def __init__(self, filename='high_scores.txt'):
        self.filename = filename
        self.scores = self.load_scores()

    def add_score(self, name, score):
        print(f"Adding score: {name}, {score}")
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)  # Ordena por pontuação, maior primeiro

    def save_scores(self):
        with open(self.filename, 'w') as file:
            for name, score in self.scores:
                file.write(f"{name},{score}\n")

    def load_scores(self):
        scores = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    name, score = line.strip().split(',')
                    scores.append((name, int(score)))
        return scores

    def get_top_scores(self, n=3):
        return self.scores[:n]
    
    def draw_high_scores(self, screen, font, header_font, text_color, header_color, screen_width, screen_height):
        # Configurações para o retângulo translúcido
        background_alpha = 128  # Define a transparência (0=transparente, 255=opaco)
        background_color = (70, 110, 119) 

        start_y = 380
        name_x = 300
        score_x = screen_width - 300

        # Calcula a altura e a largura do retângulo baseado no número de scores e no tamanho da fonte
        rect_height = 40 * len(self.get_top_scores(3)) + 95  # Altura dependente do número de linhas
        rect_width = 660  # Largura arbitrária
        rect_x = 70  # Posição X do retângulo
        rect_y = start_y - 76  # Posição Y do retângulo

        # Cria uma superfície para o retângulo
        rect_surface = pygame.Surface((rect_width, rect_height))
        rect_surface.set_alpha(background_alpha)  # Define a transparência
        rect_surface.fill(background_color)  # Preenche com a cor
        screen.blit(rect_surface, (rect_x, rect_y))  # Desenha a superfície no screen

        header_text = header_font.render('HIGH SCORES', True, header_color)
        header_rect = header_text.get_rect(center=(screen_width / 2, 350))
        screen.blit(header_text, header_rect)


        for name, score in self.get_top_scores(3):  # Busca os top 3 scores
            # Renderiza o nome
            name_text = font.render(name, True, text_color)
            name_rect = name_text.get_rect(topleft=(name_x, start_y))
            screen.blit(name_text, name_rect)

            # Renderiza o score
            score_text = font.render(str(score), True, text_color)
            score_rect = score_text.get_rect(topright=(score_x, start_y))
            screen.blit(score_text, score_rect)

            start_y += 30
