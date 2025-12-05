from ending import *

def check_collision(player, items, sound):
    hit_list = pygame.sprite.spritecollide(player, items, False)

    for item in hit_list:
        if item.active:
            item.use(player) 

            sound.play_item()

            item.active = False

            if item in items:
                items.remove(item)
