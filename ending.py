import pygame
from map import *
from player import *

class Ending:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font_title = pygame.font.Font("DNFBitBitTTF.ttf", 80)
        self.font_text = pygame.font.Font("DNFBitBitTTF.ttf", 40)
        self.font_btn = pygame.font.Font("DNFBitBitTTF.ttf", 20)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.image_dorm = pygame.image.load("image/dormitory.png")
        self.image_classroom = pygame.image.load("image/classroom.png")
        self.image_retry = pygame.image.load("image/Retry.png")

        btn_w, btn_h = 200, 60
        center_x = width // 2

        self.rect_restart = pygame.Rect(center_x-btn_w-20, height-150, btn_w, btn_h)
        self.rect_quit = pygame.Rect(center_x+20, height-150, btn_w, btn_h)
        
        #최고학점 기록
        try:
            with open("best_grade.txt", "r") as f:
                data = f.read().strip()
                if data:
                    self.best_grade = float(data)
                    
        except FileNotFoundError:
            self.best_grade = 0.0
            with open("best_grade.txt", "w") as f:
                f.write(str(self.best_grade))

    # 엔딩 진입할 때 최고 학점 갱신
    def update_best_grade(self, grade):
        if grade > self.best_grade:
            self.best_grade = grade

            with open("best_grade.txt", "w") as f:
                f.write(str(self.best_grade))

    # 최종 학점 + 최고 학점 표시
    def draw_final_grade(self, screen, grade):
        # 최종 학점
        txt = self.font_text.render(f"최종 학점: {grade:.2f}", True, self.WHITE)
        bg_rect = txt.get_rect(center=(self.width//2, self.height//2 + 50))
        pygame.draw.rect(screen, (0, 0, 0), bg_rect.inflate(20, 10))
        screen.blit(txt, bg_rect)

        # BEST 학점
        best = self.font_text.render(f"최고 학점: {self.best_grade:.2f}", True, self.WHITE)
        best_rect = best.get_rect(center=(self.width//2, self.height//2 + 110))
        pygame.draw.rect(screen, (0, 0, 0), best_rect.inflate(20, 10))
        screen.blit(best, best_rect)

    # 버튼 그리기
    def draw_buttons(self, screen):
        pygame.draw.rect(screen, self.WHITE, self.rect_restart)
        txt_restart = self.font_btn.render("다시 시작하기", True, self.BLACK)
        screen.blit(txt_restart, (self.rect_restart.centerx - txt_restart.get_width()//2, 
                                  self.rect_restart.centery - txt_restart.get_height()//2))
        
        pygame.draw.rect(screen, self.WHITE, self.rect_quit)
        txt_quit = self.font_btn.render("종료 하기", True, self.BLACK)
        screen.blit(txt_quit, (self.rect_quit.centerx - txt_quit.get_width()//2, 
                               self.rect_quit.centery - txt_quit.get_height()//2))
        
    def draw_common_layout(self, screen, image, grade, title_color, sub_color, title_text="", sub_text=""):
        screen.blit(image, (0, 0))

        if title_text:
            title = self.font_title.render(title_text, True, title_color)
            screen.blit(title, (self.width//2 - title.get_width()//2, 150))
        
        if sub_text:
            sub = self.font_title.render(sub_text, True, sub_color)
            screen.blit(sub, (self.width//2 - sub.get_width()//2, 220))

        self.draw_final_grade(screen, grade)
        self.draw_buttons(screen)

    def check_click(self, pos):
        if self.rect_restart.collidepoint(pos):
            return "restart"
        elif self.rect_quit.collidepoint(pos):
            return "quit"
        return None

    def ending_dorm(self, screen, grade):
        title_color = (255, 255, 255)
        sub_color = (255, 255, 255)
        self.draw_common_layout(screen, self.image_dorm, grade, title_color, sub_color)

    def ending_retry(self, screen, grade):
        title_color = (255, 0, 0)
        sub_color = (255, 0, 0)
        self.draw_common_layout(screen, self.image_retry, grade, title_color, sub_color, 
                                title_text="재수강 확정...", 
                                sub_text="BOO는 재수강을 해야합니다.")

    def ending_classroom(self, screen, grade):
        if grade == 4.50: text = "A+"
        elif grade >= 4.00: text = "A0"
        elif grade >= 3.50: text = "B+"
        elif grade >= 3.00: text = "B0"
        elif grade >= 2.50: text = "C+"
        elif grade >= 2.00: text = "C0"
        elif grade >= 1.50: text = "D+"
        elif grade >= 1.00: text = "D0"
        else: text = "F"

        msg = f"축하합니다. {text}학점을 받았습니다."

        title_color = (255, 255, 255)
        sub_color = (255, 255, 255)
        self.draw_common_layout(screen, self.image_classroom, grade, title_color, sub_color, title_text=msg)