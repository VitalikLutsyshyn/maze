from pygame import*
from random import*
#ЗНАЙТИ МУЗИКУ ДЛЯ ГРИ
init()
font.init()
mixer.init()
FONT_NAME = "asets/alagard_by_pix3m-d6awiwp.ttf"

FPS = 90
WIDTH,HEIGH = 900,612
MAX_LEVEL = 2
run = True
MAP_WIDTH = 25
MAP_HEIGHT = 25
TILE_SIZE = WIDTH/MAP_WIDTH
WHITE = (255,255,255)
window = display.set_mode((WIDTH,HEIGH))
display.set_caption("maze")
clock = time.Clock()
#Музика
wallking_sound = mixer.Sound("asets/music/full steps stereo.ogg")
wallking_sound.set_volume(0.4)
chest_sound = mixer.Sound("asets/music/Chest Creak.wav")
coin_sound = mixer.Sound("asets/music/coin.wav")
mixer.music.load("asets/music/Burnt Spirit.mp3")
mixer.music.set_volume(0.01)
mixer.music.play()#Відтвореня музики


sprites = sprite.Group()
walls = sprite.Group()
dragons = sprite.Group()
golds = sprite.Group()
scrolls = sprite.Group()
keys = sprite.Group()
chests = sprite.Group()
doors = sprite.Group()

wall_img1 = image.load("asets/map/catacombs_0.png")
dragon_img_green = image.load("asets/map/dragon_form_green.png")
dragon_img_purple = image.load("asets/map/dragon_form_mottled.png")
gold_img = image.load("asets/map/gold_pile_9.png")
player_img = image.load("asets/map/minotaur_brown_2_male.png")
brick_img0 = image.load("asets/map/brick_gray_0.png")
brick_img1 = image.load("asets/map/brick_gray_1.png")
wall_img8 = image.load("asets/map/catacombs_8.png")
scroll_img = image.load("asets/map/scroll-cyan.png")
key_img = image.load("asets/map/key.png")
chest_open_img = image.load("asets/map/chest_2_open.png")
chest_close_img = image.load("asets/map/chest_2_closed.png")
close_door_img = image.load("asets/map/closed_door.png")
open_door_img = image.load("asets/map/open_door.png")
hp_img = image.load("asets/map/heart_old.png")
btn_img = image.load("asets/map/BTN.png")






class Counter:
    def __init__(self,value,sprite_img,x,y,width,height):
        self.image = transform.scale(sprite_img,(width,height))
        self.font = font.Font(FONT_NAME,height-5 )
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
        chest_sound.play()
        self.treasure = choice(self.treasure_list)
        if self.treasure == "gold":
            self.count = randint(1,10)
        else:
            self.count = 5

        self.image = self.opened_image
        self.opened = True
        return self.treasure, self.count


class Door(GameSprite):
    def __init__(self, x, y,):
        super().__init__(close_door_img, x, y,TILE_SIZE,TILE_SIZE)
        self.opened = False
        self.opened_image  = transform.scale(open_door_img,(TILE_SIZE,TILE_SIZE))

    def open(self):
        chest_sound.play()

        self.image = self.opened_image
        self.opened = True


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
        self.hp = 10000
        self.dir = "right"
        self.speed = 3
        self.get_hit = False
        self.level = 1
    

    def update(self):
        global win,result_text
        old_pos = self.rect.x,self.rect.y
        keys_pressed = key.get_pressed()
        
        if keys_pressed[K_a]:
            self.rect.x -= self.speed
        elif keys_pressed[K_d]:
            self.rect.x += self.speed 
        elif keys_pressed[K_w]:
            self.rect.y -= self.speed
        elif keys_pressed[K_s]:
            self.rect.y += self.speed
        else:
            wallking_sound.stop()

        if wallking_sound.get_num_channels() == 0:
            wallking_sound.play(loops = -1)

        sprites_list = sprite.spritecollide(self,doors,False,sprite.collide_mask)
        for door in sprites_list:
            if len(scrolls) == 0 and not door.opened:
                door.open()
                door.remove(walls)
                self.scrolls = 0
                scroll_counter.set_value(self.scrolls)
                if self.level < MAX_LEVEL :
                    next_level()
                else:
                    win = True
                    result_text = font1.render("YOU WIN",True,WHITE)


        if self.check_collision(walls):
            self.rect.x,self.rect.y = old_pos

        if self.check_collision(golds,True):
            self.gold += 5
            gold_counter.set_value(self.gold)
            coin_sound.play()

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

class Button(GameSprite):
    def __init__(self,text, x, y,):
        super().__init__(btn_img, x, y,300,100)
        self.font = font.Font(FONT_NAME,35)
        self.label = self.font.render(str(text),True,WHITE)
        self.label_rect = self.label.get_rect(center = (self.rect.centerx, self.rect.centery))
        self.remove(sprites)
    
    def draw(self,window):
        window.blit(self.image,self.rect)
        window.blit(self.label,self.label_rect)

 
                 
def read_map(filename="map1.txt"):
    global player

    for s in sprites:
        if s != player:
            s.kill()

    with open(filename,"r") as file:
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
                    player.rect.centerx =x   
                    player.rect.centery = y  
                if symbol == "j":
                    door = Door(x,y)
                    walls.add(door)
                    doors.add(door)
                

                x += TILE_SIZE
            y += TILE_SIZE
            x = TILE_SIZE/2


def new_game():
    global gold_counter ,scroll_counter,keys_counter,hp_counter,game_over,win,player
    player = Player(0,0,100,0)
    read_map()
    gold_counter =Counter(player.gold,gold_img,300,0,30,30)
    scroll_counter =Counter(player.scroll,scroll_img,100,0,30,30)
    keys_counter =Counter(player.keys,key_img,200,0,30,30)
    hp_counter =Counter(player.hp,hp_img,10,0,30,30)
    
    game_over = False
    win = False

def next_level():
    player.level += 1
    mapfile = f"map{player.level}.txt"
    read_map(mapfile)


font1 = font.Font(FONT_NAME,80)
result_text = font1.render("GAME OVER!",True,WHITE)
restart_btn = Button("RESTART",WIDTH/2,HEIGH-150)


new_game()

while run:
    window.fill((0,0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False

        if game_over or win:
            if e.type == MOUSEBUTTONDOWN:
                x,y = e.pos
                if restart_btn.rect.collidepoint(x,y):
                    new_game()



    if player.hp <= 0:
        game_over = True
    if not game_over and not win:
        sprites.update()  

    sprites.draw(window)
    gold_counter.draw(window)
    scroll_counter.draw(window)
    keys_counter.draw(window)
    hp_counter.draw(window)

    if game_over or win:
        window.blit(result_text,(250,250))
        restart_btn.draw(window)

    display.update()
    clock.tick(FPS)