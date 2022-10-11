import sys
import pygame
from pygame.locals import KEYDOWN, K_q, K_LEFT, K_RIGHT, K_UP, K_DOWN
import numpy as np

import pi_gen
import colour_paletts as colp

# CONSTANTS:
#SCREENSIZE = WIDTH, HEIGHT = 800, 600
WIDTH, HEIGHT = 0, 0 # width and height are correctly defined later
GRIDPIXELSIZE = 0 # correctly defined later
BUFFER = 50
SMALLBUFFER = 10
PALETTEID = 0
ARRAYOFFSET = 0

GRIDDIMENSIONS = 34 # shouldn't be greater then 500. CAN'T BE GREATER THEN 1000

# COLORS:
BACKGROUNDCOL = (50, 50, 50)
GREY = (210, 210, 207)
LIGHTGREY = (226, 226, 223)
WHITE = (255, 255, 255)   #3
BLACK = (0, 0, 0)         #.

# OUR GRID MAP SKELLETON:
cellMAP = np.random.randint(10, size=(GRIDDIMENSIONS, GRIDDIMENSIONS))
# SURFACE:
_VARS = {'surf': False, 'gridWH': 400,
     'gridOrigin': (BUFFER, 10), 'gridCells': cellMAP.shape[0]}


# BUTTONS -------------------------------------------
buttons = []
class Button:
    def __init__(self, id, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.id = id

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        buttons.append(self)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(_VARS['surf'], self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(_VARS['surf'], self.top_color, self.top_rect, border_radius=12)
        _VARS['surf'].blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global PALETTEID, GRIDDIMENSIONS, buttons
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                # Change PaletteID which changes the colour palette if button.id 0,1,2 or 3
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    if not isinstance(self.id, int):
                        if self.id == '+' and GRIDDIMENSIONS < 500:
                            GRIDDIMENSIONS += 1
                        elif self.id == '+10' and GRIDDIMENSIONS <= 490:
                            GRIDDIMENSIONS = GRIDDIMENSIONS + 10
                        elif self.id == '-' and GRIDDIMENSIONS > 3:
                            GRIDDIMENSIONS -= 1
                        elif self.id == '-10' and GRIDDIMENSIONS >= 13:
                            GRIDDIMENSIONS = GRIDDIMENSIONS - 10
                        make_pi_array(ARRAYOFFSET)
                        buttons = []
                        drawStaticElements()
                        drawButtons()
                    else:
                        if self.id >= 0 and self.id <= 3:
                            PALETTEID = self.id
                        else:
                            GRIDDIMENSIONS = self.id
                            make_pi_array(ARRAYOFFSET)
                            buttons = []
                            drawStaticElements()
                            drawButtons()

        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

def showButtons():
    for b in buttons:
        b.draw()
#----------------------------------------------------

def main():
    # global gui_font for Button class
    global gui_font
    pygame.init()
    gui_font = pygame.font.SysFont('Aller', 40)
    get_display_dimensions()
    _VARS['surf'] = pygame.display.set_mode((WIDTH, HEIGHT))
    make_pi_array(ARRAYOFFSET)
    drawStaticElements()
    drawButtons()
    while True:
        checkEvents()
        drawStaticElements()
        showButtons()
        pygame.display.update()

# fill background, sets colour palette, draws cells and legend
def drawStaticElements():
    _VARS['surf'].fill(BACKGROUNDCOL)
    current_palette = setCellColour()
    placeCells(current_palette)
    drawLegend()


def checkEvents():
    global ARRAYOFFSET
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_LEFT and ARRAYOFFSET > 0:
            ARRAYOFFSET -= 1
            make_pi_array(ARRAYOFFSET)
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            ARRAYOFFSET += 1
            make_pi_array(ARRAYOFFSET)
        elif event.type == KEYDOWN and event.key == K_UP:
            if ARRAYOFFSET-GRIDDIMENSIONS < 0:
                ARRAYOFFSET = 0
            else:
                ARRAYOFFSET -= GRIDDIMENSIONS
            make_pi_array(ARRAYOFFSET)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            ARRAYOFFSET += GRIDDIMENSIONS
            make_pi_array(ARRAYOFFSET)

# set the current colourpallet for the cells
def setCellColour():
    # 0 ... Pastel
    # 1 ... Grayscale
    # 2 ... Retro
    # 3 ... Neon
    palette = colp.COLOURPALETTES[PALETTEID]
    return palette

# NEW METHOD FOR ADDING CELLS :
def placeCells(colourPalette):
    # GET CELL DIMENSIONS...
    global GRIDPIXELSIZE
    cellBorder = 0
    celldimX = celldimY = round(((HEIGHT-20)/GRIDDIMENSIONS) - (cellBorder*2))
    GRIDPIXELSIZE = celldimX * GRIDDIMENSIONS
    # DOUBLE LOOP
    for row in range(cellMAP.shape[0]):
        for column in range(cellMAP.shape[1]):
            # 1st cell always WHITE when it is the '3' infront of the '.'
            if(column == 0 and row == 0 and cellMAP[column][row+1] == '.'): cell_color = colourPalette[2]#WHITE
            else:
                # 2nd cell ('.') always BLACK
                if(cellMAP[column][row] == '.'): cell_color = BLACK
                # color other cells depending on digit
                else: cell_color = colourPalette[int(cellMAP[column][row])]
            # draw colored cell
            drawSquareCell(
                _VARS['gridOrigin'][0] + (celldimY*row)
                + cellBorder + (2*row*cellBorder),
                _VARS['gridOrigin'][1] + (celldimX*column)
                + cellBorder + (2*column*cellBorder),
                celldimX, celldimY, cell_color)


# Draw filled rectangle at coordinates
def drawSquareCell(x, y, dimX, dimY, cell_color):
    pygame.draw.rect(_VARS['surf'], cell_color,(x, y, dimX, dimY))


# Make right sized, drawable 2D-Array from the pi string
def make_pi_array(offset):
    global cellMAP
    n = GRIDDIMENSIONS ** 2 + offset# - 2 ## '- 2' only if you use 'pi_gen.compute_pi(n)' in the next line
    pii = pi_gen.million_digits_pi[offset:n] # pi_gen.compute_pi(n) ## !!!also use 'list(str(pii))' instead of 'pii' in the next line if you use 'pi_gen.compute_pi(n)' here!!!
    cellMAP = np.reshape(pii, (GRIDDIMENSIONS, GRIDDIMENSIONS))


# Draw legends / colorpaletts
def drawLegend():
    # background rect
    pygame.draw.rect(_VARS['surf'], (150, 150, 150),(GRIDPIXELSIZE + 2*BUFFER, BUFFER, WIDTH - (GRIDPIXELSIZE + 3*BUFFER), HEIGHT - 2*BUFFER))
    # dyn title:
    font = pygame.font.SysFont('Aller', 55)
    textsurface = font.render('You are looking at {0} digits of π'.format(GRIDDIMENSIONS**2), False, BACKGROUNDCOL)
    _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 3*BUFFER, BUFFER + 4*SMALLBUFFER))
    # underline
    pygame.draw.line(_VARS['surf'], BACKGROUNDCOL, (GRIDPIXELSIZE + 3*BUFFER, 3*BUFFER), (WIDTH - 2*BUFFER, 3*BUFFER), 5)
    # 'Colour Palettes':
    font = pygame.font.SysFont('Aller', 40)
    textsurface = font.render('--- Colour Palettes ---', False, BACKGROUNDCOL)
    _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 7*BUFFER, 3*BUFFER + 1.5*SMALLBUFFER))

    # background rects:
    colPalBackRectWidth = (WIDTH - (GRIDPIXELSIZE + 8 * BUFFER)) / 4
    for i in range(4):
        pygame.draw.rect(_VARS['surf'], LIGHTGREY,
                         (GRIDPIXELSIZE + (i+3)*BUFFER + i*colPalBackRectWidth, 4 * BUFFER, colPalBackRectWidth, HEIGHT - 10*BUFFER))
    # color rects:
    ## Palette 1 Pastel
    colRectHeight = (HEIGHT - 10*BUFFER - 2*SMALLBUFFER)/10
    colRectWidth = colPalBackRectWidth - 4*SMALLBUFFER
    for i in range(10):
        pygame.draw.rect(_VARS['surf'], colp.COLOURPALETTES[0][i], (GRIDPIXELSIZE + 3*BUFFER + 3*SMALLBUFFER, 4*BUFFER + (i*colRectHeight) + SMALLBUFFER, colRectWidth, colRectHeight))
        # numbers
        font = pygame.font.SysFont('Aller', 40)
        textsurface = font.render(str(i), False, BACKGROUNDCOL)
        _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 3*BUFFER + SMALLBUFFER, 4*BUFFER + (i*colRectHeight) + SMALLBUFFER + (colRectHeight/4)))
    # palette name:
    # font = pygame.font.SysFont('Aller', 50)
    # textsurface = font.render('Pastel', False, BACKGROUNDCOL)
    # _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 3*BUFFER + 1.5*SMALLBUFFER, HEIGHT - (5.75*BUFFER)))

    ## Palette 2 Grayscale
    colRectHeight = (HEIGHT - 10 * BUFFER - 2 * SMALLBUFFER) / 10
    colRectWidth = colPalBackRectWidth - 4 * SMALLBUFFER
    for i in range(10):
        pygame.draw.rect(_VARS['surf'], colp.COLOURPALETTES[1][i], (
        GRIDPIXELSIZE + 4 * BUFFER + colPalBackRectWidth + 3*SMALLBUFFER, 4 * BUFFER + (i * colRectHeight) + SMALLBUFFER, colRectWidth,
        colRectHeight))
        # numbers
        font = pygame.font.SysFont('Aller', 40)
        textsurface = font.render(str(i), False, BACKGROUNDCOL)
        _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 4 * BUFFER + colPalBackRectWidth + SMALLBUFFER, 4 * BUFFER + (i * colRectHeight) + SMALLBUFFER + (colRectHeight / 4)))

    ## Palette 3 Retro
    colRectHeight = (HEIGHT - 10 * BUFFER - 2 * SMALLBUFFER) / 10
    colRectWidth = colPalBackRectWidth - 4 * SMALLBUFFER
    for i in range(10):
        pygame.draw.rect(_VARS['surf'], colp.COLOURPALETTES[2][i], (
            GRIDPIXELSIZE + 5 * BUFFER + 2*colPalBackRectWidth + 3*SMALLBUFFER,
            4 * BUFFER + (i * colRectHeight) + SMALLBUFFER, colRectWidth,
            colRectHeight))
        # numbers
        font = pygame.font.SysFont('Aller', 40)
        textsurface = font.render(str(i), False, BACKGROUNDCOL)
        _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 5 * BUFFER + 2*colPalBackRectWidth + SMALLBUFFER, 4 * BUFFER + (i * colRectHeight) + SMALLBUFFER + (colRectHeight / 4)))

    ## Palette 4 Neon
    colRectHeight = (HEIGHT - 10 * BUFFER - 2 * SMALLBUFFER) / 10
    colRectWidth = colPalBackRectWidth - 4 * SMALLBUFFER
    for i in range(10):
        pygame.draw.rect(_VARS['surf'], colp.COLOURPALETTES[3][i], (
            GRIDPIXELSIZE + 6 * BUFFER + 3 * colPalBackRectWidth + 3*SMALLBUFFER,
            4 * BUFFER + (i * colRectHeight) + SMALLBUFFER, colRectWidth,
            colRectHeight))
        # numbers
        font = pygame.font.SysFont('Aller', 40)
        textsurface = font.render(str(i), False, BACKGROUNDCOL)
        _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 6 * BUFFER + 3 * colPalBackRectWidth + SMALLBUFFER, 4 * BUFFER + (i * colRectHeight) + SMALLBUFFER + (colRectHeight / 4)))

    # 2nd underline
    pygame.draw.line(_VARS['surf'], BACKGROUNDCOL, (GRIDPIXELSIZE + 3*BUFFER, HEIGHT - (4.5*BUFFER)), (WIDTH - 2*BUFFER, HEIGHT - (4.5*BUFFER)), 5)

    # 'Change Dimentions'
    font = pygame.font.SysFont('Aller', 50)
    textsurface = font.render('Change Grid Dimensions:', False, BACKGROUNDCOL)
    _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 3*BUFFER,  HEIGHT - (4.3*BUFFER)))
    font = pygame.font.SysFont('Aller', 30)
    textsurface = font.render('currently ({0} x {0})'.format(GRIDDIMENSIONS, GRIDDIMENSIONS), False, BACKGROUNDCOL)
    _VARS['surf'].blit(textsurface, (GRIDPIXELSIZE + 3.2*BUFFER,  HEIGHT - (3.6*BUFFER)))


def drawButtons():
    colPalBackRectWidth = (WIDTH - (GRIDPIXELSIZE + 8 * BUFFER)) / 4
    button1 = Button(0, 'Pastel', colPalBackRectWidth, 40, (GRIDPIXELSIZE + 3*BUFFER , HEIGHT - (5.75*BUFFER)), 5)
    button2 = Button(1, 'Gray', colPalBackRectWidth, 40, (GRIDPIXELSIZE + 4 * BUFFER + colPalBackRectWidth, HEIGHT - (5.75*BUFFER)), 5)
    button3 = Button(2, 'Retro', colPalBackRectWidth, 40, (GRIDPIXELSIZE + 5 * BUFFER + 2*colPalBackRectWidth, HEIGHT - (5.75*BUFFER)), 5)
    button4 = Button(3, 'Neon', colPalBackRectWidth, 40, (GRIDPIXELSIZE + 6 * BUFFER + 3*colPalBackRectWidth, HEIGHT - (5.75*BUFFER)), 5)

    button5 = Button(4, '4x4', 80, 30, (GRIDPIXELSIZE + 3*BUFFER, HEIGHT - (3*BUFFER)), 5)
    button6 = Button(7, '7x7', 80, 30, (GRIDPIXELSIZE + 3*BUFFER, HEIGHT - (2.2*BUFFER)), 5)
    button7 = Button(10, '10x10', 100, 30, (GRIDPIXELSIZE + 4.8*BUFFER, HEIGHT - (3*BUFFER)), 5)
    button8 = Button(20, '20x20', 100, 30, (GRIDPIXELSIZE + 4.8*BUFFER, HEIGHT - (2.2*BUFFER)), 5)
    button9 = Button(30, '30x30', 100, 30, (GRIDPIXELSIZE + 6.9*BUFFER, HEIGHT - (3*BUFFER)), 5)
    button10 = Button(50, '50x50', 100, 30, (GRIDPIXELSIZE + 6.9*BUFFER, HEIGHT - (2.2*BUFFER)), 5)
    button11 = Button(70, '70x70', 100, 30, (GRIDPIXELSIZE + 9*BUFFER, HEIGHT - (3*BUFFER)), 5)
    button12 = Button(85, '85x85', 100, 30, (GRIDPIXELSIZE + 9*BUFFER, HEIGHT - (2.2*BUFFER)), 5)
    button13 = Button(100, '100x100', 120, 30, (GRIDPIXELSIZE + 11.1*BUFFER, HEIGHT - (3*BUFFER)), 5)
    button14 = Button(150, '150x150', 120, 30, (GRIDPIXELSIZE + 11.1*BUFFER, HEIGHT - (2.2*BUFFER)), 5)
    button15 = Button(250, '250x250', 120, 30, (GRIDPIXELSIZE + 13.7*BUFFER, HEIGHT - (3*BUFFER)), 5)
    button16 = Button(500, '500x500', 120, 30, (GRIDPIXELSIZE + 13.7*BUFFER, HEIGHT - (2.2*BUFFER)), 5)

    button17 = Button('+', '+', 40, 40, (GRIDPIXELSIZE + 14*BUFFER, HEIGHT - (4.2*BUFFER)), 5)
    button18 = Button('-', '-', 40, 40, (GRIDPIXELSIZE + 13*BUFFER, HEIGHT - (4.2*BUFFER)), 5)
    button19 = Button('-10', '-10', 50, 40, (GRIDPIXELSIZE + 11.8*BUFFER, HEIGHT - (4.2*BUFFER)), 5)
    button20 = Button('+10', '+10', 50, 40, (GRIDPIXELSIZE + 15*BUFFER, HEIGHT - (4.2*BUFFER)), 5)


def get_display_dimensions():
    global WIDTH, HEIGHT
    displayInfoObject = pygame.display.Info()
    WIDTH = displayInfoObject.current_w
    HEIGHT = displayInfoObject.current_h - 60


if __name__ == '__main__':
    main()