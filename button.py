import pygame.font

class Play_Button:
    def __init__(self,ai_game,msg,width,height,button_color,text_color,font_size,pos,val = 0):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimentions and properties of the button
        self.width,self.height = width,height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont('showcard gothic',font_size)
        self.val = val

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.screen_rect.bottom - pos

        # The button needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """Turn msg into arendered image and center text on the button"""
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        # Adjusts the text position in the button
        if not self.val == 0: 
            self.msg_image_rect.y = self.rect.y + self.val

    def draw_button(self):
        # draw blank button and then draw message
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)