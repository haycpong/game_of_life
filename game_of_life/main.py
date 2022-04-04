"""Game entry point
This file is doing the tasks:
    Defining of window width
    Defining of window height
    Creation of GameofLife object
    Defining of thge game status update rate
    Running the game loop
"""
import sys
import pygame
from game_of_life import GameofLife

WIDTH = 640
HEIGHT = 480
EXPECTED_FPS = 30
pause = False
pen_on = False
screen = None
display = None
fonts = None
clock = None


def init_game():
    global screen, display, fonts, clock
    pygame.init()
    WINDOW_SIZE = (WIDTH, HEIGHT)
    pygame.display.set_caption("Game of Life")
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    pygame.font.init()
# This create different font size in one line
    fonts = create_fonts([32, 16, 14, 8])
    clock = pygame.time.Clock()

def create_fonts(font_sizes_list):
    "Creates different fonts with one list"
    fonts = []
    for size in font_sizes_list:
        fonts.append(
            pygame.font.SysFont("Arial", size))
    return fonts
 
 
def update_text(fnt, what, antialias, color, where):
    "Renders the fonts as passed from display_fps"
    text_to_show = fnt.render(what, antialias, pygame.Color(color))
    screen.blit(text_to_show, where)
 

def update_button(msg,x,y,w,h,inactive_color,active_color,action=None):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
#    print(click)
    if x+w > mouse_x > x and y+h > mouse_y > y:
        pygame.draw.rect(screen, active_color,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, inactive_color,(x,y,w,h))

#    textSurf, textRect = text_objects(msg, smallText)
#    textRect.center = ((x+(w/2)), (y+(h/2)))
    button_text = fonts[1].render(str(msg),0,pygame.Color("black"))
    (text_width, text_height) = fonts[1].size(str(msg))
    screen.blit(button_text, (x+(w-text_width)/2, y+(h-text_height)/2) )

def get_pen():
    global pen_on
    return pen_on

def set_pen_on():
    global pen_on
    pen_on=True
    return

def set_pen_off():
    global pen_on
    pen_on=False
    return

def pause_game():
    global pause
    pause = True
    return

def resume_game():
    global pause
    pause = False
    return

def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
  #initialize game setting
  init_game()
  game_obj = GameofLife(screen, scale=20)

  while True:
    clock.tick(EXPECTED_FPS)
#    screen.fill((0, 0, 0))
    pygame.draw.rect(screen,(0,0,0),(0,0,WIDTH,35))

    #update user input
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    (grid_x, grid_y) = game_obj.get_grid_pos(mouse_x,mouse_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if (get_pen()):
                    set_pen_off()
                else:
                    set_pen_on()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause:
                game_obj.alternate_grid_state(grid_x,grid_y)

        if event.type == pygame.MOUSEMOTION:
            if pen_on:
                game_obj.set_grid_live(grid_x,grid_y)


    #update game
    if not(pause):
        game_obj.run()
    else:
        game_obj.draw_grid()

    #update fps
    update_text(fonts[0],'FPS:'+str(int(clock.get_fps())), 0, "red", (0,0))

    #update mouse in which grid
    update_text(fonts[0],'Pos('+str(mouse_x)+','+str(mouse_y)+')', 0, "green", (98,0))
    update_text(fonts[0],'Grid('+str(grid_x)+','+str(grid_y)+')', 0, "blue", (260,0))
    update_text(fonts[0],'Press e:toggle pen', 0, "blue", (400,0))

    #update button
    update_text(fonts[1],'Pen:', 0, "green", (5,445))

    if pen_on:
        update_button("on",50,440,25,30,"green","green",None)
        update_button("off",75,440,25,30,"darkgreen","darkgreen",set_pen_off)
    else:
        update_button("on",50,440,25,30,"darkgreen","darkgreen",set_pen_on)
        update_button("off",75,440,25,30,"green","green",None)

    if pause:
        update_button("Pause",100,440,100,30,"green","green",None)
        update_button("Update",200,440,100,30,"darkgreen","darkgreen",resume_game)
    else:
        update_button("Pause",100,440,100,30,"darkgreen","darkgreen",pause_game)
        update_button("Update",200,440,100,30,"green","green",None)

    update_button("Fill",350,440,50,30,"yellow4","yellow",game_obj.fill)
    update_button("Clear",400,440,50,30,"yellow4","yellow",game_obj.clear)
    update_button("Regenerate",450,440,100,30,"yellow4","yellow",game_obj.regenerate)

    update_button("Quit",550,440,50,30,"darkred","red",quit_game)


    pygame.display.update()