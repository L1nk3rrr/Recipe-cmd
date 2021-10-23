from Setting import *
from Ingedients import *
from Recipe import *
from Measure import *
def main_menu():
    while True:
        os.system('cls')
        print('\n ===========[ MAIN MENU ]=============')
        print(' -------------------------------------')
        print('  1. Recipe Menu')
        print('  2. Ingredients Manager')
        print('  3. Measure Manager')
        print('  4. Setting')
        print('  9. Exit.')

        uinput = input('\n Select the required action:  ')
        if uinput == '1':
            recipes_menu()
        elif uinput == '2':
            ingredient_menu()
        elif uinput == '3':
            measure_menu()
        elif uinput == '4':
            setting_menu()
        elif uinput == '9':
            print('Ty for use my program!')
            return
        else:
            print('\n  You need to select from the menu..')

main_menu()



