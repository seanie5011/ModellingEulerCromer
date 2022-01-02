import pygame

class TextBox():
    def __init__(self, x, y, font, width, height, ani=False, text_color=(0,0,0), fill_color=(255,255,255), outline_width=0, border_radius=0):
        self.font = font
        self.width = width
        self.height = height
        self.text_color = text_color
        self.fill_color = fill_color

        self.clicked = False #whether or not clicked in this loop
        self.since_clicked = False #whether or not in clicked state

        self.outline_width = outline_width
        if outline_width <= 0: #if 0, then will just be self.rect but empty, if < 0, then wont draw
            self.rectoutline = pygame.Rect((x, y), (width, height)) #(x, y) are topleft coords
            self.rect = self.rectoutline
        else: #if an even outline, same amount of pixels on either side, but with one extra pixel to the right of the x, and below the y (so in positive y direction) #if an odd outline, same amount of pixels on either side
            extrapixels = 2 * (outline_width) #total extra pixels
            totalx = width + extrapixels
            totaly = height + extrapixels
            self.rectoutline = pygame.Rect((x, y), (totalx, totaly))
            self.rect = pygame.Rect((x + extrapixels / 2, y + extrapixels / 2), (width, height))

        self.ani = ani #whether or not we want animation of grey line
        self.draw_ani = False #whether or not we draw it in this loop
        offsetx = int(width / 10.0) #one tenth of length will always be left free (will start one tenth of total away)
        offsety = int(height / 10.0)
        endy = height - 2 * offsety #total length of line
        self.ani_startpos = (self.rect.x + offsetx, self.rect.y + offsety)
        self.ani_startpos_initial = self.ani_startpos #keep track of where text starts
        self.ani_endpos = (self.rect.x + offsetx, self.rect.y + offsety + endy)
        self.ani_endpos_initial = self.ani_endpos

        self.usable_x = (self.rect.x + width - offsetx) - (self.rect.x + offsetx) #finding how much space text can have, finding difference between final and initial points in x direction
        self.usable_y = (self.rect.y + height - offsety) - (self.rect.y + offsety)

        self.border_radius = border_radius

        self.text = ""

        self.rendertot = 0 #can fit no letters, if 1 can fit 1 letter etc.
        test_text = ""
        while self.font.size(test_text + "a")[0] < self.usable_x: #while test plus next letter is smaller than usable space
            test_text += "a" #keep adding a letter until test is bigger than usable_x
            self.rendertot += 1
        self.rendersize = self.font.size("a") #width and height of one test letter

        self.str_start = 0 #where text starts
        self.str_end = 0 #where text ends
        self.str_index = 0 #where bar goes
        self.displaytext = self.text[self.str_start:self.str_end]

        self.entered = False

    def reinit(self):
        self.clicked = False #whether or not clicked in this loop
        self.since_clicked = False #whether or not in clicked state

        self.text = ""

        self.str_start = 0 #where text starts
        self.str_end = 0 #where text ends
        self.str_index = 0 #where bar goes
        self.displaytext = self.text[self.str_start:self.str_end]

        self.entered = False


    def setting_text(self, event): #do for all events, as this does the event check here
        if self.since_clicked == True: #if textbox activated, then buttons do this, will have to make sure there is an if statement in main while loop
            passed = True #tells us that the text box was clicked
            self.entered = False #now no longer being entered
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: #resets textbox completely
                    self.clicked = False
                    self.since_clicked = False
                    action = False
                    self.update_time = pygame.time.get_ticks()
                    self.str_start = 0 #where text starts
                    self.text = ""
                    self.str_end = 0 #where text ends
                    self.str_index = 0 #where bar goes
                    self.displaytext = self.text[self.str_start:self.str_end]
                    self.ani_startpos = self.ani_startpos_initial #keep track of where text starts
                    self.ani_endpos = self.ani_endpos_initial
                    self.entered = True
                if event.key == pygame.K_RETURN: #pressing enter has same effect as clicking outside box
                    self.clicked = False
                    self.since_clicked = False
                    action = False
                    self.update_time = pygame.time.get_ticks()
                    self.entered = True #tells us that it has been inputted
                elif event.key == pygame.K_BACKSPACE: #removes one letter
                    if len(self.text) > 0 and self.str_index != 0: #make sure there is stuff to remove
                        self.text = self.text[:self.str_index - 1] + self.text[self.str_index:]
                        self.str_index -= 1 #must decrement as new letter moves everything up
                        if self.str_start != 0: #if it is at zero, dont want to move backwards
                            self.str_start -= 1
                            self.str_end -= 1
                        elif self.str_end - 1 >= len(self.text): #unless the end is over usable_x, then want to move it back one
                            self.str_end -= 1
                elif event.key != pygame.K_RIGHT and event.key != pygame.K_LEFT: #pressing any other key
                    self.text = self.text[:self.str_index] + event.unicode + self.text[self.str_index:] #gives a string of that key just pressed, place at index
                    if self.str_index == self.str_end: #if placing at end of word
                        if abs(self.str_start - self.str_end) == self.rendertot: #if all usable_x is taken up, want to move start up
                            self.str_start += 1
                        self.str_end += 1 #when placing at end, always want end to move up
                    self.str_index += 1

                if event.key == pygame.K_RIGHT:
                    if self.str_index == self.str_end and self.str_end != len(self.text): #Call (1) and (2), (1) means that index is at the end of displayed, (2) means that displayed end is not actual end
                        self.str_index += 1
                        self.str_end += 1
                        self.str_start += 1
                    if self.str_index != self.str_end and self.str_index != len(self.text): #Call (3) and (4), (3) means that index is not at the end of displayed, (4) means that index is not at actual end (cant go right if at end)
                        self.str_index += 1 #^works cause its doing check again

                if event.key == pygame.K_LEFT:
                    if self.str_index == self.str_start and self.str_start != 0: #checking that we are at start but start isnt zero
                        self.str_index -= 1
                        self.str_end -= 1
                        self.str_start -= 1
                    if self.str_index != self.str_start and self.str_index != 0: #check we arent at start and start isnt zero
                        self.str_index -= 1
                #note that left and right both ustilise the fact that even if statement (1) works, (2) can now also work (even if before statement (1) they wouldnt work)

                anitext_size = self.font.size(self.text[self.str_start:self.str_index]) #where to put flashing bar
                self.ani_startpos = (self.ani_startpos_initial[0] + anitext_size[0], self.ani_startpos_initial[1])
                self.ani_endpos = (self.ani_endpos_initial[0] + anitext_size[0], self.ani_endpos_initial[1]) #tuples are immutable, basically cant change individual elements directly, need to fully reassign
                self.displaytext = self.text[self.str_start:self.str_end] #update display
        else:
            passed = False #tells us that the text box was not clicked

        return passed

    def draw(self, surface):
        #initialise stuff
        action = False
        cooldown = 500

        #check animation of textline
        if self.since_clicked == True:
            if self.ani == True and pygame.time.get_ticks() - self.update_time > cooldown: #how much time it stays up and disappears
                self.update_time = pygame.time.get_ticks()
                self.draw_ani = not self.draw_ani
        else:
            self.draw_ani = False #if not clicked on, then dont draw

        #get mouse pos:
        pos = pygame.mouse.get_pos()
        #check if mouse on rect:
        if self.rectoutline.collidepoint(pos): #includes outline in button
            if pygame.mouse.get_pressed()[0] and self.clicked == False: #0 is left click, 1 is middle, 2 is right
                self.clicked = True
                self.since_clicked = not self.since_clicked
                action = not action
                self.update_time = pygame.time.get_ticks()
        elif pygame.mouse.get_pressed()[0]: #if a click but not on button, then act as if button was never clicked
            self.clicked = False
            self.since_clicked = False
            action = False
            self.update_time = pygame.time.get_ticks()
            self.entered = True #tells us that it has been inputted, this is for the clicking not on it part! if get rid of this, must press enter to have self.entered = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        #draw to screen:
        if self.outline_width <= 0: #if there is an outline, the outline takes the border radius
            pygame.draw.rect(surface, self.fill_color, self.rect, width = 0, border_radius = self.border_radius) #fill
        else:
            pygame.draw.rect(surface, self.text_color, self.rectoutline, width = self.outline_width, border_radius = self.border_radius) #outline
            pygame.draw.rect(surface, self.fill_color, self.rect, width = 0, border_radius = 0) #fill

        if self.draw_ani == True: #textline animate
            pygame.draw.line(surface, self.text_color, self.ani_startpos, self.ani_endpos)

        #rendering
        textrender = self.font.render(self.displaytext, True, self.text_color)
        surface.blit(textrender, (self.ani_startpos_initial[0] ,self.ani_startpos_initial[1] + self.usable_y / 2 - self.rendersize[1] / 2))

        return self.text