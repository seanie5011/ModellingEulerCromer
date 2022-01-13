import pygame, math, time
from pygame import gfxdraw #might be experimental? if code breakes, check this
import spring

#---Classes---#
class EOM():
    def __init__(self, x, v, theta1, omega1, m1, l1, theta2, omega2, m2, l2, k, g, gamma, A, B, t, dt, FPS):
        self.x = x #displacement of spring
        self.v = v #velocity of displacement
        self.a = 0 #acceleration of displacement

        self.theta1 = theta1 * math.pi / 180 #angle of pend1, converted from DEG - RAD
        self.omega1 = omega1 #angular velocity of pend1
        self.alpha1 = 0 #angular acceleration of pend1
        self.m1 = m1 #mass of pend1
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
        
        self.pos1 = (self.l1 * math.sin(self.theta1), -self.l1 * math.cos(self.theta1)) #initial position of mass of pendulum 1
        self.pos2 = (self.pos1[0] + (self.l2 + self.x) * math.sin(self.theta2), self.pos1[1] - (self.l2 + self.x) * math.cos(self.theta2)) #initial position of mass of pendulum 2 (added to pendulum 1 for position from base point)

        self.reinit_list = [self.x, self.v, self.a, self.theta1, self.omega1, self.alpha1, self.m1, self.l1, self.theta2, self.omega2, self.alpha2, self.m2, self.l2, self.g, self.k, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos1, self.pos2] #saves initial values
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.x = self.true_reinit_list[0]
        self.v = self.true_reinit_list[1]
        self.a = self.true_reinit_list[2]

        self.theta1 = self.true_reinit_list[3]
        self.omega1 = self.true_reinit_list[4]
        self.alpha1 = self.true_reinit_list[5]
        self.m1 = self.true_reinit_list[6]
        self.l1 = self.true_reinit_list[7]

        self.theta2 = self.true_reinit_list[8]
        self.omega2 = self.true_reinit_list[9]
        self.alpha2 = self.true_reinit_list[10]
        self.m2 = self.true_reinit_list[11]
        self.l2 = self.true_reinit_list[12]

        self.g = self.true_reinit_list[13]
        self.k = self.true_reinit_list[14]

        self.gamma = self.true_reinit_list[15]

        self.A = self.true_reinit_list[16]
        self.B = self.true_reinit_list[17]

        self.t = self.true_reinit_list[18]
        self.dt = self.true_reinit_list[19]
        self.iterations = self.true_reinit_list[20]
        
        self.pos1 = self.true_reinit_list[21]
        self.pos2 = self.true_reinit_list[22]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the EOM to initial conditions
        self.x = self.reinit_list[0]
        self.v = self.reinit_list[1]
        self.a = self.reinit_list[2]

        self.theta1 = self.reinit_list[3]
        self.omega1 = self.reinit_list[4]
        self.alpha1 = self.reinit_list[5]
        self.m1 = self.reinit_list[6]
        self.l1 = self.reinit_list[7]

        self.theta2 = self.reinit_list[8]
        self.omega2 = self.reinit_list[9]
        self.alpha2 = self.reinit_list[10]
        self.m2 = self.reinit_list[11]
        self.l2 = self.reinit_list[12]

        self.g = self.reinit_list[13]
        self.k = self.reinit_list[14]

        self.gamma = self.reinit_list[15]

        self.A = self.reinit_list[16]
        self.B = self.reinit_list[17]

        self.t = self.reinit_list[18]
        self.dt = self.reinit_list[19]
        self.iterations = self.reinit_list[20]
        
        self.pos1 = self.reinit_list[21]
        self.pos2 = self.reinit_list[22]

    def changeinit(self, x, v, theta1, omega1, m1, l1, theta2, omega2, m2, l2, k, g, gamma, A, B, t, dt, FPS): #exact same as init, changes initial values
        try:
            self.x = x
            self.v = v
            self.a = 0

            self.theta1 = theta1 * math.pi / 180
            self.omega1 = omega1
            self.alpha1 = 0
            self.m1 = m1
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
        
            self.pos1 = (self.l1 * math.sin(self.theta1), -self.l1 * math.cos(self.theta1))
            self.pos2 = (self.pos1[0] + (self.l2 + self.x) * math.sin(self.theta2), self.pos1[1] - (self.l2 + self.x) * math.cos(self.theta2))

            self.reinit_list = [self.x, self.v, self.a, self.theta1, self.omega1, self.alpha1, self.m1, self.l1, self.theta2, self.omega2, self.alpha2, self.m2, self.l2, self.g, self.k, self.gamma, self.A, self.B, self.t, self.dt, self.iterations, self.pos1, self.pos2]
        except:
            self.reinit()

    def update(self):
        for i in range(self.iterations): #do the method at dt until 1/FPS seconds have passed, then draw this
            #formulae
            A = self.l1 * self.alpha1 * math.sin(self.theta2 - self.theta1)
            B = (self.l2 + self.x) * (self.omega2)**2
            C = self.g * math.cos(self.theta2)
            D = self.k * self.x / self.m2
            E = self.l1 * math.cos(self.theta2 - self.theta1) * (self.omega1)**2
            F = (self.m1 + self.m2) * (self.l1)
            G = self.m2 * (self.l2 + self.x) * math.cos(self.theta2 - self.theta1) * self.alpha2
            H = self.m2 * math.sin(self.theta2 - self.theta1) * self.a
            I = 2 * self.m2 * self.v * self.omega2 * math.cos(self.theta2 - self.theta1)
            J = self.m2 * (self.l2 + self.x) * math.sin(self.theta2 - self.theta1) * (self.omega2)**2
            K = (self.m1 + self.m2) * self.g * math.sin(self.theta1)
            P = self.l2 + self.x
            Q = self.l1 * math.cos(self.theta2 - self.theta1) * self.alpha1
            S = self.l1 * math.sin(self.theta2 - self.theta1) * (self.omega1)**2
            V = self.g * math.sin(self.theta2)
            W = 2 * self.omega2 * self.x

            #pendulum 1
            self.alpha1 = -(G + H + I - J + K) / F #standard motion
            self.alpha1 += -2 * self.gamma * self.omega1 #damping
            self.alpha1 += self.A * math.cos(self.B * self.t) #driving force

            self.omega1 += self.alpha1 * self.dt

            self.theta1 += self.omega1 * self.dt

            self.pos1 = (self.l1 * math.sin(self.theta1), -self.l1 * math.cos(self.theta1))

            #pendulum 2
            #length
            self.a = -A + B + C - D + E #standard motion
            self.a += (-self.gamma / self.m2) * self.v #damping, velocity dependant
            self.a += self.A * math.cos(self.B * self.t) #driving force, no dependance on system

            self.v += self.a * self.dt

            self.x += self.v * self.dt

            #angle
            self.alpha2 = -(Q + S + V + W) / P #standard motion
            self.alpha2 += -2 * self.gamma * self.omega2 #damping
            self.alpha2 += self.A * math.cos(self.B * self.t) #driving force

            self.omega2 += self.alpha2 * self.dt

            self.theta2 += self.omega2 * self.dt

            self.pos2 = (self.pos1[0] + (self.l2 + self.x) * math.sin(self.theta2), self.pos1[1] - (self.l2 + self.x) * math.cos(self.theta2))

            self.t += self.dt

class SPPygame(pygame.sprite.Sprite): #draws the pendulum to any surface (passed in the draw method)
    def __init__(self, mass_eom, mass1_color, mass2_color, mass_radius, stick_pos, stick_color, stick_width, spring_width, nodes, scale):
        pygame.sprite.Sprite.__init__(self)

        self.zoom = 1

        self.m = mass_eom
        self.m1_color = mass1_color
        self.m2_color = mass2_color
        self.m_radius = mass_radius

        self.s_color = stick_color
        self.start_pos = stick_pos #where the base of the stick is
        self.end1_pos = (int(stick_pos[0] + self.m.pos1[0] * scale), int(stick_pos[1] - self.m.pos1[1] * scale)) #treat the stick_pos as the new origin, add the position of the mass1, scaled by whatever factor
        self.end2_pos = (int(stick_pos[0] + self.m.pos2[0] * scale), int(stick_pos[1] - self.m.pos2[1] * scale)) #treat the stick_pos as the new origin, add the position of the mass2, scaled by whatever factor
        self.stick_width = stick_width #width of line, line length when drawing
        self.spring_width = spring_width #width for spring function, not width of line being drawn
        self.nodes = nodes
        self.scale = scale #makes the stick perceived to be longer, by a scale amount (has properties of whatever entered in EOM, but looks as big as scaled here)
        self.newzero = stick_pos #where to place the drawings in a new zero point (moving the origin)

        self.make_spring = spring.Spring(self.end1_pos, self.end2_pos, self.spring_width, nodes, lead1=25, lead2=25, line_width=3, line_color=stick_color) #start_pos, end_pos, spring_width, nodes, node_draw=False, node_color=(0,0,0), node_radius=0, lead1=0, lead2=0, line_width=1, line_color=(0,0,0)
        self.make_spring.end_pos = (self.end2_pos[0] - int(self.m_radius/2 * self.zoom), self.end2_pos[1]) #shift end_pos of spring to start of block

        self.list1_points = [self.end1_pos] #all the positions of the centre of the mass1
        self.list2_points = [self.end2_pos] #all the positions of the centre of the mass2

        self.tracing = True

        self.reinit_list = [self.m, self.m1_color, self.m2_color, self.m_radius, self.s_color, self.start_pos, self.end1_pos, self.end2_pos, self.stick_width, self.spring_width, self.nodes, self.make_spring, self.scale, self.newzero, self.list1_points[:], self.list2_points[:], self.tracing] #use the [:] to save lists, this creates a copy of the list that is not tied to the original
        self.true_reinit_list = self.reinit_list[:] #keeps initial vales from first load of game, cannot be changed

    def true_reinit(self):
        self.zoom = 1

        self.m = self.true_reinit_list[0]
        self.m1_color = self.true_reinit_list[1]
        self.m2_color = self.true_reinit_list[2]
        self.m_radius = self.true_reinit_list[3]

        self.s_color = self.true_reinit_list[4]
        self.start_pos = self.true_reinit_list[5]
        self.end1_pos = self.true_reinit_list[6]
        self.end2_pos = self.true_reinit_list[7]
        self.stick_width = self.true_reinit_list[8]
        self.spring_width = self.true_reinit_list[9]
        self.nodes = self.true_reinit_list[10]
        self.make_spring = self.true_reinit_list[11]
        self.scale = self.true_reinit_list[12]
        self.newzero = self.true_reinit_list[13]

        self.list1_points = self.true_reinit_list[14][:] #for lists, need to add the [:] at the end when copying as otherwise it points to the same modified list and not the original one, alternatively use list(self.reinit_list[9])
        self.list2_points = self.true_reinit_list[15][:]

        self.tracing = self.true_reinit_list[16]

        self.reinit_list = self.true_reinit_list[:]

    def reinit(self): #resets the Display to initial conditions
        self.zoom = 1

        self.m = self.reinit_list[0]
        self.m1_color = self.reinit_list[1]
        self.m2_color = self.reinit_list[2]
        self.m_radius = self.reinit_list[3]

        self.s_color = self.reinit_list[4]
        self.start_pos = self.reinit_list[5]
        self.end1_pos = self.reinit_list[6]
        self.end2_pos = self.reinit_list[7]
        self.stick_width = self.reinit_list[8]
        self.spring_width = self.reinit_list[9]
        self.nodes = self.reinit_list[10]
        self.make_spring = self.reinit_list[11]
        self.scale = self.reinit_list[12]
        self.newzero = self.reinit_list[13]

        self.list1_points = self.reinit_list[14][:]
        self.list2_points = self.reinit_list[15][:]

        self.tracing = self.reinit_list[16]

    def changeinit(self, mass_eom, mass1_color, mass2_color, mass_radius, stick_pos, stick_color, stick_width, spring_width, nodes, scale): #exact same as init, changes initial values
        try:
            self.zoom = 1

            self.m = mass_eom
            self.m1_color = mass1_color
            self.m2_color = mass2_color
            self.m_radius = mass_radius

            self.s_color = stick_color
            self.start_pos = stick_pos
            self.end1_pos = (int(stick_pos[0] + self.m.pos1[0] * scale), int(stick_pos[1] - self.m.pos1[1] * scale))
            self.end2_pos = (int(stick_pos[0] + self.m.pos2[0] * scale), int(stick_pos[1] - self.m.pos2[1] * scale))
            self.stick_width = stick_width
            self.spring_width = spring_width
            self.nodes = nodes
            self.scale = scale
            self.newzero = stick_pos

            self.make_spring = spring.Spring(self.end1_pos, self.end2_pos, self.spring_width, nodes, lead1=25, lead2=25, line_width=3, line_color=stick_color)
            self.make_spring.end_pos = (self.end2_pos[0] - int(self.m2_radius/2 * self.zoom), self.end2_pos[1])

            self.list1_points = [self.end1_pos]
            self.list2_points = [self.end2_pos]

            self.tracing = True

            self.reinit_list = [self.m, self.m1_color, self.m2_color, self.m_radius, self.s_color, self.start_pos, self.end1_pos, self.end2_pos, self.stick_width, self.spring_width, self.nodes, self.make_spring, self.scale, self.newzero, self.list1_points[:], self.list2_points[:], self.tracing]
            self.true_reinit_list = self.reinit_list[:]
        except:
            self.reinit()

    def reset_tracing(self):
        self.list1_points = [self.end1_pos] #resets tracing to most recent position
        self.list2_points = [self.end2_pos]
                
    def update(self):
        self.m.update()
        self.end1_pos = (int(self.newzero[0] + self.m.pos1[0] * self.scale), int(self.newzero[1] - self.m.pos1[1] * self.scale)) #made into integers for drawing
        self.end2_pos = (int(self.newzero[0] + self.m.pos2[0] * self.scale), int(self.newzero[1] - self.m.pos2[1] * self.scale))
        self.make_spring.start_pos = self.end1_pos[:] #dont need to shift position of spring as using radius for ball
        self.make_spring.end_pos = self.end2_pos[:]
        self.make_spring.update()
        self.list1_points.append(self.end1_pos) #list of all positions per update (all displayed), used for tracing
        self.list2_points.append(self.end2_pos)

    def draw(self, surface, zoom):
        pygame.draw.line(surface, self.s_color, self.start_pos, self.end1_pos, width = int(self.stick_width * zoom)) #the stick for pend1
        self.make_spring.draw(surface, zoom) #the spring for pend2
        pygame.draw.circle(surface, self.s_color, self.start_pos, int(2 * self.stick_width * zoom)) #base of stick

        if self.tracing == True and len(self.list1_points) >= 2 and len(self.list2_points) >= 2: #if there are more than 2 points
            pygame.draw.aalines(surface, self.m1_color, False, self.list1_points) #the trace, antialiasing smoothes the line (check performance issues with long traces?)
            pygame.draw.aalines(surface, self.m2_color, False, self.list2_points) #the trace, antialiasing smoothes the line (check performance issues with long traces?)

        gfxdraw.aacircle(surface, self.end1_pos[0], self.end1_pos[1], int(self.m_radius * zoom), self.m1_color) #smoother circle, pend1
        gfxdraw.filled_circle(surface, self.end1_pos[0], self.end1_pos[1], int(self.m_radius * zoom), self.m1_color)
        gfxdraw.aacircle(surface, self.end2_pos[0], self.end2_pos[1], int(self.m_radius * zoom), self.m2_color) #smoother circle, pend2
        gfxdraw.filled_circle(surface, self.end2_pos[0], self.end2_pos[1], int(self.m_radius * zoom), self.m2_color)