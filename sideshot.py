import arcade
import pathlib
from enum import auto, Enum
BULLET_SPEED = 5
SPRITE_SCALING_LASER = 0.8


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MinimalSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed:int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window
        self.bullet_list = None

    def slide(self,direction:MoveEnum):
        self.speed = 0
        self.center_x -= 5
        if(self.right == 0):
            self.left = 1000


    def slide2(self,direction:MoveEnum):
        self.speed = 0
        self.center_x -= 5
        if(self.right == 0):
            self.left = 1000







    def move(self, direction:MoveEnum):
        #as a class exercise, lets fix this so it doesn't go off the window
        if direction == MoveEnum.UP and not self.center_y+self.height/2 > self.game.height:
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN and not self.center_y-self.height/2 < 0:
            self.center_y -= self.speed
        elif direction == MoveEnum.LEFT and not self.center_x-self.width/2 < 0:
            self.center_x -=self.speed
        elif direction == MoveEnum.RIGHT and not self.center_x+self.width/2 > self.game.width:
            self.center_x += self.speed
        else: #should be MoveEnum.NONE
            pass


class playspace(arcade.Window):

    def __init__(self, screen_w:int = 1000, screen_h:int =500):
        super().__init__(screen_w, screen_h)
        self.image_path = pathlib.Path.cwd() / 'Assets' / 'PlayerShip.png'
        self.back2 = pathlib.Path.cwd() / 'Assets' / 'temp back2.png'
        self.back = pathlib.Path.cwd() / 'Assets' / 'temp back.png'
        #self.back2 = pathlib.Path.cwd() / 'Assets' / 'temp back2.png'
        self.pict = None
        self.backg = None
        self.backg2 = None
        self.direction = MoveEnum.NONE
        self.pictlist = None
        self.backgrounds = None
        self.bullet_list = None
        self.set_mouse_visible(False)
        self.backgrounds2 = None
        self.bullet_list = arcade.SpriteList()
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")


    def setup(self):
        self.pict = MinimalSprite(str(self.image_path), speed=3, game_window=self)
        self.pict.center_x = 300
        self.pict.center_y = 300
        self.backg = MinimalSprite(str(self.back), speed=3, game_window=self)
        self.backg.center_x = 1000
        self.backg.center_y = 250
        self.backg2 = MinimalSprite(str(self.back), speed=3, game_window=self)
        self.backg2.center_x = 0
        self.backg2.center_y = 250
        self.pictlist = arcade.SpriteList()
        self.backgrounds = arcade.SpriteList()
        self.backgrounds2 = arcade.SpriteList()
        self.backgrounds.append(self.backg)
        self.backgrounds.append(self.backg2)
        self.pictlist.append(self.pict)


    def on_update(self, delta_time: float):
        #to get really smooth movement we would use the delta time to
        #adjust the movement, but for this simple version I'll forgo that.
        self.pict.move(self.direction)
        #self.backg.slide(self.direction)
        self.backg.slide(self.direction)
        self.backg2.slide2(self.direction)
        self.bullet_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:



            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.height:
                bullet.remove_from_sprite_lists()





    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        self.backg2.draw()
        self.backg.draw()
        self.pictlist.draw()
        self.bullet_list.draw()



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.direction = MoveEnum.LEFT
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.direction = MoveEnum.RIGHT
        if (key == arcade.key.SPACE):
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)
            # The image points to the right, and we want it to point up. So
            # rotate it.
            bullet.angle = 0

            # Give the bullet a speed
            bullet.change_x = BULLET_SPEED

            # Position the bullet
            bullet.center_y = self.pict.center_y + 30
            bullet.center_x = self.pict.center_x+60
            #bullet.center_y = self.pict.center_y
            bullet.bottom = self.pict.top

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)
            arcade.play_sound(self.gun_sound)



    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
                self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and\
                self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.LEFT or key == arcade.key.A) and \
                self.direction == MoveEnum.LEFT:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.RIGHT or key == arcade.key.D) and \
                self.direction == MoveEnum.RIGHT:
            self.direction = MoveEnum.NONE

def main():
    """ Main method """
    window = playspace()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
