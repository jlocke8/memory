#!/bin/python3

import random
import time
import re
import subprocess
import pyttsx3

#initialize speech engine
speak = pyttsx3.init()

#define game commands
game_commands = [['help', '?', 'h'], ['exit', 'quit', 'q', 'x'], ['show', 's', 'status'],['repeat', 'r', 'again', 'a', 'peek', 'p'], \
['menu', 'configure', 'm', 'c']]

#game configuration options
game_modes = ['numbers', 'letters', 'alphanumeric', 'password_characters']
game_mode_case = ['ignore_case', 'specify_case']
game_difficulty = ['easy', 'normal', 'hard'] 

#make random numbers to memorize
memory_numbers = [random.randint(0,9) for _ in range(100) ]

print(memory_numbers)

state_game = 'HOME'
number_level = 1;

#create a dictionary of lists that contain a series responses to choose from
responses_dict = \
{'WIN':['You got it!',    #response type: WIN 
'Awesome sauce!',
'Correct!',
'Way to go!',
'Yup. Thats right',
'Very good.',
'That is craze balls.',
'Your memory is very good.',
'How do you remember all those numbers?',
'Incredible!',
'Thats right!',
'Woo hoo!',
'You are amazing!',
'Congratulations!',
'Those are the correct numbers!',
'Excellent',
'Wow, you are good.',
'I am amazed.',
'Amaze balls.',
'Yes. All the numbers are correct'
'You got it right!'],

'MISS':['Sorry. Thats wrong.',
'Oops!  I think you missed one.',
'Oh no.',
'Good effort, but wrong.',
'That is incorrect.',
'Ah man.  Too bad.',
'Come on, man!',
'Ah, come on.',
'Hmm, I think not.',
'What are you thinking?',
'Are you sure?  That does not seem right.',
'Too bad, incorrect.',
'No no, no!'],

'TRYAGAIN':['Keep trying.',
'You can do it! I believe in you.',
'Dont give up',
'Try again.',
'Give it another shot.',
'No pain. no gain.',
'Be persistent.',
'You are growing your brain.',
'I think you will win this next time.',
'Please try again.',
'Do it again!',
'You need more practice.',
'The next time is a charm.',
'Youll get it. Keep trying.']}

#function to print responses and speak responses
def sayResponse(custom_text , response_type, is_print = True):
    if custom_text is not None:
        response = custom_text
    else:
        response = random.choice(responses_dict[response_type])

        if response_type == 'WIN':
            pass
        elif response_type == 'MISS':
            pass
        elif response_type == 'TRYAGAIN':
            pass
        elif response_type == 'LOSE':
            pass
        elif response_type == 'BYE':
            pass
        else:
            pass
    if is_print is True:
        print(response)    
    
#    result = subprocess.run(["espeak", response])
    
    speak.say(response)
    speak.runAndWait()

#-----------game loop---------
while state_game != 'DONE':
    #game state, home
    if state_game == 'HOME':
        print("\nWelcome to the memory game.\n")
        state_game = 'START'

    #game state, start
    elif state_game == 'START':
        state_game = 'DISPLAY'

    #game state, display numbers
    elif state_game == 'DISPLAY':
        print("\n")
        #print("Memorize the following numbers as displayed. Then enter them from memory.\n")
        #result = subprocess.run(["espeak", "Memorize the following numbers as displayed. Then enter them from memory.\n"])
        sayResponse("Memorize the following numbers as displayed. Then enter them from memory.\n", None)
        time.sleep(2)
        #show numbers sequentially
        print(*memory_numbers[0: number_level])
        for i in range( number_level):
            #time.sleep(1)
            #print(str(memory_numbers[i]) + "  ")
            sayResponse(str(memory_numbers[i]), None, False)
            #result = subprocess.run(["espeak", str(memory_numbers[i]) ])
#            print(str(memory_numbers[i]) + "  ", end=" ")
            time.sleep(1)

        time.sleep(1)
        #clear numbers from console
        print ("\033[A\033[K\033[A")  #move curser up one line clear line and move curser up line
         
        #print("\nWhat are the " + str(number_level) + " number(s) I just showed?:\n")
        #result = subprocess.run(["espeak", "\nWhat are the " + str(number_level) + " numbers I just showed?:\n"])
        sayResponse("\nWhat are the " + str(number_level) + " numbers I just showed?:\n", None)
        #for i in range( number_level+1):
        #    print ("\033[A\033[K\033[A")  #move curser up one line clear line and move curser up line

        state_game = 'INPUT'

    #game state, player inputs numbers
    elif state_game == 'INPUT':
        player_input=input()
        for i in range( 1):
            print ("\033[A\033[K\033[A")  #move curser up one line clear line and move curser up line
        if player_input == '':
            state_tame = 'INPUT'
        else:
            state_game = 'PARSE'   

    #game state, parse input
    elif state_game == 'PARSE':
        #check whether input has letter text to parse any game commands
        if player_input.isupper() or player_input.islower():
            input_type = 'command'
        else:
            input_type = 'numbers'
        #split input into list based on multiple delimiters
        player_input_split = re.split('[.,;:&\*\-\s]', player_input)
        #print(player_input_split)

        #parse command
        if input_type == 'command':
            print("Command entered: " + player_input_split[0])
            command_number = ''
            for i,commands in enumerate(game_commands): #get index and each element in game_commands
                for cmd in commands:
                    if player_input_split[0] == cmd:
                        print("Command found.")
                        #command_number = commands
                        command_number = i
                        break
                    
                    
            if command_number != '':
                print("Valid command.")
                print(command_number)
                state_game = 'INPUT'
            else:
                print("Invalid command.")
                state_game = 'INPUT'

        #parse numbers 
        elif input_type == 'numbers':
            #split any multiple digit numbers inputted without spaces into single digits and place into one long list
            player_input_digits = []            
            for number in player_input_split:
                for digit in str(number):
                    player_input_digits.append(int(digit))
            print("Numbers entered: ", end="")
            print(*player_input_digits)
            
            #first check if player entered correct number of numbers,  too much or too little?
            if len(player_input_digits) == number_level:
        
                #check if player entered correct numbers
                correct_numbers_flag = 1
                for i in range(number_level):
                    if player_input_digits[i] != memory_numbers[i]:
                        correct_numbers_flag = 0
                        break
                
                #if wrong let player try again, else proceed to next level
                if correct_numbers_flag == 0:
                    print("Incorrect numbers entered")
                    sayResponse(None, 'MISS')
                    state_game = 'TRYAGAIN'
                else:
                    #print("Congratulations. Those are the correct numbers entered.")
                    #result = subprocess.run(["espeak", "Congratulations. Those are the correct numbers entered."])
                    sayResponse(None, 'WIN')
                    state_game = 'NEXT'
            else:
                print("Incorrect amount of numbers entered")
                sayResponse(None, 'MISS')
                state_game = 'TRYAGAIN'

            for i in range( 3):
                print ("\033[A\033[K\033[A")  #move curser up one line clear line and move curser up line

        else:
            print("Input Error")
        time.sleep(1)

    #game state, next level
    elif state_game == 'NEXT':
        number_level = number_level + 1
        print("LEVEL " + str(number_level))
        result = subprocess.run(["espeak", "level" + str(number_level)])
        state_game = 'DISPLAY'

    #game state, try again
    elif state_game == 'TRYAGAIN':
        print("\nSorry those were not the correct numbers. Try again.\n")
        #result = subprocess.run(["espeak", "Sorry those were not the correct numbers. Try again"])
        sayResponse(None, 'TRYAGAIN')
        state_game = 'DISPLAY'
    #game state, lose
    elif state_game == 'LOSE':
        print("\nSorry you lose. Try again next time.\n")
    #game state, exit game
    elif state_game == 'EXIT':
        print("\nThanks for playing!\n")
        state_game = 'DONE'
    else:
        print("\nThanks for playing!\n")

