import pygame
import time
import sys
import os

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Play_Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from pyvidplayer import Video

class Alieninvasion:

    def __init__(self):
        #Initializing pygame
        pygame.init()

        self.path = os.getcwd()
        self.game_on = True
        self.game_paused = True

        self.settings=Settings()
        
        #Create the game screen
        # self.screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics
        #  and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Sound effects
        self.bullet_sfx = pygame.mixer.Sound(self.path+"/sounds/laser3.mp3")
        self.collision_sfx = pygame.mixer.Sound(self.path+"/sounds/blast6.mp3") # Bullet AlienSahip Alien collision
        self.game_over_sfx = pygame.mixer.Sound(self.path+"/sounds/gameOver.mp3")

        # Make the instances of active buttons
        self.play_button = Play_Button(self,"Click here to Play",200,40,(0,0,0),(255,255,255),15,100)
        self.how_to_play_button = Play_Button(self,"How to Play",200,40,(0,0,0),(255,255,255),20,150)
        self.replay_button = Play_Button(self,"Restart",280,40,(100,100,100),(255,255,255),20,350)
        self.quit_button = Play_Button(self,"Quit",280,40,(100,100,100),(255,255,255),20,300)
        self.resume_button = Play_Button(self,"Resume",280,40,(100,100,100),(255,255,255),20,400)

        # Play the intro video
        self._play_video()
        
    def _play_video(self):
        """Plays the intro video for a limited time"""
        vid = Video("Intro/space.mp4")
        vid.set_size((600,700))
        # Notes starting time
        start = time.time()
        key = 0
        while True:
            vid.draw(self.screen,(0,0))
            pygame.display.update()
            # Ends the video if mouseclick detected
            for event in pygame.event.get():
                if event.type ==  pygame.MOUSEBUTTONDOWN:
                    key = 1
                if event.type == pygame.QUIT:
                    exit()
                   
            #Notes anding time
            end = time.time()
            #Ends the video if 4 sec have passed
            if (end - start) > 4 or key == 1:
                vid.close()
                break

    def run_game(self): 
        #Looping to keep the game screen open
        while True:
            #Watch for keyboard and mouse events
            self._check_events()

            # Draws the intro page
            if not self.stats.game_active and self.game_on and  self.game_paused:
                self._draw_intro_page()

            # Draws the game over screen
            if self.stats.ships_left == 0 and not self.game_on:
                self._draw_game_over_buttons()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()

    def _draw_intro_page(self):
        #draws the intro image
        img = pygame.image.load("Images/space.png")
        rect = img.get_rect()
        rect.midbottom = self.screen.get_rect().midbottom
        self.screen.blit(img,rect)
        
        #Draw the play button if the game is inactive
        self.how_to_play_button.draw_button()
        self.play_button.draw_button()
        pygame.display.update()

    def _draw_game_over_buttons(self):
        # Creates the instance for inactive buttons in game over screen
        self.game_over_button = Play_Button(self,"GAME OVER",300,250,(0,0,0),(255,255,255),40,500,40)

        score = self.stats.score
        score_str = "{:,}".format(score)
        self.score_button = Play_Button(self,"Score: "+score_str ,280,40,(0,0,0),(255,255,255),20,410)
        
        # Draws the buttons
        self.game_over_button.draw_button()
        self.score_button.draw_button()
        self.replay_button.draw_button()
        self.quit_button.draw_button()
        pygame.display.update()

    def _draw_pause_buttons(self):
        # Creates the instance for inactive buttons in game over screen
        self.button = Play_Button(self,"",300, 210,(0,0,0),(255,255,255),40,460)

        score = self.stats.score
        score_str = "{:,}".format(score)
        self.score_button = Play_Button(self,"Score: "+score_str ,280,40,(0,0,0),(255,255,255),20,450)
        
        # Draws the buttons
        self.button.draw_button()
        self.score_button.draw_button()
        self.resume_button.draw_button()
        self.replay_button.draw_button()
        self.quit_button.draw_button()
        pygame.display.update()

    def _check_events(self):
        """Respond to keypress and mouse movements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type ==  pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_how_to_play_button(mouse_pos)
                self._check_play_button(mouse_pos)
                self._check_replay_button(mouse_pos)
                self._check_resume_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_how_to_play_button(self,mouse_pos):
        """ Shows how to play the game when the player clicks how to play"""
        button_clicked = self.how_to_play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game_on:
            img = pygame.image.load("Images/rules.png")
            rect = img.get_rect()
            rect.midbottom = self.screen.get_rect().midbottom
            self.screen.blit(img,rect)
            self.play_button.draw_button()
            pygame.display.update()
            
            self.game_paused = False

    def _check_play_button(self,mouse_pos):
        """ Starts the new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game_on:
            #Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of the remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fllet and center the ship
            self._create_fleet()
            self.ship.center_ship()   

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_replay_button(self,mouse_pos):
        """ Starts the game again when the player clicks play again"""
        button_clicked = self.replay_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_on:
            #Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of the remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fllet and center the ship
            self._create_fleet()
            self.ship.center_ship()   

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_resume_button(self,mouse_pos):
        """ Resumes the game when the player clicks play again"""
        button_clicked = self.resume_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_on:

            #Resumes the game
            self.stats.game_active = True
            self.game_on = True
            
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_quit_button(self,mouse_pos):
        """Closes the game when player clicks quit button"""
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            sys.exit()

    def _check_keydown_events(self,event):
        #Respond to keypress
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True

        if event.key == pygame.K_SPACE and self.stats.game_active:
            self.fire_bullet()

        if event.key == pygame.K_ESCAPE and self.stats.game_active:
            # Pauses the game
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.game_on = False
            self._draw_pause_buttons()    

    def _check_keyup_events(self,event):
        #Respond to key release
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            # plays the laser sound
            self.bullet_sfx.play()

            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Updates position of the bullets and get rid of the old bullets"""
        self.bullets.update()
        # Get rid of thee bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to bullet alien collisions """
        # Removes the bullet and the aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if collisions:
            for aliens in collisions.values():
                # plays the blast sound
                self.collision_sfx.play()
    
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score( )

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Creste fleet of aliens"""
        # Make an alien
        alien = Alien(self)
        
        alien_width, alien_height = alien.rect.size

        # Determine the no of aliens that fit in a row
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        # Determine the no of aliens that fit in a row
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3*alien_height) - ship_height
        number_rows = available_space_y // (2*alien_width)

        # Creste the first row of aliens
        for row_number in range(1,number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
            # Create an alien and place it in the row
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size

            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
             
            alien.y = 2 * alien_height * row_number
            alien.rect.y = alien.y
            
            self.aliens.add(alien)

    def _check_fleet_eddges(self):
        """respond appropriately if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Check if the fleet is at an edge,
            Update the positions of the aliens in the fleet"""
        self._check_fleet_eddges()
        self.aliens.update()

        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Delete the aliens that have reached the bottom and reduce points
                self.aliens.remove(alien)
                self.stats.score -= self.settings.alien_points
                self.sb.prep_score()
                break
        # If no aliens are left start the next level
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        # Decrement no of ships left
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            # Plays collision music
            self.collision_sfx.play()

            # update scoreboard
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fllet of aliens and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            time.sleep(1)

        else:
            # Deletes the last life sign
            self.sb.prep_ships()

            self.game_on = False
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

            # plays game over music
            self.game_over_sfx.play()

            # Pause
            time.sleep(2)

    def _update_screen(self):
        """Update images on the screen and flip the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        #Updates the screen
        pygame.display.update()
    

if __name__=="__main__":                   

    a=Alieninvasion()
    a.run_game()