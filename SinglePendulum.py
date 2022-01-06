import pygame, math, time
from pygame import gfxdraw #might be experimental? if code breakes, check this

#---Classes---#
class EOM():
    def __init__(self, theta, omega, l, g, gamma, A, B, t, dt, FPS):
        self.theta = theta * math.pi / 180 #angle, converted from DEG - RAD
        self.omega = omega #angular velocity
        self.alpha = 0 #angular acceleration

        self.l = l #length of pendulum
        self.g = g #gravity

        self.gamma = gamma #damping constant

        self.A = A #amplitude of driving force
        self.B = B #frequency of driving force

        self.t = t #time elapsed seconds
        self.dt = dt #deltatime, for the Euler-Cromer Method
        self.iterations = int((1/FPS) / self.dt) #how many dts give 1 frametime
        
        self.pos = (self.l * math.sin(self.theta), -self.l * math.cos(self.theta)) #initial position of mass of pendulum

        self.reinit_list = [self.theta, self.omega, self.alpha, self.l, self.g, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos] #saves initial values
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.theta = self.true_reinit_list[0]
        self.omega = self.true_reinit_list[1]
        self.alpha = self.true_reinit_list[2]

        self.l = self.true_reinit_list[3]
        self.g = self.true_reinit_list[4]

        self.gamma = self.true_reinit_list[5]

        self.A = self.true_reinit_list[6]
        self.B = self.true_reinit_list[7]

        self.t = self.true_reinit_list[8]
        self.dt = self.true_reinit_list[9]
        self.iterations = self.true_reinit_list[10]
        
        self.pos = self.true_reinit_list[11]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the EOM to initial conditions
        self.theta = self.reinit_list[0]
        self.omega = self.reinit_list[1]
        self.alpha = self.reinit_list[2]

        self.l = self.reinit_list[3]
        self.g = self.reinit_list[4]

        self.gamma = self.reinit_list[5]

        self.A = self.reinit_list[6]
        self.B = self.reinit_list[7]

        self.t = self.reinit_list[8]
        self.dt = self.reinit_list[9]
        self.iterations = self.reinit_list[10]
        
        self.pos = self.reinit_list[11]

    def changeinit(self, theta, omega, l, g, gamma, A, B, t, dt, FPS): #exact same as init, changes initial values
        try:
            self.theta = theta * math.pi / 180
            self.omega = omega
            self.alpha = 0

            self.l = l
            exceptiontest = 1 / self.l #will throw an exception if l = 0
            self.g = g

            self.gamma = gamma

            self.A = A
            self.B = B

            self.t = t
            self.dt = dt
            self.iterations = int((1/FPS) / self.dt)
        
            self.pos = (self.l * math.sin(self.theta), -self.l * math.cos(self.theta)) #notice y is in negative direction, as mass is defined in eom as being below the stick (hence negative in pos below)

            self.reinit_list = [self.theta, self.omega, self.alpha, self.l, self.g, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos]
        except:
            self.reinit()

    def update(self):
        for i in range(self.iterations): #do the method at dt until 1/FPS seconds have passed, then draw this
            self.alpha = -(self.g / self.l) * math.sin(self.theta) #standard motion
            self.alpha += -2 * self.gamma * self.omega #damping
            self.alpha += self.A * math.cos(self.B * self.t) #driving force

            self.omega += self.alpha * self.dt

            self.theta += self.omega * self.dt

            self.pos = (self.l * math.sin(self.theta), -self.l * math.cos(self.theta))

            self.t += self.dt

class SPPygame(pygame.sprite.Sprite): #draws the pendulum to any surface (passed in the draw method)
    def __init__(self, mass_eom, mass_color, mass_radius, stick_pos, stick_color, stick_width, scale):
        pygame.sprite.Sprite.__init__(self)

        self.m = mass_eom
        self.m_color = mass_color
        self.m_radius = mass_radius

        self.s_color = stick_color
        self.start_pos = stick_pos #where the base of the stick is
        self.end_pos = (int(stick_pos[0] + self.m.pos[0] * scale), int(stick_pos[1] - self.m.pos[1] * scale)) #treat the stick_pos as the new origin, add the position of the mass, scaled by whatever factor
        self.s_width = stick_width
        self.scale = scale #makes the stick perceived to be longer, by a scale amount (has properties of whatever entered in EOM, but looks as big as scaled here)
        self.newzero = stick_pos #where to place the drawings in a new zero point (moving the origin)

        self.list_points = [self.end_pos] #all the positions of the centre of the mass

        self.tracing = True

        self.reinit_list = [self.m, self.m_color, self.m_radius, self.s_color, self.start_pos, self.end_pos, self.s_width, self.scale, self.newzero, self.list_points[:], self.tracing] #use the [:] to save lists, this creates a copy of the list that is not tied to the original
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.m = self.true_reinit_list[0]
        self.m_color = self.true_reinit_list[1]
        self.m_radius = self.true_reinit_list[2]

        self.s_color = self.true_reinit_list[3]
        self.start_pos = self.true_reinit_list[4]
        self.end_pos = self.true_reinit_list[5]
        self.s_width = self.true_reinit_list[6]
        self.scale = self.true_reinit_list[7]
        self.newzero = self.true_reinit_list[8]

        self.list_points = self.true_reinit_list[9][:]

        self.tracing = self.true_reinit_list[10]

        self.reinit_list = self.true_reinit_list[:]


    def reinit(self): #resets the Display to initial conditions
        self.m = self.reinit_list[0]
        self.m_color = self.reinit_list[1]
        self.m_radius = self.reinit_list[2]

        self.s_color = self.reinit_list[3]
        self.start_pos = self.reinit_list[4]
        self.end_pos = self.reinit_list[5]
        self.s_width = self.reinit_list[6]
        self.scale = self.reinit_list[7]
        self.newzero = self.reinit_list[8]

        self.list_points = self.reinit_list[9][:] #for lists, need to add the [:] at the end when copying as otherwise it points to the same modified list and not the original one, alternatively use list(self.reinit_list[9])

        self.tracing = self.reinit_list[10]

    def changeinit(self, mass_eom, mass_color, mass_radius, stick_pos, stick_color, stick_width, scale): #exact same as init, changes initial values
        try:
            self.m = mass_eom
            self.m_color = mass_color
            self.m_radius = mass_radius

            self.s_color = stick_color
            self.start_pos = stick_pos
            self.end_pos = (int(stick_pos[0] + self.m.pos[0] * scale), int(stick_pos[1] - self.m.pos[1] * scale))
            self.s_width = stick_width
            self.scale = scale
            self.newzero = stick_pos

            self.list_points = [self.end_pos]

            self.tracing = True

            self.reinit_list = [self.m, self.m_color, self.m_radius, self.s_color, self.start_pos, self.end_pos, self.s_width, self.scale, self.newzero, self.list_points[:], self.tracing]
        except:
            self.reinit()

    def reset_tracing(self):
        self.list_points = [self.end_pos] #resets tracing to most recent position
                
    def update(self):
        self.m.update()
        self.end_pos = (int(self.newzero[0] + self.m.pos[0] * self.scale), int(self.newzero[1] - self.m.pos[1] * self.scale)) #made into integers for drawing
        self.list_points.append(self.end_pos) #list of all positions per update (all displayed), used for tracing

    def draw(self, surface, zoom):
        pygame.draw.line(surface, self.s_color, self.start_pos, self.end_pos, width = int(self.s_width * zoom)) #the stick
        pygame.draw.circle(surface, self.s_color, self.start_pos, int(2 * self.s_width * zoom)) #base of stick

        if self.tracing == True and len(self.list_points) >= 2: #if there are more than 2 points
            pygame.draw.aalines(surface, self.s_color, False, self.list_points) #the trace, antialiasing smoothes the line (check performance issues with long traces?)

        gfxdraw.aacircle(surface, self.end_pos[0], self.end_pos[1], int(self.m_radius * zoom), self.m_color) #smoother circle
        gfxdraw.filled_circle(surface, self.end_pos[0], self.end_pos[1], int(self.m_radius * zoom), self.m_color)