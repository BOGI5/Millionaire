from questions import *
from pygame.locals import *
import pygame.transform
import pygame
from time import *
pygame.init()


class Button:
    def __init__(self, x, y, image, scale, height, width):
        width = image.get_width()-width
        height = image.get_height() / height
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        screen.screen.blit(self.image, (self.rect.x, self.rect.y))

    def click(self):
        pos = pygame.mouse.get_pos()

        action = False

        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class Task:
    def __init__(self, answer_box_left, answer_box_right, question_box, marked_box_left, marked_box_right,
                 correct_box_left, correct_box_right, fifty, audience, phone, task, hints, used):
        self.question_box = setup_button(0, 555, question_box, 2, 1.5, 1)
        self.answer_a = setup_button(0, 690, answer_box_left, 2, 1.5, 1)
        self.answer_b = setup_button(774, 688, answer_box_right, 2, 1.5, 1)
        self.answer_c = setup_button(0, 780, answer_box_left, 2, 1.5, 1)
        self.answer_d = setup_button(774, 778, answer_box_right, 2, 1.5, 1)
        self.marked_left = marked_box_left
        self.marked_right = marked_box_right
        self.correct_left = correct_box_left
        self.correct_right = correct_box_right
        self.fifty = setup_button(1190, 0, fifty, 0.5)
        self.audience = setup_button(1300, 0, audience, 0.5)
        self.phone = setup_button(1410, 0, phone, 0.5)
        self.task = task
        self.hints = hints
        self.used = used
        self.money = ['500', '1 000', '2 000', '3 000', '5 000', '10 000', '15 000', '25 000', '50 000',
                      '100 000', '200 000', '400 000', '800 000', '1 500 000', '3 000 000']

    def print(self, screen, quest_number, question=None):
        self.question = question
        if self.question == None:
            self.question = self.task.forming()

        screen.draw_image(400, 0, '../Images/window.png', 1)
        screen.write_text('Въпрос ' + str(quest_number) + ':', (184, 184, 0), 500, 30, 45)
        screen.write_text(self.money[quest_number-1], (255, 255, 255), 775, 30, 45)

        self.question_box.draw(screen)
        screen.write_question(self.question['Question'], (255, 255, 255), 35)

        self.answer_a.draw(screen)
        if self.question['A'] != 0:
            screen.write_text('A.', (184, 184, 0), 100, 713, 35)
            screen.write_text(self.question['A'], (255, 255, 255), 135, 713, 35)

        self.answer_b.draw(screen)
        if self.question['B'] != 0:
            screen.write_text('B.', (184, 184, 0), 850, 713, 35)
            screen.write_text(self.question['B'], (255, 255, 255), 885, 713, 35)

        self.answer_c.draw(screen)
        if self.question['C'] != 0:
            screen.write_text('C.', (184, 184, 0), 100, 804, 35)
            screen.write_text(self.question['C'], (255, 255, 255), 135, 804, 35)

        self.answer_d.draw(screen)
        if self.question['D'] != 0:
            screen.write_text('D.', (184, 184, 0), 850, 804, 35)
            screen.write_text(self.question['D'], (255, 255, 255), 885, 804, 35)

        self.fifty.draw(screen)
        if self.hints[0]:
            screen.draw_image(1200, 0, self.used, 0.3)
        self.audience.draw(screen)
        if self.hints[1]:
            screen.draw_image(1310, 0, self.used, 0.3)
        self.phone.draw(screen)
        if self.hints[2]:
            screen.draw_image(1420, 0, self.used, 0.3)

        self.correct = self.question['Correct']

    def get_answer(self):
        if self.answer_a.click() and self.question['A'] != 0:
            self.answer_a = setup_button(0, 678, self.marked_left, 2, 1.5, 1)
            if self.correct == 'A':
                return 2
            else:
                return 1

        elif self.answer_b.click() and self.question['B'] != 0:
            self.answer_b = setup_button(770, 688, self.marked_right, 2, 1.5, 1)
            if self.correct == 'B':
                return 2
            else:
                return 1

        elif self.answer_c.click() and self.question['C'] != 0:
            self.answer_c = setup_button(0, 768, self.marked_left, 2, 1.5, 1)
            if self.correct == 'C':
                return 2
            else:
                return 1

        elif self.answer_d.click() and self.question['D'] != 0:
            self.answer_d = setup_button(770, 778, self.marked_right, 2, 1.5, 1)
            if self.correct == 'D':
                return 2
            else:
                return 1
        return 0

    def mark_correct(self):
        if self.correct == 'A':
            self.answer_a = setup_button(0, 680, self.correct_left, 2, 1.5, 1)
        elif self.correct == 'B':
            self.answer_b = setup_button(771, 682, self.correct_right, 2, 1.5, 1)
        elif self.correct == 'C':
            self.answer_c = setup_button(0, 770, self.correct_left, 2, 1.5, 1)
        elif self.correct == 'D':
            self.answer_d = setup_button(771, 772, self.correct_right, 2, 1.5, 1)

    def get_hint(self, window, screen):
        if self.fifty.click() and not self.hints[0]:
            self.task.fifty_fifty()
            self.hints[0] = True
            return 1

        elif self.audience.click() and not self.hints[1]:
            self.task.audience(window, screen)
            self.hints[1] = True
            return 2

        elif self.phone.click() and not self.hints[2]:
            self.task.phone(window, screen)
            self.hints[2] = True
            return 3
        return 0


class Screen:
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), flags=FULLSCREEN)
        self.screen.fill(background_color)

    def clear_screen(self, background_color):
        self.screen.fill(background_color)

    def set_background(self, source, height=1):
        background = pygame.image.load(source)
        background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height() / height))
        self.screen.blit(background, (0, 0))

    def write_text(self, text, colour, x, y, size):
        font = pygame.font.SysFont('calibri', size, True, True)
        text = font.render(text, True, colour)
        self.screen.blit(text, (x, y))

    def write_question(self, text, colour, size):
        font = pygame.font.SysFont('calibri', size, True, True)
        text = font.render(text, True, colour)
        text_rect = text.get_rect()
        x = (self.width - text_rect.width) / 2 - 180
        y = 600
        self.screen.blit(text, (x, y))

    def draw_image(self, x, y, image, scale):
        image = pygame.image.load(image).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        rect = image.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(image, (rect.x, rect.y))


def setup_button(x, y, file, scale, height=1.0, width=0):
    image = pygame.image.load(file).convert_alpha()
    return Button(x, y, image, scale, height, width)


def mark_correct(task, screen, question_number):
    task.mark_correct()
    screen.clear_screen((24, 10, 54))
    screen.set_background('../Images/studio.jpg', 1.4)
    task.print(screen, question_number, task.task.answers)
    pygame.display.update()
    pygame.time.wait(1500)


def clear_screen(screen, color, background=None, height=1.0):
    screen.clear_screen(color)
    if background is not None:
        screen.set_background(background, height)


def draw_pause_menu(screen, game):
    money_tree = {
        '../Images/1.png': [962, 755],
        '../Images/2.png': [960, 705],
        '../Images/3.png': [962, 655],
        '../Images/4.png': [964, 600],
        '../Images/5.png': [963, 542],
        '../Images/6.png': [964, 492],
        '../Images/7.png': [963, 436],
        '../Images/8.png': [964, 383],
        '../Images/9.png': [964, 331],
        '../Images/10.png': [964, 277],
        '../Images/11.png': [964, 224],
        '../Images/12.png': [963, 170],
        '../Images/13.png': [964, 117],
        '../Images/14.png': [963, 64],
        '../Images/../Images/15.png': [963, 11]
    }
    clear_screen(screen, (0, 0, 0), '../Images/studio_pause.jpg')
    resume_button = setup_button(130, 500, '../Images/box.png', 2, 1.5, 1)
    save_button = setup_button(130, 600, '../Images/box.png', 2, 1.5, 1)
    leave_button = setup_button(130, 700, '../Images/box.png', 2, 1.5, 1)
    resume_button.draw(screen)
    save_button.draw(screen)
    leave_button.draw(screen)
    screen.draw_image(950, 0, '../Images/money_tree.png', 1.1)
    for i in range(1, game.question_number):
        file = '../Images/' + str(i) + '.png'
        screen.draw_image(money_tree[file][0], money_tree[file][1], '../Images/got_price.png', 1.1)
    file = '../Images/' + str(game.question_number) + '.png'
    screen.draw_image(money_tree[file][0], money_tree[file][1], file, 1.1)
    screen.write_text('Resume', (255, 255, 255), 385, 517, 50)
    screen.write_text('Save', (255, 255, 255), 410, 617, 50)
    screen.write_text('Leave', (255, 255, 255), 400, 717, 50)
    pygame.display.update()
    return [resume_button, save_button, leave_button]


def price_won(screen, money_list, question_number):
    clear_screen(screen, (24, 10, 54), '../Images/studio.jpg', 1.4)
    button = setup_button(0, 555, '../Images/question.png', 2, 1.5, 1)
    button.draw(screen)
    if question_number == 1:
        question_number = 2
    if question_number == 0:
        screen.write_text('Ти загуби. Опитай пак.', (255, 255, 255), 470, 600, 60)
    elif question_number == 16:
        screen.write_text('Ти спечели! Честито.', (255, 255, 255), 500, 600, 60)
        price = setup_button(0, 690, '../Images/question.png', 2, 1.5, 1)
        price.draw(screen)
        screen.write_text('Печалба: ', (184, 184, 0), 500, 735, 60)
        screen.write_text(str(money_list[14]), (255, 255, 255), 800, 735, 60)
    else:
        screen.write_text('Печалба: ', (184, 184, 0), 500, 600, 60)
        screen.write_text(str(money_list[question_number-2]), (255, 255, 255), 800, 600, 60)
    screen.write_text('Натисни "space", за да продължиш.', (255, 255, 255), 600, 570, 20)
    pygame.display.update()
    pressed = True
    while pressed:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pressed = False
