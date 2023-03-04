# import the pygame module
import pygame.transform
import json
from pygame.locals import *
import pygame
from visualization import *
from questions import *
# from text_input import *
pygame.init()


def main():
    screen = Screen(1920, 1080, (28, 0, 99))
    running = 1
    progress = None
    pygame.display.set_caption('Стани богат')
    while running:
        clock = pygame.time.Clock()
        clock.tick(5)
        if running == 1:
            running = main_menu(screen)
        elif running == 2:
            running = gaming(screen, progress)
        elif running == 3:
            result = load_progress(screen)
            running = result[0]
            progress = result[1]
            if len(progress) == 0:
                progress = None
        elif running == 4:
            running = about_us(screen)
    pygame.quit()


def main_menu(screen):
    """
    This is the main menu.
    Here you choose between:
    start, exit and options menu.
    """
    clear_screen(screen, (28, 0, 99), 'background.png')
    exit_button = setup_button(770, 785, 'answer_box_right.png', 2, 1.5)
    about_button = setup_button(770, 700, 'answer_box_right.png', 2, 1.5)
    start_button = setup_button(0, 787, 'answer_box_left.png', 2, 1.5)
    load_button = setup_button(0, 702, 'answer_box_left.png', 2, 1.5)
    exit_button.draw(screen)
    about_button.draw(screen)
    start_button.draw(screen)
    load_button.draw(screen)
    screen.write_text('New game', (255, 255, 255), 325, 809, 35)
    screen.write_text('Load game', (255, 255, 255), 325, 724, 35)
    screen.write_text('Exit', (255, 255, 255), 1110, 809, 35)
    screen.write_text('About us', (255, 255, 255), 1085, 724, 35)
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
            elif load_button.click():
                running = 3
            elif about_button.click():
                running = 4
    pygame.display.update()
    return running


def about_us(screen):
    running = 4
    clear_screen(screen, (24, 10, 54), 'studio.jpg', 1.4)
    about = setup_button(0, 555, 'question.png', 2, 1.5, 1)
    about.draw(screen)
    esc = setup_button(0, 0, 'menu.png', 0.2)
    esc.draw(screen)
    screen.write_text('Тази игра е направена от Богдан Яков 9б, като проект за Въведение в скриптовите езици.', (255, 255, 255), 170, 600, 30)
    pygame.display.update()
    while running == 4:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 1
            elif event.type == QUIT:
                running = 1
            elif esc.click():
                running = 1
    return running


def gaming(screen, progress=None):
    running = 2
    game = Game(progress)
    while 0 < game.question_number <= 15 and running == 2:
        clear_screen(screen, (24, 10, 54), 'studio.jpg', 1.4)
        quest = game.get_question()
        quest = Question(quest['Question'], quest['Correct'], quest['Incorrect'])
        task = Task('answer_box_left.png', 'answer_box_right.png', 'question.png', 'marked_box_left.png',
                    'marked_box_right.png', 'correct_box_left.png', 'correct_box_right.png', 'fifty_fifty.png',
                    'audience.png', 'phone.png', quest, game.hints, 'x.png')
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
                    clear_screen(screen, (24, 10, 54), 'studio.jpg', 1.4)
                    task.print(screen, game.question_number, task.task.answers)
                    pygame.display.update()
                    pygame.time.wait(1500)
                    if answer == 1:
                        mark_correct(task, screen, game.question_number)
                        game.question_number = 0
                    elif answer == 2:
                        mark_correct(task, screen, game.question_number)
                        game.question_number += 1
                elif hint:
                    clear_screen(screen, (24, 10, 54), 'studio.jpg', 1.4)
                    task.print(screen, game.question_number, task.task.answers)
                    pygame.display.update()
                    game.hints[hint-1] = True
                elif esc.click():
                    running = 4
                    while running == 4:
                        running = pause_menu(screen, game)
                    if running != 2:
                        return running
                    clear_screen(screen, (24, 10, 54), 'studio.jpg', 1.4)
                    esc.draw(screen)
                    task.print(screen, game.question_number, task.task.answers)
                    pygame.display.update()
        price_won(screen, task.money, game.question_number)

    pygame.display.update()
    running = 1
    return running


def pause_menu(screen, game):
    buttons = draw_pause_menu(screen, game)
    running = 4
    while running == 4:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 2
            elif event.type == QUIT:
                running = 0
            elif buttons[0].click():
                running = 2
            elif buttons[2].click():
                running = 1
            elif buttons[1].click():
                save_progress(screen, game)
                pygame.time.wait(2000)
                buttons = draw_pause_menu(screen, game)
    return running


def save_progress(screen, game):
    pressed = 1
    save = {
        'Quest_num': game.question_number,
        'Hints': game.hints,
        'Got_questions': game.got_questions
    }
    with open('save.json', 'r') as file:
        data = json.load(file)
    if len(data) != 0:
        pressed = 0
        screen.draw_image(10, 0, 'window.png', 1.3)
        screen.write_text("It's already have a saved game.", (184, 184, 0), 120, 15, 55)
        screen.write_text("Do you want to overwrite your save?", (184, 184, 0), 60, 55, 55)
        confirm_button = setup_button(482, 118, 'answer_box_right.png', 2, 1.5, 147)
        cancel_button = setup_button(0, 120, 'answer_box_left.png', 2, 1.5, 147)
        confirm_button.draw(screen)
        cancel_button.draw(screen)
        screen.write_text('Confirm', (255, 255, 255), 625, 137, 50)
        screen.write_text('Cancel', (255, 255, 255), 170, 137, 50)
        pygame.display.update()
        while pressed == 0:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pressed = 2
                elif confirm_button.click():
                    pressed = 1
                elif cancel_button.click():
                    pressed = 2
    if pressed == 1:
        with open('save.json', 'w') as file:
            json.dump(save, file)
        screen.draw_image(10, 0, 'window.png', 1.3)
        screen.write_text('Saved successfully', (184, 184, 0), 90, 15, 100)
        pygame.display.update()


def load_progress(screen):
    '''
    This function load the saved progress
    of the game.
    :param screen:
    :return progress of the game:
    '''
    running = 3
    with open('save.json', 'r') as file:
        progress = json.load(file)
    clear_screen(screen, (0, 0, 0), 'background.png')
    next_button = setup_button(770, 785, 'answer_box_right.png', 2, 1.5)
    back_button = setup_button(0, 787, 'answer_box_left.png', 2, 1.5)
    next_button.draw(screen)
    back_button.draw(screen)
    screen.write_text('Back', (255, 255, 255), 325, 809, 35)
    if len(progress) != 0:
        hints = ['fifty_fifty.png', 'audience.png', 'phone.png', 'x.png']
        screen.write_text('Continue', (255, 255, 255), 1080, 809, 35)
        screen.draw_image(225, 0, 'window.png', 1.5)
        screen.write_text('Saved data:', (184, 184, 0), 675, 15, 45)
        screen.write_text('Question:', (184, 184, 0), 360, 70, 45)
        screen.write_text(str(progress['Quest_num']), (255, 255, 255), 550, 70, 45)
        screen.write_text('Hints:', (184, 184, 0), 750, 70, 45)
        screen.draw_image(870, 60, hints[0], 0.5)
        if progress['Hints'][0]:
            screen.draw_image(880, 60, hints[3], 0.3)
        screen.draw_image(980, 60, hints[1], 0.5)
        if progress['Hints'][1]:
            screen.draw_image(990, 60, hints[3], 0.3)
        screen.draw_image(1090, 60, hints[2], 0.5)
        if progress['Hints'][2]:
            screen.draw_image(1100, 60, hints[3], 0.3)
    else:
        screen.draw_image(225, 0, 'window.png', 1.5)
        screen.write_text('No saved data', (184, 184, 0), 560, 40, 75)
        screen.write_text('N/A', (184, 184, 0), 1110, 809, 35)
    pygame.display.update()
    while running == 3:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 1
            elif event.type == QUIT:
                running = 0
            elif back_button.click():
                running = 1
            elif next_button.click() and len(progress) != 0:
                with open('save.json', 'w') as file:
                    json.dump({}, file)
                running = 2
    return [running, progress]


if __name__ == '__main__':
    main()
