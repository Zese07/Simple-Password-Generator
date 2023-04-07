import PySimpleGUI as sg
import random

letters = [chr(letter) for letter in range(ord('a'), ord('z')+1)] +\
          [chr(letter) for letter in range(ord('A'), ord('Z')+1)]
symbols = [chr(symbol) for symbol in range(ord('!'), ord('/')+1)] +\
          [chr(symbol) for symbol in range(ord(':'), ord('@')+1)] +\
          [chr(symbol) for symbol in range(ord('['), ord('`')+1)] +\
          [chr(symbol) for symbol in range(ord('{'), ord('~')+1)]
numbers = list(range(10))
generate = False
password = ""

layout = [[sg.Text('Input the length of the password:'),
           sg.Input(key='LENGTH', size=(10, 1), justification='center')],
    [sg.Radio('Letters', 'TOP', default=True, key='LETTERS'),
     sg.Radio('Numbers', 'TOP', key='NUMBERS'),
     sg.Radio('Symbols', 'TOP', key='SYMBOLS'),
     sg.Radio('Combination', 'TOP', key='COMBINATION')],
    [sg.Radio('Both Upper/Lower', 'BOT', default=True, key='BOTHUPPERLOWER'),
     sg.Radio('Only Upper', 'BOT', key='ONLYUPPER'),
     sg.Radio('Only Lower', 'BOT', key='ONLYLOWER')],
    [sg.Button('Generate', bind_return_key=True)],
    [sg.Text('Password:'),
     sg.Input(key="PASSWORD", size=(30, 1)),
     sg.Button('Copy', size=(5, 1), bind_return_key=True)]]

window = sg.Window('Simple Password Generator', layout, size=(400, 160), element_justification='c', finalize=True)
window.set_icon('icon.ico')

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


window.close()
