from import_connection import *
def measure_menu():
    while True:
        os.system('cls')
        print('\n ===========[ INGREDIENT MENU ]=============')
        print(' -------------------------------------------')
        print(' 1. Show all Measure.')
        print(' 2. Add Measure.')
        print(' 3. Delete Measure. ')
        print(' 4. Edit Measure')
        print(' 9. Exit')
        uinp = input('\n Enter your Selection: ')

        if uinp == '1':
            show_measure()
        elif uinp == '2':
            add_measure()
        elif uinp == '3':
            del_measure()
        elif uinp == '4':
            edit_measure()
        elif uinp == '9':
            return
        else:
            print('\n  Please select from the Menu.')

def show_measure():
    os.system('cls')
    print('\n ====== Show All Measure =====')
    print(' -----------------------------')
    c.execute('select * from measure where m_id > 0')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])

    input('\n   ..   Press any key .. ')
def add_measure():
    while True:
        os.system('cls')
        print('\n ====== Adding New Measure =====')
        print(' -------------------------------')
        print(' 1. Add basic Measures.(MUST BE SELECTED ONLY 1 TIME TO DB)')
        print(' 2. Add Measure.')
        uinp = input('Enter your Selection: ')
        if uinp == '1':
            mea_list = ["ML", "L", "GR", "KG", "Teaspoon", "Tablespoon","Cup","large","small","ounces"]
            for item in range(len(mea_list)):
                mea_name = mea_list[item].capitalize()
                c.execute("INSERT INTO measure (m_name) VALUES(:m_name)", {"m_name":mea_name})
                db_conn.commit()
            input('\n  ..Measures Added ..   Press any key .. ')
            break
        elif uinp =='2':
            mea_name = input('Enter an Measure you want to add: ').capitalize()
            c.execute("select * from measure where m_name = '{}'".format(mea_name))
            check = c.fetchone()
            if check:
                print("{} already in measure list with id {}.".format(check[1],check[0]))
            else:
                c.execute("INSERT INTO measure (m_name) VALUES(:m_name)", {"m_name":mea_name})
                db_conn.commit()
                input('\n  .. One Measure Added ..   Press any key .. ')
            break
        else:
            print('\n  Please select from the Menu.')



def del_measure():
    os.system('cls')
    print('\n ====== Delete an Measure =====')
    print(' ------------------------------')
    c.execute('select * from measure where m_id > 0')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])
    i = False
    while i == False:
        mea_del = input('  Enter an Ingredient ID to Delete: ')
        if mea_del.isnumeric() and int(mea_del) in range(1, each[0] + 1):
            i = True
        else:
            print('  You must Enter a Numeric Measure ID.')

    if mea_del:
        sure_remove = input(
            '\nPlease Note that if you Delete this Measure it will delete ingredient and value of measure from all recipes where used!.'
            '\nAre you sure you want to Remove it [Y,N] ')

        if sure_remove in ['y', 'Y']:
            c.execute("Delete from rec_ingredient where m_id = {}".format(mea_del))
            c.execute("Delete from measure where m_id = {}".format(mea_del))
            db_conn.commit()
            input('\n  .. Measure Deleted ..   Press any key .. ')
        else:
            print('\n  You select NOT to remove the Measure.')
            input('\n  ..  Press any key .. ')


def edit_measure():
    os.system('cls')
    print('\n ====== Edit an Measure =====')
    print(' ----------------------------')
    print('List of Measures:\n')

    c.execute('select * from measure where m_id > 0')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])
    i = False
    while i == False:
        mea_edit = input('\n  Enter an Measure ID to Change: ')
        if mea_edit.isnumeric() and int(mea_edit) in range(1, each[0] + 1):
            i = True
        else:
            print('  You must Enter a Measure ID.')

    if mea_edit:
        c.execute('select m_name from measure where m_id  = {}'.format(mea_edit))
        print('  You select to change the: ', c.fetchall())
        new_mea = input('\n  Enter the New Update for it: ')

        c.execute("update measure set m_name = '{}' where m_id  = {}".format(new_mea.capitalize(), int(mea_edit)))
        db_conn.commit()
        input('\n   .. Measure Updated ..   Press any key .. ')
