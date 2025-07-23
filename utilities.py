import os
def clear_terminal(): #To clear the terminal
    if os.name == 'nt': # For Windows
        os.system('cls')
    else: #for Linux and macOS
        os.system('clear')