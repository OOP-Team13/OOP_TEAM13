import pygame

class Player:
    def __init__(self, x, y, screen_width, ground_level):
        # 기본 이미지 로드
        self.image_boo = pygame.image.load("image/boo.png").convert_alpha()
        self.image_boo = pygame.transform.scale(self.image_boo, (100, 144))
        self.image_fly = pygame.image.load("image/fly_boo.png").convert_alpha()

        self.image = self.image_boo

        # 이미지 크기
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = self.rect.width
        self.height = self.rect.height

        # 시작 위치
        self.start_x = x
        self.start_y = y

        # 이동 가능한 범위 (화면 절반까지만)
        self.left_limit = 20
        self.right_limit = screen_width // 2 - self.width - 20

        # 바닥 Y좌표
        self.ground_y = ground_level
        
        # 물리 요소
        self.gravity = 1
        self.jump_power = -22
        self.on_ground = True

        self.reset()

    def reset(self):
        self.hp = 3
        self.grade = 0.00

        self.have_B = False
        self.have_O_lib = False
        self.have_O_stu = False

        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0
        self.vy = 0
        self.on_ground = True

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # 키 입력 처리
    def handle_input(self, keys):
        self.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 8

    # 점프 처리
    def jump(self):
        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

    # 물리 업데이트
    def update(self):
        # 좌우 이동
        self.rect.x += self.vx

        # 화면 절반까지만 이동 제한
        if self.rect.x < self.left_limit:
            self.rect.x = self.left_limit

        if self.rect.x > self.right_limit:
            self.rect.x = self.right_limit

        # 중력 적용
        self.vy += self.gravity
        self.rect.y += self.vy

        # 바닥 충돌 처리
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vy = 0
            self.on_ground = True

        self.x = self.rect.x
        self.y = self.rect.y

    # 명수당 입장 → 날기 이미지 적용
    def set_fly_mode(self):
        center = self.rect.center

        self.image = self.image_fly

        self.rect = self.image.get_rect(center=center)
        self.width = self.rect.width
        self.height = self.rect.height

    # 명수당 종료 → 다시 기본 이미지
    def set_boo_mode(self):
        center = self.rect.center

        self.image = self.image_boo

        self.rect = self.image.get_rect(center=center)
        self.width = self.rect.width
        self.height = self.rect.height

    # 부 그리기
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    #학점 변경
    def update_grade(self, amount):
        self.grade += amount
        if self.grade >= 4.50:
            self.grade = 4.50
        elif self.grade < 0.00:
            self.grade = 0.00

    def get_hp(self, amount=1):
        if self.hp < 3:
            self.hp += amount
        
    def lose_hp(self, amount=1):
        if self.hp > 0:
            self.hp -= amount

    def get_bonus_item(self, item_name):
        if item_name == "B":
            self.have_B = True
        elif item_name == "O_lib":
            self.have_O_lib = True
        elif item_name == "O_stu":
            self.have_O_stu = True