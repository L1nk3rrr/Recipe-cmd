from import_connection import *


def recipes_menu():
    while True:
        os.system("cls")
        print('\n ===========[ RECIPES MENU ]=============')
        print('  --------------------------------------')
        print(' 1. Show Recipes.')
        print(' 2. Add Recipe.')
        print(' 3. Delete Recipe. ')
        print(' 4. Edit Recipe.')
        print(' 9. Exit')
        uinp = input('\n Enter your Selection: ')

        if uinp == '1':
            show_recipes()
        elif uinp == '2':
            add_recipe()
        elif uinp == '3':
            del_recipe()
        elif uinp == '4':
            edit_recipe()
        elif uinp == '9':
            return
        else:
            print('\n  Please select from the Menu.')


def show_recipes():
    while True:
        os.system('cls')
        print('\n ===========[ Show Recipes ]=============')
        print(' ----------------------------------------')
        print(' 1. Show All Recipes.')
        print(' 2. Show Recipes By Date. ')
        print(' 3. Show Recipes By Ingredients.')
        print(' 4. Show Recipes By Tags.(wait for gui)')
        print(' 5. Show Recipes By Name (detailed).')
        print(' 6. Show Recipes By Type.')
        print(' 9. Exit')
        uinp = input('\n Enter your Selection: ')

        if uinp == '1':
            show_all_rec('all')
        elif uinp == '2':
            show_all_rec('date')
        elif uinp == '3':
            show_all_rec('ing')
        elif uinp == '4':
            show_all_rec('tag')
        elif uinp == '5':
            show_all_rec('name')
        elif uinp == '6':
            show_all_rec('type')
        elif uinp == '9':
            return
        else:
            print('\n  Please select from the Menu.')


def add_recipe():
    os.system('cls')
    print('\n ====== Adding New Recipe =====')
    print(' ------------------------------')
    print('\n First let''s Enter some Information about the Recipe..')
    r_name = input('  Enter The Recipe Name: ').capitalize()
    r_date = input('  Enter The Date in dd.mm.yyyy format: ')
    # Now to select the Recipe Type.
    print('\nA Recipe Type can be:\n  1.Breakfast.\n  2.Dinner.\n  3.Lunch.\n  4.Snack.\n  5.Sweet.')
    r_type = False
    while r_type == False:
        rec_type = input('  Select a Type [1,2,3,4,5]: ')
        if rec_type == '1':
            rec_type = 'Breakfast'
            r_type = True
        elif rec_type == '2':
            rec_type = 'Dinner'
            r_type = True
        elif rec_type == '3':
            rec_type = 'Lunch'
            r_type = True
        elif rec_type == '4':
            rec_type = 'Snack'
            r_type = True
        elif rec_type == '5':
            rec_type = 'Sweet'
            r_type = True
        else:
            print('\n  You have to select from the List')
    r_details = input('\nEnter Short information for the Recipe, like\n  Timefor cooking,\n  Country of this Meal,\n  Other short details.\n[USE (, ) to SEPARATE EACH INFO]\n\nENTER here: ')
    c.execute("INSERT INTO recipes (r_name, r_date, r_type, r_details ) VALUES(:r_name,:r_date,:r_type,:r_details)",
              {"r_name": r_name, "r_date": r_date, "r_type": rec_type, "r_details": r_details})
    db_conn.commit()

    c.execute("SELECT max(r_id) from recipes")
    rec_max = c.fetchall()[0][0]

    os.system("cls")

    # Select the Ingredient for the Recipe.
    print('\n  Now, Select the Ingredients of your Recipe:')
    print(
        "\nIf the Ingredient is not in the List you will Add it shortly.\nFIRST select the exist ones write it's ID Separated by ( , ) ")
    print('List of Ingredients:\n')
    c.execute('select * from ingredients_list where i_l_id > 0 order by i_name')
    for each in c.fetchall():
        print('  ', each[0], '....', each[1])
    ing_l = input('  Enter the Ingredients ID Seperated by ( , ) ')
    Yn = input('\n  Is there any more Ingredients you want to add? [Y,N]: ')
    i = False
    while i == False:
        if Yn in ['y', 'Y']:
            new_ing = input('\n  Enter the Ingdredients Separeted by ( , ):')
            new_ing = new_ing.split(",")
            # To get max ingredients ID.
            c.execute("SELECT max(i_l_id) from ingredients_list")
            max_ing_id = c.fetchall()[0][0]
            ing_l2 = []
            for each in range(len(new_ing)):
                c.execute("INSERT INTO ingredients_list (i_name) VALUES(:i_name)",
                          {"i_name": new_ing[each].capitalize()})
                db_conn.commit()
                ing_l2.append(str(max_ing_id + (each + 1)))
            ing_l = ing_l.split(",")
            ing_l2 = ing_l + ing_l2

            # To add the ingredients list
            print("\nNow you can see a measure for your ingredients")
            c.execute('select * from measure where m_id > 0')
            for each_basic in c.fetchall():
                print('  ', each_basic[0], '....', each_basic[1])
            for each in range(len(ing_l2)):
                i = False
                while i == False:
                    c.execute('select i_name from ingredients_list where i_l_id  = {}'.format(ing_l2[each]))
                    print("Now please select ID measure for {} :".format(c.fetchall()), end='')
                    meas = input()
                    v_meas = input("Please write a value of measure:")
                    if meas.isnumeric() and int(meas) in range(1, each_basic[0] + 1):
                        i = True
                c.execute("INSERT INTO rec_ingredient (i_l_id,r_id,m_val,m_id) VALUES(:i_l_id, :r_id, :m_val, :m_id)",
                          {"i_l_id": ing_l2[each], "r_id": rec_max, "m_val": v_meas, "m_id": meas})
                db_conn.commit()
            break
        elif Yn in ['n', 'N']:
            ing_l = ing_l.split(",")
            print("\nNow you can see a measure for your ingredients")
            c.execute('select * from measure where m_id > 0')
            for each_basic in c.fetchall():
                print('  ', each_basic[0], '....', each_basic[1])
            for each in range(len(ing_l)):
                i = False
                while i == False:
                    c.execute('select i_name from ingredients_list where i_l_id  = {}'.format(ing_l[each]))
                    print("Now please select ID measure for {} :".format(c.fetchall()),end = '')
                    meas = input()
                    v_meas = input("Please write a value of measure:")
                    if meas.isnumeric() and int(meas) in range(1, each_basic[0] + 1):
                        i = True
                c.execute("INSERT INTO rec_ingredient (i_l_id,r_id,m_val,m_id) VALUES(:i_l_id, :r_id, :m_val, :m_id)",
                          {"i_l_id": ing_l[each], "r_id": rec_max, "m_val": v_meas, "m_id": meas})
                db_conn.commit()
            break
        else:
            Yn = input('\n Is there any more Ingredients you want to add? [Y,N]: ')
    print('\nNow we can write the Cooking Steps, Press Enter After each Step.\nWhen you finish just enter (q).')
    stop = False
    while stop == False:
        c_step = input('Enter a Cooking Step:\n[Press ENTER after each step, q or Q to Finish]:\nWrite here:')
        if c_step not in ['q', 'Q']:
            c.execute("INSERT INTO recipes_steps(r_id, rec_steps) VALUES(:r_id, :rec_steps)",
                      {"r_id": rec_max, "rec_steps": c_step})
            db_conn.commit()
        else:
            stop = True
    image = input('\nYou want to add image?[Y:N]:')
    if image in ['y', 'Y']:
        image_name = input('Write please image name\n[EXAMPLE:картинка.png].\nWrite:')
        with open(image_name, 'rb') as f:
            data = f.read()
        c.execute("INSERT INTO photo (r_id, p_name,p_file) VALUES(?,?,?)", (rec_max, image_name, data))
        db_conn.commit()
    input('\n   .. One Recipe Added ..   Press any key .. ')


def edit_recipe():
    os.system('cls')
    print('\n ====== Edit Recipe =====')
    print(' --------------------')
    print('List of Recipes:\n')

    c.execute("select r_id,r_name from recipes where r_id > 0")
    i = False
    count = 1
    while i == False:
        for each_r_name in c.fetchall():
            print('   ID:', each_r_name[0], 'Name:', each_r_name[1])
            count += 1
        rec_edit = input('\n  Enter Recipe ID you want to Change: ')
        if rec_edit.isnumeric() and int(rec_edit) in range(1, count + 1):
            i = True

    if rec_edit:
        i = False
        while i == False:
            c.execute("select * from recipes where r_id ={}".format(rec_edit))
            for each_basic in c.fetchall():
                print('\n    ID: ', each_basic[0])
                print('1.  Name: ', each_basic[1])
                print('2.  Date: ', each_basic[2])
                print('3.  Type: ', each_basic[3])
                print('4. Other: ', each_basic[4])
            # Get all Recipe Ingredients.
            print('5. Recipe Ingredient:')
            get_sql = '''select i_name from ingredients_list INNER JOIN rec_ingredient ON ingredients_list.i_l_id = rec_ingredient.i_l_id where rec_ingredient.r_id = {}'''
            c.execute(get_sql.format(each_basic[0]))
            prinname = []
            prinvalue = []
            prinmeasure = []
            st = 1
            for each in c.fetchall():
                prinname.append(each[0])
            get_sql2 = '''select m_name from measure INNER JOIN rec_ingredient ON measure.m_id = rec_ingredient.m_id where rec_ingredient.r_id = {}'''
            c.execute(get_sql2.format(each_basic[0]))
            for each in c.fetchall():
                prinmeasure.append(each[0])
            c.execute('select m_val from rec_ingredient where r_id={}'.format(each_basic[0]))
            for each in c.fetchall():
                prinvalue.append(each[0])
            st = 1
            for i, j, z in zip(prinname, prinvalue, prinmeasure):
                print('  ', st, ': ', i, '', j, z)
                st = st + 1
            print('6. Cooking Steps:')
            c.execute("select * from recipes_steps where r_id = {}".format(each_basic[0]))
            print()
            st = 1
            for each in c.fetchall():
                print('Step-', st, ':', each[2])
                st = st + 1
            print('7. Photo:')
            c.execute("select p_name,p_file from photo where r_id = {}".format(each_basic[0]))
            result = c.fetchall()
            if int(len(result)) != 0:
                for x in result:
                    name = x[0]
                    data = x[1]
                with open(name, 'wb') as f:
                    f.write(data)
            else:
                print('no photo')
            print(' - - - - - - - - - - - - - - - - - - -')
            new_rec_item = input('\nPlease select the item which you want to update [1-7]: ')
            if new_rec_item.isnumeric() and int(new_rec_item) in range(1, 8):
                i = True
        ##############
        # EDITING NAME#
        ##############
        if new_rec_item == '1':
            new_rec = input('\n  Enter the New Update for it: ')
            c.execute("update recipes set r_name = '{}' where r_id  = {}".format(new_rec.capitalize(), int(rec_edit)))
            db_conn.commit()
            input('\n   .. Name Updated ..   Press any key .. ')
        ##############
        # EDITING DATE#
        ##############
        elif new_rec_item == '2':
            new_rec = input('\n  Enter the New Update for it: ')
            c.execute("update recipes set r_date = '{}' where r_id  = {}".format(new_rec, int(rec_edit)))
            db_conn.commit()
            input('\n   .. Date Updated ..   Press any key .. ')
        ##############
        # EDITING TYPE#
        ##############
        elif new_rec_item == '3':
            print('\nA Recipe Type can be:\n 1.Breakfast.\n 2.Dinner.\n 3.Lunch.\n 4.Snack.\n 5.Sweet.')
            r_type = False
            while r_type == False:
                new_rec = input('\n  Enter the New Update for it [1-5]: ')
                if new_rec == '1':
                    new_rec = 'Breakfast'
                    r_type = True
                elif new_rec == '2':
                    new_rec = 'Dinner'
                    r_type = True
                elif new_rec == '3':
                    new_rec = 'Lunch'
                    r_type = True
                elif new_rec == '4':
                    new_rec = 'Snack'
                    r_type = True
                elif new_rec == '5':
                    new_rec = 'Sweet'
                    r_type = True
                else:
                    print('\n  You have to select from the List')
            c.execute("update recipes set r_type = '{}' where r_id  = {}".format(new_rec, int(rec_edit)))
            db_conn.commit()
            input('\n  .. Type Updated ..   Press any key .. ')
        #################
        # EDITING DETAILS#
        #################
        elif new_rec_item == '4':
            new_rec = input('Enter Short information for the Recipe, like: \nTimefor cooking,\nCountry of this Meal,\
    \nOther short details.\n[USE (, ) to SEPARATE EACH INFO]\n\nENTER here: ')
            c.execute("update recipes set r_details = '{}' where r_id  = {}".format(new_rec, int(rec_edit)))
            db_conn.commit()
            input('\n  .. Details Updated ..   Press any key .. ')

        #####################
        # EDITING INGREDIENTS#
        #####################
        elif new_rec_item == '5':
            c.execute("Delete  from rec_ingredient where r_id = {}".format(rec_edit))
            db_conn.commit()
            print('\n Now, Select the Ingredients of your Recipe:')
            print(
                "\nIf the Ingredient is not in the List you will Add it shortly, FIRST select the exist ones \nwrite it's ID Separated by ( , ) ")
            print('List of Ingredients:\n')
            c.execute('select * from ingredients_list where i_l_id > 0 order by i_name')
            for each in c.fetchall():
                print('  ', each[0], '....', each[1])
            ing_l = input('\n  Enter the Ingredients ID Seperated by ( , ) ')
            Yn = input('\n  Is there any more Ingredients you want to add? [Y,N]: ')
            i = False
            while i == False:
                if Yn in ['y', 'Y']:
                    new_ing = input('\n  Enter the Ingdredients Separeted by ( , ):')
                    new_ing = new_ing.split(",")
                    # To get max ingredients ID.
                    c.execute("SELECT max(i_l_id) from ingredients_list")
                    max_ing_id = c.fetchall()[0][0]
                    ing_l2 = []
                    for each in range(len(new_ing)):
                        c.execute("INSERT INTO ingredients_list (i_name) VALUES(:i_name)",
                                  {"i_name": new_ing[each].capitalize()})
                        db_conn.commit()
                        ing_l2.append(str(max_ing_id + (each + 1)))
                    ing_l = ing_l.split(",")
                    ing_l2 = ing_l + ing_l2

                    # To add the ingredients list
                    print("Now you can see a measure for your ingredients")
                    c.execute('select * from measure where m_id > 0')
                    for each_basic in c.fetchall():
                        print('  ', each_basic[0], '....', each_basic[1])
                    for each in range(len(ing_l2)):
                        i = False
                        while i == False:
                            c.execute('select m_name from measure where m_id  = {}'.format(ing_l2[each]))
                            meas = input("Now please select ID measure for {} :".format(c.fetchall()))
                            v_meas = input("  Please write a value of measure:")
                            if meas.isnumeric() and v_meas.isnumeric() and int(meas) in range(1, each_basic[0] + 1):
                                i = True
                        c.execute(
                            "INSERT INTO rec_ingredient (i_l_id,r_id,m_val,m_id) VALUES(:i_l_id, :r_id, :m_val, :m_id)",
                            {"i_l_id": ing_l2[each], "r_id": rec_edit, "m_val": v_meas, "m_id": meas})
                        db_conn.commit()
                    break
                elif Yn in ['n', 'N']:
                    ing_l = ing_l.split(",")
                    print("Now you can see a measure for your ingredients")
                    c.execute('select * from measure where m_id > 0')
                    for each_basic in c.fetchall():
                        print('  ', each_basic[0], '....', each_basic[1])
                    for each in range(len(ing_l)):
                        i = False
                        while i == False:
                            c.execute('select m_name from measure where m_id  = {}'.format(ing_l[each]))
                            meas = input("  Now please select ID measure for {} :".format(c.fetchall()))
                            v_meas = input("  Please write a value of measure:")
                            if meas.isnumeric() and v_meas.isnumeric() and int(meas) in range(1, each_basic[0] + 1):
                                i = True
                        c.execute(
                            "INSERT INTO rec_ingredient (i_l_id,r_id,m_val,m_id) VALUES(:i_l_id, :r_id, :m_val, :m_id)",
                            {"i_l_id": ing_l[each], "r_id": rec_edit, "m_val": v_meas, "m_id": meas})
                        db_conn.commit()
                    break
                else:
                    Yn = input('PLEASE Y(y) or N(n):')
            input('\n  .. Ingredients Updated ..   Press any key .. ')
        ################
        # EDITING STEPS#
        ################
        elif new_rec_item == '6':
            c.execute("Delete  from recipes_steps where r_id = {}".format(rec_edit))
            db_conn.commit()
            print(
                '\nNow we can write the Cooking Steps, Press Enter After each Step.\nWhen you finish just enter (q).')
            stop = False
            while stop == False:
                c_step = input('\n  Enter a Cooking Step:')
                if c_step not in ['q', 'Q']:
                    c.execute("INSERT INTO recipes_steps(r_id, rec_steps) VALUES(:r_id, :rec_steps)",
                              {"r_id": rec_edit, "rec_steps": c_step})
                    db_conn.commit()
                else:
                    stop = True
            input('\n  .. Steps Updated ..   Press any key .. ')
        ################
        # EDITING PHOTO#
        ################
        elif new_rec_item == '7':
            image_name = input('Write please image name\n[EXAMPLE:картинка.png].\nWrite:')
            c.execute("Delete  from photo where r_id = {}".format(rec_edit))
            with open(image_name, 'rb') as f:
                data = f.read()
            c.execute("INSERT INTO photo (r_id, p_name,p_file) VALUES(?,?,?)", (rec_edit, image_name, data))
            db_conn.commit()
            input('\n  .. Photo Updated ..   Press any key .. ')
        else:
            print('  .. All is done ..   Press any key .. ')


def del_recipe():
    os.system("cls")
    print('\n ====== Delete a Recipe =====')
    print(' ----------------------------')
    # Start to list down all the Recipes Name.
    print("List of ALL Recipes we have.\n")
    c.execute("select r_id,r_name from recipes where r_id > 0")
    for each_r_name in c.fetchall():
        print('   ID:', each_r_name[0], 'Name:', each_r_name[1])
    # Now we ask the user to Enter the Recipe ID.
    rec_del = input('\n  Enter an Recipe ID to be Deleted: ')
    # Now we ask the user to Confirm Deleting Recipe.
    sure_remove = input(
        '\nThe Recipe will be DELETE and can''t be Rolled-Back.Are you sure you want to Remove it [Y,N]:')
    if sure_remove in ['y', 'Y']:
        c.execute("Delete  from recipes_steps where r_id = {}".format(rec_del))
        db_conn.commit()
        c.execute("Delete  from recipes where r_id = {}".format(rec_del))
        db_conn.commit()
        c.execute("Delete  from rec_ingredient where r_id = {}".format(rec_del))
        db_conn.commit()
        c.execute("Delete  from photo where r_id = {}".format(rec_del))
        db_conn.commit()
    elif sure_remove in ['n', 'N']:  # If the user decide not to delete and select N
        print('\n  You select NOT to remove the Recipe.')
    else:  # If the user enter anything else than Y or N
        print('\n  You must select (Y or N).')
    input('\n  .. One Recipe Removed ..   Press any key .. ')


def show_all_rec(opt):
    os.system('clr')
    print('\n============ Show Recipes ===========')
    print('-------------------------------------')
    if opt == 'all':
        c.execute("select * from recipes where r_id > 0")
        for each in c.fetchall():
            print('\n   ID: ', each[0])
            print('   Name: ', each[1])
            print('   Date: ', each[2])
            print('   Type: ', each[3])
            print('  Other: ', each[4])
            print(' - - - - - - - - - - - - - - - - - - -')
    elif opt == "date":
        rdate = input('\n  Enter the date in dd.mm.yyyy:')
        c.execute("select * from recipes where r_date = {}".format(rdate))
        for each in c.fetchall():
            print('\n   ID: ', each[0])
            print('   Name: ', each[1])
            print('   Date: ', each[2])
            print('   Type: ', each[3])
            print('  Other: ', each[4])
            print(' - - - - - - - - - - - - - - - - - - -')

    elif opt == "ing":
        c.execute('select * from ingredients_list where i_l_id > 0')
        for each in c.fetchall():
            print('  ', each[0], '....', each[1])
        ring = input('\n  Enter the Ingredient ID:')
        c.execute("SELECT r_id from rec_ingredient where i_l_id = {}".format(ring))
        for basic_id in c.fetchall():
            c.execute("select * from recipes where r_id = {}".format(basic_id[0]))
            for each in c.fetchall():
                print('\n   ID: ', each[0])
                print('   Name: ', each[1])
                print('   Date: ', each[2])
                print('   Type: ', each[3])
                print('  Other: ', each[4])
                print(' - - - - - - - - - - - - - - - - - - -')
    elif opt == "tag":
        print('Waiting for gui')
    elif opt == "name":
        # First we will list down all Recipes Names.
        c.execute("select r_id,r_name from recipes where r_id > 0")
        for each_r_name in c.fetchall():
            print(' ID:', each_r_name[0], ' Name:', each_r_name[1])
        get_rec_id = input('\n  Enter the Recipe ID you want to read: ')
        # Get the Recipe information based on ID.
        c.execute("select * from recipes where r_id ={}".format(get_rec_id))
        for each_basic in c.fetchall():
            print('\n  ID: ', each_basic[0])
            print('  Name: ', each_basic[1])
            print('  Date: ', each_basic[2])
            print('  Type: ', each_basic[3])
            print('  Other: ', each_basic[4])

            print('\n  The Recipe Ingredients: ')
            # Get all Recipe Ingredients.
            get_sql = '''select i_name from ingredients_list INNER JOIN rec_ingredient ON ingredients_list.i_l_id = rec_ingredient.i_l_id where rec_ingredient.r_id = {}'''
            c.execute(get_sql.format(each_basic[0]))
            # st = 1
            # for each in c.fetchall():
            #     print('  ', st, ': ', each[0])
            #     st = st + 1
            prinname = []
            prinvalue = []
            prinmeasure = []
            st = 1
            for each in c.fetchall():
                prinname.append(each[0])
            get_sql2 = '''select m_name from measure INNER JOIN rec_ingredient ON measure.m_id = rec_ingredient.m_id where rec_ingredient.r_id = {}'''
            c.execute(get_sql2.format(each_basic[0]))
            for each in c.fetchall():
                prinmeasure.append(each[0])
            c.execute('select m_val from rec_ingredient where r_id={}'.format(each_basic[0]))
            for each in c.fetchall():
                prinvalue.append(each[0])
            st = 1
            for i,j,z in zip(prinname,prinvalue,prinmeasure):
                print('  ', st, ': ', i,'',j,z)
                st = st + 1
            print('\n\n  Cooking Steps: ')
            # Get the Cooking Steps.
            c.execute("select * from recipes_steps where recipes_steps.r_id = {}".format(each_basic[0]))
            st = 1
            for each in c.fetchall():
                print('\n    Step-', st, ': ', each[2])
                st = st + 1
            # Get photo
            c.execute("select p_name,p_file from photo where r_id = {}".format(each_basic[0]))
            result = c.fetchall()
            if int(len(result)) != 0:
                for x in result:
                    name = x[0]
                    data = x[1]
                with open(name, 'wb') as f:
                    f.write(data)
            else:
                print('no photo')

            print('\n ---------------------------------------------')
    elif opt == "type":
        r_type = False
        print('\n  A Recipe Type can be:\n1.Breakfast.\n2.Dinner.\n3.Lunch.\n4.Snack.\n5.Sweet.')
        while r_type == False:
            rec_type = input('   Select a Type [1,2,3,4,5]: ')
            if rec_type == '1':
                rec_type = 'Breakfast'
                r_type = True
            elif rec_type == '2':
                rec_type = 'Dinner'
                r_type = True
            elif rec_type == '3':
                rec_type = 'Lunch'
                r_type = True
            elif rec_type == '4':
                rec_type = 'Snack'
                r_type = True
            elif rec_type == '5':
                rec_type = 'Sweet'
                r_type = True
            else:
                print('\n   You have to select from the List')
        c.execute("select * from recipes where r_type = '{}'".format(rec_type))
        for each in c.fetchall():
            print('\n   ID: ', each[0])
            print('   Name: ', each[1])
            print('   Date: ', each[2])
            print('   Type: ', each[3])
            print('  Other: ', each[4])
            print(' - - - - - - - - - - - - - - - - - - -')
    input('\n  .. Press any key .. ')
