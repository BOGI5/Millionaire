# import the pygame module
import pygame.transform
from pygame.locals import *
import pygame
from button import *
from questions import *
pygame.init()


def main():
    screen = Screen(1920, 1080, (28, 0, 99))
    running = 1
    pygame.display.set_caption('Стани богат')
    while running:
        clock = pygame.time.Clock()
        clock.tick(5)
        if running == 1:
            running = main_menu(screen)
        if running == 2:
            running = question(screen)
    pygame.quit()


def main_menu(screen):
    """
    This is the main menu.
    Here you choose between:
    start, exit and options menu.
    """
    screen.clear_screen((28, 0, 99))
    screen.set_background('background.png')
    exit_button = setup_button(770, 750, 'answer_box_right.png', 2, 1.5)
    start_button = setup_button(0, 752, 'answer_box_left.png', 2, 1.5)
    exit_button.draw(screen)
    start_button.draw(screen)
    screen.write_text('Start', (0, 0, 0), 350, 779, 35)
    screen.write_text('Exit', (0, 0, 0), 1150, 779, 35)
    running = 1
    pygame.display.update()
    while running == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
            elif event.type == QUIT:
                running = 0
            elif exit_button.click():
                running = 0
            elif start_button.click():
                running = 2
    pygame.display.update()
    return running


def question(screen):
    running = 2
    game = Game()
    while 0 < game.question_number <= 15 and running == 2:
        screen.clear_screen((24, 10, 54))
        screen.set_background('studio.jpg', 1.4)
        quest = game.get_question()
        quest = Question(quest['Question'], quest['Correct'], quest['Incorrect'])
        task = Task('answer_box_left.png', 'answer_box_right.png', 'question.png', 'marked_box.png',
                    'correct_box.png', 'fifty_fifty.png', 'audience.png', 'phone_2.png', quest, game.hints, 'x.png')
        esc = setup_button(0, 0, 'menu.png', 0.2)
        esc.draw(screen)
        task.print(screen, game.question_number)
        pygame.display.update()
        answer = 0
        while answer == 0 and running == 2:
            for event in pygame.event.get():
                answer = task.get_answer()
                hint = task.get_hint('window.png', screen)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = 1
                elif event.type == QUIT:
                    running = 0
                elif answer:
                    if answer == 1:
                        game.question_number = 0
                    elif answer == 2:
                        game.question_number += 1
                elif hint:
                    screen.clear_screen((24, 10, 54))
                    screen.set_background('studio.jpg', 1.4)
                    task.print(screen, game.question_number, task.task.answers)
                    pygame.display.update()
                    game.hints[hint-1] = True
                elif esc.click():
                    running = 1

    pygame.display.update()
    running = 1
    return running


if __name__ == '__main__':
    main()
