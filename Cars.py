from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from midpoint_line import midpoint_line
from midpoint_circle import midpoint_circle

class fill_polygon_with_points:
    def __init__(self, car_type, points, base_intensity, car_color_state=False, car_mirror=False):
        self.points = points
        self.base_intensity = base_intensity
        self.car_color_state = car_color_state
        self.car_mirror = car_mirror
        self.car_type = car_type

    def draw(self):
        glBegin(GL_POINTS)
        min_y = min(p[1] for p in self.points)
        max_y = max(p[1] for p in self.points)

        if self.car_type == 'scratched_sedan':
            cx, cy, cz = (0.8, 0.4, 0.2)
        elif self.car_type == 'wrecked_coupe':
            cx, cy, cz = (0.2, 0.5, 0.9)
        else:
            cx, cy, cz = (0.9, 0.7, 0.4)  


        for y in range(int(min_y), int(max_y) + 1):
            intersections = []
            for i in range(len(self.points)):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % len(self.points)]

                if (p1[1] > y and p2[1] <= y) or (p2[1] > y and p1[1] <= y):
                    x = p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1])
                    intersections.append(x)

            intersections.sort()
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    for x in range(int(intersections[i]), int(intersections[i + 1])):
                        intensity = self.base_intensity + random.uniform(-0.1, 0.1)
                        intensity = max(0.1, min(0.8, intensity))
                        glColor3f(cx, cy, cz) if self.car_color_state else glColor3f(intensity, intensity, intensity)
                        glColor3f(0, 0, 0) if self.car_mirror else None
                        glVertex2f(x, y)
        glEnd()

class draw_scratched_sedan:
    def __init__(self, x_offset=0, y_offset=0, orientation="right", car_color_state=False):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.orientation = orientation
        self.car_color_state = car_color_state
        self.car_type = 'scratched_sedan'

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x_offset, self.y_offset, 0)
        glScalef(0.5, 0.5, 1.0)

        car_body = [
            (300, 100), (100, 90), (60, 140),
            (130, 160), (250, 150), (300, 100)
        ] if self.orientation == "left" else [
            (100, 100), (300, 90), (340, 140),
            (270, 160), (150, 150), (100, 100)
        ]
        fill_polygon_with_points(self.car_type, car_body, 0.4, self.car_color_state).draw()

        windshield = [
            (190, 150), (180, 120), (140, 125),
            (150, 145), (190, 150)
        ] if self.orientation == "left" else [
            (150, 150), (160, 120), (200, 125),
            (190, 145), (150, 150)
        ]
        fill_polygon_with_points(self.car_type, windshield, 0.6, self.car_color_state, True).draw()

        glBegin(GL_POINTS)
        for radius in range(10, 20):
            wheel1_x, wheel2_x = (260, 140) if self.orientation == "left" else (140, 260)
            for x, y in midpoint_circle(wheel1_x, 85, radius):
                glColor3f(0, 0, 0)
                glVertex2f(x, y)
            for x, y in midpoint_circle(wheel2_x, 90, radius):
                glColor3f(0, 0, 0)
                glVertex2f(x, y)
        glEnd()

        glBegin(GL_POINTS)
        damage = [
            (200, 130, 220, 125),
            (180, 140, 195, 135)
        ]
        for line in damage:
            if self.orientation == "left":
                line = (300 - line[0], line[1], 300 - line[2], line[3])
            for x, y in midpoint_line(*line):
                glColor3f(0.5, 0.5, 0.5)
                glVertex2f(x, y)
        glEnd()

        glPopMatrix()

class draw_wrecked_coupe:
    def __init__(self, x_offset=0, y_offset=0, orientation="right", car_color_state=False):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.orientation = orientation
        self.car_color_state = car_color_state
        self.car_type = 'wrecked_coupe'

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x_offset, self.y_offset, 0)
        glScalef(0.5, 0.5, 1.0)

        car_body = [
            (300, 100), (100, 85), (70, 130),
            (150, 150), (240, 140), (300, 100)
        ] if self.orientation == "left" else [
            (100, 100), (300, 85), (330, 130),
            (250, 150), (140, 140), (100, 100)
        ]
        fill_polygon_with_points(self.car_type, car_body, 0.3, self.car_color_state).draw()

        windshield = [
            (180, 135), (185, 105), (150, 110),
            (160, 130), (180, 135)
        ] if self.orientation == "left" else [
            (150, 140), (155, 110), (190, 115),
            (180, 135), (150, 140)
        ]
        fill_polygon_with_points(self.car_type, windshield, 0.5, self.car_color_state, True).draw()

        glBegin(GL_POINTS)
        for radius in range(10, 18):
            wheel1_x, wheel2_x = (260, 140) if self.orientation == "left" else (140, 260)
            for x, y in midpoint_circle(wheel1_x, 80, radius):
                glColor3f(0, 0, 0)
                glVertex2f(x, y)
            for x, y in midpoint_circle(wheel2_x, 85, radius):
                glColor3f(0, 0, 0)
                glVertex2f(x, y)
        glEnd()

        glBegin(GL_POINTS)
        damage = [
            (200, 120, 230, 110),
            (180, 135, 195, 120),
            (240, 140, 255, 125)
        ]
        for line in damage:
            if self.orientation == "left":
                line = (300 - line[0], line[1], 300 - line[2], line[3])
            for x, y in midpoint_line(*line):
                glColor3f(0, 0, 0) if self.car_color_state else glColor3f(0.5, 0.5, 0.5)
                glVertex2f(x, y)
        glEnd()

        glPopMatrix()

class draw_totaled_wreck:
    def __init__(self, x_offset=0, y_offset=0, orientation="right", car_color_state=False):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.orientation = orientation
        self.car_color_state = car_color_state
        self.car_type = 'totaled_wreck'

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x_offset, self.y_offset, 0)
        glScalef(0.5, 0.5, 1.0)

        car_body = [
            (270, 95), (100, 80), (70, 120),
            (140, 140), (230, 130), (270, 95)
        ] if self.orientation == "left" else [
            (100, 95), (270, 80), (300, 120),
            (230, 140), (130, 130), (100, 95)
        ]
        fill_polygon_with_points(self.car_type, car_body, 0.2, self.car_color_state).draw()

        windshield = [
            (160, 125), (145, 95), (120, 100),
            (130, 120), (160, 125)
        ] if self.orientation == "left" else [
            (140, 130), (145, 100), (170, 105),
            (160, 125), (140, 130)
        ]
        fill_polygon_with_points(self.car_type, windshield, 0.4, self.car_color_state, True).draw()

        glBegin(GL_POINTS)
        for radius in range(8, 15):
            wheel1_x, wheel2_x = (250, 130) if self.orientation == "left" else (130, 250)
            for x, y in midpoint_circle(wheel1_x, 75, radius):
                glColor3f(0, 0, 0)
                glVertex2f(x, y)
            for x, y in midpoint_circle(wheel2_x, 80, radius):
                glColor3f(0, 0, 0)
                glVertex2f(x, y)
        glEnd()

        glBegin(GL_POINTS)
        damage = [
            (180, 110, 220, 90),
            (160, 125, 190, 105),
            (230, 135, 250, 115),
            (140, 120, 170, 100)
        ]
        for line in damage:
            if self.orientation == "left":
                line = (300 - line[0], line[1], 300 - line[2], line[3])
            for x, y in midpoint_line(*line):
                glColor3f(0, 0, 0) if self.car_color_state else glColor3f(0.5, 0.5, 0.5)
                glVertex2f(x, y)
        glEnd()

        glPopMatrix()