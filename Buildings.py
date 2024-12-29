from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
from midpoint_line import midpoint_line

class damaged_building_left:
    def __init__(self, base_x, base_y, width, height):
        self.base_x = base_x
        self.base_y = base_y
        self.width = width
        self.height = height
        self.wall_color = (0.4, 0.4, 0.4)
        self.shadow_color = (0.3, 0.3, 0.3)
        self.window_color = (0.1, 0.1, 0.1)
        
        # Generate the building structure
        self.structure_points = set()
        self.broken_edges = set()
        self.windows = set()
        self.generate_building()

    def generate_building(self):
        # First, create full building
        for x in range(int(self.base_x), int(self.base_x) + self.width):
            for y in range(int(self.base_y), int(self.base_y) + self.height):
                self.structure_points.add((x, y))
        
        # Define break control points for zigzag pattern
        control_points = [
            (self.base_x, self.base_y + self.height//2),  # Start at left-middle
            (self.base_x + 30, self.base_y + self.height - 70),
            (self.base_x + 70, self.base_y + self.height - 120),
            (self.base_x + self.width//2, self.base_y + self.height)   # End at top-middle
        ]

        # Connect control points with jagged lines
        for i in range(len(control_points)-1):
            start = control_points[i]
            end = control_points[i+1]
            
            # Create jagged line between points
            steps = 20
            for t in range(steps):
                # Interpolate between points with some randomness
                progress = t / steps
                x = int(start[0] + (end[0] - start[0]) * progress + random.randint(-5, 5))
                y = int(start[1] + (end[1] - start[1]) * progress + random.randint(-5, 5))
                
                # Remove everything above this line
                for remove_x in range(x - 2, x + 3):  # Thickness of break line
                    for remove_y in range(y, int(self.base_y) + self.height):
                        if (remove_x, remove_y) in self.structure_points:
                            self.structure_points.remove((remove_x, remove_y))
                        # Add to broken edges if it's at the border of removal
                        if (remove_x, y) in self.structure_points:
                            self.broken_edges.add((remove_x, y))

        # Generate windows that aren't in the broken section
        window_width = 15
        window_height = 20
        window_spacing = 30
        
        for x in range(self.base_x + 20, self.base_x + self.width - 20, window_spacing):
            for y in range(self.base_y + 30, self.base_y + self.height - 20, window_spacing + 10):
                window_area = set()
                if all((x + dx, y + dy) in self.structure_points 
                      for dx in range(window_width) 
                      for dy in range(window_height)):
                    # Create broken window effect
                    for wx in range(window_width):
                        for wy in range(window_height):
                            if random.random() < 0.7:  # Make windows look broken
                                window_area.add((x + wx, y + wy))
                    self.windows.update(window_area)

    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        
        # Draw main building structure
        glColor3f(*self.wall_color)
        for x, y in self.structure_points - self.windows:
            glVertex2f(x, y)

        # Draw broken edges (slightly darker for depth)
        glColor3f(*self.shadow_color)
        for x, y in self.broken_edges:
            glVertex2f(x, y)
            # Add some debris near edges
            if random.random() < 0.1:  # Sparse debris
                debris_x = x + random.randint(-3, 3)
                debris_y = y + random.randint(-3, 3)
                if (debris_x, debris_y) not in self.structure_points:
                    glVertex2f(debris_x, debris_y)

        # Draw windows
        glColor3f(*self.window_color)
        for x, y in self.windows:
            glVertex2f(x, y)

        glEnd()

class damaged_building_mid_spikes:
    def __init__(self, base_x, base_y, width, height):
        self.base_x = base_x
        self.base_y = base_y
        self.width = width
        self.height = height
        self.wall_color = (0.4, 0.4, 0.4)
        self.shadow_color = (0.3, 0.3, 0.3)
        self.window_color = (0.1, 0.1, 0.1)
        
        self.structure_points = set()
        self.broken_edges = set()
        self.windows = set()
        self.generate_building()

    def create_zigzag_break(self, control_points):
        break_points = set()
        
        for i in range(len(control_points)-1):
            start = control_points[i]
            end = control_points[i+1]
            
            steps = 20
            for t in range(steps):
                progress = t / steps
                # Add randomness to create jagged effect
                x = int(start[0] + (end[0] - start[0]) * progress + random.randint(-5, 5))
                y = int(start[1] + (end[1] - start[1]) * progress + random.randint(-5, 5))
                
                break_points.add((x, y))
                # Add thickness to break line
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        break_points.add((x + dx, y + dy))
        
        return break_points

    def generate_building(self):
        # Create initial building structure
        for x in range(int(self.base_x), int(self.base_x) + self.width):
            for y in range(int(self.base_y), int(self.base_y) + self.height):
                self.structure_points.add((x, y))

        # Right side break control points (top-middle to right-middle)
        right_control_points = [
            (self.base_x + self.width//2 + 20, self.base_y + self.height),
            (self.base_x + self.width//2 + 50, self.base_y + self.height - 60),
            (self.base_x + self.width//2 + 90, self.base_y + self.height - 140),
            (self.base_x + self.width - 10, self.base_y + self.height//2 + 30)
        ]

        # Left side break control points (top-middle to left-middle)
        left_control_points = [
            (self.base_x + self.width//2 - 20, self.base_y + self.height),
            (self.base_x + self.width//2 - 40, self.base_y + self.height - 80),
            (self.base_x + self.width//2 - 70, self.base_y + self.height - 160),
            (self.base_x + 10, self.base_y + self.height//2 - 30)
        ]

        # Create both breaks
        right_break = self.create_zigzag_break(right_control_points)
        left_break = self.create_zigzag_break(left_control_points)

        # Remove structure above both break lines
        for x, y in right_break:
            for remove_y in range(y, self.base_y + self.height):
                if (x, remove_y) in self.structure_points:
                    self.structure_points.remove((x, remove_y))
                if (x, y) in self.structure_points:
                    self.broken_edges.add((x, y))

        for x, y in left_break:
            for remove_y in range(y, self.base_y + self.height):
                if (x, remove_y) in self.structure_points:
                    self.structure_points.remove((x, remove_y))
                if (x, y) in self.structure_points:
                    self.broken_edges.add((x, y))

        # Add debris near breaks
        for edge_x, edge_y in self.broken_edges.copy():
            if random.random() < 0.15:  # 15% chance for debris at each edge point
                for _ in range(3):  # Create multiple debris points
                    debris_x = edge_x + random.randint(-4, 4)
                    debris_y = edge_y + random.randint(-4, 4)
                    if (debris_x, debris_y) not in self.structure_points:
                        self.broken_edges.add((debris_x, debris_y))

        # Generate windows in remaining structure
        window_width = 15
        window_height = 20
        window_spacing = 30
        
        for x in range(self.base_x + 20, self.base_x + self.width - 20, window_spacing):
            for y in range(self.base_y + 30, self.base_y + self.height - 20, window_spacing + 10):
                # Check if window area exists in structure
                if all((x + dx, y + dy) in self.structure_points 
                      for dx in range(window_width) 
                      for dy in range(window_height)):
                    # Create broken window effect
                    for wx in range(window_width):
                        for wy in range(window_height):
                            if random.random() < 0.7:  # Random broken pattern
                                self.windows.add((x + wx, y + wy))

    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        
        # Draw main structure
        glColor3f(*self.wall_color)
        for x, y in self.structure_points - self.windows:
            glVertex2f(x, y)

        # Draw break edges and debris
        glColor3f(*self.shadow_color)
        for x, y in self.broken_edges:
            glVertex2f(x, y)

        # Draw windows
        glColor3f(*self.window_color)
        for x, y in self.windows:
            glVertex2f(x, y)

        glEnd()

class damaged_building_mid_spikes_2:
    def __init__(self, base_x, base_y, width, height):
        self.base_x = base_x
        self.base_y = base_y
        self.width = width
        self.height = height
        self.wall_color = (0.4, 0.4, 0.4)
        self.shadow_color = (0.3, 0.3, 0.3)
        self.window_color = (0.1, 0.1, 0.1)
        
        self.structure_points = set()
        self.broken_edges = set()
        self.windows = set()
        self.generate_building()

    def create_irregular_break(self, start_region, end_region):
        break_points = set()
        current_y = start_region[1]
        
        while current_y >= end_region[1]:
            # Create irregular horizontal segments
            segment_length = random.randint(10, 25)
            x_offset = random.randint(-8, 8)
            
            # Determine x-range based on y-position progress
            progress = (start_region[1] - current_y) / (start_region[1] - end_region[1])
            center_x = start_region[0] + (end_region[0] - start_region[0]) * progress
            
            # Add jagged segment
            for x in range(int(center_x - segment_length/2), int(center_x + segment_length/2)):
                y_variation = random.randint(-3, 3)
                break_points.add((x + x_offset, current_y + y_variation))
            
            # Random vertical drop
            current_y -= random.randint(15, 30)
            
            # Add some random debris chunks
            if random.random() < 0.3:
                chunk_size = random.randint(3, 7)
                chunk_x = center_x + random.randint(-20, 20)
                chunk_y = current_y + random.randint(-10, 10)
                for dx in range(chunk_size):
                    for dy in range(chunk_size):
                        if random.random() < 0.7:
                            break_points.add((int(chunk_x + dx), int(chunk_y + dy)))
        
        return break_points

    def generate_building(self):
        # Create initial building structure
        for x in range(int(self.base_x), int(self.base_x) + self.width):
            for y in range(int(self.base_y), int(self.base_y) + self.height):
                self.structure_points.add((x, y))

        # Define break regions
        right_start = (self.base_x + self.width//2 + 20, self.base_y + self.height)
        right_end = (self.base_x + self.width - 20, self.base_y + self.height//2 + 30)
        
        left_start = (self.base_x + self.width//2 - 20, self.base_y + self.height)
        left_end = (self.base_x + 20, self.base_y + self.height//2 - 30)

        # Create irregular breaks
        right_break = self.create_irregular_break(right_start, right_end)
        left_break = self.create_irregular_break(left_start, left_end)

        # Remove structure above breaks and add broken edges
        for x, y in right_break | left_break:
            for remove_y in range(y, self.base_y + self.height):
                self.structure_points.discard((x, remove_y))
            if (x, y) in self.structure_points:
                self.broken_edges.add((x, y))

        # Add scattered debris
        for edge_x, edge_y in list(self.broken_edges):
            if random.random() < 0.2:
                for _ in range(random.randint(2, 5)):
                    debris_x = edge_x + random.randint(-6, 6)
                    debris_y = edge_y + random.randint(-6, 6)
                    self.broken_edges.add((debris_x, debris_y))

        # Generate windows in remaining structure
        window_width = 15
        window_height = 20
        window_spacing = 30
        
        for x in range(self.base_x + 20, self.base_x + self.width - 20, window_spacing):
            for y in range(self.base_y + 30, self.base_y + self.height - 20, window_spacing + 10):
                if all((x + dx, y + dy) in self.structure_points 
                      for dx in range(window_width) 
                      for dy in range(window_height)):
                    for wx in range(window_width):
                        for wy in range(window_height):
                            if random.random() < 0.7:
                                self.windows.add((x + wx, y + wy))

    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        
        # Draw main structure
        glColor3f(*self.wall_color)
        for x, y in self.structure_points - self.windows:
            glVertex2f(x, y)

        # Draw break edges and debris
        glColor3f(*self.shadow_color)
        for x, y in self.broken_edges:
            glVertex2f(x, y)

        # Draw windows
        glColor3f(*self.window_color)
        for x, y in self.windows:
            glVertex2f(x, y)

        glEnd()


class damaged_building_mid:
    def __init__(self, base_x, base_y, width, height):
        self.base_x = base_x
        self.base_y = base_y
        self.width = width
        self.height = height
        self.wall_color = (0.4, 0.4, 0.4)
        self.shadow_color = (0.3, 0.3, 0.3)
        self.window_color = (0.1, 0.1, 0.1)
        
        self.structure_points = set()
        self.broken_edges = set()
        self.windows = set()
        self.generate_building()

    def create_destruction_chunk(self, center_x, center_y, max_radius):
        chunk_points = set()
        # Create irregular chunk shape
        angles = list(range(0, 360, 10))  # Control points every 10 degrees
        points = []
        
        # Generate irregular radius for each angle
        for angle in angles:
            radius = random.randint(max_radius // 2, max_radius)
            rad = math.radians(angle)
            x = center_x + int(radius * math.cos(rad))
            y = center_y + int(radius * math.sin(rad))
            points.append((x, y))
        
        # Fill the chunk area
        min_x = min(p[0] for p in points) - 5
        max_x = max(p[0] for p in points) + 5
        min_y = min(p[1] for p in points) - 5
        max_y = max(p[1] for p in points) + 5
        
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if random.random() < 0.8:  # Create slightly irregular edges
                    chunk_points.add((x, y))
        
        return chunk_points

    def generate_building(self):
        # Create initial building structure
        for x in range(int(self.base_x), int(self.base_x) + self.width):
            for y in range(int(self.base_y), int(self.base_y) + self.height):
                self.structure_points.add((x, y))

        # Create multiple destruction chunks in the top area
        chunks = []
        num_chunks = random.randint(6, 8)
        top_section = self.height // 3  # Top third of the building
        
        for _ in range(num_chunks):
            chunk_x = random.randint(self.base_x + 40, self.base_x + self.width - 40)
            chunk_y = random.randint(self.base_y + self.height - top_section, 
                                   self.base_y + self.height - 20)
            chunk_radius = random.randint(20, 35)
            chunk = self.create_destruction_chunk(chunk_x, chunk_y, chunk_radius)
            chunks.append(chunk)

        # Remove chunks from structure and create edges
        for chunk in chunks:
            for x, y in chunk:
                # Remove all points above the chunk
                for remove_y in range(y, int(self.base_y) + self.height):
                    if (x, remove_y) in self.structure_points:
                        self.structure_points.remove((x, remove_y))
                
                # Create edges
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        check_point = (x + dx, y + dy)
                        if check_point in self.structure_points:
                            self.broken_edges.add(check_point)

        # Add scattered debris
        for edge_x, edge_y in list(self.broken_edges):
            if random.random() < 0.15:  # 15% chance for debris at each edge
                for _ in range(random.randint(1, 3)):
                    debris_x = edge_x + random.randint(-8, 8)
                    debris_y = edge_y + random.randint(-8, 8)
                    if (debris_x, debris_y) not in self.structure_points:
                        self.broken_edges.add((debris_x, debris_y))

        # Generate windows in remaining structure
        window_width = 15
        window_height = 20
        window_spacing = 30
        
        for x in range(self.base_x + 20, self.base_x + self.width - 20, window_spacing):
            for y in range(self.base_y + 30, self.base_y + self.height - 20, window_spacing + 10):
                if all((x + dx, y + dy) in self.structure_points 
                      for dx in range(window_width) 
                      for dy in range(window_height)):
                    for wx in range(window_width):
                        for wy in range(window_height):
                            if random.random() < 0.7:
                                self.windows.add((x + wx, y + wy))

    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        
        # Draw main structure
        glColor3f(*self.wall_color)
        for x, y in self.structure_points - self.windows:
            glVertex2f(x, y)

        # Draw break edges and debris
        glColor3f(*self.shadow_color)
        for x, y in self.broken_edges:
            glVertex2f(x, y)

        # Draw windows
        glColor3f(*self.window_color)
        for x, y in self.windows:
            glVertex2f(x, y)

        glEnd()


class damaged_building_right:

    def __init__(self, base_x, base_y, width, height):
        self.base_x = base_x
        self.base_y = base_y
        self.width = width
        self.height = height
        self.wall_color = (0.4, 0.4, 0.4)  # Building color
        self.shadow_color = (0.3, 0.3, 0.3)  # For depth effect
        self.window_color = (0.1, 0.1, 0.1)
        
        # Generate the building structure
        self.structure_points = set()
        self.broken_edges = set()
        self.windows = set()
        self.generate_building()

    def generate_building(self):
        # First, create full building
        for x in range(int(self.base_x), int(self.base_x) + self.width):
            for y in range(int(self.base_y), int(self.base_y) + self.height):
                self.structure_points.add((x, y))

        # Create the broken section (diagonal break from top-middle to right-middle)
        break_points = set()
        
        # Define break control points for zigzag pattern
        control_points = [
            (self.base_x + self.width//2, self.base_y + self.height),  # Start at top-middle
            (self.base_x + self.width//2 + 30, self.base_y + self.height - 50),
            (self.base_x + self.width//2 + 70, self.base_y + self.height - 120),
            (self.base_x + self.width - 20, self.base_y + self.height//2)   # End at right-middle
        ]

        # Connect control points with jagged lines
        for i in range(len(control_points)-1):
            start = control_points[i]
            end = control_points[i+1]
            
            # Create jagged line between points
            steps = 20
            for t in range(steps):
                # Interpolate between points with some randomness
                progress = t / steps
                x = int(start[0] + (end[0] - start[0]) * progress + random.randint(-5, 5))
                y = int(start[1] + (end[1] - start[1]) * progress + random.randint(-5, 5))
                
                # Remove everything above this line
                for remove_x in range(x - 2, x + 3):  # Thickness of break line
                    for remove_y in range(y, int(self.base_y) + self.height):
                        if (remove_x, remove_y) in self.structure_points:
                            self.structure_points.remove((remove_x, remove_y))
                        # Add to broken edges if it's at the border of removal
                        if (remove_x, y) in self.structure_points:
                            self.broken_edges.add((remove_x, y))

        # Generate windows that aren't in the broken section
        window_width = 15
        window_height = 20
        window_spacing = 30
        
        for x in range(self.base_x + 20, self.base_x + self.width - 20, window_spacing):
            for y in range(self.base_y + 30, self.base_y + self.height - 20, window_spacing + 10):
                window_area = set()
                if all((x + dx, y + dy) in self.structure_points 
                      for dx in range(window_width) 
                      for dy in range(window_height)):
                    # Create broken window effect
                    for wx in range(window_width):
                        for wy in range(window_height):
                            if random.random() < 0.7:  # Make windows look broken
                                window_area.add((x + wx, y + wy))
                    self.windows.update(window_area)

    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        
        # Draw main building structure
        glColor3f(*self.wall_color)
        for x, y in self.structure_points - self.windows:
            glVertex2f(x, y)

        # Draw broken edges (slightly darker for depth)
        glColor3f(*self.shadow_color)
        for x, y in self.broken_edges:
            glVertex2f(x, y)
            # Add some debris near edges
            if random.random() < 0.1:  # Sparse debris
                debris_x = x + random.randint(-3, 3)
                debris_y = y + random.randint(-3, 3)
                if (debris_x, debris_y) not in self.structure_points:
                    glVertex2f(debris_x, debris_y)

        # Draw windows
        glColor3f(*self.window_color)
        for x, y in self.windows:
            glVertex2f(x, y)

        glEnd()


class damaged_building_tall:

    def __init__(self, base_x, base_y, width, height):
        self.base_x = base_x
        self.base_y = base_y
        self.width = width
        self.height = height
        # Define building colors
        self.wall_color = (0.4, 0.4, 0.4)  # Gray for walls
        self.damage_color = (0.3, 0.3, 0.3)  # Darker gray for damaged areas
        self.window_color = (0.1, 0.1, 0.1)  # Dark for broken windows
        
        # Generate random damage patterns
        self.damage_points = self.generate_damage_pattern()
        # Generate windows
        self.windows = self.generate_windows()
        # Generate cracks
        self.cracks = self.generate_cracks()

    def generate_damage_pattern(self):
        damage = set()
        # Instead of a round hole, we create irregular damage
        # Create a large irregular hole
        hole_x = self.base_x + self.width // 3
        hole_y = self.base_y + self.height // 4
        
        # Generate a jagged or irregular hole using cracks or lines
        for _ in range(20):  # Randomize number of points for irregular hole
            x_offset = random.randint(-15, 15)
            y_offset = random.randint(-15, 15)
            damage.add((hole_x + x_offset, hole_y + y_offset))
        
        return damage

    def generate_windows(self):
        windows = []
        window_width = 15
        window_height = 20
        window_spacing = 30
        
        # Create a grid of windows
        for x in range(int(self.base_x) + 20, int(self.base_x) + self.width - 20, window_spacing):
            for y in range(int(self.base_y) + 30, int(self.base_y) + self.height - 20, window_spacing + 10):
                # Randomly make some windows broken (irregular shapes)
                if random.random() < 0.7:  # 70% chance of window being broken
                    broken_points = set()
                    for px in range(window_width):
                        for py in range(window_height):
                            if random.random() < 0.7:  # Create irregular broken pattern
                                broken_points.add((x + px, y + py))
                    windows.append(broken_points)
                else:
                    # Intact window (regular rectangle)
                    intact_points = set()
                    for px in range(window_width):
                        for py in range(window_height):
                            intact_points.add((x + px, y + py))
                    windows.append(intact_points)
        
        return windows

    def generate_cracks(self):
        cracks = []
        # Generate several cracks starting from damage points
        for _ in range(5):
            start_x = random.randint(self.base_x, self.base_x + self.width)
            start_y = random.randint(self.base_y, self.base_y + self.height)
            end_x = start_x + random.randint(-50, 50)
            end_y = start_y + random.randint(-50, 50)
            
            # Use midpoint line algorithm for cracks
            crack_points = midpoint_line(start_x, start_y, end_x, end_y)
            cracks.append(crack_points)
            
            # Add some branching cracks
            if random.random() < 0.5:
                branch_x = end_x + random.randint(-30, 30)
                branch_y = end_y + random.randint(-30, 30)
                branch_points = midpoint_line(end_x, end_y, branch_x, branch_y)
                cracks.append(branch_points)
        
        return cracks

    def draw(self):
        # Draw main building structure
        glPointSize(1.0)
        glBegin(GL_POINTS)
        
        # Draw the main wall
        glColor3f(*self.wall_color)
        for x in range(int(self.base_x), int(self.base_x) + self.width):
            for y in range(int(self.base_y), int(self.base_y) + self.height):
                if (x, y) not in self.damage_points:  # Don't draw where there's damage
                    glVertex2f(x, y)
        
        # Draw the damage (darker color)
        glColor3f(*self.damage_color)
        for x, y in self.damage_points:
            glVertex2f(x, y)
        
        # Draw windows
        glColor3f(*self.window_color)
        for window in self.windows:
            for x, y in window:
                glVertex2f(x, y)
        
        # Draw cracks
        glColor3f(0.2, 0.2, 0.2)  # Dark gray for cracks
        for crack in self.cracks:
            for x, y in crack:
                glVertex2f(x, y)
        
        glEnd()


