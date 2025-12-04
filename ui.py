import pygame
from player import *
from sound import *

class UI:
    def __init__(self, screen_width, screen_height):
        self.font = pygame.font.Font("DNFBitBitTTF.ttf", 30)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (200, 200, 200)

        self.hp_full_img = pygame.image.load("image/hp.png").convert_alpha()
        self.hp_empty_img = pygame.image.load("image/lose_hp.png").convert_alpha()

        self.pause_btn_rect = pygame.Rect(screen_width - 70, 20, 50, 50)
        self.sound_btn_rect = pygame.Rect(screen_width - 130, 20, 50, 50)

        self.item_start_x = screen_width - 130

        self.sound_on_img = pygame.image.load("image/sound_on.png").convert_alpha()
        self.sound_off_img = pygame.image.load("image/sound_off.png").convert_alpha()
        self.round = 10  # 버튼 둥글기 정도


        #일시정지 관련
        #self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.pause_font = pygame.font.Font("DNFBitBitTTF.ttf", 60)

        center_x = screen_width // 2
        center_y = screen_height // 2
        btn_w, btn_h = 200, 60

        self.btn_resume = pygame.Rect(center_x - btn_w//2, center_y - 60, btn_w, btn_h)
        self.btn_restart = pygame.Rect(center_x - btn_w//2, center_y + 20, btn_w, btn_h)
        self.btn_quit = pygame.Rect(center_x - btn_w//2, center_y + 100, btn_w, btn_h) 

    def draw(self, screen, player, is_paused, sound):
        self._draw_status(screen, player)
        self._draw_bonus(screen, player)
        self._draw_buttons(screen, is_paused, sound)

        if is_paused:
            self._draw_pause_screen(screen)
        
    def _draw_status(self, screen, player):
        screen.blit(self.font.render("HP", True, self.black), (20, 20))
        for i in range(3):
            img = self.hp_full_img if player.hp >= (i+1) else self.hp_empty_img
            screen.blit(img, (80+(i*60), 7))
        
        grade_text = f"학점: {player.grade:.2f}"
        grade_surt = self.font.render(grade_text, True, self.black)
        screen.blit(grade_surt, (20, 80))

    def _draw_bonus(self, screen, player):
        y = 20
        spacing = 50

        x_o_stu = self.item_start_x - spacing
        x_o_lib = x_o_stu - spacing
        x_b = x_o_lib - spacing

        if player.have_B:
            B = pygame.image.load("image/b.png").convert_alpha()
            screen.blit(B, (x_b, y))
        
        if player.have_O_lib:
            O_lib = pygame.image.load("image/o_library.png").convert_alpha()
            screen.blit(O_lib, (x_o_lib, y))

        if player.have_O_stu:
            O_stu = pygame.image.load("image/o_student_hall.png").convert_alpha()
            screen.blit(O_stu, (x_o_stu, y))
    
    def _draw_buttons(self, screen, is_paused, sound):
        # ---- 사운드 버튼 (둥근 UI) ----
        pygame.draw.rect(screen, (255,255,255), self.sound_btn_rect, border_radius=self.round)
        pygame.draw.rect(screen, self.black, self.sound_btn_rect, 3, border_radius=self.round)

        # 사운드 아이콘
        icon = self.sound_on_img if sound.bgm_on else self.sound_off_img
        icon_rect = icon.get_rect(center=self.sound_btn_rect.center)
        screen.blit(icon, icon_rect)

        # ---- 일시정지 버튼 (둥근 UI) ----
        pause_color = (255, 0, 0) if is_paused else (255, 255, 255)
        pygame.draw.rect(screen, pause_color, self.pause_btn_rect, border_radius=self.round)
        pygame.draw.rect(screen, self.black, self.pause_btn_rect, 3, border_radius=self.round)

        symbol = "▶" if is_paused else "||"
        text_p = self.font.render(symbol, True, (0, 0, 0))
        text_p_rect = text_p.get_rect(center=self.pause_btn_rect.center)
        screen.blit(text_p, text_p_rect)

    
    def _draw_pause_screen(self, screen):
        dark_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 150))
        screen.blit(dark_overlay, (0, 0))

        title_surf = self.pause_font.render("일시정지 되었습니다", True, self.white)
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        title_rect = title_surf.get_rect(center=(center_x, center_y - 150))
        screen.blit(title_surf, title_rect)

        self._draw_centered_btn(screen, self.btn_resume, "계속하기")
        self._draw_centered_btn(screen, self.btn_restart, "다시 시작하기")
        self._draw_centered_btn(screen, self.btn_quit, "종료하기")

    def _draw_centered_btn(self, screen, rect, text):
        color = (255, 255, 255)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, self.black, rect, 3)

        text_surf = self.font.render(text, True, self.black)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event, is_paused):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if is_paused:
                if self.btn_resume.collidepoint(mouse_pos):
                    return "btn_resume"
                if self.btn_restart.collidepoint(mouse_pos):
                    return "btn_restart"
                if self.btn_quit.collidepoint(mouse_pos):
                    return "btn_quit"

            if self.sound_btn_rect.collidepoint(mouse_pos):
                return "toggle_sound"
            
            if self.pause_btn_rect.collidepoint(mouse_pos):
                return "toggle_pause"
            
        return None