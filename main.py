import PySimpleGUI as sg
import random
import re

letters = [chr(letter) for letter in range(ord('a'), ord('z')+1)] +\
          [chr(letter) for letter in range(ord('A'), ord('Z')+1)]
symbols = [chr(symbol) for symbol in range(ord('!'), ord('/')+1)] +\
          [chr(symbol) for symbol in range(ord(':'), ord('@')+1)] +\
          [chr(symbol) for symbol in range(ord('['), ord('`')+1)] +\
          [chr(symbol) for symbol in range(ord('{'), ord('~')+1)]
numbers = list(range(10))
generate = False
password = ""

layout = [[sg.Text('Input the length of the password:', font=('', 10, 'bold')),
           sg.Input(key='LENGTH', size=(10, 1), justification='center')],
    [sg.Radio('Letters', 'TOP', default=True, key='LETTERS'),
     sg.Radio('Numbers', 'TOP', key='NUMBERS'),
     sg.Radio('Symbols', 'TOP', key='SYMBOLS'),
     sg.Radio('Combination', 'TOP', key='COMBINATION')],
    [sg.Radio('Both Upper/Lower', 'BOT', default=True, key='BOTHUPPERLOWER'),
     sg.Radio('Only Upper', 'BOT', key='ONLYUPPER'),
     sg.Radio('Only Lower', 'BOT', key='ONLYLOWER')],
    [sg.Button('Generate', bind_return_key=True)],
    [sg.Text('Strength:', font=('', 10, 'bold')), sg.Text('NONE', key='STRENGTH', font=('', 10, 'bold'))],
    [sg.Text('Password:', font=('', 10, 'bold')),
     sg.Input(key="PASSWORD", size=(30, 1), justification='center'),
     sg.Button('Copy', size=(5, 1), bind_return_key=True),
     sg.Button('Check', size=(5, 1), bind_return_key=True)]]

window = sg.Window('Simple Password Generator', layout, size=(450, 200), element_justification='c', finalize=True)
window.set_icon('icon.ico')


def check_password(password):
    length_count = len(password) * 0.25
    letters_count = len(re.findall(r'[a-z]', password)) * 1.25 + len(re.findall(r'[A-Z]', password)) * 1.5

    symbols_count = 0
    for symbols in password:
        if 33 <= ord(symbols) <= 47 or 58 <= ord(symbols) <= 64 or 91 <= ord(symbols) <= 96 or 123 <= ord(symbols) <= 126:
            symbols_count += 1.5

    numbers_count = len(re.findall(r'\d', password)) * 1.15
    score = length_count + letters_count + symbols_count + numbers_count

    unique = 3
    if not re.search(r'[a-zA-Z]', password):
        unique -= 1
    if symbols_count == 0:
        unique -= 1
    if not re.search(r'\d', password):
        unique -= 1
    else:
        pass

    if unique == 3:
        if len(password) <= 10:
            score += 2.5
        elif 10 < len(password) <= 20:
            pass
        else:
            score -= 2.5
    elif unique == 2:
        if len(password) <= 10:
            score -= 1
        elif 10 < len(password) <= 20:
            score -= 3.5
        else:
            score -= 6
    elif unique == 1:
        if len(password) <= 10:
            score -= 4.5
        elif 10 < len(password) <= 20:
            score -= 7
        else:
            score -= 9.5

    if score <= 7:
        window['STRENGTH'].update('Very Weak', text_color='red')
    elif 7 < score <= 11:
        window['STRENGTH'].update('Weak', text_color='orange')
    elif 11 < score <= 16:
        window['STRENGTH'].update('Good', text_color='yellow')
    elif 16 < score <= 22:
        window['STRENGTH'].update('Great', text_color='yellowgreen')
    elif 22 < score <= 29:
        window['STRENGTH'].update('Strong', text_color='green')
    else:
        window['STRENGTH'].update('Very Strong', text_color='lime')


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Generate':
        length = values['LENGTH']
        if length == '':
            sg.popup('There is no input to generate.', title='X', icon='icon.ico')
        elif length.isdigit():
            length = int(length)
            if length <= 6:
                sg.popup('The input should be minimum of 7.', title='X', icon='icon.ico')
            elif length >= 26:
                sg.popup('The input maximum is 25.', title='X', icon='icon.ico')
            elif length in range(7, 26):
                generate = True
            else:
                pass
        else:
            sg.popup('The input is not an integer.', title='X', icon='icon.ico')
        if generate:
            for i in range(0, length):
                randomize = random.randint(0, 51)
                if values['LETTERS']:
                    password += letters[randomize]
                elif values['SYMBOLS']:
                    randomize = random.randint(0, 31)
                    password += str(symbols[randomize])
                elif values['NUMBERS']:
                    randomize = random.randint(0, 9)
                    password += str(numbers[randomize])
                elif values['COMBINATION']:
                    crandomize = random.randint(0, 8)
                    if crandomize < 4:
                        password += letters[randomize]
                    elif crandomize == 4:
                        randomize = random.randint(0, 31)
                        password += symbols[randomize]
                    else:
                        randomize = random.randint(0, 9)
                        password += str(numbers[randomize])
                else:
                    pass

            if values['BOTHUPPERLOWER']:
                window['PASSWORD'].update(password)
            elif values['ONLYUPPER']:
                window['PASSWORD'].update(password.upper())
            elif values['ONLYLOWER']:
                window['PASSWORD'].update(password.lower())
            else:
                pass

            generate = False
            password = ""
        else:
            pass

    elif event == 'Copy':
        if values['PASSWORD'] == '':
            sg.popup('There is no password to copy.', title='X', icon='icon.ico')
        else:
            sg.clipboard_set(values['PASSWORD'])
            sg.popup('Successfully copied to clipboard.', title='/', icon='icon.ico')

    elif event == 'Check':
        if values['PASSWORD'] == '':
            sg.popup('There is no password to check.', title='X', icon='icon.ico')
        else:
            check_password(values['PASSWORD'])


window.close()
