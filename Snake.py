ygame
import random


class Snake:
    def __init__(self, x, y, L, sw, sh, length: int = 3, spd: int=12):
        self.speed = spd
        self.direction = 1
        self.size = L
        self.dead = False
        self.body = []
        kx = 1
        added = False
        for i in range(length):
            if added:
                added = False
                continue
            self.body.append([x, y])
            if x < self.size and kx == 1 and i < length-1:
                added = True
                y -= self.size
                if y < 0:
                    y += sh
                self.body.append([x, y])
                kx = -1
            elif x + self.size >= sw and i < length-1:
                added = True
                y -= self.size
                if y < 0:
                    y += sh
                self.body.append([x, y])
                kx = 1
            x -= kx * self.size

        self.screen_width = sw
        self.screen_height = sh

    def up(self, coords):
        coords[1] += self.size
        coords[1] %= self.screen_height

    def right(self, coords):
        coords[0] += self.size
        coords[0] %= self.screen_width

    def down(self, coords):
        coords[1] -= self.size
        coords[1] %= self.screen_height

    def left(self, coords):
        coords[0] -= self.size
        coords[0] %= self.screen_width

    def above(self, c1, c2):
        x = (c1[1] + self.screen_height - c2[1])
        return x % self.screen_height == self.size

    def rightof(self, c1, c2):
        x = (c1[0] + self.screen_width - c2[0])
        return x % self.screen_width == self.size

    def below(self, c1, c2):
        x = (c1[1] + self.screen_height - c2[1])
        return x % self.screen_height == self.screen_height - self.size

    def leftof(self, c1, c2):
        x = (c1[0] + self.screen_width - c2[0])
        return x % self.screen_width == self.screen_width - self.size

    def eat(self):
        k = self.body[-2]
        tail = [self.body[-1][0], self.body[-1][1]]
        if self.above(k, tail):
            self.down(tail)
        if self.rightof(k, tail):
            self.left(tail)
        if self.below(k, tail):
            self.up(tail)
        if self.leftof(k, tail):
            self.right(tail)
        self.body.append(tail)

    def move(self):
        self.body.pop()
        neck = [self.body[0][0], self.body[0][1]]
        self.body.insert(1, neck)
        if self.direction == 2:
            self.up(self.body[0])
        if self.direction == 1:
            self.right(self.body[0])
        if self.direction == 0:
            self.down(self.body[0])
        if self.direction == 3:
            self.left(self.body[0])
        if self.body[0] in self.body[1:]:
            self.dead = True


snake_s = 32
snake_l = 15
food_x = 0
food_y = 0
food_size = snake_s/2

SWIDTH = 20*snake_s
SHEIGH = 20*snake_s
FRAMES = 120

pygame.init()
pygame.font.init()
pygame.display.set_caption("Snaix")
window = pygame.display.set_mode((SWIDTH, SHEIGH))


Snake = Snake(SWIDTH/2-snake_s+1, SHEIGH / 2, snake_s, SWIDTH, SHEIGH, snake_l)


def GenFood():
    global food_x, food_y
    food_x = random.randint(0, int(SWIDTH / Snake.size)) * Snake.size + 1 + (Snake.size - food_size)/2
    food_y = random.randint(0, int(SHEIGH / Snake.size)) * Snake.size + (Snake.size - food_size)/2
    if [food_x - (Snake.size - food_size)/2, food_y - (Snake.size - food_size)/2] in Snake.body: food_y = (food_y + Snake.size) % SHEIGH
    for i in range(int(SHEIGH / Snake.size)):
        food_y = (food_y + i * Snake.size) % SHEIGH
        for j in range(int(SWIDTH / Snake.size)):
            food_x = (food_x + j * Snake.size) % SWIDTH
            if [food_x - (Snake.size - food_size)/2, food_y - (Snake.size - food_size)/2] not in Snake.body: break


GenFood()

R, G, B = [], [], []
for i in range(len(Snake.body)):
    B.append(255)
    R.append(random.randint(0, 200))
    G.append(200 - R[i])

def snake_draw():
    global food_x, food_y
    body = Snake.body
    for i in range(len(body)):
        pygame.draw.rect(window, (R[i], G[i], B[i]), pygame.Rect(body[i][0], body[i][1], Snake.size - 1, Snake.size - 1))
    if body[0][0] == food_x - (Snake.size - food_size)/2 and body[0][1] == food_y - (Snake.size - food_size)/2:
        GenFood()
        B.append(255)
        R.append(random.randint(0, 255))
        G.append(255 - R[i])
        Snake.eat()
        return
    if [food_x - (Snake.size - food_size)/2, food_y - (Snake.size - food_size)/2] in Snake.body:
        GenFood()
    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(food_x, food_y, food_size, food_size))


time_to_move = 0

dead = False

cd = Snake.direction

while not dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and Snake.direction != 2:
            cd = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a and Snake.direction != 1:
            cd = 3
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and Snake.direction != 0:
            cd = 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d and Snake.direction != 3:
            cd = 1
    window.fill((0, 0, 0))
    snake_draw()
    time_to_move += 1
    if time_to_move >= FRAMES / Snake.speed:
        time_to_move = 0
        Snake.direction = cd
        Snake.move()
    if Snake.dead:
        while not dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dead = True
            myfont = pygame.font.SysFont('Comic Sans MS', 72)#,True)
            textsurface = myfont.render('Game Over!', True, (255, 255, 0))
            sz = myfont.size("Game Over!")
            window.blit(textsurface, ((SWIDTH-sz[0])/2, SHEIGH/4))
            pygame.display.flip()
    pygame.display.flip()
    pygame.time.Clock().tick(FRAMES)
