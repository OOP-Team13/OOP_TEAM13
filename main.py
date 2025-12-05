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
ground = window_H - 140 - 50

# player 객체 생성
player = Player(100, ground, window_W, ground)

# 배경 이미지 로드
ending_ui = Ending(window_W, window_H)
map = MapManager(window_W, window_H, player, ending_ui)
game_ui = UI(window_W, window_H)
menu = pygame.image.load("image/menu.png").convert_alpha()
explain = pygame.image.load("image/explain.png").convert_alpha()

# 일시정지 관련
start_ticks = pygame.time.get_ticks()
total_paused_time = 0
pause_start = 0
is_paused = False

game_state = "menu" # menu, explain, playing

# 버튼 Rect 정의
btn_explain = pygame.Rect(280, 460, 150, 60)
btn_start = pygame.Rect(770, 460, 150, 60)
btn_explain_to_start = pygame.Rect(900, 500, 180, 50)

# 버튼 그리기 헬퍼 함수
def draw_button(rect, text):
    pygame.draw.rect(screen, (255, 255, 255), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 3)
    txt = FONT.render(text, True, (0, 0, 0))
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

def restart_game():
    global player, map, game_state, is_paused

    player.reset()
    player.set_boo_mode()

    map = MapManager(window_W, window_H, player, ending_ui)

    sound.play_bgm()
    is_paused = False
    game_state = "playing"

# 메인 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # UI 처리
        action = game_ui.handle_event(event, is_paused)

        if action == "toggle_sound":
            sound.toggle_bgm()

        elif action == "toggle_pause":
            if not is_paused:
                is_paused = True
                pause_start = pygame.time.get_ticks()
            else:
                is_paused = False
                total_paused_time += (pygame.time.get_ticks() - pause_start)

        elif action == "btn_resume":
            is_paused = False
        
        elif action == "btn_quit":
            running = False
        
        elif action == "btn_restart":
            restart_game()

        # 키보드 입력 처리
        elif event.type == KEYDOWN:
            if game_state == "playing" and map.is_playing:
                if event.key == pygame.K_SPACE:
                    player.jump()
                    sound.play_jump()

        # 마우스 클릭 입력 (버튼 클릭)
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos

            if game_state == "menu":
                if btn_explain.collidepoint(mx, my):
                    game_state = "explain"
                elif btn_start.collidepoint(mx, my):
                    restart_game()

            elif game_state == "explain":
                if btn_explain_to_start.collidepoint(mx, my):
                    restart_game()

            elif game_state == "playing" and not map.is_playing:
                action = ending_ui.check_click(event.pos)

                if action == "quit":
                    running = False
                elif action == "restart":
                    restart_game()

    # ================= 화면 그리기 =================

    if game_state == "menu":
        screen.blit(menu, (0, 0))
        draw_button(btn_explain, "게임설명")
        draw_button(btn_start, "게임시작")

    elif game_state == "explain":
        screen.blit(explain, (0, 0))
        draw_button(btn_explain_to_start, "게임시작")

    elif game_state == "playing":

        if map.is_fading:
            map.draw(screen, player)
            pygame.display.update()
            clock.tick(FPS)
            continue

        # 일시정지가 아닐 때 정상 진행
        if not is_paused:
            map.update(player, total_paused_time)

            if map.is_playing:
                # 플레이어 움직임
                keys = pygame.key.get_pressed()
                player.handle_input(keys)
                player.update()
                
                # 아이템 움직임 (맵에 있는 리스트를 순회)
                for item in map.items:
                    item.update(map.item_speed)
                
                # 충돌 체크 (collide.py) - item.use()가 내부에서 실행됨
                check_collision(player, map.items, sound)
            
            else:
                # 게임이 끝났으면(엔딩화면) BGM 끄기
                sound.stop_bgm()

        map.draw(screen, player)

        # 플레이 중이면 캐릭터 & 아이템 표시
        if map.is_playing:
            player.draw(screen)
            for item in map.items:
                item.draw(screen)
            game_ui.draw(screen, player, is_paused, sound)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()