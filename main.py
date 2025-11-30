import pygame
import sys
from pygame.locals import *
from collide import *
from player import *
from object import *
from map import *
from ending import *
from sound import SoundManager
from ui import UI

# 기본 설정
window_W = 1200
window_H = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((window_W, window_H))
pygame.display.set_caption("학교 가BOO자고!")
clock = pygame.time.Clock()

# 사운드 초기화 및 로드
sound = SoundManager()
sound.play_bgm()

FONT = pygame.font.Font("DNFBitBitTTF.ttf", 30)
FONT_TITLE = pygame.font.Font("DNFBitBitTTF.ttf", 100)

# 바닥 높이
ground = window_H - 140 -50

#player 객체 생성
player = Player(100, ground, window_W, ground)

# 배경 이미지 로드
map = Map(window_W, window_H)
menu = pygame.image.load("image/menu.png").convert_alpha()
explain = pygame.image.load("image/explain.png").convert_alpha()

# 아이템 생성
map.spawn_stage_items("main_building", player)

# UI 생성
game_ui = UI(window_W, window_H)
is_paused = False

# 시작 버튼
btn_explain = pygame.Rect(280, 460, 150, 60)
btn_start = pygame.Rect(770, 460, 150, 60)
btn_explain_to_start = pygame.Rect(900, 500, 180, 50)

def draw_button(rect, text):
    pygame.draw.rect(screen, (255, 255, 255), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 3)
    txt = FONT.render(text, True, (0, 0, 0))
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

# 현재 화면 상태
game_state = "menu"

# 메인 루프
running = True
while running:
    # ================= 이벤트 처리 =================
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # UI
        action = game_ui.handle_event(event, is_paused)
        if action == "toggle_sound":
            sound.toggle_bgm()

        elif action == "toggle_pause":
            is_paused = not is_paused

        elif action == "btn_resume":
            is_paused = False
        
        elif action == "btn_quit":
            running = False
        
        elif action == "btn_restart":
            is_paused = False
            player.reset()
            player.set_boo_mode()
            map.reset()

            map.spawn_stage_items("main_building", player)

            sound.play_bgm()

            game_state = "playing"

        # 키보드 입력
        elif event.type == KEYDOWN:
            if game_state == "playing" and map.is_playing:
                if event.key == pygame.K_SPACE:
                    player.jump()
                    sound.play_jump()

         # 마우스 클릭 입력 (버튼 클릭)
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos

            # 메인 화면
            if game_state == "menu":

                if btn_explain.collidepoint(mx, my):
                    game_state = "explain"

                elif btn_start.collidepoint(mx, my):
                    game_state = "playing"
                    map.reset()

            # 게임설명 화면
            elif game_state == "explain":
                if btn_explain_to_start.collidepoint(mx, my):
                    game_state = "playing"
                    map.reset()

             # 엔딩 화면
            elif game_state == "playing" and not map.is_playing:
                action = map.ending_ui.check_click(event.pos)

                if action == "quit":
                    running = False
                
                elif action == "restart":
                    player.reset()
                    player.set_boo_mode()
                    map.reset()
                    sound.play_bgm()
                    
                    # 아이템 새로 생성
                    map.spawn_stage_items("main_building", player)

                    # 플레이 상태로 전환
                    game_state = "playing"

      # 화면 그리기 
    if game_state == "menu":
        screen.blit(menu, (0, 0))
        draw_button(btn_explain, "게임설명")
        draw_button(btn_start, "게임시작")

    elif game_state == "explain":
        screen.blit(explain, (0, 0))
        draw_button(btn_explain_to_start, "게임시작")

    elif game_state == "playing":

        #일시정지가 아닐 때
        if not is_paused:
            # 1) 맵 업데이트 (GPA/HP 조건 판단 포함)
            map.update(player)

            if not map.is_playing:
                sound.stop_bgm()

            # 2) 진행 중인 경우에만 플레이어 동작 가능
            if map.is_playing:
                keys = pygame.key.get_pressed()
                player.handle_input(keys)
                player.update()

                # 3) 아이템 이동 업데이트
                for item in map.items:
                    item.update(map.item_speed)
                    item.draw(screen)

                # 4) 아이템/장애물 충돌 확인
                check_collision(player, map.items, sound)

        map.draw(screen, player)

        if map.is_playing:
            player.draw(screen)

            for item in map.items:
                item.draw(screen)

        # 게임 중일 때만 ui 적용됨
        if game_state == "playing" and map.is_playing:
            game_ui.draw(screen, player, is_paused, sound)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()  