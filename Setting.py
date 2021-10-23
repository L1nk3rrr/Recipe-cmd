from import_connection import *
def setting_menu():
    while True:
        os.system('cls')
        print('\n ===========[ SETTING MENU ]=============')
        print(' ----------------------------------------')
        print(' 1. Create the needed Tables.')
        print(' 2. Drop Tables. ')
        print(' 3. Insert Dummy Data. (MUST be run One-Time after Tables Creation)')
        print(' 9. Exit')
        uinp = input('\n Enter your Selection: ')

        if uinp == '1':
            create_tables_()
        elif uinp == '2':
            drop_table()
        elif uinp == '3':
            insert_rec_0()
        elif uinp == '9':
            return
        else:
            print('\n  Please select from the Menu.')


def create_tables_():  # to create tables.

    sql_recipes = "CREATE TABLE IF NOT EXISTS recipes (r_id INTEGER PRIMARY KEY AUTOINCREMENT, r_name text, r_date text, r_type text, r_details text, r_tags text )"

    sql_photo = "CREATE TABLE IF NOT EXISTS photo (p_id INTEGER PRIMARY KEY AUTOINCREMENT ,r_id integer , p_name text, p_file BLOB)"

    sql_ingredients_list = "CREATE TABLE IF NOT EXISTS ingredients_list (i_l_id INTEGER PRIMARY KEY AUTOINCREMENT, i_name text )"

    sql_rec_ingredient = "CREATE TABLE IF NOT EXISTS rec_ingredient (ing_id INTEGER PRIMARY KEY AUTOINCREMENT, i_l_id integer, r_id integer, m_val text, m_id integer)"

    sql_recipes_steps = "CREATE TABLE if not exists recipes_steps(st_id INTEGER PRIMARY KEY AUTOINCREMENT, r_id integer, rec_steps text )"

    sql_measure = "CREATE TABLE if not exists measure(m_id INTEGER PRIMARY KEY AUTOINCREMENT, m_name text )"

    c.execute(sql_measure)
    db_conn.commit()

    c.execute(sql_recipes_steps)
    db_conn.commit()

    c.execute(sql_recipes)
    db_conn.commit()

    c.execute(sql_photo)
    db_conn.commit()

    c.execute(sql_ingredients_list)
    db_conn.commit()

    c.execute(sql_rec_ingredient)
    db_conn.commit()

    input('\n   .. Cooking  Tables created..  Press any key .. ')


def drop_table():
    try:
        # First we will print-out the list of Tables.
        c.execute("SELECT name FROM sqlite_master  WHERE type = 'table'")
        db_tables = []
        for each in c.fetchall():
            for t in each:
                db_tables.append(t)
        print('\n  Table List .. ')
        for x in range(len(db_tables)):
            print((x + 1), db_tables[x])
        t = int(input('\n  Enter the number next to Table you want to Drop:  '))
        c.execute("DROP TABLE {}".format(db_tables[t - 1]))
        db_conn.commit()
        print('\n ... One Table been Dropped')

    except:
        print('\n  No Tables with this name .. ')

    input('\n  . . . Press any key  . . ')


def insert_rec_0():
    c.execute("INSERT INTO recipes (r_id) VALUES(:r_id)", {"r_id": 0})

    c.execute("INSERT INTO ingredients_list (i_l_id) VALUES(:i_l_id)", {"i_l_id": 0})

    c.execute("INSERT INTO rec_ingredient (ing_id) VALUES(:ing_id)", {"ing_id": 0})

    c.execute("INSERT INTO photo (p_id) VALUES(:p_id)", {"p_id": 0})

    c.execute("INSERT INTO recipes_steps(st_id) VALUES(:st_id)", {"st_id": 0})

    c.execute("INSERT INTO measure(m_id) VALUES(:m_id)", {"m_id": 0})

    db_conn.commit()

    input('\n ...Dummy records been Inserted ....  Press any key  .. ')

