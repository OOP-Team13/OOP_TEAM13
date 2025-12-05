import pygame
from player import *
from object import *

class MapManager:
    def __init__(self, window_W, window_H, player, ending_ui):
        self.window_W = window_W
        self.window_H = window_H
        self.duration = 20000


        self.items = []
        self.item_speed = 7
        self.player = player

        self.ending_ui = ending_ui

        # 이미지 로드
        self.images = {
            "main_building": self._load("image/main_building.png"),
            "library": self._load("image/library.png"),
            "student_hall": self._load("image/student_hall.png"),
            "bonus": self._load("image/bonus.png"),
            "liberal_arts_building": self._load("image/liberal_arts_building.png"),
            "classroom": self._load("image/classroom.png"),
            "retry": self._load("image/retry.png"),
            "dormitory": self._load("image/dormitory.png")
        }

        self.current_stage = "main_building"
        self.state = "playing"
        self.pending_ending_state = None 

        self.bonus_duration = 10000
        
        from ending import Ending
        self.ending_ui = Ending(window_W, window_H)
        
        # 초기 상태 설정
        self.state_object = MainBuildingState(self) 
        
        self.fade_alpha = 0
        self.is_fading = False

    def _load(self, img_path):
        return pygame.image.load(img_path).convert_alpha()

    def spawn_stage_items(self, stage_name, player):
        items = StageItem()
        self.items = items.create_items(30, self.item_speed, self.window_W, self.window_H, stage_name, player)

    # 상태 변경 시 current_stage 문자열도 변경됨
    def change_state(self, new_state_object):
        self.state_object = new_state_object
        self.current_stage = new_state_object.name 

    def trigger_fade_out(self, ending_key):
        self.pending_ending_state = ending_key
        self.is_fading = True
        self.fade_alpha = 0

    def update(self, player, paused_time):
        if self.is_fading or not self.is_playing:
            return 
        
        if player.hp <= 0:
            self.ending_ui.update_best_grade(player.grade)
            self.trigger_fade_out("ending_dorm")
            return
            
        if self.state == "playing":
            self.state_object.update(player, paused_time)

    def draw(self, screen, player):
        # 1. 페이드 중일 때
        if self.is_fading:
            # 페이드 중에는 현재 멈춘 화면(current_stage)을 그림
            screen.blit(self.images[self.current_stage], (0, 0))

            fade_surface = pygame.Surface((self.window_W, self.window_H))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0))

            if self.fade_alpha < 255:
                self.fade_alpha += 8
            else:
                self.is_fading = False
                # 실제 엔딩 상태로 전환
                if self.pending_ending_state:
                    self.state = self.pending_ending_state
                    self.pending_ending_state = None

        # 2. 게임 플레이 중일 때
        elif self.state == "playing":
            self.state_object.draw(screen)

        # 3. 엔딩 화면일 때
        elif self.state == "ending_retry":
            self.ending_ui.ending_retry(screen, player.grade)

        elif self.state == "ending_dorm":
            self.ending_ui.ending_dorm(screen, player.grade)

        elif self.state == "ending_classroom":
            self.ending_ui.ending_classroom(screen, player.grade)

    @property
    def is_playing(self):
        return self.state == "playing"

    @property
    def is_finished(self):
        return self.state != "playing"

class MapState:
    def __init__(self, game_map):
        self.game_map = game_map
        self.start_ticks = None
        self.name = "main_building"

        self.paused_time = 0
        self.pause_start_time = 0
        self.is_paused = False

    def update(self, player, paused_time):
        pass

    def draw(self, screen):
        screen.blit(self.game_map.images[self.name], (0, 0))

class MainBuildingState(MapState):
    def __init__(self, game_map):
        super().__init__(game_map)
        self.name = "main_building"
        self.start_ticks = None
        self.game_map.spawn_stage_items(self.name, self.game_map.player) 

    def update(self, player, paused_time):
        if self.start_ticks is None:
            self.start_ticks = pygame.time.get_ticks() - paused_time

        elapsed = pygame.time.get_ticks() - self.start_ticks - paused_time
        
        if elapsed >= self.game_map.duration:
            self.game_map.change_state(LibraryState(self.game_map))

class LibraryState(MapState):
    def __init__(self, game_map):
        super().__init__(game_map)
        self.name = "library"
        self.start_ticks = None
        self.game_map.spawn_stage_items(self.name, self.game_map.player) 

    def update(self, player, paused_time):
        if self.start_ticks is None:
            self.start_ticks = pygame.time.get_ticks() - paused_time

        elapsed = pygame.time.get_ticks() - self.start_ticks - paused_time

        if elapsed >= self.game_map.duration:
            self.game_map.change_state(StudentHallState(self.game_map))

class StudentHallState(MapState):
    def __init__(self, game_map):
        super().__init__(game_map)
        self.name = "student_hall"
        self.entered_bonus = False
        self.start_ticks = None
        self.game_map.spawn_stage_items(self.name, self.game_map.player) 

    def update(self, player, paused_time):
        if self.start_ticks is None:
            self.start_ticks = pygame.time.get_ticks() - paused_time

        elapsed = pygame.time.get_ticks() - self.start_ticks - paused_time

        if player.have_B and player.have_O_lib and player.have_O_stu and not self.entered_bonus:
            self.game_map.change_state(BonusState(self.game_map, elapsed))
            player.set_fly_mode()
            return

        if elapsed >= self.game_map.duration:
            player.set_boo_mode()
            self.game_map.change_state(LiberalArtsState(self.game_map))

class LiberalArtsState(MapState):
    def __init__(self, game_map):
        super().__init__(game_map)
        self.name = "liberal_arts_building"
        self.start_ticks = None 
        self.game_map.spawn_stage_items(self.name, self.game_map.player) 

    def update(self, player, paused_time):
        if self.start_ticks is None:
            self.start_ticks = pygame.time.get_ticks() - paused_time

        elapsed = pygame.time.get_ticks() - self.start_ticks - paused_time

        if elapsed >= self.game_map.duration:
            self.game_map.ending_ui.update_best_grade(player.grade)
            if player.grade <= 2.50:
                self.game_map.trigger_fade_out("ending_retry")
            else:
                self.game_map.trigger_fade_out("ending_classroom")

class BonusState(MapState):
    def __init__(self, game_map, previous_elapsed):
        super().__init__(game_map)
        self.name = "bonus"
        self.previous_elapsed = previous_elapsed
        self.start_ticks = None
        self.game_map.spawn_stage_items(self.name, self.game_map.player) 

    def update(self, player, paused_time):
        if self.start_ticks is None:
            self.start_ticks = pygame.time.get_ticks() - paused_time

        elapsed = pygame.time.get_ticks() - self.start_ticks - paused_time
        
        if elapsed >= self.game_map.bonus_duration:
             next_state = StudentHallState(self.game_map)
             next_state.entered_bonus = True
             
             self.game_map.change_state(next_state)

             player.set_boo_mode()