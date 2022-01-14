import pygame as pg

from functools import reduce
from random import random, choice, randint
import time


class Life:
    def __init__(self, app, container=None):
        self.app = app
        if container:
            self.container, self.SIZE = container, len(container)
        else:
            self.container, self.SIZE = self.create_container()

    def create_container(self):
        SIZE = 30 + randint(1, 10)

        list1 = [[0]*SIZE for i in range(SIZE)]

        def create_random_pos(container):
            param = 3
            for y in range(len(container)):
                for x in range(len(container)):
                    number = int(bool(randint(0, 10) % param))
                    if number:
                        param = 3
                    else:
                        param += 1
                    container[y][x] = number

        create_random_pos(list1)
        return list1, SIZE

    def check_for_ones(self, items, index):
        return reduce(lambda x, y: x[index]+y[index], items)

    def make_emty_edge(self):

        def add_zeros():
            for item in self.container:
                item.insert(0, 0)
                item.append(0)

        def check_for_ones(index):

            return sum(map(lambda x: x[index], self.container))
        if (sum(self.container[0]) > 0 or sum(self.container[-1]) > 0) or (
                check_for_ones(0) > 0 or check_for_ones(-1) > 0):
            self.container.insert(0, [0]*self.SIZE)

            self.container.append([0]*(self.SIZE))

            add_zeros()
            self.SIZE = len(self.container)

    def game_rule(self):
        fake_container = [[0]*self.SIZE for i in range(self.SIZE)]

        def summof_side(x, y):

            list_of_inkr = [(0, -1), (1, -1), (1, 0), (1, 1),
                            (0, 1), (-1, 1), (-1, 0), (-1, -1)]
            res = 0
            for (dy, dx) in list_of_inkr:
                if x+dx < 0 or x+dx >= self.SIZE or y+dy < 0 or y+dy >= self.SIZE:
                    continue
                res += self.container[y+dy][x+dx]
            return res
        for index_y, items in enumerate(self.container):
            for index_x, item in enumerate(items):
                if item == 1:
                    if summof_side(index_x, index_y) >= 2 and summof_side(index_x, index_y) <= 3:
                        fake_container[index_y][index_x] = 1
                else:
                    if summof_side(index_x, index_y) == 3:
                        fake_container[index_y][index_x] = 1
        self.container = fake_container.copy()

    def run(self):
        self.app.screen.fill('black')
        for index_y, items in enumerate(self.container):
            for index_x, item in enumerate(items):
                rect = index_x * (1000 // self.SIZE), index_y * (1000 //
                                                                 self.SIZE), (1000 // self.SIZE)-2, (1000 // self.SIZE)-2
                if item:
                    pg.draw.rect(self.app.screen, pg.Color('orange'), rect)
        self.make_emty_edge()
        self.game_rule()


class App:
    def __init__(self, WIDTH=1000, HEIGHT=1000):
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.life = Life(
            app=self)

    def run(self):
        while True:
            time.sleep(0.4)
            self.life.run()
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            pg.display.flip()
            self.clock.tick()


if __name__ == '__main__':
    app = App()
    app.run()
