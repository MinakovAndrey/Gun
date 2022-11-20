import math
import random
from random import choice

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.count = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if (WIDTH - self.x) <= self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx/2
        if self.x <= self.r:
            self.x = self.r
            self.vx = -self.vx/2
        if (HEIGHT - self.y) <= self.r:
            self.y = HEIGHT - self.r
            self.vy = -self.vy/1.2
            self.count += 1
        if self.y <= self.r:
            self.y = self.r
            self.vy = -self.vy
        if self.count == 5:
            self.vx = 0
            self.vy = 0
        self.vy -= 1
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r + 1
        )
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def dead(self):
        if self.count >= 3:
            self.live -= 1
        if self.live <= 0:
            return False

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj и одинакового ли он с ней цвета.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        global bullet
        if ((self.y-obj.y)**2+(self.x-obj.x)**2<=(self.r+obj.r)**2)and(self.color==obj.color):
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY


    def fire2_start(self, event):
        self.f2_on = True

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        if event.pos[0] != 20:
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        if event.pos[0] == 0:
            self.an = math.asin(1)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = False
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event.pos[0] != 20:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self,event):
        if event.pos[0] != 20:
            self.an = math.atan((450 - event.pos[1]) / (event.pos[0] - 20))
        if event.pos[0] == 0:
            self.an = math.asin(1)
        l = self.f2_power + 10
        cos = math.cos(self.an)
        sin = math.sin(self.an)
        pygame.draw.polygon(
            self.screen,
            self.color,
            [(20 + 5*sin, 450 + 5*cos),
             (20 + l*cos + 5*sin, 450 - l*sin + 5*cos),
             (20 + l*cos - 5*sin, 450 - l*sin - 5*cos),
             (20 - 5*sin, 450 - 5*cos)]
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.surface):
        self.screen = screen
        self.color = choice(GAME_COLORS)
        self.death = 50
        self.x = random.randint(600, 780)
        self.y = random.randint(100, 250)
        self.r = random.randint(5, 50)
        self.points = 0
        self.live = 1
        self.attempts = 0
        self.screen = screen
        self.vx = random.randint(-2, 3)
        self.vy = random.randint(-2, 3)


    def move(self):
        if (WIDTH - self.x) <= self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.x <= self.r:
            self.x = self.r
            self.vx = -self.vx
        if (HEIGHT - self.y) <= self.r:
            self.y = HEIGHT - self.r
            self.vy = -self.vy
        if self.y <= self.r:
            self.y = self.r
            self.vy = -self.vy
        self.x += self.vx
        self.y -= self.vy

    def new_target(self):
        """ Инициализация новой цели. """
        self.death = 100
        x = self.x = random.randint(600, 780)
        y = self.y = random.randint(100, 250)
        r = self.r = random.randint(2, 50)
        vy = self.vy = 0
        vx = self.vx = random.randint(-2, 3)
        color = self.color = choice(GAME_COLORS)
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        self.live = 0

    def draw(self):
        if self.live:
            pygame.draw.circle(
                self.screen,
                BLACK,
                (self.x, self.y),
                self.r + 1
            )
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )


    def dead(self):
        if self.live != 1:
            self.death -= 1
        if self.death <= 0:
            return True


    def show_points(self):
        pygame.draw.rect(
            self.screen,
            WHITE,
            (0,0,120,30)
        )
        points = 'Points: ' + str(self.points)
        surface_points = pygame.font.Font(None, 30)
        text_points = surface_points.render(points, True, BLACK)
        self.screen.blit(text_points, (10,10))


    def show_attempts(self, bullet):
        if self.death < 100:
            pygame.draw.rect(
                self.screen,
                WHITE,
                (200, 100, 200, 30)
            )
            attempts = 'Attempts: ' + str(bullet)
            surface_attempts = pygame.font.Font(None, 30)
            text_attempts = surface_attempts.render(attempts, True, BLACK)
            self.screen.blit(text_attempts, (350, 250))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
boolean = False
boolean1 = False

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False


while not finished:
    screen.fill(WHITE)
    target.show_points()
    target.draw()
    if boolean1:
        target.show_attempts(bullet)

    if boolean:
        gun.draw(motion)
    for b in balls:
        b.draw()
    target.move()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
            motion = event
            boolean = True
    for b in balls:
        b.move()
        b.dead()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.dead()
            boolean1 = True
        if target.dead():
            target.new_target()
            bullet = 0
        if b.dead() == False:
            balls.remove(b)

    gun.power_up()

pygame.quit()