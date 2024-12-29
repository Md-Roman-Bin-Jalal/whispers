from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from midpoint_line import midpoint_line
from midpoint_circle import midpoint_circle
import random

class PointDrawer:
    def draw(self, x, y, color=(1.0, 1.0, 1.0)):
        # glPointSize(3)
        glColor3f(*color)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

class CircleFiller:
    def fill(self, center_x, center_y, radius, color):
        for r in range(radius):
            points = midpoint_circle(center_x, center_y, r)
            for px, py in points:
                PointDrawer().draw(px, py, color)

class GlowCreator:
    def create(self, x, y, radius, intensity):
        for r in range(radius, 0, -1):
            fade = intensity * (r / radius)
            points = midpoint_circle(x, y, r)
            for px, py in points:
                PointDrawer().draw(px, py, (fade, fade, fade * 0.8))


class Stand:
    def draw(self, x, y, height, orientation="right", is_fallen=False):

        if is_fallen:
            # Connect the base to the fallen stand
            for offset in range(-3, 4):
                if orientation == "left":
                    points = midpoint_line(x + offset, y, x - 30 + offset, y + 50)
                else:
                    points = midpoint_line(x + offset, y, x + 30 + offset, y + 50)
                for px, py in points:
                    PointDrawer().draw(px, py, (0.5, 0.5, 0.5))

            # Draw the fallen stand
            for offset in range(-3, 4):
                if orientation == "left":
                    points = midpoint_line(x - 30 + offset, y + 50, x - 60 + offset, y + 50)
                else:
                    points = midpoint_line(x + 30 + offset, y + 50, x + 60 + offset, y + 50)
                for px, py in points:
                    PointDrawer().draw(px, py, (0.5, 0.5, 0.5))

        else:
            for offset in range(-3, 4):
                points = midpoint_line(x + offset, y, x + offset, y + height)
                for px, py in points:
                    PointDrawer().draw(px, py, (0.5, 0.5, 0.5))

            for offset in range(-2, 3):
                arm_points = []
                for i in range(30):
                    px = x - offset - i if orientation == "left" else x + offset + i
                    py = y + height + int(-(i * i) / 50)
                    arm_points.extend(midpoint_line(px, py, px + 1, py))
                for px, py in arm_points:
                    PointDrawer().draw(px, py, (0.5, 0.5, 0.5))

class LampHead:
    def draw(self, x, y, lamp_light_state=False):
        # Lamp hood (semi-circle)
        hood_points = midpoint_circle(x, y, 20)
        for px, py in hood_points:
            if py >= y:
                PointDrawer().draw(px, py, (0.2, 0.2, 0.2))

        # Side supports
        support_points1 = midpoint_line(x - 20, y, x - 15, y - 15)
        support_points2 = midpoint_line(x + 20, y, x + 15, y - 15)
        for px, py in support_points1 + support_points2:
            PointDrawer().draw(px, py, (0.3, 0.3, 0.3))

        if lamp_light_state:
            intensity = random.uniform(0.6, 1.0)
            GlowCreator().create(x, y - 5, 25, intensity)
            CircleFiller().fill(x, y - 5, 8, (intensity, intensity, intensity * 0.9))
        else:
            CircleFiller().fill(x, y - 5, 8, (0.2, 0.2, 0.2))

class single_head_lemp:
    def __init__(self, x, y, orientation, lamp_light_state=False, is_fallen=False):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.lamp_light_state = lamp_light_state
        self.is_fallen = is_fallen
        self.lamp_head = LampHead()

    def draw(self):
        stand_height = 120 if not self.is_fallen else 30
        Stand().draw(self.x, self.y, stand_height, orientation=self.orientation, is_fallen=self.is_fallen)

        # Adjust lamp head position for fallen state
        lamp_x = self.x - 60 if self.orientation == "left" and self.is_fallen else self.x + 60 if self.orientation == "right" and self.is_fallen else self.x - 30 if self.orientation == "left" else self.x + 30
        lamp_y = self.y + 30 if self.is_fallen else self.y + 83
        self.lamp_head.draw(lamp_x, lamp_y, self.lamp_light_state)

class double_head_lamp:
    def __init__(self, x, y, ignore, lamp_light_state=False, is_fallen=False):
        self.x = x
        self.y = y
        self.lamp_light_state = lamp_light_state
        self.is_fallen = is_fallen
        self.lamp_head = LampHead()

    def draw(self):
        stand_height = 120 if not self.is_fallen else 30
        s1, s2 = (True, False) if self.is_fallen else (True, True)

        Stand().draw(self.x, self.y, stand_height, orientation='left', is_fallen=self.is_fallen) if s1 else None
        Stand().draw(self.x, self.y, stand_height, orientation='right', is_fallen=self.is_fallen) if s2 else None

        if self.is_fallen:
            left_lamp_x = self.x - 60
            left_lamp_y = self.y + 30
            right_lamp_x = self.x + 60
            right_lamp_y = self.y + 30
        else:
            left_lamp_x = self.x - 30
            left_lamp_y = self.y + 83
            right_lamp_x = self.x + 30
            right_lamp_y = self.y + 83

        if s1:
            self.lamp_head.draw(left_lamp_x, left_lamp_y, self.lamp_light_state)
        if s2:
            self.lamp_head.draw(right_lamp_x, right_lamp_y, self.lamp_light_state)
