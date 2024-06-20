class Settings:
    def __init__(self):
        """Initialize the game's constant settings"""
        #Screen Settings
        self.screen_width = 600
        self.screen_height = 700
        self.bg_color = (20,20,30)

        #Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_colour = (255,117,24)
        self.bullets_allowed = 10


        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point vslues increase
        self.score_scale = 1.5

        # Scoring
        self.alien_points = 20

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        self.ship_speed = 0.5
        self.bullet_speed = 2.0
        self.alien_speed = 0.3

        # Fleet direction 1 represents right, -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale 
        self.bullet_speed *= self.speedup_scale 
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)   