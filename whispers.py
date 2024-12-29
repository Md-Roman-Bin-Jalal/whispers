from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
from midpoint_line import midpoint_line
from midpoint_circle import midpoint_circle
from Buildings import damaged_building_left, damaged_building_mid_spikes, damaged_building_mid_spikes_2, damaged_building_mid, damaged_building_right, damaged_building_tall
from Forest import tall_slender_tree, bushy_fat_tree, slim_columnar_tree, compact_thick_tree, miniature_tree, pyramid_tree, umbrella_tree, multi_layer_tree
from Cars import draw_scratched_sedan, draw_wrecked_coupe, draw_totaled_wreck
from Lamps import single_head_lemp, double_head_lamp

key_states = {b'a': False, b'd': False}  # Track key presses

class Whispers:

    def __init__(self, width, height):

        # width height of the window
        self.width = int(width)
        self.height = int(height)
        self.road_height = int(height * 0.15)
        
        # Adjust robot's initial position and scale
        self.robot_scale = 0.5  # Added scale factor for robot
        self.robot_x = 50  # Start from left side
        self.robot_y = self.road_height // 2  # Place robot on road's center line
        self.step_state = 0     # for walking animation
        self.spacing = 300      # spaces between obj

        self.robot_width = 40 * self.robot_scale  # Add robot dimensions
        self.robot_height = 110 * self.robot_scale

        self.buildings = []     # to store obj
        self.trees = []
        self.lamps = []
        self.cars = []

        self.last_mist_time = time.time()
        self.interval = 15  # Seconds
        self.animation_step = 0
        self.mirror_arms = False
        self.robot_speed = 10  # Slightly reduced for smoother movement

        # World position tracking
        self.world_offset = 0  # Tracks camera offset in the world
        self.camera_speed = 0

        self.num_points = 3000  # for the mists
        self.fog_radius = 25
        self.movement_speed = 0.05
        self.points = []

        self.collision_count = 0 # mist and robot
        self.mist_position_variable = 4
        self.mist_position = self.width / self.mist_position_variable
        self.tree_color_state = False
        self.car_color_state = False
        self.lamp_light_state = False
        self.lamp_is_fallen = True

        self.is_paused = False  # tarck game paused or not
        self.show_text = False
        self.text_start_time = 0
        self.current_text_phase = 0  # 0: no text, 1: fragment name, 2: description
        self.fragments = [
            ("\"Chapter 01\" : The City of Echoes", "\"The streets were once alive, filled with voices ... but some voices should never have been heard.\"", (0.9, 0.7, 0.3), (0.75, 0.55, 0.25)),
            ("Obtained \"Flickers of Dread\"", "\"The flame that once lit the streets now flickers in the hearts of the lost. Some truths are buried too deep to be revealed.\"", (0.6, 0.1, 0.1), (0.8, 0.3, 0.3)),
            ("Obtained \"Shards of Silence\"", "\"In the shadows of stone, a pact was made. A bargain no soul should ever seal.\"", (0.7, 1.0, 0.7), (0.4, 0.7, 0.4)),
            ("Obtained \"Glimmers_of Fear\"", "\"They sought salvation in the wrong places. But salvation is never without its price.\"", (1.0, 0.7, 0.7), (0.7, 0.4, 0.4)),
            ("End of \"Chapter 0!\"", "\"The city never fell. It was abandoned. Abandoned by those who could never leave.\"", (0.7, 0.7, 1.0), (0.4, 0.4, 0.7))
        ]
        self.current_fragment = None

        self.flickers_of_dread = True
        self.shards_of_silence = True
        self.glimmers_of_fear = True

        self.previous_game_state = False  # Track previous game state when menu is opened via escape
        self.game_in_progress = False  # Track if a game has been started
        self.came_from_escape = False  # Track if menu was opened via escape

        # Add menu states 
        self.show_menu = False
        self.game_started = False
        self.show_goodbye = False
        self.selected_button = 0  # 0: Play, 1: Restart, 2: Exit
        self.menu_buttons = ["Play", "Restart", "Exit"]
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 20

        self.show_title_sequence = True
        self.title_start_time = time.time()
        self.title_scale = 0.1  # Starting scale
        self.title_alpha = 0.0  # Starting opacity
        
        # Add after other menu-related variables
        self.game_title = "Whispers"
        self.subtitle = "Beneath the Darkness"

        self.generate_initial_scene()

    def create_character_points(self, char, base_x, base_y, scale=1):
        """Convert a character into points using midpoint line algorithm"""
        points = set()  # Use set to avoid duplicate points
        
        # Define characters using line segments
        characters = {
            # Letters
            'A': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,0)], [(0,1.5), (2,1.5)]],
            'B': [[(0,0), (0,3)], [(0,3), (1.5,3)], [(1.5,3), (2,2.5)], [(2,2.5), (2,2)], 
                [(2,2), (1.5,1.5)], [(1.5,1.5), (0,1.5)], [(1.5,1.5), (2,1)], [(2,1), (2,0.5)], 
                [(2,0.5), (1.5,0)], [(1.5,0), (0,0)]],
            'C': [[(2,3), (0,3)], [(0,3), (0,0)], [(0,0), (2,0)]],
            'D': [[(0,0), (0,3)], [(0,3), (1.5,3)], [(1.5,3), (2,2)], [(2,2), (2,1)], 
                [(2,1), (1.5,0)], [(1.5,0), (0,0)]],
            'E': [[(2,3), (0,3)], [(0,3), (0,0)], [(0,0), (2,0)], [(0,1.5), (1.5,1.5)]],
            'F': [[(2,3), (0,3)], [(0,3), (0,0)], [(0,1.5), (1.5,1.5)]],
            'G': [[(2,3), (0,3)], [(0,3), (0,0)], [(0,0), (2,0)], [(2,0), (2,1.5)], [(2,1.5), (1,1.5)]],
            'H': [[(0,0), (0,3)], [(2,0), (2,3)], [(0,1.5), (2,1.5)]],
            'I': [[(1,0), (1,3)], [(0,3), (2,3)], [(0,0), (2,0)]],
            'J': [[(2,3), (2,0)], [(2,0), (1,0)], [(1,0), (0,0)], [(0,0), (0,1)]],
            'K': [[(0,0), (0,3)], [(0,1.5), (2,3)], [(0,1.5), (2,0)]],
            'L': [[(0,3), (0,0)], [(0,0), (2,0)]],
            'M': [[(0,0), (0,3)], [(0,3), (1,1.5)], [(1,1.5), (2,3)], [(2,3), (2,0)]],
            'N': [[(0,0), (0,3)], [(0,3), (2,0)], [(2,0), (2,3)]],
            'O': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,0)], [(2,0), (0,0)]],
            'P': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,1.5)], [(2,1.5), (0,1.5)]],
            'Q': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,0)], [(2,0), (0,0)], [(1.5,0.5), (2,0)]],
            'R': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,1.5)], [(2,1.5), (0,1.5)], 
                [(0,1.5), (2,0)]],
            'S': [[(2,3), (0,3)], [(0,3), (0,1.5)], [(0,1.5), (2,1.5)], [(2,1.5), (2,0)], 
                [(2,0), (0,0)]],
            'T': [[(1,0), (1,3)], [(0,3), (2,3)]],
            'U': [[(0,3), (0,0)], [(0,0), (2,0)], [(2,0), (2,3)]],
            'V': [[(0,3), (1,0)], [(1,0), (2,3)]],
            'W': [[(0,3), (0,0)], [(0,0), (1,1)], [(1,1), (2,0)], [(2,0), (2,3)]],
            'X': [[(0,3), (2,0)], [(2,3), (0,0)]],
            'Y': [[(0,3), (1,1.5)], [(2,3), (1,1.5)], [(1,1.5), (1,0)]],
            'Z': [[(0,3), (2,3)], [(2,3), (0,0)], [(0,0), (2,0)]],
            # Numbers
            '0': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,0)], [(2,0), (0,0)]],
            '1': [[(1,0), (1,3)]],
            '2': [[(0,3), (2,3)], [(2,3), (2,1.5)], [(2,1.5), (0,0)], [(0,0), (2,0)]],
            '3': [[(0,3), (2,3)], [(2,3), (2,1.5)], [(2,1.5), (0,1.5)], [(2,1.5), (2,0)], [(2,0), (0,0)]],
            '4': [[(0,3), (0,1.5)], [(0,1.5), (2,1.5)], [(2,3), (2,0)]],
            '5': [[(2,3), (0,3)], [(0,3), (0,1.5)], [(0,1.5), (2,1.5)], [(2,1.5), (2,0)], [(2,0), (0,0)]],
            '6': [[(2,3), (0,3)], [(0,3), (0,0)], [(0,0), (2,0)], [(2,0), (2,1.5)], [(2,1.5), (0,1.5)]],
            '7': [[(0,3), (2,3)], [(2,3), (0,0)]],
            '8': [[(0,0), (0,3)], [(0,3), (2,3)], [(2,3), (2,0)], [(2,0), (0,0)], [(0,1.5), (2,1.5)]],
            '9': [[(0,0), (2,0)], [(2,0), (2,3)], [(2,3), (0,3)], [(0,3), (0,1.5)], [(0,1.5), (2,1.5)]],
            # Symbols
            '.': [[(0,0), (0.2,0)]],
            ' ': [],
            ':': [[(0,0), (0.2,0)], [(0,2), (0.2,2)]],
            ',': [[(0.1, 0), (0.2, -0.2)], [(0.2, -0.2), (0.15, -0.4)], [(0.15, -0.4), (0.1, -0.5)]],
            "'": [[(0,3), (0,2.5)]],
            '!': [[(0,0), (0.2,0)], [(0,1), (0,3)]],
            '?': [[(0.8,0), (1.2,0)], [(1,1), (1,1.5)], [(1,1.5), (1.8,2)], [(1.8,2), (1.8,2.5)], 
                 [(1.8,2.5), (1.5,3)], [(1.5,3), (0.5,3)], [(0.5,3), (0.2,2.5)], [(0.2,2.5), (0.2,2)]],
            '"': [[(0,3), (0,2.5)], [(1,3), (1,2.5)]],
            '-': [[(0,1.5), (2,1.5)]],
            '_': [[(0,0), (2,0)]],
            '=': [[(0,2), (2,2)], [(0,1), (2,1)]],
            '+': [[(1,0), (1,3)], [(0,1.5), (2,1.5)]],
        }
        
        char = char.upper()
        if char in characters:
            for line in characters[char]:
                if len(line) == 2:
                    x1, y1 = line[0]
                    x2, y2 = line[1]
                    # Scale and translate the points
                    p1 = (base_x + x1 * scale, base_y + y1 * scale)
                    p2 = (base_x + x2 * scale, base_y + y2 * scale)
                    # Use midpoint line algorithm
                    line_points = midpoint_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
                    points.update(line_points)
        
        return list(points)

    def draw_point_text(self, x, y, text, color, scale=1):
        """Draw text using points with proper scaling"""
        current_x = x
        spacing = scale * 3     # Adjust spacing between characters
        glPointSize(5) if self.current_text_phase == 1 else glPointSize(4)
        glBegin(GL_POINTS)
        glColor3f(*color)
        
        for char in text:
            points = self.create_character_points(char, current_x, y, scale)
            for px, py in points:
                glVertex2f(px, py)
            current_x += spacing
        
        glEnd()
        glPointSize(1.0)   # Reset point size

    def create_blur_effect(self):
        """Create a point-based blur effect"""
        glPointSize(3)
        glBegin(GL_POINTS)
        glColor4f(0.0, 0.0, 0.0, 0.5)
        
        spacing = 2  # Reduced spacing for denser points
        for x in range(0, self.width, spacing):
            for y in range(0, self.height, spacing):
                glVertex2f(x, y)
        
        glEnd()
        glPointSize(1.0)  # Reset point size

    def handle_collision_text(self):
        current_time = time.time()
        
        if not self.show_text:
            return

        self.create_blur_effect()

        if self.current_text_phase == 1:
            fragment_name = self.current_fragment[0]
            available_width = self.width / 1.67
            char_scale = int(available_width / (len(fragment_name) * 4))  # 4 units per character
            
            text_width = len(fragment_name) * char_scale * 3
            x = (self.width - text_width) / 2
            y = self.height / 2
            
            self.draw_point_text(x, y, fragment_name, self.current_fragment[2], char_scale)
            
            if current_time - self.text_start_time > 3:
                self.text_start_time = current_time
                self.current_text_phase = 2
                
        elif self.current_text_phase == 2:
            description = self.current_fragment[1]
            available_width = self.width / 1.25
            char_scale = int(available_width / (35 * 4))  # max 35 chars per line
            
            # Split text into lines
            words = description.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                word_length = len(word)
                if current_length + word_length <= 35:
                    current_line.append(word)
                    current_length += word_length + 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length + 1
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw each line
            line_height = char_scale * 7
            start_y = self.height/2 + (len(lines) * line_height)/2
            
            for i, line in enumerate(lines):
                text_width = len(line) * char_scale * 3
                x = (self.width - text_width) / 2
                y = start_y - (i * line_height)
                self.draw_point_text(x, y, line, self.current_fragment[3], char_scale)
            
            if current_time - self.text_start_time > 6:
                self.show_text = False
                self.current_text_phase = 0
                self.is_paused = False

    def get_random_building(self, x, y, width, height):
        BuildingClass = random.choice([damaged_building_left, damaged_building_mid_spikes, damaged_building_mid_spikes_2, damaged_building_mid, damaged_building_right, damaged_building_tall])
        return BuildingClass(
            int(x),
            int(y),
            int(width),
            int(height)
        )

    def get_random_tree(self, x, y):
        TreeClass = random.choice([tall_slender_tree, bushy_fat_tree, slim_columnar_tree, compact_thick_tree, miniature_tree, pyramid_tree, umbrella_tree, multi_layer_tree])
        tree = TreeClass(int(x), int(y), self.height, self.tree_color_state)
        return tree

    def get_random_lamp(self, x, y):
        LampClass = random.choice([single_head_lemp, double_head_lamp])
        lamp_orientation = random.choice(['Left', 'Right'])
        return (LampClass, x, y, lamp_orientation, self.lamp_light_state, self.lamp_is_fallen)

    def get_random_car(self, x, y):
        """Generate a car with position relative to the current view"""
        car_y = self.road_height * 0.3  # Raised to 30% of road height
        
        bounded_x = max(0, min(x, self.width * 2))    # Keep x position within a reasonable range
        
        car_type = random.choice([draw_scratched_sedan, draw_wrecked_coupe, draw_totaled_wreck])
        orientation = 'left' if random.random() > 0.5 else 'right'

        return (car_type, bounded_x, car_y, orientation)

    def generate_initial_scene(self):
        # Generate more initial content for smoother scrolling
        start_x = -self.width * 2  # Extended range for backward movement
        end_x = self.width * 3
        current_x = start_x

        while current_x < end_x:

            width = random.randint(150, 250)
            height = random.randint(300, 400)

            building = self.get_random_building(current_x, self.road_height, width, height)
            self.buildings.append(building)

            tree_x = current_x + width // 2 + random.randint(40, 60)
            tree = self.get_random_tree(tree_x, self.road_height)
            self.trees.append(tree)

            lamp_x = current_x + width // 2 + random.randint(-20, 20)
            lamp = self.get_random_lamp(lamp_x, self.road_height)
            self.lamps.append(lamp)

            car_x = current_x + width // 2 + random.randint(-50, 50)
            car = self.get_random_car(car_x, self.road_height)
            self.cars.append(car)

            current_x += self.spacing

    def generate_mists(self):
        self.points = []
        for _ in range(self.num_points):
            angle = random.uniform(0, 2 * math.pi)  # Random angle
            radius = random.uniform(0, self.fog_radius)  # Random distance from center
            x = radius * math.cos(angle) # Wider spread
            y = radius * math.sin(angle) # Vertical spread
            z = random.uniform(-1.0, 1.0)
            color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
            self.points.append((x, y, z, color))

    def update_mist(self):
        for i in range(len(self.points)):
            x, y, z, color = self.points[i]
            x += random.uniform(-self.movement_speed, self.movement_speed)
            y += random.uniform(-self.movement_speed, self.movement_speed)
            z += random.uniform(-self.movement_speed, self.movement_speed)
            # Keep points within the fog radius
            distance = math.sqrt(x**2 + y**2)
            if distance > self.fog_radius:
                angle = math.atan2(y, x)
                x = self.fog_radius * math.cos(angle)
                y = self.fog_radius * math.sin(angle)

            self.points[i] = (x, y, z, color)
        
        # Add collision check after updating mist positions
        self.check_mist_collision()

    def draw_mist(self):
        glPointSize(1)  # Set point size for mist particles
        glBegin(GL_POINTS)
        for point in self.points:
            x, y, z, color = point
            x += self.mist_position + random.uniform(0, 10)  # Adjust for robot and camera position
            y += self.robot_y + 25 # Center around the robot's y position
            glColor3f(color[0], color[1], color[2])  # Set the point color
            glVertex3f(x, y, z)  # Draw the point
        glEnd()

    def has_collided(self, box1, box2):     # checks collision
        """Check if two bounding boxes intersect"""
        return (box1["x"] < box2["x"] + box2["width"] and
                box1["x"] + box1["width"] > box2["x"] and
                box1["y"] < box2["y"] + box2["height"] and
                box1["y"] + box1["height"] > box2["y"])

    def check_mist_collision(self):
        """Check for collision between robot and mist points"""
        robot_box = {
            "x": self.robot_x - self.robot_width/2,
            "y": self.robot_y - self.robot_height/2,
            "width": self.robot_width,
            "height": self.robot_height
        }
        
        # Check each mist point against robot bounding box
        for i, point in enumerate(self.points):
            x, y, z, color = point
            x_adjusted = x + self.mist_position  # Apply the same adjustment as in draw_mist
            y_adjusted = y + self.robot_y + 25  # Apply the same adjustment as in draw_mist
            
            mist_point_box = {
                "x": x_adjusted - 1,  # Small bounding box for mist point
                "y": y_adjusted - 1,
                "width": 2,
                "height": 2
            }
            
            if self.has_collided(robot_box, mist_point_box):
                print('collided')
                self.collision_count += 1
                self.points.clear()
                
                # Pause game and show text
                self.is_paused = True
                self.show_text = True
                self.current_text_phase = 1
                self.text_start_time = time.time()
                
                # Select appropriate fragment based on collision count
                if self.collision_count <= 5:
                    self.current_fragment = self.fragments[self.collision_count]
                break

    def add_mist(self):
        current_time = time.time()
        if current_time - self.last_mist_time >= self.interval:
            self.generate_mists()
            self.last_mist_time = current_time
            self.interval += 1

    def update_scene(self):
        if key_states[b'a']:
            self.camera_speed = -self.robot_speed
        elif key_states[b'd']:
            self.camera_speed = self.robot_speed
        elif self.camera_speed != 0:  # Continue moving if no key is pressed
            self.camera_speed = self.camera_speed  # Maintain previous speed
        else:
            self.camera_speed = 0

        # Update world offset
        self.world_offset += self.camera_speed

        # Calculate the relative position for scene elements
        visible_range = self.width * 1.5
        min_x = self.world_offset - visible_range
        max_x = self.world_offset + visible_range

        # Remove out-of-range objects
        self.buildings = [b for b in self.buildings if min_x < b.base_x < max_x]
        self.trees = [t for t in self.trees if min_x < t.base_x < max_x]
        self.lamps = [l for l in self.lamps if min_x < l[1] < max_x]
        self.cars = [c for c in self.cars if min_x < c[1] < max_x]

        # Generate new content in both directions
        if len(self.buildings) < 15:  # Maintain a minimum number of buildings
            if self.camera_speed >= 0:
                last_x = max((b.base_x for b in self.buildings), default=self.world_offset)
                self.add_new_section(last_x + self.spacing)
            else:
                first_x = min((b.base_x for b in self.buildings), default=self.world_offset)
                self.add_new_section(first_x - self.spacing)

    def add_new_section(self, x):
        width = random.randint(150, 250)
        height = random.randint(300, 400)

        building = self.get_random_building(x, self.road_height, width, height)
        self.buildings.append(building)

        tree_x = x + width // 2 + random.randint(40, 60)
        tree = self.get_random_tree(tree_x, self.road_height)
        self.trees.append(tree)

        if random.random() > 0.5:   # 50% chance of drawing lamps
            lamp_x = x + width // 2 + random.randint(-20, 20)
            lamp = self.get_random_lamp(lamp_x, self.road_height)
            self.lamps.append(lamp)

        if random.random() > 0.3:      # 30% chance of drawing cars
            car_x = x + width // 2 + random.randint(-30, 30)
            car = self.get_random_car(car_x, self.road_height)
            self.cars.append(car)

    def check_collision_count(self):

        if self.collision_count == 3 and self.glimmers_of_fear:

            self.tree_color_state = True
            for tree in self.trees:
                tree.tree_color_state = self.tree_color_state

            self.glimmers_of_fear = False

            self.mist_position_variable = random.uniform(1.3, 3)
            self.mist_position = self.width / self.mist_position_variable

            if abs(self.mist_position - self.robot_x) < 100:    # ensures mist is drawn away from robot
                self.mist_position + random.choice([-100, 100])

        if self.collision_count == 2 and self.shards_of_silence:

            self.car_color_state = True
            for car in self.cars:
                car_type = car[0]
                car_type.car_color_state = self.car_color_state

            self.shards_of_silence = False

            self.mist_position_variable = random.uniform(1.3, 3)
            self.mist_position = self.width / self.mist_position_variable

            if abs(self.mist_position - self.robot_x) < 100:
                self.mist_position + random.choice([-100, 100])

        if self.collision_count == 1 and self.flickers_of_dread:

            self.lamp_light_state = True
            self.lamp_is_fallen = False
            
            new_lamps = []
            for lamp in self.lamps:
                lamp_class, x, y, orientation, _, _ = lamp
                new_lamps.append((lamp_class, x, y, orientation, self.lamp_light_state, self.lamp_is_fallen))
            self.lamps = new_lamps

            self.flickers_of_dread = False

            self.mist_position_variable = random.uniform(1.3, 3)
            self.mist_position = self.width / self.mist_position_variable

            if abs(self.mist_position - self.robot_x) < 100:
                self.mist_position + random.choice([-100, 100])

        # Add check for game completion
        if self.collision_count == 4:
            self.current_fragment = self.fragments[4]
            self.is_paused = True
            self.show_text = True
            self.current_text_phase = 1
            self.text_start_time = time.time()
            
            # Schedule reset and return to menu
            def reset_to_menu():
                self.reset_game()
                self.show_menu = True
                self.game_started = False
                
            glutTimerFunc(9000, lambda _: reset_to_menu(), 0)   # 9s wait to auto exit game

    def move_robot_and_camera(self, direction):
        """Move both robot and camera"""
        self.robot_x += direction * self.robot_speed
        self.world_offset += direction * self.robot_speed

    def draw(self):

        if self.show_title_sequence:
            self.draw_title_sequence()
            return
        
        if self.show_menu:
            self.draw_menu()
            return
        
        if self.show_goodbye:
            glClear(GL_COLOR_BUFFER_BIT)
            self.draw_point_text(
                self.width/4 - 50,
                self.height/2,
                "City of echoes will wait for your arrival !!!",    # game ending quote
                (1.0, 1.0, 1.0),
                6
            )
            return

        self.draw_road()

        glPushMatrix()

        # Translate world based on camera offset
        glTranslatef(-self.world_offset, 0, 0)

        # Only draw objects that are within the visible range
        visible_range = self.width * 1.5
        min_x = self.world_offset - visible_range
        max_x = self.world_offset + visible_range

        # Draw other elements
        for building in self.buildings:
            if min_x <= building.base_x <= max_x:     # Only draw if in visible range
                building.draw()

        for tree in self.trees:
            if min_x <= tree.base_x <= max_x:
                tree.draw()

        for lamp in self.lamps:
            lamp_class, x, y, orientation, lamp_light, is_fallen = lamp
            if min_x <= x <= max_x:
                lamp_instance = lamp_class(x, y, orientation, lamp_light, is_fallen)
                lamp_instance.draw()

        for car in self.cars:
            car_type, x, y, orientation = car
            if min_x <= x <= max_x:
                car_type(x, y, orientation, self.car_color_state).draw()

        glPopMatrix()

        self.add_mist()
        self.update_mist()
        self.draw_mist()
        self.draw_robot()
        self.check_collision_count()

        if self.show_text:
            self.handle_collision_text()

    def draw_robot(self):
        glColor3f(1.0, 1.0, 1.0)
        self.draw_robot_side_view(self.robot_x, self.step_state, self.mirror_arms)
        # Uncomment for debugging the collision box
        # self.draw_robot_collision_box()
        # self.draw_mist_collision_box()

    def draw_robot_collision_box(self):
        """Debug method to visualize the robot's collision box"""
        glColor3f(1.0, 0.0, 0.0)  # Red color for collision box
        glBegin(GL_LINE_LOOP)
        x = self.robot_x - self.robot_width/2
        y = self.robot_y - self.robot_height/2
        glVertex2f(x, y)
        glVertex2f(x + self.robot_width, y)
        glVertex2f(x + self.robot_width, y + self.robot_height)
        glVertex2f(x, y + self.robot_height)
        glEnd()

    def draw_mist_collision_box(self):
        """Debug method to visualize the mist points' collision boxes"""
        glColor3f(0.0, 1.0, 0.0)  # Green color for mist collision boxes
        glBegin(GL_POINTS)
        for point in self.points:
            x, y, z, color = point
            x_adjusted = x + (self.width/1.5)
            y_adjusted = y + self.robot_y + 25
            
            # Draw collision box corners
            glVertex2f(x_adjusted - 1, y_adjusted - 1)
            glVertex2f(x_adjusted + 1, y_adjusted - 1)
            glVertex2f(x_adjusted + 1, y_adjusted + 1)
            glVertex2f(x_adjusted - 1, y_adjusted + 1)
        glEnd()

    def draw_robot_side_view(self, x_offset, step_state, mirror_arms=False):

        glPushMatrix()
        glTranslatef(x_offset, self.robot_y, 0)
        glScalef(self.robot_scale, self.robot_scale, 1.0)
        glTranslatef(-x_offset, -self.robot_y, 0)

        def draw_circle_points(points):
            glBegin(GL_POINTS)
            for (x, y) in points:
                glVertex2f(x, y)
            glEnd()

        def draw_two_part_arm(x_offset, y_offset, is_left_arm=False, mirror_arms=False):
            if step_state % 2 == 0:
                lux, luy, llx, lly, rux, rlx, rly = 23, 13, 23, 13, 13, 13, 23
            else:
                lux, luy, llx, lly, rux, rlx, rly = 15, 20, 15, 20, 20, 20, 15

            if mirror_arms:
                luy, llx, rux, rly = -luy, -llx, -rux, -rly

            if is_left_arm:
                upper_arm_end_x = x_offset + luy
                upper_arm_end_y = y_offset - lux
                lower_arm_end_x = upper_arm_end_x + llx
                lower_arm_end_y = upper_arm_end_y + lly
            else:
                upper_arm_end_x = x_offset + rux
                upper_arm_end_y = y_offset - 30
                lower_arm_end_x = upper_arm_end_x + rly
                lower_arm_end_y = upper_arm_end_y + rlx

            upper_arm_points = midpoint_line(x_offset, y_offset, upper_arm_end_x, upper_arm_end_y)
            lower_arm_points = midpoint_line(upper_arm_end_x, upper_arm_end_y, lower_arm_end_x, lower_arm_end_y)

            return upper_arm_points, lower_arm_points

        head_points = midpoint_circle(x_offset, self.robot_y + 70, 20)
        draw_circle_points(head_points)

        body_points = midpoint_line(x_offset, self.robot_y + 50, x_offset, self.robot_y)
        draw_circle_points(body_points)

        right_arm_upper, right_arm_lower = draw_two_part_arm(x_offset, self.robot_y + 50, mirror_arms=mirror_arms)
        left_arm_upper, left_arm_lower = draw_two_part_arm(x_offset, self.robot_y + 50, is_left_arm=True, mirror_arms=mirror_arms)
        draw_circle_points(right_arm_upper)
        draw_circle_points(right_arm_lower)
        draw_circle_points(left_arm_upper)
        draw_circle_points(left_arm_lower)

        if step_state == 0:     # simulates walking
            right_leg_points = midpoint_line(x_offset, self.robot_y, x_offset + 10, self.robot_y - 40)
            left_leg_points = midpoint_line(x_offset, self.robot_y, x_offset - 10, self.robot_y - 40)
        elif step_state == 1:
            right_leg_points = midpoint_line(x_offset, self.robot_y, x_offset + 20, self.robot_y - 20)
            left_leg_points = midpoint_line(x_offset, self.robot_y, x_offset - 10, self.robot_y - 50)
        elif step_state == 2:
            right_leg_points = midpoint_line(x_offset, self.robot_y, x_offset + 10, self.robot_y - 50)
            left_leg_points = midpoint_line(x_offset, self.robot_y, x_offset - 20, self.robot_y - 20)

        draw_circle_points(right_leg_points)
        draw_circle_points(left_leg_points)
        
        glPopMatrix()

    def draw_road(self):
        glColor3f(0.3, 0.3, 0.3)
        for x in range(0, self.width, 1):
            line_points = midpoint_line(x, 0, x, self.road_height)
            glBegin(GL_POINTS)
            for px, py in line_points:
                glVertex2f(px, py)
            glEnd()

        glColor3f(1.0, 1.0, 1.0)
        marking_width = 40
        marking_gap = 60
        marking_y = self.road_height // 2
        marking_height = 5

        # Adjust road markings based on world offset
        offset = self.world_offset % (marking_width + marking_gap)

        x = -offset

        while x < self.width:
            line_points = midpoint_line(x, marking_y - marking_height // 2, x + marking_width, marking_y - marking_height // 2)
            glBegin(GL_POINTS)
            for px, py in line_points:
                glVertex2f(px, py)
            glEnd()

            line_points = midpoint_line(x, marking_y + marking_height // 2, x + marking_width, marking_y + marking_height // 2)
            glBegin(GL_POINTS)
            for px, py in line_points:
                glVertex2f(px, py)
            glEnd()

            x += marking_width + marking_gap

    def draw_title_sequence(self):
        """Draw the opening title sequence"""
        current_time = time.time()
        elapsed_time = current_time - self.title_start_time
        
        if elapsed_time >= 5:  # 05 seconds
            self.show_title_sequence = False
            self.show_menu = True
            return
            
        # Calculate scale and alpha based on elapsed time
        progress = min(elapsed_time / 3.0, 1.0)
        self.title_scale = 0.1 + (2.0 - 0.1) * progress  # Scale from 0.1 to 2.0
        self.title_alpha = min(progress * 2, 1.0)  # Fade in faster than scale
        
        # Clear screen to black
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Draw title with current scale and alpha
        title_x = self.width / 2.6

        title_y = self.height / 2
        
        # Add slight randomization to letters for static effect
        letters = []
        for i, char in enumerate(self.game_title):
            offset_x = random.uniform(-1, 1) * progress
            offset_y = random.uniform(-1, 1) * progress
            letters.append((char, offset_x, offset_y))
            
        # Draw main title
        glPointSize(4)
        glColor3f(self.title_alpha, self.title_alpha, self.title_alpha)
        glBegin(GL_POINTS)
        
        for i, (char, offset_x, offset_y) in enumerate(letters):
            base_x = title_x - (len(self.game_title) * 20 * self.title_scale) / 2 + (i * 40 * self.title_scale)
            base_y = title_y + (20 * self.title_scale)
            
            points = self.create_character_points(
                char, 
                base_x + offset_x, 
                base_y + offset_y, 
                scale=8 * self.title_scale
            )
            
            for px, py in points:
                glVertex2f(px, py)
                
        glEnd()

        title_x = self.width / 3
        
        # Draw subtitle with smaller scale
        if elapsed_time > 2:  # Start showing subtitle after 2 seconds
            subtitle_alpha = min((elapsed_time - 2.0), 1.0)
            glColor3f(subtitle_alpha * 0.7, subtitle_alpha * 0.7, subtitle_alpha * 0.7)
            glPointSize(3)
            
            subtitle_x = title_x - (len(self.subtitle) * 15 * self.title_scale) / 2 - 30
            subtitle_y = title_y - (30 * self.title_scale)
            
            subtitle_points = []
            for i, char in enumerate(self.subtitle):
                offset_x = random.uniform(-0.5, 0.5) * progress
                offset_y = random.uniform(-0.5, 0.5) * progress
                char_points = self.create_character_points(
                    char,
                    subtitle_x + (i * 30 * self.title_scale) + offset_x,
                    subtitle_y + offset_y,
                    scale=6 * self.title_scale
                )
                subtitle_points.extend(char_points)
            
            glBegin(GL_POINTS)
            for px, py in subtitle_points:
                glVertex2f(px, py)
            glEnd()

    def reset_game(self):
        """Reset all game state variables"""
        self.collision_count = 0
        self.world_offset = 0
        self.robot_x = 50
        self.robot_y = self.road_height // 2
        self.step_state = 0
        self.points.clear()
        self.buildings.clear()
        self.trees.clear()
        self.lamps.clear()
        self.cars.clear()
        self.is_paused = False
        self.show_text = False
        self.current_text_phase = 0
        self.relic_lamp = True
        self.relic_car = True
        self.relic_tree = True
        self.tree_color_state = False
        self.car_color_state = False
        self.lamp_light_state = False
        self.lamp_is_fallen = True
        self.mist_position_variable = 4
        self.mist_position = self.width / self.mist_position_variable
        self.generate_initial_scene()

    def draw_button(self, x, y, width, height, text, is_selected):

        color = (0.7, 0.7, 0.7) if is_selected else (0.0, 0.6, 0.8)  # Modern Neutrals
        glColor3f(*color)

        width += 100  # Adjust width to make it wider
        x -= 60
        y -= 100

        lines = [
            (x, y, x + width, y),  # Bottom
            (x + width, y, x + width, y + height),  # Right
            (x + width, y + height, x, y + height),  # Top
            (x, y + height, x, y)  # Left
        ]

        glBegin(GL_POINTS)
        for x0, y0, x1, y1 in lines:
            points = midpoint_line(int(x0), int(y0), int(x1), int(y1))
            for px, py in points:
                glVertex2f(px, py)
        glEnd()

        current_x = x + (width - len(text) * 25) / 2  # Center text horizontally
        text_y = y + height / 2 - 10   
        glPointSize(3)              
        glBegin(GL_POINTS)
        for char in text:
            char_points = self.create_character_points(char, current_x, text_y, scale=6)
            for px, py in char_points:
                glVertex2f(px, py)
            current_x += 30  # Space between characters
        glEnd()

    def draw_menu(self):
        """Modified menu drawing with title"""
        # Clear screen to black
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Draw title at the top of the menu
        title_x = self.width / 2 - (len(self.game_title) * 25)
        title_y = self.height - 100
        
        glPointSize(4)
        glColor3f(0.8, 0.8, 0.8)
        
        time_offset = time.time() * 2  # For continuous animation
        
        # Draw title with slight wave effect
        glBegin(GL_POINTS)
        for i, char in enumerate(self.game_title):
            offset_y = math.sin(time_offset + i * 0.5) * 2  # Wavy effect
            points = self.create_character_points(char, title_x + i * 50, title_y + offset_y, scale=10)
            for px, py in points:
                glVertex2f(px, py)
        glEnd()
        
        # Draw subtitle
        subtitle_x = self.width / 2 - (len(self.subtitle) * 15)
        subtitle_y = title_y - 50
        glPointSize(3)
        glColor3f(0.6, 0.6, 0.6)
        
        glBegin(GL_POINTS)
        for i, char in enumerate(self.subtitle):
            offset_y = math.sin(time_offset + i * 0.5) * 1  # Smaller wave effect
            points = self.create_character_points(char, subtitle_x + i * 30, subtitle_y + offset_y, scale=6)
            for px, py in points:
                glVertex2f(px, py)
        glEnd()

        # Draw menu buttons
        start_y = self.height / 2 + len(self.menu_buttons) * (self.button_height + self.button_spacing) / 2
        
        for i, text in enumerate(self.menu_buttons):
            if i == 0 and self.came_from_escape and self.game_in_progress:
                display_text = "Resume"
            else:
                display_text = text

            button_x = (self.width - self.button_width) / 2
            button_y = start_y - i * (self.button_height + self.button_spacing)
            self.draw_button(
                button_x,
                button_y,
                self.button_width,
                self.button_height,
                display_text,
                i == self.selected_button
            )

    def handle_menu_key(self, key):
        """Handle menu key presses"""
        if key == b'\r':  # Enter key
            if self.selected_button == 0:  # Play/Resume
                self.show_menu = False
                
                if self.came_from_escape:
                    # Resume from where we left off
                    self.is_paused = self.previous_game_state
                    self.came_from_escape = False
                else:
                    # Start new game
                    self.game_started = True
                    self.game_in_progress = True
                    # Show first fragment text
                    self.is_paused = True
                    self.show_text = True
                    self.current_text_phase = 1
                    self.current_fragment = self.fragments[0]
                    self.text_start_time = time.time()
                    
            elif self.selected_button == 1:  # Restart
                self.reset_game()
                self.show_menu = False
                self.game_started = True
                self.game_in_progress = True
                self.came_from_escape = False
                # Show first fragment text
                self.is_paused = True
                self.show_text = True
                self.current_text_phase = 1
                self.current_fragment = self.fragments[0]
                self.text_start_time = time.time()
                
            elif self.selected_button == 2:  # Exit
                self.show_menu = False
                self.show_goodbye = True
                glutTimerFunc(2000, lambda _: glutLeaveMainLoop(), 0)

        elif key in (b'w', b'W'):  # W or w
            self.selected_button = (self.selected_button - 1) % len(self.menu_buttons)
        elif key in (b's', b'S'):  # S or s
            self.selected_button = (self.selected_button + 1) % len(self.menu_buttons)


def init_gl(width, height):
    glClearColor(0.15, 0.15, 0.15, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if simulator.show_title_sequence:
        simulator.draw_title_sequence()
    elif not simulator.show_menu and not simulator.is_paused:
        if key_states[b'a']:
            simulator.move_robot_and_camera(-1)
        if key_states[b'd']:
            simulator.move_robot_and_camera(1)
        simulator.update_scene()
    simulator.draw()
    glutSwapBuffers()
    glutPostRedisplay()

def animate_walking_right(value):
    global simulator
    simulator.mirror_arms = False
    if simulator.animation_step < 3:
        simulator.step_state = (simulator.step_state + 1) % 3
        simulator.robot_x += simulator.robot_speed
        simulator.world_offset += simulator.robot_speed
        simulator.animation_step += 1
        glutPostRedisplay()
        glutTimerFunc(200, animate_walking_right, 0)
    else:
        simulator.animation_step = 0

def animate_walking_left(value):
    global simulator
    simulator.mirror_arms = True
    if simulator.animation_step < 3:
        simulator.step_state = (simulator.step_state + 1) % 3
        simulator.robot_x -= simulator.robot_speed
        simulator.world_offset -= simulator.robot_speed
        simulator.animation_step += 1
        glutPostRedisplay()
        glutTimerFunc(200, animate_walking_left, 0)
    else:
        simulator.animation_step = 0

def keyboard(key, x, y):
    if key == b'\x1b':  # Escape key
        if not simulator.show_menu:
            # Store current game state and mark that we came from escape
            simulator.previous_game_state = simulator.is_paused
            simulator.show_menu = True
            simulator.is_paused = True
            simulator.came_from_escape = True
        else:
            # Return to game with previous pause state
            simulator.show_menu = False
            simulator.is_paused = simulator.previous_game_state
            simulator.came_from_escape = False
    elif simulator.show_menu:
        simulator.handle_menu_key(key)
    elif not simulator.is_paused:  # Only process game input if not paused
        if key in key_states:
            key_states[key] = True
        if key in (b'd', b'D') and simulator.animation_step == 0:
            animate_walking_right(0)
        elif key in (b'a', b'A') and simulator.animation_step == 0:
            animate_walking_left(0)

def keyboard_up(key, x, y):
    global simulator
    if key in key_states:
        key_states[key] = False
        simulator.camera_speed = 0  # Stop the camera if no keys are pressed

def main():
    global simulator
    simulator = Whispers(1400, 600)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(1400, 600)
    glutCreateWindow(b"whispers beneath the Darkness")
    init_gl(1400, 600)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMainLoop()

if __name__ == '__main__':
    main()
