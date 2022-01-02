import pygame, math, time
from pygame import gfxdraw #might be experimental? if code breakes, check this
import spring #relies on other file spring.py for drawing

#---Classes---#
class EOM():
    def __init__(self, x, v, k, m, g, gamma, A, B, t, dt, FPS): #note that equilibrium position will be at end of spring for convenience of drawing
        self.x = x #position
        self.v = v #velocity
        self.a = 0 #=acceleration

        self.k = k #spring constant
        self.m = m #mass
        self.g = g #gravity

        self.gamma = gamma #damping constant

        self.A = A #amplitude of driving force
        self.B = B #frequency of driving force

        self.t = t #time elapsed seconds
        self.dt = dt #deltatime, for the Euler-Cromer Method
        self.iterations = int((1/FPS) / self.dt) #how many dts give 1 frametime
        
        self.pos = (self.x, 0) #initial position of mass of spring

        self.reinit_list = [self.x, self.v, self.a, self.k, self.m, self.g, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos] #saves initial values
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.x = self.true_reinit_list[0]
        self.v = self.true_reinit_list[1]
        self.a = self.true_reinit_list[2]

        self.k = self.true_reinit_list[3]
        self.m = self.true_reinit_list[4]
        self.g = self.true_reinit_list[5]

        self.gamma = self.true_reinit_list[6]

        self.A = self.true_reinit_list[7]
        self.B = self.true_reinit_list[8]

        self.t = self.true_reinit_list[9]
        self.dt = self.true_reinit_list[10]
        self.iterations = self.true_reinit_list[11]
        
        self.pos = self.true_reinit_list[12]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the EOM to initial conditions
        self.x = self.reinit_list[0]
        self.v = self.reinit_list[1]
        self.a = self.reinit_list[2]

        self.k = self.reinit_list[3]
        self.m = self.reinit_list[4]
        self.g = self.reinit_list[5]

        self.gamma = self.reinit_list[6]

        self.A = self.reinit_list[7]
        self.B = self.reinit_list[8]

        self.t = self.reinit_list[9]
        self.dt = self.reinit_list[10]
        self.iterations = self.reinit_list[11]
        
        self.pos = self.reinit_list[12]

    def changeinit(self, x, v, k, m, g, gamma, A, B, t, dt, FPS): #exact same as init, changes initial values
        try:
            self.x = x #position
            self.v = v #velocity
            self.a = 0 #=acceleration

            self.k = k #spring constant
            self.m = m #mass
            self.g = g #gravity

            self.gamma = gamma #damping constant

            self.A = A #amplitude of driving force
            self.B = B #frequency of driving force

            self.t = t #time elapsed seconds
            self.dt = dt #deltatime, for the Euler-Cromer Method
            self.iterations = int((1/FPS) / self.dt) #how many dts give 1 frametime
        
            self.pos = (self.x, 0) #initial position of mass of spring

            self.reinit_list = [self.x, self.v, self.a, self.k, self.m, self.g, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos] #saves initial values
        except:
            self.reinit()

    def update(self):
        for i in range(self.iterations): #do the method at dt until 1/FPS seconds have passed, then draw this
            self.a = (-self.k / self.m) * self.x #standard motion
            self.a += (-self.gamma / self.m) * self.v #damping, velocity dependant
            self.a += self.A * math.cos(self.B * self.t) #driving force, no dependance on system

            self.v += self.a * self.dt

            self.x += self.v * self.dt

            self.pos = (self.x, 0)

            self.t += self.dt

class SPPygame(pygame.sprite.Sprite): #draws the pendulum to any surface (passed in the draw method)
    def __init__(self, mass_eom, mass_color, mass_width, spring_pos, spring_offset, spring_color, spring_width, nodes):
        pygame.sprite.Sprite.__init__(self)

        self.zoom = 1

        self.m = mass_eom
        self.m_color = mass_color
        self.m_width = mass_width

        self.s_color = spring_color
        self.start_pos = spring_pos #where the base of the spring is
        self.s_width = spring_width
        self.spring_offset = spring_offset
        self.end_pos = (int(spring_pos[0] + self.m.pos[0] + self.spring_offset), int(spring_pos[1] + self.m.pos[1])) #treat the spring_pos as the new origin, add the position of the mass, scaled by whatever factor
        self.newzero = spring_pos #where to place the drawings in a new zero point (moving the origin)

        self.make_spring = spring.Spring(self.start_pos, self.end_pos, self.s_width, nodes, lead1=25, lead2=25, line_width=3, line_color=spring_color) #start_pos, end_pos, spring_width, nodes, node_draw=False, node_color=(0,0,0), node_radius=0, lead1=0, lead2=0, line_width=1, line_color=(0,0,0)
        self.make_spring.end_pos = (self.end_pos[0] - int(self.m_width/2 * self.zoom), self.end_pos[1]) #shift end_pos of spring to start of block

        self.list_points = [self.end_pos] #all the positions of the centre of the mass

        self.tracing = True

        self.reinit_list = [self.m, self.m_color, self.m_width, self.s_color, self.start_pos, self.end_pos, self.spring_offset, self.s_width, self.make_spring, self.newzero, self.list_points[:], self.tracing] #use the [:] to save lists, this creates a copy of the list that is not tied to the original
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.m = self.true_reinit_list[0]
        self.m_color = self.true_reinit_list[1]
        self.m_width = self.true_reinit_list[2]

        self.s_color = self.true_reinit_list[3]
        self.start_pos = self.true_reinit_list[4]
        self.end_pos = self.true_reinit_list[5]
        self.spring_offset = self.true_reinit_list[6]
        self.s_width = self.true_reinit_list[7]
        self.make_spring = self.true_reinit_list[8]
        self.newzero = self.true_reinit_list[9]

        self.list_points = self.true_reinit_list[10][:]

        self.tracing = self.true_reinit_list[11]

        self.reinit_list = self.true_reinit_list[:]

        self.zoom = 1


    def reinit(self): #resets the Display to initial conditions
        self.m = self.reinit_list[0]
        self.m_color = self.reinit_list[1]
        self.m_width = self.reinit_list[2]

        self.s_color = self.reinit_list[3]
        self.start_pos = self.reinit_list[4]
        self.end_pos = self.reinit_list[5]
        self.spring_offset = self.reinit_list[6]
        self.s_width = self.reinit_list[7]
        self.make_spring = self.reinit_list[8]
        self.newzero = self.reinit_list[9]

        self.list_points = self.reinit_list[10][:]

        self.tracing = self.reinit_list[11]

        self.zoom = 1

    def changeinit(self, mass_eom, mass_color, mass_width, spring_pos, spring_offset, spring_color, spring_width, nodes): #exact same as init, changes initial values
        try:
            self.zoom = 1

            self.m = mass_eom
            self.m_color = mass_color
            self.m_width = mass_width

            self.s_color = spring_color
            self.start_pos = spring_pos
            self.s_width = spring_width
            self.spring_offset = spring_offset
            self.end_pos = (int(spring_pos[0] + self.m.pos[0] + self.spring_offset), int(spring_pos[1] + self.m.pos[1]))
            self.newzero = spring_pos

            self.make_spring = spring.Spring(self.start_pos, self.end_pos, self.s_width, nodes, lead1=25, lead2=25, line_width=3, line_color=spring_color)
            self.make_spring.end_pos = (self.end_pos[0] - int(self.m_width/2 * self.zoom), self.end_pos[1]) #shift end_pos of spring to start of block

            self.list_points = [self.end_pos]

            self.tracing = True

            self.reinit_list = [self.m, self.m_color, self.m_width, self.s_color, self.start_pos, self.end_pos, self.spring_offset, self.s_width, self.make_spring, self.newzero, self.list_points[:], self.tracing]
        except:
            self.reinit()
                
    def update(self):
        self.m.update()
        self.end_pos = (int(self.newzero[0] + self.m.pos[0] + self.spring_offset), int(self.newzero[1] + self.m.pos[1])) #made into integers for drawing
        self.make_spring.end_pos = (self.end_pos[0] - int(self.m_width/2 * self.zoom), self.end_pos[1]) #shift end_pos of spring to start of block
        self.make_spring.update()
        self.list_points.append(self.end_pos) #list of all positions per update (all displayed), used for tracing

    def draw(self, surface, zoom):
        self.zoom = zoom
        self.make_spring.draw(surface, zoom) #the spring

        if self.tracing == True and len(self.list_points) >= 2: #if there are more than 2 points
            pygame.draw.aalines(surface, self.s_color, False, self.list_points) #the trace, antialiasing smoothes the line (check performance issues with long traces?)

        pygame.draw.rect(surface, self.m_color, (self.end_pos[0] - int(self.m_width/2 * zoom), self.end_pos[1] - int(self.m_width/2 * zoom), int(self.m_width * zoom), int(self.m_width * zoom))) #shift end_pos so tracing from middle of block