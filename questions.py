import random
import pygame
import json
from visualization import *


class Question:
    def __init__(self, question, correct_answer, incorrect_answers):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.answers = {}
        self.letters = ['A', 'B', 'C', 'D']

    def forming(self):
        random.seed()
        temp = []
        correct = None
        length = 4
        temp.append(str(self.correct_answer))
        temp.append(str(self.incorrect_answers[0]))
        temp.append(str(self.incorrect_answers[1]))
        temp.append(str(self.incorrect_answers[2]))
        while length:
            i = random.randint(0, length)
            if i in range(0, length):
                self.answers[self.letters[len(self.answers)]] = temp[i]
                if correct is None and i == 0:
                    correct = self.letters[len(self.answers)-1]
                length -= 1
                temp.__delitem__(i)
        self.answers['Correct'] = correct
        self.answers['Question'] = str(self.question)
        return self.answers

    def fifty_fifty(self):
        temp = []
        correct = self.answers['Correct']
        for i in range(0, 4):
            if self.letters[i] != correct:
                temp.append(self.letters[i])
        random.seed()
        incorrect = None
        while incorrect is None:
            i = random.randint(0, 3)
            if len(temp) > i >= 0:
                incorrect = temp[i]
        for i in range(0, 4):
            if self.letters[i] != correct and self.letters[i] != incorrect:
                self.answers[self.letters[i]] = 0

    def audience(self, window, screen):
        answer = {}
        balance = 100
        i = 0
        while balance == 100:
            rand = random.randint(70, 95)
            if 50 <= rand <= 95:
                answer[self.answers['Correct']] = rand
                balance -= rand

        while balance > 0:
            flag = True
            if self.answers['Correct'] != self.letters[i]:
                while flag:
                    rand = random.randint(0, int(balance * 0.7))
                    if i == 2 and self.answers['Correct'] == 'D':
                        if not self.answers[self.letters[i]] == 0:
                            answer[self.letters[i]] = balance
                        else:
                            answer[self.letters[i]] = 0
                            if self.letters[i-1] == self.answers['Correct'] or self.answers[self.letters[i-1]] == 0:
                                answer[self.letters[i-2]] += balance
                            else:
                                answer[self.letters[i-1]] += balance
                        balance = 0
                        flag = False
                    elif i == 3 and self.answers['Correct'] != 'D':
                        if self.answers[self.letters[i]] == 0:
                            if self.answers[self.letters[i-1]] == 0 or self.answers['Correct'] == self.letters[i-1]:
                                if self.answers['Correct'] == self.letters:
                                    answer[self.letters[i-2]] += balance
                                answer[self.letters[i-1]] = 0
                            else:
                                answer[self.letters[i-1]] += balance
                            answer[self.letters[i]] = 0
                        else:
                            answer[self.letters[i]] = balance
                        balance = 0
                        flag = False
                    elif 0 <= rand < int(balance * 0.7):
                        if not self.answers[self.letters[i]] == 0:
                            answer[self.letters[i]] = rand
                            balance -= rand
                        else:
                            answer[self.letters[i]] = 0
                        flag = False
            i += 1

        screen.draw_image(400, 100, window, 1)
        screen.write_text('Помощ от публиката', (184, 184, 0), 645, 115, 25)

        screen.write_text('A.', (184, 184, 0), 480, 150, 35)
        screen.write_text(str(answer['A']) + '%', (255, 255, 255), 510, 150, 35)

        screen.write_text('B.', (184, 184, 0), 630, 150, 35)
        screen.write_text(str(answer['B']) + '%', (255, 255, 255), 660, 150, 35)

        screen.write_text('C.', (184, 184, 0), 780, 150, 35)
        screen.write_text(str(answer['C']) + '%', (255, 255, 255), 810, 150, 35)

        screen.write_text('D.', (184, 184, 0), 930, 150, 35)
        screen.write_text(str(answer['D']) + '%', (255, 255, 255), 960, 150, 35)
        pygame.display.update()
        pygame.time.wait(5000)

    def phone(self, window, screen):
        rand = -5
        answers = ['Не съм сигурен, но мисля, че е ', 'Разбира се, че отговора е ', 'Според мен отговора е ',
                   'Правилният отговор е ', 'Съжалявам, но не знам отговора.', 'Отговора е очевиден - ']
        while 0 <= rand <= len(answers):
            rand = random.randint(0, len(answers))
        screen.draw_image(400, 100, window, 1)
        screen.write_text('Обади се на приятел', (184, 184, 0), 645, 115, 25)
        if rand == 4:
            screen.write_text(answers[rand] + self.answers['Correct'], (255, 255, 255), 480, 150, 35)
        else:
            screen.write_text(answers[rand] + self.answers['Correct'], (255, 255, 255), 480, 150, 35)
        pygame.display.update()
        pygame.time.wait(5000)


class Game:
    def __init__(self, progress=None):
        if progress is None:
            self.question_number = 1
            self.hints = [False, False, False]
            self.got_questions = [0]
        else:
            self.question_number = progress['Quest_num']
            self.hints = progress['Hints']
            self.got_questions = progress['Got_questions']

    def get_question(self):
        with open('database.json', 'r') as file:
            all_questions = json.load(file)
        rand = 0
        while len(all_questions) < rand < 1 or rand in self.got_questions:
            rand = random.randint(1, len(all_questions))
        self.got_questions.append(rand)
        question = all_questions[str(rand)]
        question = {'Question': question['Question'], 'Correct': question['Correct'], 'Incorrect': question['Incorrect']}
        return question
