import pygame

class SoundManager:
    def __init__(self):
        # 믹서 초기화 (효과음 재생을 위해 필수!)
        pygame.mixer.init()

        # BGM 상태
        self.bgm_on = True
        
        # ===== BGM 로드 =====
        try:
            pygame.mixer.music.load("sound/bgm.mp3")
            pygame.mixer.music.set_volume(0.5)
        except:
            print("BGM 파일(bgm.mp3)을 찾을 수 없습니다.")

        # ===== 효과음 로드 =====
        try:
            self.jump_sound = pygame.mixer.Sound("sound/jump.wav")
            self.jump_sound.set_volume(0.7)
        except:
            print("jump.wav 파일을 찾을 수 없습니다.")

        try:
            self.item_sound = pygame.mixer.Sound("sound/coin.wav")
            self.item_sound.set_volume(0.7)
        except:
            print("item.wav 파일을 찾을 수 없습니다.")

    def play_bgm(self):
        if self.bgm_on:
            pygame.mixer.music.play(-1)

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def play_jump(self):
        try:
            self.jump_sound.play()
        except:
            pass

    def play_item(self):
        try:
            self.item_sound.play()
        except:
            pass

    def quit(self):
        pygame.mixer.stop()
        pygame.mixer.quit()

    #bgm on&off
    def toggle_bgm(self):
        self.bgm_on = not self.bgm_on

        if self.bgm_on:
            pygame.mixer.music.unpause()

            if not pygame.mixer.music.get_busy():
                self.play_bgm()
        else:
            pygame.mixer.music.pause()