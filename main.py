from pygame import*
init()
FPS = 60
WIDTH,HEIGH = 900,600
run = True

window = display.set_mode((WIDTH,HEIGH))
display.set_caption("maze")
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False


    display.update()
    clock.tick(FPS)
