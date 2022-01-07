import pygame, math
from pygame import gfxdraw #might be experimental? if code breakes, check this

class Spring():
    def __init__(self, start_pos, end_pos, spring_width, nodes, node_draw=False, node_color=(0,0,0), node_radius=0, lead1=0, lead2=0, line_width=1, line_color=(0,0,0)):
        self.start_pos = start_pos
        self.end_pos = end_pos

        #find which direction spring is facing, direct unit vectors accordingly
        sign_par = +1
        sign_per = +1
        sign_x = self.end_pos[0] > self.start_pos[0] #if pointing right or left (true/false)
        sign_y = self.end_pos[1] > self.start_pos[1] #if pointing down or up (true/false)

        if sign_x:
            sign_par = +1
        else:
            sign_par = -1
        if sign_y:
            sign_per = +1
        else:
            sign_per = -1

        if self.end_pos[1] == self.start_pos[1]: #so only movement in x direction, unit vector parallel (1, 0)
            self.e_par = (sign_par, 0)
            self.e_per = (0, sign_per)
        elif self.end_pos[0] == self.start_pos[0]: #so only movement in y direction, unit vector parallel (0, 1)
            sign_par = sign_per
            self.e_par = (0, sign_par)
            self.e_per = (sign_per, 0)
        else: #if movement diagonally
            slope = (self.end_pos[1] - self.start_pos[1]) / (self.end_pos[0] - self.start_pos[0])
            intercept = self.start_pos[1] - slope * self.start_pos[0] #y = m*x + c

            par_adjusted_zero = (self.start_pos[0], self.start_pos[1] - intercept)
            par_mag = math.sqrt((par_adjusted_zero[0])**2 + (par_adjusted_zero[1])**2)
            self.e_par = (par_adjusted_zero[0] / par_mag * sign_par, par_adjusted_zero[1] / par_mag * sign_par)

            per_point = (1, -1/slope * 1 + intercept)
            per_adjusted_zero = (per_point[0], per_point[1] - intercept)
            per_mag = math.sqrt((per_adjusted_zero[0])**2 + (per_adjusted_zero[1])**2)
            self.e_per = (per_adjusted_zero[0] / per_mag * sign_per, per_adjusted_zero[1] / per_mag * sign_per)

        self.s_start_pos = (start_pos[0] + lead1 * self.e_par[0], start_pos[1] + lead1 * self.e_par[1]) #where spring starts, adding lead 1 to start
        self.s_end_pos = (end_pos[0] - lead2 * self.e_par[0], end_pos[1] - lead2 * self.e_par[1]) #where spring ends, taking lead 2 from end
        self.length = math.sqrt((self.s_end_pos[0] - self.s_start_pos[0])**2 + (self.s_end_pos[1] - self.s_start_pos[1])**2) #distance between two points for spring

        if nodes < 1: #cant have 0 or negative nodes (0 nodes is just a line!, negative is just...???)
            nodes = 1
        self.nodes = nodes

        self.spring_width = spring_width #"diagonal" distance between nodes

        if self.length > nodes * spring_width: #max length is n*w
            self.length = nodes * spring_width

        self.nodes_pos = [self.s_start_pos] #will be a list of tuples of the (x, y) of each node to be drawn, initialise with start of spring
        for i in range(1, self.nodes + 1): #will start at 1, then finish with nodes, so if nodes = 1 > i=1; if nodes = 2 > i=1, i=2; etc.
            d_x = ((self.length) / (2 * self.nodes)) * (2 * (i) - 1) #d_par = l/2n * (2i - 1), only odd nodes are real, this is distance between odd nodes
            d_y = (1.0 / 2.0) * math.sqrt((self.spring_width)**2 - (self.length / self.nodes)**2) * math.pow(-1, i) #d_per = 1/2 * sqrt(w**2 - (l/n)**2) * (-1)**i, alternates between being in minus an plus direction from parallel
            
            new_node_x = self.s_start_pos[0] + d_x * self.e_par[0] + d_y * self.e_per[0] #distance in parallel direction
            new_node_y = self.s_start_pos[1] + d_x * self.e_par[1] + d_y * self.e_per[1] #distance in perpendicular direction

            new_node = (new_node_x, new_node_y)
            self.nodes_pos.append(new_node) #append new node
        self.nodes_pos.append(self.s_end_pos) #append end of spring

        #assigning rest of stuff
        self.node_draw = node_draw
        self.node_color = node_color
        self.node_radius = node_radius
        self.lead1 = lead1
        self.lead2 = lead2
        self.line_width = line_width
        self.line_color = line_color

    def update(self): #will have to change self.start_pos and self.end_pos outside of class
        #find which direction spring is facing, direct unit vectors accordingly
        sign_par = +1
        sign_per = +1
        sign_x = self.end_pos[0] > self.start_pos[0] #if pointing right or left (true/false)
        sign_y = self.end_pos[1] > self.start_pos[1] #if pointing down or up (true/false)

        if sign_x:
            sign_par = +1
        else:
            sign_par = -1
        if sign_y:
            sign_per = +1
        else:
            sign_per = -1

        if self.end_pos[1] == self.start_pos[1]: #so only movement in x direction, unit vector parallel (1, 0)
            self.e_par = (sign_par, 0)
            self.e_per = (0, sign_per)
        elif self.end_pos[0] == self.start_pos[0]: #so only movement in y direction, unit vector parallel (0, 1)
            sign_par = sign_per
            self.e_par = (0, sign_par)
            self.e_per = (sign_per, 0)
        else: #if movement diagonally
            slope = (self.end_pos[1] - self.start_pos[1]) / (self.end_pos[0] - self.start_pos[0])
            intercept = self.start_pos[1] - slope * self.start_pos[0] #y = m*x + c

            par_adjusted_zero = (self.start_pos[0], self.start_pos[1] - intercept)
            par_mag = math.sqrt((par_adjusted_zero[0])**2 + (par_adjusted_zero[1])**2)
            self.e_par = (par_adjusted_zero[0] / par_mag * sign_par, par_adjusted_zero[1] / par_mag * sign_par)

            per_point = (1, -1/slope * 1 + intercept)
            per_adjusted_zero = (per_point[0], per_point[1] - intercept)
            per_mag = math.sqrt((per_adjusted_zero[0])**2 + (per_adjusted_zero[1])**2)
            self.e_per = (per_adjusted_zero[0] / per_mag * sign_per, per_adjusted_zero[1] / per_mag * sign_per)

        self.s_start_pos = (self.start_pos[0] + self.lead1 * self.e_par[0], self.start_pos[1] + self.lead1 * self.e_par[1])
        self.s_end_pos = (self.end_pos[0] - self.lead2 * self.e_par[0], self.end_pos[1] - self.lead2 * self.e_par[1])
        self.length = math.sqrt((self.s_end_pos[0] - self.s_start_pos[0])**2 + (self.s_end_pos[1] - self.s_start_pos[1])**2)

        if self.length > self.nodes * self.spring_width: #max length is n*w
            self.length = self.nodes * self.spring_width

        self.nodes_pos = [self.s_start_pos] #reset each update, with initial spring start
        for i in range(1, self.nodes + 1):
            d_x = ((self.length) / (2 * self.nodes)) * (2 * (i) - 1)
            d_y = (1.0 / 2.0) * math.sqrt((self.spring_width)**2 - (self.length / self.nodes)**2) * math.pow(-1, i)
            
            new_node_x = self.s_start_pos[0] + d_x * self.e_par[0] + d_y * self.e_per[0] #distance in parallel direction
            new_node_y = self.s_start_pos[1] + d_x * self.e_par[1] + d_y * self.e_per[1] #distance in perpendicular direction

            new_node = (new_node_x, new_node_y)
            self.nodes_pos.append(new_node) #append new node
        self.nodes_pos.append(self.s_end_pos) #append end of spring

    def draw(self, surface, zoom=1): #zoom increases width of lines and node radii, default zoom=1 means no change in size
        #lines
        pygame.draw.lines(surface, self.line_color, False, self.nodes_pos, width = int(self.line_width * zoom)) #draws lines between each node
        #leads
        if self.lead1 >= 1: #only if lead1 is larger than 1 pixel
            pygame.draw.line(surface, self.line_color, self.start_pos, self.s_start_pos, width = int(self.line_width * zoom)) #goes from start to start of spring
        if self.lead2 >= 1: #only if lead2 is larger than 1 pixel
            pygame.draw.line(surface, self.line_color, self.s_end_pos, self.end_pos, width = int(self.line_width * zoom)) #goes from end of spring to end
        #nodes
        if self.node_draw == True:
            for i in range(1, len(self.nodes_pos) - 1): #prints indices 1, 2, ... len(self.nodes_pos) - 2; this is because we dont want to draw the start and end of spring as circles
                gfxdraw.aacircle(surface, int(self.nodes_pos[i][0]), int(self.nodes_pos[i][1]), int(self.node_radius * zoom), self.node_color) #smoother circle
                gfxdraw.filled_circle(surface, int(self.nodes_pos[i][0]), int(self.nodes_pos[i][1]), int(self.node_radius * zoom), self.node_color)
