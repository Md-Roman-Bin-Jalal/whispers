from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from midpoint_line import midpoint_line
from midpoint_circle import midpoint_circle

class tall_slender_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 1.2)
        self.trunk_width = int(self.scale_factor * 0.1)
        self.leaf_radius = int(self.scale_factor * 0.2)
        

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        leaf_positions = [
            (self.base_x, self.base_y + self.trunk_height),
            (self.base_x - int(self.leaf_radius * 1.2), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x + int(self.leaf_radius * 1.2), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x, self.base_y + self.trunk_height + int(self.leaf_radius * 1.6))
        ]
        
        for x_center, y_center in leaf_positions:
            # Draw filled circle using midpoint circle algorithm and fill
            for r in range(self.leaf_radius + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class bushy_fat_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 0.6)
        self.trunk_width = int(self.scale_factor * 0.1)
        self.leaf_radius = int(self.scale_factor * 0.25)

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        leaf_positions = [
            (self.base_x, self.base_y + self.trunk_height),
            (self.base_x - int(self.leaf_radius * 1.3), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x + int(self.leaf_radius * 1.3), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x, self.base_y + self.trunk_height + int(self.leaf_radius * 1.6))
        ]
        
        for x_center, y_center in leaf_positions:
            for r in range(self.leaf_radius + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class slim_columnar_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 1.0)
        self.trunk_width = int(self.scale_factor * 0.05)
        self.leaf_radius = int(self.scale_factor * 0.15)

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        leaf_positions = [
            (self.base_x, self.base_y + self.trunk_height),
            (self.base_x - int(self.leaf_radius * 1.2), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x + int(self.leaf_radius * 1.2), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x, self.base_y + self.trunk_height + int(self.leaf_radius * 1.6))
        ]
        
        for x_center, y_center in leaf_positions:
            for r in range(self.leaf_radius + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class compact_thick_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 0.7)
        self.trunk_width = int(self.scale_factor * 0.2)
        self.leaf_radius = int(self.scale_factor * 0.3)

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        leaf_positions = [
            (self.base_x, self.base_y + self.trunk_height),
            (self.base_x - int(self.leaf_radius * 1.5), self.base_y + self.trunk_height + int(self.leaf_radius * 1.0)),
            (self.base_x + int(self.leaf_radius * 1.5), self.base_y + self.trunk_height + int(self.leaf_radius * 1.0)),
            (self.base_x, self.base_y + self.trunk_height + int(self.leaf_radius * 2.0))
        ]
        
        for x_center, y_center in leaf_positions:
            for r in range(self.leaf_radius + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class miniature_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 0.4)  # Shorter trunk
        self.trunk_width = int(self.scale_factor * 0.05)  # Very thin trunk
        self.leaf_radius = int(self.scale_factor * 0.12)  # Small leaves

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        leaf_positions = [
            (self.base_x, self.base_y + self.trunk_height),
            (self.base_x - int(self.leaf_radius * 1.0), self.base_y + self.trunk_height + int(self.leaf_radius * 0.6)),
            (self.base_x + int(self.leaf_radius * 1.0), self.base_y + self.trunk_height + int(self.leaf_radius * 0.6)),
            (self.base_x, self.base_y + self.trunk_height + int(self.leaf_radius * 1.2))
        ]
        
        for x_center, y_center in leaf_positions:
            for r in range(self.leaf_radius + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class pyramid_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 0.8)
        self.trunk_width = int(self.scale_factor * 0.15)
        self.leaf_radius = int(self.scale_factor * 0.25)

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        # Create a pyramidal shape with gradually smaller circles
        levels = 5
        for i in range(levels):
            current_radius = self.leaf_radius * (1 - i * 0.15)
            y_offset = self.trunk_height + (i * current_radius * 1.5)
            x_center = self.base_x
            y_center = self.base_y + y_offset
            
            for r in range(int(current_radius) + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class umbrella_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 1.1)
        self.trunk_width = int(self.scale_factor * 0.12)
        self.leaf_radius = int(self.scale_factor * 0.45)

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        # Single large circle at the top for umbrella shape
        x_center = self.base_x
        y_center = self.base_y + self.trunk_height + int(self.leaf_radius * 0.5)
        
        for r in range(self.leaf_radius + 1):
            circle_points = midpoint_circle(x_center, y_center, r)
            glBegin(GL_POINTS)
            for px, py in circle_points:
                glVertex2f(px, py)
            glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()

class multi_layer_tree:
    def __init__(self, base_x, base_y, display_height, tree_color_state = False):
        self.base_x, self.base_y, self.tree_color_state = base_x, base_y, tree_color_state
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 0.9)
        self.trunk_width = int(self.scale_factor * 0.15)
        self.leaf_radius = int(self.scale_factor * 0.3)

    def draw_trunk(self):
        glColor3f(0.4, 0.2, 0.1) if self.tree_color_state else glColor3f(0.2, 0.2, 0.2)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            trunk_points = midpoint_line(x, self.base_y, x, self.base_y + self.trunk_height)
            glBegin(GL_POINTS)
            for px, py in trunk_points:
                glVertex2f(px, py)
            glEnd()

    def draw_leaves(self):
        glColor3f(0.2, 0.6, 0.2) if self.tree_color_state else glColor3f(0.7, 0.7, 0.7)
        # Multiple layers of circles with different sizes
        layers = [
            (0, 1.0),     # (height_factor, radius_factor)
            (0.6, 0.8),
            (1.2, 0.6),
            (1.8, 0.4)
        ]
        
        for height_factor, radius_factor in layers:
            current_radius = int(self.leaf_radius * radius_factor)
            y_offset = self.trunk_height + int(self.leaf_radius * height_factor)
            x_center = self.base_x
            y_center = self.base_y + y_offset
            
            for r in range(current_radius + 1):
                circle_points = midpoint_circle(x_center, y_center, r)
                glBegin(GL_POINTS)
                for px, py in circle_points:
                    glVertex2f(px, py)
                glEnd()

    def draw(self):
        self.draw_trunk()
        self.draw_leaves()