import pygame
pygame.init()
import random 
pygame.mixer.init() 
import sys 





#set up the screen 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")
screen_2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
screen_shake = 0 

#set frame rate 
clock = pygame.time.Clock()
FPS = 60 

#set game variables 
GREEN = (136, 231, 136)
WHITE = (255, 255, 255) 
RED = (255, 127, 127)
BLUE = (135, 206, 235)
ORANGE = (255, 153, 28)
MAIN_FONT = pygame.font.SysFont("comicsans", 30)
SMALL_FONT = pygame.font.SysFont("comicsans", 15)




#load images 
items_imgs = {} 
ball_expand = pygame.image.load("ball_expand.png")
items_imgs["ball_expand"] = pygame.transform.scale(ball_expand, (32, 32)) 
ball_shrink = pygame.image.load("ball_shrink.png")
items_imgs["ball_shrink"] = pygame.transform.scale(ball_shrink, (32, 32)) 
paddle_expand = pygame.image.load("paddle_expand.png")
items_imgs["paddle_expand"] = pygame.transform.scale(paddle_expand, (32, 32)) 
paddle_shrink = pygame.image.load("paddle_shrink.png")
items_imgs["paddle_shrink"] = pygame.transform.scale(paddle_shrink, (32, 32)) 
fake_ball = pygame.image.load("fake_ball.png")
items_imgs["fake_ball"] = pygame.transform.scale(fake_ball, (32, 32)) 
background = pygame.image.load("background_img.png")
background_img = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 


#load sound 
paddle_1_sound = pygame.mixer.Sound("paddle_1.wav")
paddle_2_sound = pygame.mixer.Sound("paddle_2.wav")
hit_wall_1_sound = pygame.mixer.Sound("hit_wall_1.wav")
hit_wall_2_sound = pygame.mixer.Sound("hit_wall_2.wav")
paddle_expand_sound = pygame.mixer.Sound("paddle_expand.wav")
paddle_shrink_sound = pygame.mixer.Sound("paddle_shrink.wav")
ball_expand_sound = pygame.mixer.Sound("ball_expand.wav")
ball_shrink_sound = pygame.mixer.Sound("ball_shrink.wav")
fake_ball_sound = pygame.mixer.Sound("fake_ball.wav")

pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.3) 
pygame.mixer.music.play(-1) 




class Table:
    def __init__(self): 
        self.level = 1

    def draw(self):
        #screen.fill(GREEN)
        screen.blit(background_img, (0, 0))
        for i in range (10, SCREEN_HEIGHT, SCREEN_HEIGHT//20): 
            if i % 2 == 0: 
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 5, i, 10, SCREEN_HEIGHT//20))
        level_text = MAIN_FONT.render(f"Level: {self.level}", 1, WHITE)
        screen_2.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 10))
        control_l_text = SMALL_FONT.render("Move up:[w]  Move down:[s]", 1, WHITE)
        screen.blit(control_l_text, (20, SCREEN_HEIGHT - 30))
        control_r_text = SMALL_FONT.render("Move up:[UP]  Move down:[DOWN]", 1, WHITE)
        screen.blit(control_r_text, (SCREEN_WIDTH - 20 - control_r_text.get_width(), SCREEN_HEIGHT - 30))


class Paddle: 
    def __init__ (self, x, y, color, player_id):
        self.rect = pygame.Rect(0, 0, 20, 100)
        self.rect.centerx = x
        self.rect.centery = y 
        self.color = color 
        self.vel = 10
        self.move_up = False 
        self.move_down = False 
        self.player_id = player_id 
        self.score = 0 
        self.paddle_expand_time = 0 
        self.paddle_shrink_time = 0 
    
    def draw(self):
        pygame.draw.rect(screen_2, self.color, self.rect)
        if self.player_id == 1: 
            left_score_text = MAIN_FONT.render(f"Score: {self.score}", 1, self.color)
            screen_2.blit(left_score_text, (20, 10))
        if self.player_id == 2: 
            right_score_text = MAIN_FONT.render(f"Score: {self.score}", 1, self.color)
            screen_2.blit(right_score_text, (SCREEN_WIDTH - 20 - right_score_text.get_width(), 10))

    def move(self): 
        if self.move_up == True and self.rect.top >= 0: 
            self.rect.centery -= self.vel 
        if self.move_down == True and self.rect.bottom <= SCREEN_HEIGHT: 
            self.rect.centery += self.vel 

    def paddle_expand(self): 
        self.paddle_expand_time = pygame.time.get_ticks()
        self.paddle_shrink_time = 0 
        x, y = self.rect.x, self.rect.y 
        self.rect = pygame.Rect(x, y, 20, 200)
        paddle_expand_sound.play()

    def paddle_shrink(self): 
        self.paddle_shrink_time = pygame.time.get_ticks()
        self.paddle_expand_time = 0 
        x, y = self.rect.x, self.rect.y 
        self.rect = pygame.Rect(x, y, 20, 50)
        paddle_shrink_sound.play()

    def update(self): 
        now = pygame.time.get_ticks() 

        if self.paddle_expand_time != 0 and now - self.paddle_expand_time > 5000: 
            x, y = self.rect.x, self.rect.y 
            self.rect = pygame.Rect(x, y, 20, 100)
            self.paddle_expand_time = 0 
            paddle_shrink_sound.play()

        if self.paddle_shrink_time != 0 and now - self.paddle_shrink_time > 5000: 
            x, y = self.rect.x, self.rect.y 
            self.rect = pygame.Rect(x, y, 20, 100)
            self.paddle_shrink_time = 0  
            paddle_expand_sound.play() 


class Ball: 
    def __init__(self, x, y): 
        self.x = x
        self.y = y 
        self.x_vel = 5
        self.y_vel = 0 
        self.radius = 10
        self.color = ORANGE 
        self.max_vel = 3 
        self.hit_count = 0
        self.ball_expand_time = 0 
        self.ball_shrink_time = 0 

    def draw(self): 
        pygame.draw.circle(screen_2, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel 
        self.y += self.y_vel 

    def handle_collision(self): 
        if self.y - self.radius <= 0: 
            self.y_vel *= -1 
            hit_wall_1_sound.play()
        elif self.y + self.radius >= SCREEN_HEIGHT:
            self.y_vel *= -1
            hit_wall_2_sound.play()

        if self.x_vel <= 0:
            if self.y >= left_player.rect.top and self.y <= left_player.rect.bottom:
                if self.x - self.radius <= left_player.rect.right: 
                    self.x_vel *= -1 
                    difference_in_y = left_player.rect.centery - self.y
                    y_vel = difference_in_y / (left_player.rect.height/2) * self.max_vel
                    self.y_vel = -1 * y_vel
                    self.hit_count += 1 
                    paddle_1_sound.play()
                    
        else:
            if self.y >= right_player.rect.top and self.y <= right_player.rect.bottom:
                if self.x + self.radius >= right_player.rect.left: 
                    self.x_vel *= -1 
                    difference_in_y = right_player.rect.centery - self.y
                    y_vel = difference_in_y / (right_player.rect.height/2) * self.max_vel
                    self.y_vel = -1 * y_vel
                    self.hit_count += 1
                    paddle_2_sound.play()
                              
        if self.hit_count >= 5: 
            if self.x_vel <0: 
                self.x_vel -= 2
                self.hit_count = 0 
                gametable.level += 1 
            elif self.x_vel >0: 
                self.x_vel += 2
                self.hit_count = 0
                gametable.level += 1  

    def check_ball_reset(self):  
        if self.x < 0: 
            right_player.score += 1
            self.x = SCREEN_WIDTH / 2
            self.y = SCREEN_HEIGHT / 2
            self.hit = 0 
            if self.x_vel < 0: 
                self.x_vel = 5
            else: 
                self.x_vel = -5
            gametable.level = 1 
            
        if self.x > SCREEN_WIDTH: 
            left_player.score += 1
            self.x = SCREEN_WIDTH / 2
            self.y = SCREEN_HEIGHT / 2
            self.hit = 0 
            if self.x_vel < 0: 
                self.x_vel = 5
            else: 
                self.x_vel = -5
            gametable.level = 1

    def ball_expand(self): 
        self.ball_expand_time = pygame.time.get_ticks()
        self.ball_shrink_time = 0 
        self.radius = 20
        ball_expand_sound.play()
        

    def ball_shrink(self): 
        self.ball_shrink_time = pygame.time.get_ticks() 
        self.ball_expand_time = 0 
        self.radius = 5
        ball_shrink_sound.play() 
        

    def update(self): 
        now = pygame.time.get_ticks()

        if self.ball_expand_time != 0 and now - self.ball_expand_time > 5000: 
            self.radius = 10 
            self.ball_expand_time = 0
            ball_shrink_sound.play()  
            

        if self.ball_shrink_time != 0 and now - self.ball_shrink_time > 5000: 
            self.radius = 10 
            self.ball_shrink_time = 0
            ball_expand_sound.play()
                   


class Item(): 
    def __init__(self): 
        self.type = random.choice(["ball_expand", "ball_shrink", "paddle_expand", "paddle_shrink", "fake_ball"])
        self.image = items_imgs[self.type] 
        self.rect = self.image.get_rect() 
        self.rect.center = (SCREEN_WIDTH //2 , random.randrange(20, SCREEN_HEIGHT-20))
        self.x_vel = random.choice([-1, 1])
        self.y_vel = 0 

    def move(self):
        self.rect.centerx += self.x_vel 
        self.rect.centery += self.y_vel 

    def draw(self): 
        screen_2.blit(self.image, self.rect) 


    def check_collision(self): 

        if self.x_vel <= 0:
            if self.rect.bottom >= left_player.rect.top and self.rect.top <= left_player.rect.bottom:
                if self.rect.left <= left_player.rect.right: 
                    if self.type == "paddle_expand":
                        left_player.paddle_expand()
                    elif self.type == "paddle_shrink":
                        left_player.paddle_shrink()
                    elif self.type == "ball_expand":
                        gameball.ball_expand()
                    elif self.type == "ball_shrink":
                        gameball.ball_shrink()            
                    elif self.type == "fake_ball":
                        shoot_fake_ball()
                    all_items.remove(self)

            elif self.rect.right < left_player.rect.left: 
                all_items.remove(self)



        elif self.x_vel > 0: 
            if self.rect.bottom >= right_player.rect.top and self.rect.top <= right_player.rect.bottom:
                if self.rect.right >= right_player.rect.left: 
                    if self.type == "paddle_expand":
                        right_player.paddle_expand()
                    elif self.type == "paddle_shrink":
                        right_player.paddle_shrink()
                    elif self.type == "ball_expand":
                        gameball.ball_expand()
                    elif self.type == "ball_shrink":
                        gameball.ball_shrink()
                    elif self.type == "fake_ball":
                        shoot_fake_ball()
                    all_items.remove(self)
  
            elif self.rect.left > right_player.rect.right: 
                all_items.remove(self) 


    

class Fakeball: 
    def __init__(self): 
        self.x = SCREEN_WIDTH //2 
        self.y = SCREEN_HEIGHT //2 
        self.x_vel = random.choice([-3, -2, -1, 1, 2, 3])
        self.y_vel = random.randrange(-2, 2)
        self.radius = 10
        self.color = WHITE

    def draw(self): 
        pygame.draw.circle(screen_2, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel 
        self.y += self.y_vel    

    def handle_collision(self): 
        if self.y - self.radius <= 0: 
            self.y_vel *= -1 
            hit_wall_1_sound.play() 

        elif self.y + self.radius >= SCREEN_HEIGHT:
            self.y_vel *= -1
            hit_wall_2_sound.play()

    def update(self): 
        if self.x < 0 or self.x > SCREEN_WIDTH : 
            all_fake_balls.remove(self)
            


def shoot_fake_ball(): 
    fake_ball_sound.play()
    for i in range (10): 
        fake_ball = Fakeball()
        all_fake_balls.append(fake_ball)


def draw_start_menu():
    screen.fill(GREEN)
    startup_text_1 = MAIN_FONT.render("Ping Pong", 1, WHITE)
    startup_text_2 = MAIN_FONT.render("Press SPACE to start...", 1, WHITE)
    screen.blit(startup_text_1, (SCREEN_WIDTH//2 - startup_text_1.get_width()//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(startup_text_2, (SCREEN_WIDTH//2 - startup_text_2.get_width()//2, SCREEN_HEIGHT//2 + 50)) 
    pygame.display.update() 
    waiting = True 
    while waiting: 
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_SPACE: 
                    waiting = False 

def check_endgame():
    if left_player.score >= 10: 
        winner_text = MAIN_FONT.render("Left Player Win!!", 1, WHITE)
        screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, SCREEN_HEIGHT//2 - winner_text.get_height()//2))       
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()
    elif right_player.score >= 10: 
        winner_text = MAIN_FONT.render("Right Player Win!!", 1, WHITE)
        screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, SCREEN_HEIGHT//2 - winner_text.get_height()//2))       
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()


#game loop 
show_start_menu = True 
run = True 
gametable = Table()
left_player = Paddle(20, SCREEN_HEIGHT//2, RED, 1)
right_player = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT//2, BLUE, 2)
gameball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
all_items = [] 
all_fake_balls = [] 



#while loop 
while run: 

    if show_start_menu:
        draw_start_menu()
        show_start_menu = False 

    #about the screen 
    screen_2.fill((0, 0, 0, 0))
    screen_shake = max (0, screen_shake-1)

    
    clock.tick(FPS) 

    # move and update 
    left_player.move()
    right_player.move()
    left_player.update()
    right_player.update()
    gameball.move()
    gameball.update() 
    if len(all_fake_balls) != 0: 
        screen_shake = 50
        for fakeball in all_fake_balls: 
            fakeball.move() 
            fakeball.update() 
            fakeball.handle_collision() 
    if len(all_items) != 0: 
        for item in all_items:
            item.move()
            item.check_collision()

               
    gameball.handle_collision()
    gameball.check_ball_reset()
    


    #drawing 
    gametable.draw() 
    left_player.draw() 
    right_player.draw()
    gameball.draw()
    if len(all_items) != 0: 
        for item in all_items: 
            item.draw() 
    if len(all_fake_balls) != 0: 
        for fakeball in all_fake_balls: 
            fakeball.draw() 



    #random generating item 
    if random.randrange(300) == 1: 
        item = Item() 
        all_items.append(item) 


    #Screen outline 
    screen_2_mask = pygame.mask.from_surface(screen_2)
    screen_2_outline = screen_2_mask.to_surface(setcolor = (0, 0, 0, 180), unsetcolor = (0, 0, 0, 0))
    for offset in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        screen.blit(screen_2_outline, offset)
    screen.blit(screen_2, (0, 0))

    #screen shaking 
    screen_shake_offset = (random.random() * screen_shake - screen_shake /2, random.random() * screen_shake - screen_shake /2)
    screen.blit(pygame.transform.scale(screen_2, screen.get_size()), (screen_shake_offset))


    pygame.display.update()

    check_endgame()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False 

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: 
                left_player.move_up = True
            if event.key == pygame.K_s: 
                left_player.move_down = True        
            if event.key == pygame.K_UP: 
                right_player.move_up = True
            if event.key == pygame.K_DOWN: 
                right_player.move_down = True
                
            
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_w: 
                left_player.move_up = False
            if event.key == pygame.K_s: 
                left_player.move_down = False        
            if event.key == pygame.K_UP: 
                right_player.move_up = False 
            if event.key == pygame.K_DOWN: 
                right_player.move_down = False   
    


pygame.quit()




#Copyright © 2025 by futuristickids (Instagram), Futuristic Kids(Facebook), ay.parentingworkshop@yahoo.com
#All rights reserved
