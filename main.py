import PySimpleGUI as sg
import random

letters = [chr(letter) for letter in range(ord('a'), ord('z')+1)] + [chr(letter) for letter in range(ord('A'), ord('Z')+1)]
numbers = list(range(10))
generate = False
password = ""

layout = [[sg.Text('Input the length of the password:'), sg.Input(key='LENGTH', size=(10, 1), justification='center')],
    [sg.Radio('Letters', 'RADIO1', default=True, key='LETTERS'),
     sg.Radio('Numbers', 'RADIO1', key='NUMBERS'),
     sg.Radio('Combination', 'RADIO1', key='COMBINATION')],
    [sg.Button('Generate', size=(10, 1), bind_return_key=True)],
    [sg.Text('Password:'), sg.Input(key="PASSWORD", size=(20, 1)), sg.Button('Copy', size=(5, 1), bind_return_key=True)]]

window = sg.Window('Password Generator', layout, size=(350, 125), element_justification='c', finalize=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Generate':
        length = values['LENGTH']
        if length.isdigit():
            length = int(length)
            if length <= 6:
                sg.popup('The input should be minimum of 7.\n', title='X')
            elif length >= 21:
                sg.popup('The input maximum is 20.\n', title='X')
            elif length in range(7, 21):
                generate = True
            else:
                pass
        else:
            sg.popup('The input is not an integer.', title='Error')
        if generate:
            for i in range(0, length):
                randomize = random.randint(0, 51)
                if values['LETTERS']:
                    password += letters[randomize]
                elif values['NUMBERS']:
                    randomize = random.randint(0, 9)
                    password += str(numbers[randomize])
                elif values['COMBINATION']:
                    crandomize = random.choice(['l', 'n'])
                    if crandomize == 'l':
                        password += letters[randomize]
                    elif crandomize == 'n':
                        randomize = random.randint(0, 9)
                        password += str(numbers[randomize])
                else:
                    pass

            window['PASSWORD'].update(password)
            generate = False
            password = ""
        else:
            pass

    elif event == 'Copy':
        sg.clipboard_set(values['PASSWORD'])
        sg.popup('Successfuly copied to clipboard.', title='/')


window.close()
