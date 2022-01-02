import pygame

#different to other button, now uses masks!
class Button():
    def __init__(self, x, y, image, scale=1, mask=False, pressed=False, cooldown=0):
        width = image.get_width()
        self.width = int(width * scale) #scaling correctly
        height = image.get_height()
        self.height = int(height * scale)

        self.image = pygame.transform.scale(image, (self.width, self.height)) #scale to correct dimensions
        self.image_used = self.image #by default use this image when blitting
        self.since_clicked = True #records what image its on, True is self.image, False is clicked image

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) #self.rect.x and self.rect.y are (x, y) which are topleft coords

        self.clicked = False

        self.mask = pygame.mask.from_surface(self.image, threshold = 0) #only contains anything that isnt transparent
        self.draw_mask = mask #whether to draw mask or image

        if pressed == False: #input either False if image doesnt change when clicked, otherwise need to input the new image
            self.pressed_state = False
            self.pressed_time = False
            self.pressed_incooldown = False
        else:
            self.pressed_state = True #determines if image changes or not
            self.pressed_img = pygame.transform.scale(pressed, (self.width, self.height)) #new image
            self.pressed_incooldown = False #whether we are in cooldown period of the button being pressed

        self.update_time = pygame.time.get_ticks() #current tick
        self.cooldown = cooldown

    def draw(self, surface):
        action = False
        if self.pressed_state == True and self.cooldown == 0: #essentially, this should cause image to just change back and forth only when clicked, not on timer
            if self.since_clicked == True:
                self.image_used = self.image #True is original
            else:
                self.image_used = self.pressed_img #False is clicked
        else:
            if self.pressed_incooldown == False: #if the button hasnt been clicked recently
                self.image_used = self.image #image used depends on whether or not there is a different image when clicked and whether or not is clicked, by default is original
            elif pygame.time.get_ticks() - self.update_time > self.cooldown: #when outside of cooldown, revert back to original image, this is to add more time to see the pressed image
                self.update_time = pygame.time.get_ticks()
                self.image_used = self.image
                self.pressed_incooldown = False
        #get mouse pos:
        pos = pygame.mouse.get_pos()
        #mask spawns at (0, 0), so wanna offset pos by (x, y)
        offset_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y) #think of moving mouse position by moving (x, y) to the origin
        #check if mouse on rect:
        try:
            if self.mask.get_at(offset_pos):
                if pygame.mouse.get_pressed()[0] and self.clicked == False: #0 is left click, 1 is middle, 2 is right
                    self.clicked = True
                    action = True
                    if self.pressed_state == True: #if there is another image
                        self.image_used = self.pressed_img #change which is blitted
                        self.update_time = pygame.time.get_ticks()
                        self.pressed_incooldown = True #start cooldown
                        self.since_clicked = not self.since_clicked #tells the button to change to next image

        except IndexError: #will give index error if mouse is not on mask, not important can just ignore
            pass

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        if self.draw_mask == True:
            #can draw mask
            masklist = self.mask.outline()
            for index, point in enumerate(masklist):
                masklist[index] = (masklist[index][0] + self.rect.x, masklist[index][1] + self.rect.y) #adding (x, y) to each point to draw mask where it actually is
            pygame.draw.polygon(surface, (200,150,150), masklist, 0)
            pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y, self.width, self.height), width = 1) #outline of full rect
        else:
            #draw to screen:
            surface.blit(self.image_used, (self.rect.x, self.rect.y))

        return action
