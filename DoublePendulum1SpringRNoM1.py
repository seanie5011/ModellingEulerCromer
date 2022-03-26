import pygame, math, time
from pygame import gfxdraw #might be experimental? if code breakes, check this
import spring

#---Classes---#
class EOM():
    def __init__(self, x, v, theta1, omega1, l1, theta2, omega2, m2, l2, k, g, gamma, A, B, t, dt, FPS):
        self.x = x #displacement of spring
        self.v = v #velocity of displacement
        self.a = 0 #acceleration of displacement

        self.theta1 = theta1 * math.pi / 180 #angle of pend1, converted from DEG - RAD
        self.omega1 = omega1 #angular velocity of pend1
        self.alpha1 = 0 #angular acceleration of pend1
        self.l1 = l1 #length of pendulum of pend1

        self.theta2 = theta2 * math.pi / 180 #angle of pend2, converted from DEG - RAD
        self.omega2 = omega2 #angular velocity of pend2
        self.alpha2 = 0 #angular acceleration of pend2
        self.m2 = m2 #mass of pend2
        self.l2 = l2 #length of equilibrium of pend2

        self.g = g #gravity
        self.k = k #spring constant

        self.gamma = gamma #damping constant

        self.A = A #amplitude of driving force
        self.B = B #frequency of driving force

        self.t = t #time elapsed seconds
        self.dt = dt #deltatime, for the Euler-Cromer Method
        self.iterations = int((1/FPS) / self.dt) #how many dts give 1 frametime
        
        self.pos1 = ((self.l1 + self.x) * math.sin(self.theta1), -(self.l1 + self.x) * math.cos(self.theta1)) #initial position of end of spring
        self.pos2 = (self.l2 * math.sin(self.theta2) + self.pos1[0], -self.l2 * math.cos(self.theta2) + self.pos1[1]) #initial position of mass of pendulum 2, added to spring end pos

        self.reinit_list = [self.x, self.v, self.a, self.theta1, self.omega1, self.alpha1, self.l1, self.theta2, self.omega2, self.alpha2, self.m2, self.l2, self.g, self.k, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos1, self.pos2] #saves initial values
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.x = self.true_reinit_list[0]
        self.v = self.true_reinit_list[1]
        self.a = self.true_reinit_list[2]

        self.theta1 = self.true_reinit_list[3]
        self.omega1 = self.true_reinit_list[4]
        self.alpha1 = self.true_reinit_list[5]
        self.l1 = self.true_reinit_list[6]

        self.theta2 = self.true_reinit_list[7]
        self.omega2 = self.true_reinit_list[8]
        self.alpha2 = self.true_reinit_list[9]
        self.m2 = self.true_reinit_list[10]
        self.l2 = self.true_reinit_list[11]

        self.g = self.true_reinit_list[12]
        self.k = self.true_reinit_list[13]

        self.gamma = self.true_reinit_list[14]

        self.A = self.true_reinit_list[15]
        self.B = self.true_reinit_list[16]

        self.t = self.true_reinit_list[17]
        self.dt = self.true_reinit_list[18]
        self.iterations = self.true_reinit_list[19]
        
        self.pos1 = self.true_reinit_list[20]
        self.pos2 = self.true_reinit_list[21]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the EOM to initial conditions
        self.x = self.reinit_list[0]
        self.v = self.reinit_list[1]
        self.a = self.reinit_list[2]

        self.theta1 = self.reinit_list[3]
        self.omega1 = self.reinit_list[4]
        self.alpha1 = self.reinit_list[5]
        self.l1 = self.reinit_list[6]

        self.theta2 = self.reinit_list[7]
        self.omega2 = self.reinit_list[8]
        self.alpha2 = self.reinit_list[9]
        self.m2 = self.reinit_list[10]
        self.l2 = self.reinit_list[11]

        self.g = self.reinit_list[12]
        self.k = self.reinit_list[13]

        self.gamma = self.reinit_list[14]

        self.A = self.reinit_list[15]
        self.B = self.reinit_list[16]

        self.t = self.reinit_list[17]
        self.dt = self.reinit_list[18]
        self.iterations = self.reinit_list[19]
        
        self.pos1 = self.reinit_list[20]
        self.pos2 = self.reinit_list[21]

    def changeinit(self, x, v, theta1, omega1, l1, theta2, omega2, m2, l2, k, g, gamma, A, B, t, dt, FPS): #exact same as init, changes initial values
        try:
            self.x = x
            self.v = v
            self.a = 0

            self.theta1 = theta1 * math.pi / 180
            self.omega1 = omega1
            self.alpha1 = 0
            self.l1 = l1

            self.theta2 = theta2 * math.pi / 180
            self.omega2 = omega2
            self.alpha2 = 0
            self.m2 = m2
            self.l2 = l2

            self.g = g
            self.k = k

            self.gamma = gamma

            self.A = A
            self.B = B

            self.t = t
            self.dt = dt
            self.iterations = int((1/FPS) / self.dt)
        
            self.pos1 = ((self.l1 + self.x) * math.sin(self.theta1), -(self.l1 + self.x) * math.cos(self.theta1))
            self.pos2 = (self.l2 * math.sin(self.theta2) + self.pos1[0], -self.l2 * math.cos(self.theta2) + self.pos1[1])

            self.reinit_list = [self.x, self.v, self.a, self.theta1, self.omega1, self.alpha1, self.l1, self.theta2, self.omega2, self.alpha2, self.m2, self.l2, self.g, self.k, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos1, self.pos2]
        except:
            self.reinit()

    def update(self):
        for i in range(self.iterations): #do the method at dt until 1/FPS seconds have passed, then draw this
            #formulae
            A = self.l1 + self.x
            B = self.l2 * math.sin(self.theta1 - self.theta2) * (self.omega2)**2
            C = self.l2 * math.cos(self.theta1 - self.theta2) * self.alpha2
            D = 2 * self.omega1 * self.v
            E = self.g * math.sin(self.theta1)
            F = self.l2 * math.sin(self.theta1 - self.theta2) * self.alpha2
            G = self.l2 * math.cos(self.theta1 - self.theta2) * (self.omega2)**2
            H = (self.l1 + self.x) * (self.omega1)**2
            I = self.g * math.cos(self.theta1)
            J = self.k * self.x / self.m2
            K = (self.l1 + self.x) * math.sin(self.theta1 - self.theta2) * (self.omega1)**2
            L = (self.l1 + self.x) * math.cos(self.theta1 - self.theta2) * self.alpha1
            M = self.a * math.sin(self.theta1 - self.theta2)
            N = 2 * self.omega1 * self.v * math.cos(self.theta1 - self.theta2)
            O = self.g * math.sin(self.theta2)

            #pendulum 1
            #length
            self.a = -F + G + H + I - J #standard motion
            self.a += (-self.gamma / self.m2) * self.v #damping, velocity dependant
            self.a += self.A * math.cos(self.B * self.t) #driving force, no dependance on system

            self.v += self.a * self.dt

            self.x += self.v * self.dt

            #angle
            self.alpha1 = -(B + C + D + E) / A #standard motion
            self.alpha1 += -2 * self.gamma * self.omega1 #damping
            self.alpha1 += self.A * math.cos(self.B * self.t) #driving force

            self.omega1 += self.alpha1 * self.dt

            self.theta1 += self.omega1 * self.dt

            #pendulum 2
            #angle
            self.alpha2 = -(-K + L + M + N + O) / self.l2 #standard motion
            self.alpha2 += -2 * self.gamma * self.omega2 #damping
            self.alpha2 += self.A * math.cos(self.B * self.t) #driving force

            self.omega2 += self.alpha2 * self.dt

            self.theta2 += self.omega2 * self.dt

            self.pos1 = ((self.l1 + self.x) * math.sin(self.theta1), -(self.l1 + self.x) * math.cos(self.theta1))
            self.pos2 = (self.l2 * math.sin(self.theta2) + self.pos1[0], -self.l2 * math.cos(self.theta2) + self.pos1[1])

            self.t += self.dt

class SPPygame(pygame.sprite.Sprite): #draws the pendulum to any surface (passed in the draw method)
    def __init__(self, mass_eom, mass2_color, mass_radius, spring_pos, stick_color, stick_width, spring_width, nodes, scale):
        pygame.sprite.Sprite.__init__(self)

        self.zoom = 1

        self.m = mass_eom
        self.m2_color = mass2_color
        self.m_radius = mass_radius

        self.s_color = stick_color
        self.start_pos = spring_pos #where the base of the stick is
        self.end1_pos = (int(spring_pos[0] + self.m.pos1[0] * scale), int(spring_pos[1] - self.m.pos1[1] * scale)) #treat the stick_pos as the new origin, add the position of the mass1, scaled by whatever factor
        self.end2_pos = (int(spring_pos[0] + self.m.pos2[0] * scale), int(spring_pos[1] - self.m.pos2[1] * scale)) #treat the stick_pos as the new origin, add the position of the mass2, scaled by whatever factor
        self.stick_width = stick_width #width of line, line length when drawing
        self.spring_width = spring_width #width for spring function, not width of line being drawn
        self.nodes = nodes
        self.scale = scale #makes the stick perceived to be longer, by a scale amount (has properties of whatever entered in EOM, but looks as big as scaled here)
        self.newzero = spring_pos #where to place the drawings in a new zero point (moving the origin)

        self.make_spring = spring.Spring(self.start_pos, self.end1_pos, self.spring_width, nodes, lead1=25, lead2=25, line_width=3, line_color=stick_color) #start_pos, end_pos, spring_width, nodes, node_draw=False, node_color=(0,0,0), node_radius=0, lead1=0, lead2=0, line_width=1, line_color=(0,0,0)
        self.make_spring.end_pos = (self.end1_pos[0] - int(self.m_radius/2 * self.zoom), self.end1_pos[1]) #shift end_pos of spring to start of block

        self.list2_points = [self.end2_pos] #all the positions of the centre of the mass2

        self.tracing = True

        self.reinit_list = [self.m, self.m2_color, self.m_radius, self.s_color, self.start_pos, self.end1_pos, self.end2_pos, self.stick_width, self.spring_width, self.nodes, self.make_spring, self.scale, self.newzero, self.list2_points[:], self.tracing] #use the [:] to save lists, this creates a copy of the list that is not tied to the original
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.zoom = 1

        self.m = self.true_reinit_list[0]
        self.m2_color = self.true_reinit_list[1]
        self.m_radius = self.true_reinit_list[2]

        self.s_color = self.true_reinit_list[3]
        self.start_pos = self.true_reinit_list[4]
        self.end1_pos = self.true_reinit_list[5]
        self.end2_pos = self.true_reinit_list[6]
        self.stick_width = self.true_reinit_list[7]
        self.spring_width = self.true_reinit_list[8]
        self.nodes = self.true_reinit_list[9]
        self.make_spring = self.true_reinit_list[10]
        self.scale = self.true_reinit_list[11]
        self.newzero = self.true_reinit_list[12]

        self.list2_points = self.true_reinit_list[13][:]

        self.tracing = self.true_reinit_list[14]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the Display to initial conditions
        self.zoom = 1

        self.m = self.reinit_list[0]
        self.m2_color = self.reinit_list[1]
        self.m_radius = self.reinit_list[2]

        self.s_color = self.reinit_list[3]
        self.start_pos = self.reinit_list[4]
        self.end1_pos = self.reinit_list[5]
        self.end2_pos = self.reinit_list[6]
        self.stick_width = self.reinit_list[7]
        self.spring_width = self.reinit_list[8]
        self.nodes = self.reinit_list[9]
        self.make_spring = self.reinit_list[10]
        self.scale = self.reinit_list[11]
        self.newzero = self.reinit_list[12]

        self.list2_points = self.reinit_list[13][:]

        self.tracing = self.reinit_list[14]

    def changeinit(self, mass_eom, mass2_color, mass_radius, spring_pos, stick_color, stick_width, spring_width, nodes, scale): #exact same as init, changes initial values
        try:
            self.zoom = 1

            self.m = mass_eom
            self.m2_color = mass2_color
            self.m_radius = mass_radius

            self.s_color = stick_color
            self.start_pos = spring_pos
            self.end1_pos = (int(spring_pos[0] + self.m.pos1[0] * scale), int(spring_pos[1] - self.m.pos1[1] * scale))
            self.end2_pos = (int(spring_pos[0] + self.m.pos2[0] * scale), int(spring_pos[1] - self.m.pos2[1] * scale))
            self.stick_width = stick_width
            self.spring_width = spring_width
            self.nodes = nodes
            self.scale = scale
            self.newzero = spring_pos

            self.make_spring = spring.Spring(self.start_pos, self.end1_pos, self.spring_width, nodes, lead1=25, lead2=25, line_width=3, line_color=stick_color)
            self.make_spring.end_pos = (self.end1_pos[0] - int(self.m2_radius/2 * self.zoom), self.end1_pos[1])

            self.list2_points = [self.end2_pos]

            self.tracing = True

            self.reinit_list = [self.m, self.m2_color, self.m_radius, self.s_color, self.start_pos, self.end1_pos, self.end2_pos, self.stick_width, self.spring_width, self.nodes, self.make_spring, self.scale, self.newzero, self.list2_points[:], self.tracing]
            self.true_reinit_list = self.reinit_list[:]
        except:
            self.reinit()

    def reset_tracing(self):
        self.list2_points = [self.end2_pos]
                
    def update(self):
        self.m.update()
        self.end1_pos = (int(self.newzero[0] + self.m.pos1[0] * self.scale), int(self.newzero[1] - self.m.pos1[1] * self.scale)) #made into integers for drawing
        self.end2_pos = (int(self.newzero[0] + self.m.pos2[0] * self.scale), int(self.newzero[1] - self.m.pos2[1] * self.scale))
        self.make_spring.start_pos = self.start_pos[:] #dont need to shift position of spring as using radius for ball
        self.make_spring.end_pos = self.end1_pos[:]
        self.make_spring.update()
        self.list2_points.append(self.end2_pos)

    def draw(self, surface, zoom):
        pygame.draw.line(surface, self.s_color, self.end1_pos, self.end2_pos, width = int(self.stick_width * zoom)) #the stick for pend2
        self.make_spring.draw(surface, zoom) #the spring for pend2
        pygame.draw.circle(surface, self.s_color, self.start_pos, int(2 * self.stick_width * zoom)) #base of stick

        if self.tracing == True and len(self.list2_points) >= 2: #if there are more than 2 points
            pygame.draw.aalines(surface, self.m2_color, False, self.list2_points) #the trace, antialiasing smoothes the line (check performance issues with long traces?)

        gfxdraw.aacircle(surface, self.end2_pos[0], self.end2_pos[1], int(self.m_radius * zoom), self.m2_color) #smoother circle, pend2
        gfxdraw.filled_circle(surface, self.end2_pos[0], self.end2_pos[1], int(self.m_radius * zoom), self.m2_color)