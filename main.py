from pygame import*
from random import*
#ЗНАЙТИ МУЗИКУ ДЛЯ ГРИ
init()
font.init()
FONT_NAME = "Impact"
FPS = 90
WIDTH,HEIGH = 900,612
run = True
MAP_WIDTH = 25
MAP_HEIGHT = 25
TILE_SIZE = WIDTH/MAP_WIDTH
WHITE = (255,255,255)
window = display.set_mode((WIDTH,HEIGH))
display.set_caption("maze")
clock = time.Clock()

sprites = sprite.Group()
walls = sprite.Group()
dragons = sprite.Group()
golds = sprite.Group()
scrolls = sprite.Group()
keys = sprite.Group()
chests = sprite.Group()

wall_img1 = image.load("asets/map/catacombs_0.png")
dragon_img_green = image.load("asets/map/dragon_form_green.png")
dragon_img_purple = image.load("asets\map\dragon_form_mottled.png")
gold_img = image.load("asets\map\gold_pile_9.png")
player_img = image.load("asets/map/minotaur_brown_2_male.png")
brick_img0 = image.load("asets/map/brick_gray_0.png")
brick_img1 = image.load("asets/map/brick_gray_1.png")
wall_img8 = image.load("asets/map/catacombs_8.png")
scroll_img = image.load("asets/map/scroll-cyan.png")
key_img = image.load("asets/map/key.png")
chest_open_img = image.load("asets/map/chest_2_open.png")
chest_close_img = image.load("asets/map/chest_2_closed.png")
close_door_img = image.load("asets/map/runed_door.png")
open_door_img = image.load("asets/map/closed_door.png")
hp_img = image.load("asets/map/heart_old.png")


class Counter:
    def __init__(self,value,sprite_img,x,y,width,height):
        self.image = transform.scale(sprite_img,(width,height))
        self.font = font.SysFont(FONT_NAME,height-5 )
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y
        self.label = self.font.render(str(value),True,WHITE)

    def draw(self,window):
        window.blit(self.image,self.rect)
        window.blit(self.label,(self.rect.right +10,self.rect.y))

    def set_value(self,new_value):
        self.label = self.font.render(str(new_value),True,WHITE)




class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image,x,y,width,height):
        super().__init__()
        self.image = transform.scale(sprite_image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)

    def check_collision(self,spritegroup,dokill = False):
        sprites_list = sprite.spritecollide(self,spritegroup,dokill,sprite.collide_mask) 
        if len(sprites_list) > 0:
            return True
        else:
            return False

class Chest(GameSprite):
    def __init__(self, x, y,):
        super().__init__(chest_close_img, x, y,TILE_SIZE,TILE_SIZE)
        self.opened = False
        self.opened_image  = transform.scale(chest_open_img,(TILE_SIZE,TILE_SIZE))   
        self.treasure = None
        self.treasure_list = ["gold","hp"]

    def open(self):
        self.treasure = choice(self.treasure_list)
        if self.treasure == "gold":
            self.count = randint(1,10)
        else:
            self.count = 5

        self.image = self.opened_image
        self.opened = True
        return self.treasure, self.count





class Dragon(GameSprite):
    def __init__(self,sprite_img, x, y,hp):
        super().__init__(sprite_img, x, y,TILE_SIZE-7 ,TILE_SIZE-7)
        self.hp = hp
        self.dir = "right"
        self.dir_list = ["right","left","down","up"]
        self.speed = 2
    
    def update(self):
        old_pos = self.rect.x,self.rect.y

        if self.dir == "up":
            self.rect.y -= self.speed
        elif self.dir == "down":
            self.rect.y += self.speed
        elif self.dir == "left":
            self.rect.x -= self.speed
        elif self.dir =="right":
            self.rect.x += self.speed
        
        if self.check_collision(walls):
            self.rect.x,self.rect.y = old_pos
            self.dir = choice(self.dir_list)

class Player(GameSprite):
    def __init__(self, x, y,hp,gold):
        super().__init__(player_img, x, y,TILE_SIZE-7 ,TILE_SIZE-7)
        self.hp = hp
        self.gold = gold
        self.scroll = 0
        self.keys = 0
        self.hp = 20
        self.dir = "right"
        self.speed = 3
        self.get_hit = False
    

    def update(self):
        old_pos = self.rect.x,self.rect.y
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w]:
            self.rect.y -= self.speed
        elif keys_pressed[K_s]:
            self.rect.y += self.speed
        elif keys_pressed[K_a]:
            self.rect.x -= self.speed
        elif keys_pressed[K_d]:
            self.rect.x += self.speed   

        if self.check_collision(walls):
            self.rect.x,self.rect.y = old_pos

        if self.check_collision(golds,True):
            self.gold += 5
            gold_counter.set_value(self.gold)

        if self.check_collision(scrolls,True):
            self.scroll += 1
            scroll_counter.set_value(self.scroll)



        if self.check_collision(keys,True):
            self.keys += 1
            keys_counter.set_value(self.keys)
        
        if self.check_collision(dragons,False):
            if not self.get_hit and self.hp >= 0:
                self.get_hit = True
                self.hp -= 10
                if self.hp <=0:
                    self.hp = 0
                hp_counter.set_value(self.hp)
                
        else:
            self.get_hit = False

        sprites_list = sprite.spritecollide(self,chests,False,sprite.collide_mask)
        for chest in sprites_list:
            if self.keys >=1 and not chest.opened:
                self.keys -= 1
                keys_counter.set_value(self.keys)
                treasure,count = chest.open()
                if treasure == "gold":
                    self.gold += count
                    gold_counter.set_value(self.gold)

                if treasure == "hp":
                    self.hp += count
                    hp_counter.set_value(self.hp)


with open("map.txt","r") as file:
    map = file.readlines()
    x,y = TILE_SIZE/2,TILE_SIZE/2
    for line in map:
        for symbol in line:
            if symbol == "w":
                walls.add(GameSprite(wall_img1,x,y,TILE_SIZE,TILE_SIZE))
            if symbol == "d":
                dragons.add(Dragon(dragon_img_green,x,y,20))
            if symbol == "q":
                dragons.add(Dragon(dragon_img_purple,x,y,20))
            if symbol == "g":
                golds.add(GameSprite(gold_img,x,y,TILE_SIZE-10,TILE_SIZE-10))
            if symbol == "b":
                walls.add(GameSprite(brick_img0,x,y,TILE_SIZE,TILE_SIZE))
            if symbol == "a":
                GameSprite(brick_img1,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "m":
                walls.add(GameSprite(wall_img8,x,y,TILE_SIZE,TILE_SIZE))
            if symbol == "s":
                scrolls.add(GameSprite(scroll_img,x,y,TILE_SIZE-10,TILE_SIZE-10))
            if symbol == "k":
                keys.add(GameSprite(key_img,x,y,TILE_SIZE-10,TILE_SIZE-10))
            if symbol == "c":
                chests.add(Chest(x,y))
            if symbol == "p":
                player = Player(x,y,100,0)
            if symbol == "j":
                walls.add(GameSprite(close_door_img,x,y,TILE_SIZE,TILE_SIZE))
            

            x += TILE_SIZE
        y += TILE_SIZE
        x = TILE_SIZE/2

gold_counter =Counter(player.gold,gold_img,300,0,30,30)
scroll_counter =Counter(player.scroll,scroll_img,100,0,30,30)
keys_counter =Counter(player.keys,key_img,200,0,30,30)
hp_counter =Counter(player.hp,hp_img,10,0,30,30)

while run:
    window.fill((0,0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False



    sprites.update()
    sprites.draw(window)
    gold_counter.draw(window)
    scroll_counter.draw(window)
    keys_counter.draw(window)
    hp_counter.draw(window)
    display.update()
    clock.tick(FPS)
