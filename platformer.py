import pygame

# Global Consts

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)


SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):

    # -- Attribute
    # Set speed vector
    change_x = 0
    change_y = 0

    # list of sprites we can bumb against
    level = None

    # -- Methods
    def __init__(self):

        # call parents constructor
        super().__init__()

        # Create image of the block
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()


    def update(self):

        # Gravity
        self.calc_grav()

        # movement
        self.rect.x += self.change_x

        # Check for collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If moving right, set right side to left side of object we are colliding with
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # do the opposite if we are moving left
                self.rect.left = block.rect.right


        # move up or down
        self.rect.y += self.change_y

        # check for collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # reset position based on top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # stop vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Caclulate effect of grav"""
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # check if we are on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when jump is pressed """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player controlled movement

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    """ Platforms to jump on """

    def __init__(self, width, height):
        """Platform constructor"""

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level():
    """Generic super-class to define a level. Creates a child class with level-specific info"""

    #List o f sprites used in each level
    platform_list = None
    enemy_list = None


    #how far the world has been scrolled left/right
    world_shift = 0

    def __init__(self, player):

        """Constructor. NEeded for when moving platforms collide w the player"""
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player


        #Update everything on the level

    def update(self):
        """update everything in the level"""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """Draw everything on the level"""

        screen.fill(BLUE)

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self,shift_x):
        """scroll left and right when the player moves"""

        #keep track of shift amount
        self.world_shift += shift_x

        #go through sprite list and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

#Create platforms
class Level_01(Level):
    """Def for level 1"""
    def __init__(self, player):

        #Call parent constructor
        Level.__init__(self,player)

        self.level_limit = -1000

        #array with width, height, x and y of platforms
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 800, 400],
                 [210, 70, 800, 400],
                 ]


        #Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

#Create platforms for level 2
class Level_02(Level):
    """Def for level 2"""

    def __init__(self, player):

        Level.__init__(self,player)
        
        self.level_limit = -1000

        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]


        # Go through array above
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def main():
    """Main Program"""
    pygame.init()


    #set height and width of screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)    

    pygame.display.set_caption("Side-Scrolling platformer")

    #Create player
    player = Player()

    #create all levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    #set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    #loop unitl user clicks the close button
    done = False

    #Used to manage how fast the screen update
    clock = pygame.time.Clock()

    #------Main Program Loop--------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        
        #Update the player
        active_sprite_list.update()

        #Update items
        current_level.update()

        #If player nears the right side, shift the world left
        if player.rect.right >= 500:
            diff = player.rect.right -500
            player.rect.right = 500
            current_level.shift_world(-diff)

        #If player nears left side, shift right
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        #If player reaches the end of the level, go to the next
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x =120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        #limit to 60fps
        clock.tick(60)

        #update screen w what we've drawn
        pygame.display.flip()

        
    pygame.quit()


if __name__ == "__main__":
    main()

