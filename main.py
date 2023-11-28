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

wall_img = image.load("asets/map/catacombs_0.png")

class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image,x,y,width,height):
        super().__init__()
        self.image = transform.scale(sprite_image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        sprites.add(self)


with open("map.txt","r") as file:
    map = file.readline()
    x,y = TILE_SIZE/2,TILE_SIZE/2
    for line in map:
        for symbol in line:
            if symbol == "w":
                GameSprite(wall_img,x,y,TILE_SIZE,TILE_SIZE)
                x += TILE_SIZE
        y += TILE_SIZE
        x = TILE_SIZE/2
        y = TILE_SIZE/2
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    sprites.draw(window)
    display.update()
    clock.tick(FPS)
