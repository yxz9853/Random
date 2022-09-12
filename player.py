import pygame
from support import import_folder
import support

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.15
        self.image=self.animations['idle'][self.frame_index]
        self.rect=self.image.get_rect(topleft=pos)

        #player movement
        self.direction=pygame.math.Vector2(0,0)
        self.speed=5
        self.gravity=0.5
        self.jump_speed=-12
        
        self.status='idle'
        self.facing_right=True
        self.on_ground=False
        self.on_ceiling=False
        self.on_left=False
        self.on_right=False

    def import_character_assets(self):
        character_path='./graphics/character/'
        self.animations={'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path=character_path+animation
            self.animations[animation]=import_folder(full_path)

    def animate(self):
        animation=self.animations[self.status]

        #loop over frame index
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(animation):
            self.frame_index=0

        image=animation[int(self.frame_index)]
        if self.facing_right:
            self.image=image
        else:
            flipped_image=pygame.transform.flip(image,True,False)
            self.image=flipped_image

        #set rectangle according to the collision
        if self.on_ground and self.on_right:
            self.rect=self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect=self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect=self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect=self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect=self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect=self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        keys=pygame.key.get_pressed()
        #checks the input for right and left
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and (not keys[pygame.K_LEFT] or not keys[pygame.K_a]):
            self.direction.x=1
            self.facing_right=True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] and (not keys[pygame.K_RIGHT] or not keys[pygame.K_d]):
            self.direction.x=-1
            self.facing_right=False
        else:
            self.direction.x=0
        #checks the input of jump
        if keys[pygame.K_UP] and self.on_ground or keys[pygame.K_w] and self.on_ground:
            self.jump()
        #checks restart
        if keys[pygame.K_r]:
            support.restart=True

    def get_status(self):
        #gets current status of player to animate
        if self.direction.y<0:
            self.status='jump'
        elif self.direction.y>0.6:
            self.status='fall'
        else:
            if self.direction.x!=0 and self.on_ground:
                self.status='run'
            elif self.on_ground:
                self.status='idle'

    def apply_gravity(self):
        #applys gravity to player
        self.direction.y+=self.gravity
        self.rect.y+=self.direction.y

    def jump(self):
        self.direction.y=self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
