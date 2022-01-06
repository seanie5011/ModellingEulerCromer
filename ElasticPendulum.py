import pygame, math, time
from pygame import gfxdraw #might be experimental? if code breakes, check this
import spring #relies on other file spring.py for drawing

#---Classes---#
class EOM():
    def __init__(self, x, v, theta, omega, k, m, l, g, gamma, A, B, t, dt, FPS): #note that equilibrium position will be at end of spring for convenience of drawing
        self.x = x #position
        self.v = v #velocity
        self.a = 0 #acceleration

        self.theta = theta * math.pi / 180 #angle, converted from DEG - RAD
        self.omega = omega #angular velocity
        self.alpha = 0 #angular acceleration

        self.k = k #spring constant
        self.m = m #mass
        self.l = l #length of equilibrium
        self.g = g #gravity

        self.gamma = gamma #damping constant

        self.A = A #amplitude of driving force
        self.B = B #frequency of driving force

        self.t = t #time elapsed seconds
        self.dt = dt #deltatime, for the Euler-Cromer Method
        self.iterations = int((1/FPS) / self.dt) #how many dts give 1 frametime
        
        self.pos = ((self.l + self.x) * math.sin(self.theta), (self.l + self.x) * math.cos(self.theta)) #initial position of mass of spring

        self.reinit_list = [self.x, self.v, self.a, self.theta, self.omega, self.alpha, self.k, self.m, self.l, self.g, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos] #saves initial values
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.x = self.true_reinit_list[0]
        self.v = self.true_reinit_list[1]
        self.a = self.true_reinit_list[2]

        self.theta = self.true_reinit_list[3]
        self.omega = self.true_reinit_list[4]
        self.alpha = self.true_reinit_list[5]

        self.k = self.true_reinit_list[6]
        self.m = self.true_reinit_list[7]
        self.l = self.true_reinit_list[8]
        self.g = self.true_reinit_list[9]

        self.gamma = self.true_reinit_list[10]

        self.A = self.true_reinit_list[11]
        self.B = self.true_reinit_list[12]

        self.t = self.true_reinit_list[13]
        self.dt = self.true_reinit_list[14]
        self.iterations = self.true_reinit_list[15]
        
        self.pos = self.true_reinit_list[16]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the EOM to initial conditions
        self.x = self.reinit_list[0]
        self.v = self.reinit_list[1]
        self.a = self.reinit_list[2]

        self.theta = self.reinit_list[3]
        self.omega = self.reinit_list[4]
        self.alpha = self.reinit_list[5]

        self.k = self.reinit_list[6]
        self.m = self.reinit_list[7]
        self.l = self.reinit_list[8]
        self.g = self.reinit_list[9]

        self.gamma = self.reinit_list[10]

        self.A = self.reinit_list[11]
        self.B = self.reinit_list[12]

        self.t = self.reinit_list[13]
        self.dt = self.reinit_list[14]
        self.iterations = self.reinit_list[15]
        
        self.pos = self.reinit_list[16]

    def changeinit(self, x, v, theta, omega, k, m, l, g, gamma, A, B, t, dt, FPS): #exact same as init, changes initial values
        try:
            self.x = x #position
            self.v = v #velocity
            self.a = 0 #acceleration

            self.theta = theta * math.pi / 180 #angle, converted from DEG - RAD
            self.omega = omega #angular velocity
            self.alpha = 0 #angular acceleration

            self.k = k #spring constant
            self.m = m #mass
            self.l = l #length of equilibrium
            self.g = g #gravity

            self.gamma = gamma #damping constant

            self.A = A #amplitude of driving force
            self.B = B #frequency of driving force

            self.t = t #time elapsed seconds
            self.dt = dt #deltatime, for the Euler-Cromer Method
            self.iterations = int((1/FPS) / self.dt) #how many dts give 1 frametime
        
            self.pos = ((self.l + self.x) * math.sin(self.theta), (self.l + self.x) * math.cos(self.theta)) #initial position of mass of spring

            self.reinit_list = [self.x, self.v, self.a, self.theta, self.omega, self.alpha, self.k, self.m, self.l, self.g, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos] #saves initial values
        except:
            self.reinit()

    def update(self):
        for i in range(self.iterations): #do the method at dt until 1/FPS seconds have passed, then draw this
            #sub in formulae for spring motion
            A = (self.l + self.x) * (self.omega)**2
            B = self.k * self.x / self.m
            C = self.g * math.cos(self.theta)

            self.a = A - B + C #standard motion
            self.a += (-self.gamma / self.m) * self.v #damping, velocity dependant
            self.a += self.A * math.cos(self.B * self.t) #driving force, no dependance on system

            self.v += self.a * self.dt

            self.x += self.v * self.dt

            #sub in formulae for pendulum motion
            D = (2 * self.v * self.omega) / (self.l + self.x)
            E = (self.g * math.sin(self.theta)) / (self.l + self.x)

            self.alpha = -(D + E) #standard motion
            self.alpha += -2 * self.gamma * self.omega #damping
            self.alpha += self.A * math.cos(self.B * self.t) #driving force

            self.omega += self.alpha * self.dt

            self.theta += self.omega * self.dt

            self.pos = ((self.l + self.x) * math.sin(self.theta), (self.l + self.x) * math.cos(self.theta))

            self.t += self.dt

class SPPygame(pygame.sprite.Sprite): #draws the pendulum to any surface (passed in the draw method)
    def __init__(self, mass_eom, mass_color, mass_radius, scale, spring_pos, spring_offset, spring_color, spring_width, nodes):
        pygame.sprite.Sprite.__init__(self)

        self.zoom = 1

        self.m = mass_eom
        self.m_color = mass_color
        self.m_radius = mass_radius
        self.scale = scale

        self.s_color = spring_color
        self.start_pos = spring_pos #where the base of the spring is
        self.s_width = spring_width
        self.spring_offset = spring_offset # a tuple containing offset in x and offset in y
        self.end_pos = (int(spring_pos[0] + self.m.pos[0] * scale + self.spring_offset[0]), int(spring_pos[1] + self.m.pos[1] * scale + self.spring_offset[1])) #treat the spring_pos as the new origin, add the position of the mass, scaled by whatever factor
        self.newzero = spring_pos #where to place the drawings in a new zero point (moving the origin)

        self.make_spring = spring.Spring(self.start_pos, self.end_pos, self.s_width, nodes, lead1=25, lead2=25, line_width=3, line_color=spring_color) #start_pos, end_pos, spring_width, nodes, node_draw=False, node_color=(0,0,0), node_radius=0, lead1=0, lead2=0, line_width=1, line_color=(0,0,0)
        self.make_spring.end_pos = (self.end_pos[0] - int(self.m_radius/2 * self.zoom), self.end_pos[1]) #shift end_pos of spring to start of block

        self.list_points = [self.end_pos] #all the positions of the centre of the mass

        self.tracing = True

        self.reinit_list = [self.m, self.m_color, self.m_radius, self.scale, self.s_color, self.start_pos, self.end_pos, self.spring_offset, self.s_width, self.make_spring, self.newzero, self.list_points[:], self.tracing] #use the [:] to save lists, this creates a copy of the list that is not tied to the original
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.m = self.true_reinit_list[0]
        self.m_color = self.true_reinit_list[1]
        self.m_radius = self.true_reinit_list[2]
        self.scale = self.true_reinit_list[3]

        self.s_color = self.true_reinit_list[4]
        self.start_pos = self.true_reinit_list[5]
        self.end_pos = self.true_reinit_list[6]
        self.spring_offset = self.true_reinit_list[7]
        self.s_width = self.true_reinit_list[8]
        self.make_spring = self.true_reinit_list[9]
        self.newzero = self.true_reinit_list[10]

        self.list_points = self.true_reinit_list[11][:]

        self.tracing = self.true_reinit_list[12]

        self.reinit_list = self.true_reinit_list[:]

        self.zoom = 1


    def reinit(self): #resets the Display to initial conditions
        self.m = self.reinit_list[0]
        self.m_color = self.reinit_list[1]
        self.m_radius = self.reinit_list[2]
        self.scale = self.reinit_list[3]

        self.s_color = self.reinit_list[4]
        self.start_pos = self.reinit_list[5]
        self.end_pos = self.reinit_list[6]
        self.spring_offset = self.reinit_list[7]
        self.s_width = self.reinit_list[8]
        self.make_spring = self.reinit_list[9]
        self.newzero = self.reinit_list[10]

        self.list_points = self.reinit_list[11][:]

        self.tracing = self.true_reinit_list[12]

        self.zoom = 1

    def changeinit(self, mass_eom, mass_color, mass_radius, scale, spring_pos, spring_offset, spring_color, spring_width, nodes): #exact same as init, changes initial values
        try:
            self.m = mass_eom
            self.m_color = mass_color
            self.m_radius = mass_radius
            self.scale = scale

            self.s_color = spring_color
            self.start_pos = spring_pos #where the base of the spring is
            self.s_width = spring_width
            self.spring_offset = spring_offset # a tuple containing offset in x and offset in y
            self.end_pos = (int(spring_pos[0] + self.m.pos[0] * scale + self.spring_offset[0]), int(spring_pos[1] + self.m.pos[1] * scale + self.spring_offset[1])) #treat the spring_pos as the new origin, add the position of the mass, scaled by whatever factor
            self.newzero = spring_pos #where to place the drawings in a new zero point (moving the origin)

            self.make_spring = spring.Spring(self.start_pos, self.end_pos, self.s_width, nodes, lead1=25, lead2=25, line_width=3, line_color=spring_color) #start_pos, end_pos, spring_width, nodes, node_draw=False, node_color=(0,0,0), node_radius=0, lead1=0, lead2=0, line_width=1, line_color=(0,0,0)
            self.make_spring.end_pos = (self.end_pos[0] - int(self.m_radius/2 * self.zoom), self.end_pos[1]) #shift end_pos of spring to start of block

            self.list_points = [self.end_pos] #all the positions of the centre of the mass

            self.tracing = True

            self.reinit_list = [self.m, self.m_color, self.m_radius, self.scale, self.s_color, self.start_pos, self.end_pos, self.spring_offset, self.s_width, self.make_spring, self.newzero, self.list_points[:], self.tracing]
        except:
            self.reinit()

    def reset_tracing(self):
        self.list_points = [self.end_pos] #resets tracing to most recent position
                
    def update(self):
        self.m.update()
        self.end_pos = (int(self.newzero[0] + self.m.pos[0] * self.scale + self.spring_offset[0]), int(self.newzero[1] + self.m.pos[1] * self.scale + self.spring_offset[1])) #made into integers for drawing
        self.make_spring.end_pos = self.end_pos[:] #dont need to shift position of spring as using radius for ball
        self.make_spring.update()
        self.list_points.append(self.end_pos) #list of all positions per update (all displayed), used for tracing

    def draw(self, surface, zoom):
        self.zoom = zoom
        self.make_spring.draw(surface, zoom) #the spring

        if self.tracing == True and len(self.list_points) >= 2: #if there are more than 2 points
            pygame.draw.aalines(surface, self.s_color, False, self.list_points) #the trace, antialiasing smoothes the line (check performance issues with long traces?)

        gfxdraw.aacircle(surface, self.end_pos[0], self.end_pos[1], int(self.m_radius * zoom), self.m_color) #smoother circle
        gfxdraw.filled_circle(surface, self.end_pos[0], self.end_pos[1], int(self.m_radius * zoom), self.m_color)