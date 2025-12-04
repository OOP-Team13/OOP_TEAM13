import pygame
import random

class Object:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.active = True

    def use(self, player):
        pass

    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self, speed):
        if self.active:
            self.x -= speed
    
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

# 아이템
class Book(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/book.png")
        self.name = "book"
    
    def use(self, player):
        player.update_grade(0.10)

class Energy(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/energy.png")
        self.name = "energy"

    def use(self, player):
        player.get_hp(1)

class B(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/b.png")
        self.name = "B"
    
    def use(self, player):
        player.get_bonus_item(self.name)

class O_lib(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/o_library.png")
        self.name = "O_lib"

    def use(self, player):
        player.get_bonus_item(self.name)

class O_stu(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/o_student_hall.png")
        self.name = "O_stu"

    def use(self, player):
        player.get_bonus_item(self.name)

class BonusBook(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/book.png")
        self.name = "bonus_book"

    def use(self, player):
        player.update_grade(0.20)

# 장애물
class Soju(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/soju.png")
        self.name = "soju"
    
    def use(self, player):
        player.update_grade(-0.05)

class Nut(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/nut.png")
        self.name = "nut"
    
    def use(self, player):
        player.lose_hp(1)

class CoffeeCup(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/coffee.png")
        self.name = "coffee"

    def use(self, player):
        player.lose_hp(1)


#스테이지별 아이템 생성
class StageItem:
    def __init__(self):
        self.common_items = [Book, Energy, Soju, Nut, CoffeeCup]
        self.common_weights = [45, 10, 25, 10, 10]
    
    def get_items_and_weights(self):
        return self.common_items[:], self.common_weights[:]
    
    def create_items(self, seconds, speed, screen_width, screen_height, stage_name, player):
        items = []
        total_distance = (seconds + 2) * 20 * speed
        current_x = screen_width + 100
        
        pool, weights = self.get_items_and_weights()
        
        bonus_class = None
        check_attr = None

        if stage_name == "main_building":
            bonus_class = B 
            check_attr = "have_B"
        elif stage_name == "library":
            bonus_class = O_lib
            check_attr = "have_O_lib"
        elif stage_name == "student_hall":
            bonus_class = O_stu
            check_attr = "have_O_stu"

        elif stage_name == "bonus":
            pool = [BonusBook, Energy]
            weights = [80, 20]
            bonus_class = None

        if bonus_class:
            pool.append(bonus_class)
            weights.append(50)

        is_spawned = False

        while current_x < total_distance:
            item_class = random.choices(pool, weights=weights, k=1)[0]

            if bonus_class and item_class == bonus_class:
                has_item = getattr(player, check_attr, False)
                if has_item or is_spawned:
                    item_class = Book
                else:
                    is_spawned = True

            y = random.randint(200, 450)
            items.append(item_class(current_x, y))
            
            next_step = random.randint(50, 150)
            current_x += next_step

        # 보너스 아이템이 안 나온 경우 강제로 스폰하고자 함
        if bonus_class and not is_spawned and items:
            if not getattr(player, check_attr, False):
                target_idx = random.randint(0, len(items) - 1)
                target_item = items[target_idx]
                
                # 기존 아이템을 보너스 아이템으로 교체
                items[target_idx] = bonus_class(target_item.x, target_item.y)
                print(f"보너스 아이템 강제 생성됨: {stage_name}")

        return items

class MainBuilding(StageItem):
    def get_bonus_info(self):
        return B, "have_B"

class Library(StageItem):
    def get_bonus_info(self):
        return O_lib, "have_O_lib"

class StudentHall(StageItem):
    def get_bonus_info(self):
        return O_stu, "have_O_stu"

class Bonus(StageItem):
    def get_pool_and_weights(self):
        return [BonusBook, Energy], [80, 20]