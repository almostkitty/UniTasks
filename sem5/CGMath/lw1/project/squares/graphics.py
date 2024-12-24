import pygame

class Drawer:
    def __init__(self, width, height, color_depth, rf):
        self.width = width
        self.height = height
        self.color_depth = color_depth
        self.rf = rf
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.color = (255, 255, 255)

    def initialize(self, caption):
        pygame.display.set_caption(caption)

    def draw_axes(self, x_min, x_max, y_min, y_max):
        pygame.draw.line(self.screen, self.color, (self.rf.get_x(x_min), self.rf.get_y(0)),
                         (self.rf.get_x(x_max), self.rf.get_y(0)), 2)
        pygame.draw.line(self.screen, self.color, (self.rf.get_x(0), self.rf.get_y(y_min)),
                         (self.rf.get_x(0), self.rf.get_y(y_max)), 2)

    def draw_point(self, x, y, size=5):
        pygame.draw.circle(self.screen, self.color, (self.rf.get_x(x), self.rf.get_y(y)), size)

    def draw_text(self, x, y, text):
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render(text, True, self.color)
        self.screen.blit(text_surface, (self.rf.get_x(x), self.rf.get_y(y)))

    def draw_line(self, x1, y1, x2, y2, width=2):
        pygame.draw.line(self.screen, self.color, (self.rf.get_x(x1), self.rf.get_y(y1)),
                         (self.rf.get_x(x2), self.rf.get_y(y2)), width)
