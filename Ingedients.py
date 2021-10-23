from import_connection import *
def ingredient_menu():
    while True:
        os.system('cls')
        print('\n ===========[ INGREDIENT MENU ]=============')
        print('  --------------------------------------')
        print(' 1. Show all Ingredient by name.')
        print(' 2. Show all Ingredient by ID.')
        print(' 3. Add Ingredient.')
        print(' 4. Delete Ingredient. ')
        print(' 5. Edit Ingredient')
        print(' 9. Exit')
        uinp = input('\n Enter your Selection: ')

        if uinp == '1':
            show_ingredient()
        elif uinp == '2':
            show_in()
        elif uinp == '3':
            add_ingredient()
        elif uinp == '4':
            del_ingredient()
        elif uinp == '5':
            edit_ingredient()
        elif uinp == '9':
            return
        else:
            print('\n  Please select from the Menu.')

def show_ingredient():
    os.system('cls')
    print('\n ====== Show All Ingredient =====')
    print(' --------------------------------')
    c.execute('select * from ingredients_list where i_l_id > 0 order by i_name')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])

    input('\n   ..   Press any key .. ')
def show_in():
    print('\n ====== Show All Ingredient =====')
    print(' --------------------------------')
    c.execute('select * from ingredients_list where i_l_id > 0')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])
    input('\n   ..   Press any key .. ')


def add_ingredient():
    while True:
        os.system('cls')
        print('\n ====== Adding New Ingredient =====')
        print(' ----------------------------------')
        print(' 1. Add basic ingredients.(MUST BE SELECTED ONLY 1 TIME TO DB)')
        print(' 2. Add Ingredient.')
        uinp = input('\n Enter your Selection: ')
        if uinp == '1':
            ing_list = ["Onion", "Spinach", "Mushroom", "Tomatoes", "Lime", "Turnip", "Snake Beans",
                        "Jalapeno", "Baking powder", "sugar", "Eggs", "Vanilla extract", "Salt", "Flour", "Butter",
                        "Oil", "Whole milk", "Orange juice", "Baking soda", "Ground cinnamon", "Dark chocolate",
                        "Cocoa", "Cherry", "Cherry jam"]
            for item in range(len(ing_list)):
                ing_name = ing_list[item].capitalize()
                c.execute("INSERT INTO ingredients_list (i_name) VALUES(:i_name)", {"i_name": ing_name})
                db_conn.commit()
            input('\n   .. Ingredients Added ..   Press any key .. ')
            break
        elif uinp =='2':
            ing_name = input('\n\nEnter an Ingredient you want to add: ').capitalize()
            c.execute("select * from ingredients_list where i_name = '{}'".format(ing_name))
            check = c.fetchone()
            if check:
                print("{} already in ingredients list with id {}.".format(check[1],check[0]))
            else:
                c.execute("INSERT INTO ingredients_list (i_name) VALUES(:i_name)", {"i_name": ing_name})
                db_conn.commit()
                input('\n   .. One Ingredient Added ..   Press any key .. ')
            break
        else:
            print('\n  Please select from the Menu.')



def del_ingredient():
    os.system('cls')
    print('\n ====== Delete an Ingredient =====\n')
    print(' ------------------------------')
    c.execute('select * from ingredients_list where i_l_id > 0')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])
    i = False
    while i == False:
        ing_del = input('\n   Enter an Ingredient ID to Delete: ')
        if ing_del.isnumeric() and int(ing_del) in range(1,each[0]+1):
            i = True
        else:
            print('   You must Enter a Numeric Ingredient ID.')

    if ing_del:
        sure_remove = input(
            '\nPlease Note that if you Delete this Ingredient it will not show in any recipes that use it.'
            '\nAre you sure you want to Remove it [Y,N] ')

        if sure_remove in ['y', 'Y']:
            c.execute("Delete from ingredients_list where i_l_id = {}".format(ing_del))
            c.execute("Delete from rec_ingredient where i_l_id = {}".format(ing_del))
            db_conn.commit()
            input('\n   .. One Ingredient Deleted ..   Press any key .. ')
        else:
            print('\n You select NOT to remove the Ingredient.')
            input('\n   ..  Press any key .. ')


def edit_ingredient():
    os.system('cls')
    print('\n ====== Edit an Ingredient =====')
    print(' -------------------------------')
    print('List of Ingredients:\n')

    c.execute('select * from ingredients_list where i_l_id > 0')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])
    i = False
    while i == False:
        ing_edit = input('\n  Enter an Ingredient ID you want to Change: ')
        if ing_edit.isnumeric() and int(ing_edit) in range(1, each[0] + 1):
            i = True
        else:
            print('  You must Enter a Ingredient ID.')

    if ing_edit.isnumeric():
        c.execute('select i_name from ingredients_list where i_l_id  = {}'.format(ing_edit))
        print('  You select to change the: ', c.fetchall())
        new_ing = input('  Enter the New Update for it: ')

        c.execute("update ingredients_list set i_name = '{}' where i_l_id  = {}".format(new_ing.capitalize(), int(ing_edit)))
        db_conn.commit()
        input('\n  .. One Ingredient Updated ..   Press any key .. ')

