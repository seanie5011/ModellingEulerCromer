import pygame, time
import button
import textbox
import spring
import SinglePendulum as SP
import SingleSpring as SS
import ElasticPendulum as EP
import DoublePendulum as DP
import DoublePendulum1Spring as DP1S

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720 #int(SCREEN_WIDTH * 9.0/16.0)

layer0 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Model Display")

#layers to blit on
layer1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) #drawing controls on 
layer2 = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT)) #drawing models on

helplayer = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT), pygame.SRCALPHA) #layer to draw help surface on
helplayer.set_colorkey((255, 0, 255)) #Sets the colorkey to that hideous purple, that colour will be transparent

introlayer = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT)) #will display info on the game in menu screen

#---Framerate---#
clock = pygame.time.Clock()
FPS = 60

#----Define Colours---#
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (235, 65, 54)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)

BG = (8, 209, 190)
TRANSPARENCY = (255, 0, 255)

#---Define Fonts---#
FuturaFont23 = pygame.font.SysFont("Futura", 23)
FuturaFont30 = pygame.font.SysFont("Futura", 30)
FuturaFont50 = pygame.font.SysFont("Futura", 50)
FuturaFont100 = pygame.font.SysFont("Futura", 100)

#---Define vars---#
run = True #lets the while loop run

#dont actually need to define these at all but sure
model_use_index = 0
model_index = model_use_index
input_index = 0
is_updating = True

input_text_test = "0"
input_text = float(input_text_test)

zoom = 1 #how much zoom, > 1 zooms in, < 1 zooms out (max 1.5, min 0.5)

hide = False #whether or not to hide timer

#---Load Images---#
#-Background
bg_img = pygame.image.load("img\\bg\\GreenBlueColourGradient.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)) #make size of screen
intro_bg_img = pygame.image.load("img\\bg\\intro_gradient.png").convert_alpha()

#-Help Assets
box_T_img = pygame.image.load("img\\helpassets\\box_T.png").convert_alpha()
box_T_des = " - Display Tracing"
box_Y_img = pygame.image.load("img\\helpassets\\box_Y.png").convert_alpha()
box_Y_des = " - Reset Tracing"
box_P_img = pygame.image.load("img\\helpassets\\box_P.png").convert_alpha()
box_P_des = " - Pause / Unpause"
box_R_img = pygame.image.load("img\\helpassets\\box_R.png").convert_alpha()
box_R_des = " - Restart"
box_I_img = pygame.image.load("img\\helpassets\\box_I.png").convert_alpha()
box_I_des = " - Display Info."
box_Plus_img = pygame.image.load("img\\helpassets\\box_Plus.png").convert_alpha()
box_Plus_des = " - Zoom In"
box_Minus_img = pygame.image.load("img\\helpassets\\box_Minus.png").convert_alpha()
box_Minus_des = " - Zoom Out"
box_Left_img = pygame.image.load("img\\helpassets\\box_Left.png").convert_alpha()
box_Left_des = " - Previous Model"
box_Right_img = pygame.image.load("img\\helpassets\\box_Right.png").convert_alpha()
box_Right_des = " - Next Model"
box_Enter_img = pygame.image.load("img\\helpassets\\box_Enter.png").convert_alpha()
box_Enter_des = " - Change Model"
box_Z_img = pygame.image.load("img\\helpassets\\box_Z.png").convert_alpha()
box_Z_des = " - Previous Input"
box_X_img = pygame.image.load("img\\helpassets\\box_X.png").convert_alpha()
box_X_des = " - Next Input"
box_C_img = pygame.image.load("img\\helpassets\\box_C.png").convert_alpha()
box_C_des = " - Input Number"
box_V_img = pygame.image.load("img\\helpassets\\box_V.png").convert_alpha()
box_V_des = " - Confirm Changes"

box_img_list = [box_T_img, box_Y_img, box_P_img, box_R_img, box_I_img, box_Plus_img, box_Minus_img, box_Left_img, box_Right_img, box_Enter_img, box_Z_img, box_X_img, box_C_img, box_V_img]
box_description_list = [box_T_des, box_Y_des, box_P_des, box_R_des, box_I_des, box_Plus_des, box_Minus_des, box_Left_des, box_Right_des, box_Enter_des, box_Z_des, box_X_des, box_C_des, box_V_des]

#-Button Images
arrowright_btn_img = pygame.image.load("img\\buttons\\ArrowButton.png").convert_alpha()
arrowright_btn_img_clicked = pygame.image.load("img\\buttons\\ArrowButtonPressed.png").convert_alpha()
arrowleft_btn_img = pygame.transform.flip(arrowright_btn_img, True, False) #flip x but not y
arrowleft_btn_img_clicked = pygame.transform.flip(arrowright_btn_img_clicked, True, False)
arrow_width = arrowright_btn_img.get_width()
arrow_height = arrowright_btn_img.get_height()

start_btn_img = pygame.image.load("img\\buttons\\StartButton.png").convert_alpha()
start_btn_img_clicked = pygame.image.load("img\\buttons\\StartButtonPressed.png").convert_alpha()
load_btn_img = pygame.image.load("img\\buttons\\LoadButton.png").convert_alpha()
load_btn_img_clicked = pygame.image.load("img\\buttons\\LoadButtonPressed.png").convert_alpha()
quit_btn_img = pygame.image.load("img\\buttons\\QuitButton.png").convert_alpha()
quit_btn_img_clicked = pygame.image.load("img\\buttons\\QuitButtonPressed.png").convert_alpha()
menu_width = start_btn_img.get_width()
menu_height = start_btn_img.get_height()

help_btn_img = pygame.image.load("img\\buttons\\NeedHelpButton.png").convert_alpha()
help_width = help_btn_img.get_width()
help_height = help_btn_img.get_height()

confirm_btn_img = pygame.image.load("img\\buttons\\ConfirmButton.png").convert_alpha()
confirm_btn_img_clicked = pygame.image.load("img\\buttons\\ConfirmButtonPressed.png").convert_alpha()
confirm_width = confirm_btn_img.get_width()
confirm_height = confirm_btn_img.get_height()

input_btn_img = pygame.image.load("img\\buttons\\InputButton.png").convert_alpha()
input_btn_img_clicked = pygame.image.load("img\\buttons\\InputButtonPressed.png").convert_alpha()
input_width = input_btn_img.get_width()
input_height = input_btn_img.get_height()

pause_btn_img = pygame.image.load("img\\buttons\\IsPausedButton.png").convert_alpha()
pause_btn_img_clicked = pygame.image.load("img\\buttons\\IsUnpausedButton.png").convert_alpha() #clicked state of pause button
restart_btn_img = pygame.image.load("img\\buttons\\RestartButton.png").convert_alpha()
zoomin_btn_img = pygame.image.load("img\\buttons\\ZoomInButton.png").convert_alpha()
zoomout_btn_img = pygame.image.load("img\\buttons\\ZoomOutButton.png").convert_alpha()
hide_btn_img = pygame.image.load("img\\buttons\\HideButton.png").convert_alpha()
controls_length = pause_btn_img.get_width() #they are all same size so can use this, also they are squares so width = height

#---Functions---#
def draw_text(layer, text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    layer.blit(img, (x, y))

def draw_textbox(layer, text, font, topleft, text_size=False, text_color=(0,0,0), fill_color=(255,255,255), outline_color=(0,0,0), outline_width=-1, xoffset=0, yoffset=0, centre=False):
    #topleft is the topleft tuple of the outline
    #xoffset and yoffset are extra padding between start / end of text and touching inside of the outline
    text_size_actual = font.size(text) #size of text as a tuple
    if text_size == False: #text_size can be set to custom value, not necessarily actual 
        text_size = text_size_actual #this will cause box to change if text changes
    topleftoutline = (topleft[0] + outline_width / 2 + 1, topleft[1] + outline_width / 2 + 1) #extra 1 pixel as outline stems from 1 pixel linewidth
    topleftoffset = (topleftoutline[0] + xoffset, topleftoutline[1] + yoffset)
    total_width = text_size[0] + 2 * xoffset + outline_width
    total_height = text_size[1] + 2 * yoffset + outline_width

    pygame.draw.rect(layer, outline_color, (topleft[0], topleft[1], total_width, total_height), width = outline_width) #outline

    pygame.draw.rect(layer, fill_color, (topleftoutline[0], topleftoutline[1], total_width - outline_width - 1, total_height - outline_width - 1)) #fill

    if centre == False: #default
        text_pos = topleftoffset #normal, not centred; 
    else:
        text_pos = (topleftoffset[0] + (total_width - outline_width - 1) / 2 - text_size_actual[0] / 2, topleftoffset[1] + (total_height - outline_width - 1) / 2 - text_size_actual[1] / 2) #takes topleftoffset as (0, 0), then takes into account width and height of box, then width and height of text
    rendertext = font.render(text, True, text_color)
    layer.blit(rendertext, text_pos) #text now drawn

#---Drawing Layers---#
layer1centre = (layer1.get_width() / 2, layer1.get_height() / 2)
layer2centre = (layer2.get_width() / 2, layer2.get_height() / 2)

#doing up helplayer
helplayer.fill(TRANSPARENCY) #fill with transparent colour, otherwise default with black
helplayer.fill((150, 150, 150, 200)) #fill with slightly transparent colour, 4th value [0, 255] a measure if how transparent
for number in range(len(box_img_list[:7])): #splitting into halves, col 2 further in x direction to split up half the items
    #col 1
    helplayer.blit(box_img_list[number], (60, 100 + 75 * (number)))
    draw_text(helplayer, box_description_list[number], FuturaFont30, (255, 255, 255), 60 + 50, 100 + 75 * (number) + 15) #drawing descriptions after the letter (arbitrary values to make look nice)
    #col 2
    helplayer.blit(box_img_list[number + len(box_img_list[:7])], (360, 100 + 75 * (number)))
    draw_text(helplayer, box_description_list[number + len(box_img_list[:7])], FuturaFont30, (255, 255, 255), 360 + 50, 100 + 75 * (number) + 15)

#doing up introlayer
introlayer.fill((120, 120, 120))
introlayer.blit(intro_bg_img, (0, 0))
#text constants
modelling_w = FuturaFont100.size("MODELLING")[0]
modelling_h = FuturaFont100.size("MODELLING")[1]
#drawing name
draw_text(introlayer, "MODELLING", FuturaFont100, (255, 255, 255), SCREEN_WIDTH/4 - modelling_w/2, 50)
pygame.draw.rect(introlayer, (255, 255, 255), (SCREEN_WIDTH/4 - modelling_w/2, 50 + modelling_h, modelling_w, 10))
#drawing info
draw_text(introlayer, "\"Simulating Physical Systems with Lagrangian Mechanics\"", FuturaFont30, (255, 255, 255), 30, 150)
draw_text(introlayer, "Equations of Motion solved with the Euler-Cromer Method.", FuturaFont30, (255, 255, 255), 30, 200)
draw_text(introlayer, "Computations done in Python.", FuturaFont30, (255, 255, 255), 30, 230)
draw_text(introlayer, "Graphics with Pygame.", FuturaFont30, (255, 255, 255), 30, 260)
#credits
draw_text(introlayer, "Sean O Riordan; December 2021.", FuturaFont23, (255, 255, 255), SCREEN_WIDTH/4 - 110, SCREEN_HEIGHT - 40)
draw_text(introlayer, "email: seanie5011@hotmail.com", FuturaFont23, (255, 255, 255), SCREEN_WIDTH/4 - 110, SCREEN_HEIGHT - 20)

#---Groups---#
eom_group = [] #not actual pygame sprite groups
display_group = []

#---Models---#
#-Lists and other useful stuff
model_namelist = [] #contains the names of each model
model_eominitnames = [] #contains lists of names of a specific models initial conditions for eom
model_eominitvals = [] #contains lists of values of a specific models initial conditions for eom
model_displayinitnames = [] #contains lists of names of a specific models initial conditions for display
model_displayinitvals = [] #contains lists of values of a specific models initial conditions for display

#-Single Pendulum with Bob
model_namelist.append("Single Pendulum")

model_eominitnames.append(["theta", "omega", "l", "g", "gamma", "A", "B", "t", "dt", "FPS"])
model_eominitvals.append([30, 0, 2, 9.8, 0, 0, 0, 0, 0.001, FPS])
SP_Mass = SP.EOM(*model_eominitvals[0]) #the * unpacks the list to give theta, omega, l, g, gamma, A, B, t, dt, FPS
eom_group.append(SP_Mass)

model_displayinitnames.append(["mass_eom", "mass_color", "mass_radius", "stick_pos", "stick_color", "stick_width", "scale"])
model_displayinitvals.append([SP_Mass, BLUE, 20, (layer2centre[0], 0), GREY, 3, 500.0/SP_Mass.l])
SP_Manager = SP.SPPygame(*model_displayinitvals[0]) #the * unpacks the list to give mass_eom, mass_color, mass_radius, stick_pos, stick_color, stick_width, scale
display_group.append(SP_Manager)

#-Single Spring with Mass
model_namelist.append("Single Spring")

model_eominitnames.append(["x", "v", "k", "m", "g", "gamma", "A", "B", "t", "dt", "FPS"])
model_eominitvals.append([50, 0, 1, 1, 9.8, 0, 0, 0, 0, 0.001, FPS])
SS_Mass = SS.EOM(*model_eominitvals[1]) #the * unpacks the list
eom_group.append(SS_Mass)

model_displayinitnames.append(["mass_eom", "mass_color", "mass_width", "spring_pos", "spring_offset", "spring_color", "spring_width", "nodes"])
model_displayinitvals.append([SS_Mass, RED, 100, (0, layer2centre[1]), 250, GREY, 50, 10])
SS_Manager = SS.SPPygame(*model_displayinitvals[1]) #the * unpacks the list
display_group.append(SS_Manager)

#-Elastic Spring with Mass
model_namelist.append("Elastic Pendulum")

model_eominitnames.append(["x", "v", "theta", "omega", "k", "m", "l", "g", "gamma", "A", "B", "t", "dt", "FPS"])
model_eominitvals.append([1, 0, 60, 0, 10, 1, 10, 9.8, 0, 0, 0, 0, 0.001, FPS])
EP_Mass = EP.EOM(*model_eominitvals[2]) #the * unpacks the list
eom_group.append(EP_Mass)

model_displayinitnames.append(["mass_eom", "mass_color", "mass_radius", "scale", "spring_pos", "spring_offset", "spring_color", "spring_width", "nodes"])
model_displayinitvals.append([EP_Mass, RED, 20, 30, (layer2centre[0], 0), (0, 0), GREY, 50, 30])
EP_Manager = EP.SPPygame(*model_displayinitvals[2]) #the * unpacks the list
display_group.append(EP_Manager)

#-Double Pendulum
model_namelist.append("Double Pendulum")

model_eominitnames.append(["theta1", "omega1", "m1", "l1", "theta2", "omega2", "m2", "l2", "g", "gamma", "A", "B", "t", "dt", "FPS"])
model_eominitvals.append([120, 0, 1, 2, 30, 0, 1, 2, 9.8, 0, 0, 0, 0, 0.001, FPS])
DP_Mass = DP.EOM(*model_eominitvals[3]) #the * unpacks the list
eom_group.append(DP_Mass)

model_displayinitnames.append(["mass_eom", "mass1_color", "mass2_color", "mass_radius", "stick_pos", "stick_color", "stick_width", "scale"])
model_displayinitvals.append([DP_Mass, BLUE, RED, 20, (layer2centre[0], layer2centre[1]), GREY, 3, 150.0/DP_Mass.l1])
DP_Manager = DP.SPPygame(*model_displayinitvals[3]) #the * unpacks the list to give mass_eom, mass_color, mass_radius, stick_pos, stick_color, stick_width, scale
display_group.append(DP_Manager)

#-Double Pendulum 1 Spring
model_namelist.append("x2 Pend with Spring")

model_eominitnames.append(["x", "v", "theta1", "omega1", "m1", "l1", "theta2", "omega2", "m2", "l2", "g", "k", "gamma", "A", "B", "t", "dt", "FPS"])
model_eominitvals.append([0, 0, 0, 0, 1, 2, 0, 0, 1, 2, 9.8, 10, 0, 0, 0, 0, 0.001, FPS])
DP1S_Mass = DP1S.EOM(*model_eominitvals[4]) #the * unpacks the list
eom_group.append(DP1S_Mass)

model_displayinitnames.append(["mass_eom", "mass1_color", "mass2_color", "mass_radius", "stick_pos", "stick_color", "stick_width", "spring_width", "nodes", "scale"])
model_displayinitvals.append([DP1S_Mass, BLUE, RED, 20, (layer2centre[0], layer2centre[1]), GREY, 3, 50, 30, 150.0/DP_Mass.l1])
DP1S_Manager = DP1S.SPPygame(*model_displayinitvals[4]) #the * unpacks the list to give mass_eom, mass_color, mass_radius, stick_pos, stick_color, stick_width, scale
display_group.append(DP1S_Manager)

#save initial values for reuse:
model_eominitvals_true = [row[:] for row in model_eominitvals]
model_displayinitvals_true = [row[:] for row in model_displayinitvals]

#---Buttons---#
#some lengths and distances to shorten names
use_width = (SCREEN_WIDTH / 2 - 100) / 2 #half of width of space to work with for these
menu_heightscale = 75/menu_height
arrow_heightscale = 100/arrow_height
confirm_heightscale = 50/confirm_height
input_heightscale = 50/input_height
#menu screen buttons - menu_width/2
start_btn = button.Button(SCREEN_WIDTH/4 - 150/2, 100, start_btn_img, menu_heightscale, False, start_btn_img_clicked, 100) #x, y, image, scale=1, mask=False, pressed=False, cooldown=0
load_btn = button.Button(SCREEN_WIDTH/4 - 75, 200, load_btn_img, menu_heightscale, False, load_btn_img_clicked, 100)
quit_btn = button.Button(SCREEN_WIDTH/4 - 75, 300, quit_btn_img, menu_heightscale, False, quit_btn_img_clicked, 100)
#help button
help_btn = button.Button(use_width - help_width/2 * 50/help_height, 600, help_btn_img, 50/help_height, pressed=help_btn_img)
#changing model index
modelindex_plus_btn = button.Button(use_width + 200, 75, arrowright_btn_img, arrow_heightscale, False, arrowright_btn_img_clicked, 100) #x, y, image, scale=1, mask=False, pressed=False, cooldown=0
modelindex_minus_btn = button.Button(use_width - arrow_width * arrow_heightscale - 200, 75, arrowleft_btn_img, arrow_heightscale, False, arrowleft_btn_img_clicked, 100) #have to adjust in x for the fact that image spawns at topleft position
modelindex_c_btn = button.Button(use_width + 80, 185, confirm_btn_img, confirm_heightscale, False, confirm_btn_img_clicked, 200) #values are arbitrary just to get what looks good
#changing inputs index
inputindex_plus_btn = button.Button(use_width + 200, 275, arrowright_btn_img, arrow_heightscale, False, arrowright_btn_img_clicked, 100) #x, y, image, scale=1, mask=False, pressed=False, cooldown=0
inputindex_minus_btn = button.Button(use_width - arrow_width * arrow_heightscale - 200, 275, arrowleft_btn_img, arrow_heightscale, False, arrowleft_btn_img_clicked, 100) #have to adjust in x for the fact that image spawns at topleft position
inputindex_i_btn = button.Button(use_width + 80, 400, input_btn_img, input_heightscale, False, input_btn_img_clicked, 200) #values are arbitrary just to get what looks good
inputindex_c_btn = button.Button(use_width + 80, 455, confirm_btn_img, confirm_heightscale, False, confirm_btn_img_clicked, 200) #values are arbitrary just to get what looks good
#textbox
input_textbox = textbox.TextBox(use_width - 175, 400, FuturaFont50, 250, 50, ani=True, outline_width=2, border_radius=5) #x, y, font, width, height, ani=False, text_color=(0,0,0), fill_color=(255,255,255), outline_width=0, border_radius=0
#controls
pause_btn = button.Button(2 * use_width + 1, 0, pause_btn_img, 100/controls_length, pressed=pause_btn_img_clicked) #only changes when clicked, no timer
restart_btn = button.Button(2 * use_width + 1, 100, restart_btn_img, 100/controls_length)
zoomin_btn = button.Button(2 * use_width + 1, 200, zoomin_btn_img, 100/controls_length) 
zoomout_btn = button.Button(2 * use_width + 1, 300, zoomout_btn_img, 100/controls_length) 
hide_btn = button.Button(2 * use_width + 1, 400, hide_btn_img, 100/controls_length) 

#---Time---#
#dont actually need to define these at all but sure
model_start = time.time()
model_now = time.time()
model_elapsed = model_now - model_start

#---Last exception checks before running---#
if len(model_namelist) != len(display_group):
    print("\n!!! Error: NameList does not have same number of elements as Displaygroup. !!!\n")
    run = False

#---Game States---#
class GameState():
    def __init__(self): #define constants and whatnot used
        self.state = "menu" #state shown starts as main

        #--Main Initialise--#
        #-Define Constants-#
        self.model_use_index = 0
        self.model_index = self.model_use_index
        self.input_index = 0
        self.is_updating = True

        self.input_text_test = "0"
        self.input_text = float(self.input_text_test)

        self.zoom = 1 #how much zoom, > 1 zooms in, < 1 zooms out (max 1.5, min 0.5)

        self.hide = False #whether or not to hide timer

        #-Time-#
        self.model_start = time.time()
        self.model_now = time.time()
        self.model_elapsed = self.model_now - self.model_start

    def menu(self, events_list):
        run = True
        for event in events_list: #now can keep event handling seperate to game loop
            #---Keys---# !!NOTE THAT PYGAME.QUIT NOT REFERENCED HERE, IN GAME LOOP ONLY!!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #always able to press escape
                    run = False #local variable, need to return it

        layer0.fill(BLACK)
        layer1.fill(BG)
        layer1.blit(bg_img, (0, 0)) #blit onto layer1 the gradient background image

        layer1.blit(introlayer, (SCREEN_WIDTH / 2, 0)) #blit onto layer1 the intro information
        pygame.draw.line(layer1, BLACK, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, layer2.get_height()), 3)

        if start_btn.draw(layer1) == True:
            self.state = "main"
            #--Main Re-Initialise--#
            #-Define Constants-#
            self.model_use_index = 0
            self.model_index = self.model_use_index
            self.input_index = 0
            self.is_updating = True

            self.input_text_test = "0"
            self.input_text = float(self.input_text_test)

            self.zoom = 1 #how much zoom, > 1 zooms in, < 1 zooms out (max 1.5, min 0.5)

            self.hide = False #whether or not to hide timer

            #-Model-#
            model_eominitvals[:] = [row[:] for row in model_eominitvals_true] #resetting input values that are displayed, have to call [:] as otherwise it thinks its a local variable
            for i in range(len(eom_group)): #reset all to complete initial conditions
                eom_group[i].true_reinit()
                display_group[i].true_reinit()

            #-Textbox-#
            input_textbox.reinit()

            #-Time-#
            self.model_start = time.time()
            self.model_now = time.time()
            self.model_elapsed = self.model_now - self.model_start

        if load_btn.draw(layer1) == True: #load from whats already been run (maybe do some file stuff that saves to file your current conditions?)
            self.state = "main"
            self.model_start += abs(time.time() - self.model_now)

        if quit_btn.draw(layer1) == True: #quit the game
            run = False

        layer0.blit(layer1, (0, 0))

        return run

    def main(self, events_list):
        for event in events_list: #pass in events list as can only have one pygame.events.get() call, pass in list of events (behaves the same, just a work around)
            #---Keys---# !!NOTE THAT PYGAME.QUIT NOT REFERENCED HERE, IN GAME LOOP ONLY!!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #always able to press escape
                    self.state = "menu"

                if input_textbox.setting_text(event) == False: #if not clicked on textbox
                    #-Traces
                    if event.key == pygame.K_t:
                        display_group[self.model_use_index].tracing = not display_group[self.model_use_index].tracing #turns on and off tracing display
                    if event.key == pygame.K_y:
                        display_group[self.model_use_index].reset_tracing()

                    #-Pause Model
                    if event.key == pygame.K_p:
                        self.is_updating = not self.is_updating
                        self.model_start += abs(time.time() - self.model_now) #add the time between last time update and when unpausing, add this to the start to essentially move the 0 time and fix

                        pause_btn.since_clicked = not pause_btn.since_clicked #ensure onscreen button is updated

                    #-Resetting
                    if event.key == pygame.K_r:
                        eom_group[self.model_use_index].reinit()
                        display_group[self.model_use_index].reinit()
                        self.model_start = time.time()
                        self.model_now = time.time()
                        self.model_elapsed = self.model_now - self.model_start

                    #-Changing Model
                    if event.key == pygame.K_RIGHT:
                        if self.model_index < len(model_namelist) - 1:
                            self.model_index += 1

                            modelindex_plus_btn.image_used = modelindex_plus_btn.pressed_img #update on screen button
                            modelindex_plus_btn.update_time = pygame.time.get_ticks()
                            modelindex_plus_btn.pressed_incooldown = True 

                    if event.key == pygame.K_LEFT: #decide on model index
                        if self.model_index > 0:
                            self.model_index -= 1

                            modelindex_minus_btn.image_used = modelindex_minus_btn.pressed_img #update on screen button
                            modelindex_minus_btn.update_time = pygame.time.get_ticks()
                            modelindex_minus_btn.pressed_incooldown = True 

                    if event.key == pygame.K_RETURN: #confirms change in model
                        if self.model_use_index != self.model_index:
                            self.model_use_index = self.model_index
                            eom_group[self.model_use_index].reinit()
                            display_group[self.model_use_index].reinit()
                            self.model_start = time.time()
                            self.model_now = time.time()
                            self.model_elapsed = self.model_now - self.model_start

                            if self.input_index > len(model_eominitnames[self.model_use_index]): #incase input index is too big for this model
                                self.input_index = len(model_eominitnames[self.model_use_index])

                            modelindex_c_btn.image_used = modelindex_c_btn.pressed_img #update on screen button
                            modelindex_c_btn.update_time = pygame.time.get_ticks()
                            modelindex_c_btn.pressed_incooldown = True

                    #-Zoom
                    if event.key == pygame.K_EQUALS and self.zoom < 1.2: #equals is where plus is
                        self.zoom += 0.1

                    if event.key == pygame.K_MINUS and self.zoom > 0.8:
                        self.zoom -= 0.1

                    #-Hide
                    if event.key == pygame.K_i:
                        self.hide = not self.hide #hidden / unhidden

                    #-Changing Conditions for that model
                    if event.key == pygame.K_x: #acts like moving arrow right
                        if self.input_index < len(model_eominitnames[self.model_use_index]) - 1:
                            self.input_index += 1

                            inputindex_plus_btn.image_used = inputindex_plus_btn.pressed_img #update on screen button
                            inputindex_plus_btn.update_time = pygame.time.get_ticks()
                            inputindex_plus_btn.pressed_incooldown = True 
                    if event.key == pygame.K_z: #acts like moving arrow left
                        if self.input_index > 0:
                            self.input_index -= 1

                            inputindex_minus_btn.image_used = inputindex_minus_btn.pressed_img #update on screen button
                            inputindex_minus_btn.update_time = pygame.time.get_ticks()
                            inputindex_minus_btn.pressed_incooldown = True 
                    #Confirm change
                    if event.key == pygame.K_c:
                        if model_eominitnames[self.model_use_index][self.input_index] != "FPS": #cant alter FPS
                            model_eominitvals[self.model_use_index][self.input_index] = self.input_text #set this particular val to input

                            inputindex_i_btn.image_used = modelindex_c_btn.pressed_img #update on screen button
                            inputindex_i_btn.update_time = pygame.time.get_ticks()
                            inputindex_i_btn.pressed_incooldown = True
                    #Implement changes
                    if event.key == pygame.K_v:
                        eom_group[self.model_use_index].changeinit(*model_eominitvals[self.model_use_index]) #reset model with new initial conditions
                        display_group[self.model_use_index].changeinit(*model_displayinitvals[self.model_use_index])

                        self.model_start = time.time()
                        self.model_now = time.time()
                        self.model_elapsed = self.model_now - self.model_start

        layer0.fill(BLACK)
        layer1.fill(BG)
        layer2.fill(WHITE)

        if self.is_updating == True:
            display_group[self.model_use_index].update()
            self.model_elapsed = self.model_now - self.model_start
            self.model_now = time.time()
        display_group[self.model_use_index].draw(layer2, self.zoom)

        layer1.blit(bg_img, (0, 0)) #blit onto layer1
        layer1.blit(layer2, ((SCREEN_WIDTH / 2, 0))) #then this above it

        #then these
        if self.hide == False: #whether or not they are hidden
            draw_textbox(layer1, "Time: {0:0.3f} s".format(self.model_elapsed), FuturaFont30, (layer1.get_width() / 2, layer2.get_height() - 25), (160, 30), outline_width=3, xoffset=5, yoffset=5) #layer, text, font, topleft, text_size=False, text_color=(0,0,0), fill_color=(255,255,255), outline_color=(0,0,0), outline_width=-1, xoffset=0, yoffset=0, centre=False
            draw_textbox(layer1, "Zoom: {0}%".format(int(self.zoom * 100)), FuturaFont30, (layer1.get_width() / 2, layer2.get_height() - 25 - 30), (160, 18), outline_width=3, xoffset=5, yoffset=5) #current zoom percent
        pygame.draw.line(layer1, BLACK, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, layer2.get_height()), 3)

        layer0.blit(layer1, (0, 0)) #finally blit all onto layer 0

        #-Button Render and some logic
        #Model Index
        if modelindex_plus_btn.draw(layer0) == True and self.model_index < len(model_namelist) - 1: #testing button, also draws at same time!
            self.model_index += 1
        elif modelindex_minus_btn.draw(layer0) == True and self.model_index > 0:
            self.model_index -= 1
        draw_textbox(layer0, "{0}".format(model_namelist[self.model_index]), FuturaFont50, (use_width - 175, 74), text_size=(350, 100), outline_width=5, centre=True)
        if modelindex_c_btn.draw(layer0) == True:
            if self.model_use_index != self.model_index:
                    self.model_use_index = self.model_index
                    eom_group[self.model_use_index].reinit()
                    display_group[self.model_use_index].reinit()
                    self.model_start = time.time()
                    self.model_now = time.time()
                    self.model_elapsed = self.model_now - self.model_start

                    if self.input_index > len(model_eominitnames[self.model_use_index]): #incase input index is too big for this model
                        self.input_index = len(model_eominitnames[self.model_use_index])
                
        #Input - textbox
        self.input_text_test = input_textbox.draw(layer0)
        if input_textbox.entered == True: #if clicked off text box or entered
            input_textbox.entered = False
            try:
                self.input_text = float(self.input_text_test)
            except:
                for c in self.input_text_test: #see testing project for explanations
                    if not str.isdigit(c):
                        self.input_text_test = self.input_text_test.replace(c, "")
                if self.input_text_test == "": #if nothing inputted, input 0
                    self.input_text = 0
                else:
                    self.input_text = float(self.input_text_test)
        #Input Index - see buttons z, x, c, v
        if inputindex_plus_btn.draw(layer0) == True and self.input_index < len(model_eominitnames[self.model_use_index]) - 1: #left and right buttons
            self.input_index += 1
        elif inputindex_minus_btn.draw(layer0) == True and self.input_index > 0:
            self.input_index -= 1
        draw_textbox(layer0, "{0}: {1:0.3f}".format(model_eominitnames[self.model_use_index][self.input_index], model_eominitvals[self.model_use_index][self.input_index]), FuturaFont50, (use_width - 175, 274), text_size=(350, 100), outline_width=5, centre=True)
        if inputindex_i_btn.draw(layer0) == True: #sets vals to this on screen
            if model_eominitnames[self.model_use_index][self.input_index] != "FPS": #cant alter FPS
                model_eominitvals[self.model_use_index][self.input_index] = self.input_text
        if inputindex_c_btn.draw(layer0) == True: #confirms inputs and resets the model
            eom_group[self.model_use_index].changeinit(*model_eominitvals[self.model_use_index])
            display_group[self.model_use_index].changeinit(*model_displayinitvals[self.model_use_index])

            self.model_start = time.time()
            self.model_now = time.time()
            self.model_elapsed = self.model_now - self.model_start

        #Help Button
        help_btn.draw(layer0) #will draw button
        if help_btn.since_clicked == False: #if it has been clicked, will flip back and forth (False is clicked so display it, True is not clicked so dont blit)
            layer0.blit(helplayer, (SCREEN_WIDTH/2, 0)) #will display over layer 0

        #Controls - in buttons too
        if pause_btn.draw(layer0) == True:
            self.is_updating = not self.is_updating #pauses
            self.model_start += abs(time.time() - self.model_now)
        if restart_btn.draw(layer0) == True:
            eom_group[self.model_use_index].reinit()
            display_group[self.model_use_index].reinit()
            self.model_start = time.time()
            self.model_now = time.time()
            self.model_elapsed = self.model_now - self.model_start
        if zoomin_btn.draw(layer0) == True and self.zoom < 1.2:
            self.zoom += 0.1
        if zoomout_btn.draw(layer0) == True and self.zoom > 0.8:
            self.zoom -= 0.1
        if hide_btn.draw(layer0) == True:
            self.hide = not self.hide

game_state = GameState()

#---Game Loop---#
while run: #while run is true
    events_list = pygame.event.get() #list of all events, instead of calling in for loop, call here and assign variable
    for event in events_list: #always want to be able to quit
        #---Quit Game---#
        if event.type == pygame.QUIT:
            run = False
    
    if game_state.state == "menu":
        run = game_state.menu(events_list) #if press escape, run = False and 
    if game_state.state == "main":
        game_state.main(events_list)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()