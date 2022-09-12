import pygame
from tiles import Tile
from settings import *
from player import Player
import support


class Level:
    def __init__(self,level_data,surface):
        #level setup
        self.display_surface=surface
        self.setup_level(level_data)
        self.world_shift=0
        self.current_x=0
        self.maximum=0
        self.current=0

    def setup_level(self,layout):
        self.tiles=pygame.sprite.Group()
        self.player=pygame.sprite.GroupSingle()
        #set tiles and player
        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x=col_index*tile_size
                y=row_index*tile_size

                if col == 'X':
                    tile=Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if col == 'P':
                    player_sprite=Player((x,y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player=self.player.sprite
        player_x=player.rect.centerx
        direction_x=player.direction.x
        if player_x<screen_width/3.3 and direction_x<0:
            self.world_shift=5
            player.speed=0
            support.bgx+=0.5
        elif player_x>screen_width-(screen_width/3.3) and direction_x>0:
            self.world_shift=-5
            player.speed=0
            support.bgx+=-0.5
        else:
            self.world_shift=0
            player.speed=5

    def horizontal_movement_collision(self):
        player=self.player.sprite
        #horizontal movement
        player.rect.x+=player.direction.x*player.speed
        #check for rectangle collision
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                #check left or right
                if player.direction.x<0:
                    player.rect.left=sprite.rect.right
                    player.on_left=True
                    self.current_x=player.rect.left
                elif player.direction.x>0:
                    player.rect.right=sprite.rect.left
                    player.on_right=True
                    self.current_x=player.rect.right

        if player.on_left and (player.rect.left<self.current_x or player.direction.x>=0):
            player.on_left=False
        if player.on_right and (player.rect.right>self.current_x or player.direction.x<=0):
            player.on_right=False

    def vertical_movement_collision(self):
        player=self.player.sprite
        #gravity/vertical movement
        player.apply_gravity()
        #check for rectangle collision
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                #check up or down
                if player.direction.y>0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y=0
                    player.on_ground=True
                elif player.direction.y<0:
                    player.rect.top=sprite.rect.bottom
                    player.direction.y=0
                    player.on_ceiling=True

        if player.on_ground and player.direction.y<0 or player.direction.y>1:
            player.on_ground=False
        if player.on_ceiling and player.direction.y>0:
            player.on_ceiling=False
        if player.on_ceiling:
            player.on_ground=False

    def edge_detection(self):
        player=self.player.sprite
        player_y=player.rect.centery
        if player_y>1000:
            support.lost=1
        if support.bgx<=-705.5:
            support.lost=-1

    def run(self):
        #level
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.edge_detection()
