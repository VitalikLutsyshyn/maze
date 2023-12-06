from pygame import*
init()
FPS = 60
WIDTH,HEIGH = 900,612
run = True
MAP_WIDTH = 25
MAP_HEIGHT = 25
TILE_SIZE = WIDTH/MAP_WIDTH

window = display.set_mode((WIDTH,HEIGH))
display.set_caption("maze")
clock = time.Clock()

sprites = sprite.Group()


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
class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image,x,y,width,height):
        super().__init__()
        self.image = transform.scale(sprite_image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        sprites.add(self)


class Player(GameSprite):
    def __init__(self, x, y,hp,gold):
        super().__init__(player_img, x, y,TILE_SIZE-7 ,TILE_SIZE-7)
        self.hp = hp
        self.gold = gold
        self.dir = "right"
        self.speed = 5
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed

with open("map.txt","r") as file:
    map = file.readlines()
    x,y = TILE_SIZE/2,TILE_SIZE/2
    for line in map:
        for symbol in line:
            if symbol == "w":
                GameSprite(wall_img1,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "d":
                GameSprite(dragon_img_green,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "q":
                GameSprite(dragon_img_purple,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "g":
                GameSprite(gold_img,x,y,TILE_SIZE-10,TILE_SIZE-10)
            if symbol == "b":
                GameSprite(brick_img0,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "a":
                GameSprite(brick_img1,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "m":
                GameSprite(wall_img8,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "s":
                GameSprite(scroll_img,x,y,TILE_SIZE-10,TILE_SIZE-10)
            if symbol == "k":
                GameSprite(key_img,x,y,TILE_SIZE-10,TILE_SIZE-10)
            if symbol == "o":
                GameSprite(chest_open_img,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "c":
                GameSprite(chest_close_img,x,y,TILE_SIZE,TILE_SIZE)
            if symbol == "p":
                player = Player(x,y,100,0)

            x += TILE_SIZE
        y += TILE_SIZE
        x = TILE_SIZE/2



while run:
    window.fill((0,0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False



    sprites.update()
    sprites.draw(window)
    display.update()
    clock.tick(FPS)
