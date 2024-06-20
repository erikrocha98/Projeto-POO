import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music_path = None
        self.music_paused = False
        self.sounds = {
            'button': pygame.mixer.Sound('assets/botao.wav'),
            'enemy': pygame.mixer.Sound('assets/enemy.ogg'),
            'lava': pygame.mixer.Sound('assets/lava.ogg'),
            'coin': pygame.mixer.Sound('assets/coin.ogg')
        }
        self.music_volume = 0.5
        pygame.mixer.music.set_volume(self.music_volume)

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_music(self, music_path, volume=0.2):
        if self.current_music_path != music_path:
            pygame.mixer.music.load(music_path)
            self.current_music_path = music_path
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_paused = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.music_paused = True

    def continue_music(self):
        if self.music_paused:
            pygame.mixer.music.play(-1)
            self.music_paused = False
