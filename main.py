
import oracledb
from my_exceptions import *
from enum import Enum

oracledb.init_oracle_client(lib_dir="instantclient_19_8")


class Status(Enum):
    DO_ZROBIENIA = 1
    W_TRAKCIE = 2
    ZAKONCZONE = 3

def add_task():
    name = input('Podaj nazwę: ')
    description = input('Podaj opis: ')
    priority = int(input('Podaj priorytet (1-5): '))
    if priority not in range(1, 6):
        raise InvalidInputException("Liczba powinna być w zakresie 1-5")

    cur.execute("SELECT MAX(id) FROM todo_list")
    max = cur.fetchone()[0]

    query = "INSERT INTO todo_list (id, name, description, creating_date, status, task_priority) VALUES ({0}, '{1}', '{2}', current_timestamp, '{3}', {4})".format(max + 1, name, description, Status.DO_ZROBIENIA.name, priority)
    cur.execute(query)
    con.commit()
    print('Utworzono zadanie o id ', max+1)

def delete_task():
    try:
        task = input('Podaj id zadania do usunięcia: ')
        query = "DELETE FROM todo_list WHERE id = '{0}'".format(task)
        cur.execute(query)
        con.commit()
    except IndentationError:
        print('Nie udało się usunąć zadania. Zweryfikuj poprawność identyfikatora')

def show_tasks():
    print('\n1. Wyświetl wszystkie')
    print('2. Friltruj po statusie')
    print('3. Z sortowaniem')
    print('4. Wyjście')

    try:
        choice = int(input('\nWybierz opcję: '))
    except:
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")

    if choice not in range(5):
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")

    if choice == 1:
        show_all()
    elif choice == 2:
        filter()
    elif choice == 3:
        sort()
    elif choice == 4:
        pass

def filter():
    print('1. DO_ZROBIENIA')
    print('2. W_TRAKCIE')
    print('3. ZAKONCZONE')

    try:
        choice = int(input('\nWybierz opcję: '))
    except:
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")

    if choice not in range(4):
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")

    if choice == 1:
        show_all(Status.DO_ZROBIENIA)
    elif choice == 2:
        show_all(Status.W_TRAKCIE)
    elif choice == 3:
        show_all(Status.ZAKONCZONE)
    else:
        print('Wybrano niepoprawną opcję')

def sort():
    print('1. ID')
    print('2. Tytuł')
    print('3. Opis')
    print('4. Data')
    print('5. Status')
    print('6. Priorytet')

    try:
        cat = int(input('Po czym chcesz sortować: '))
    except:
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")
    if cat not in range(1, 7):
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")

    if cat == 1:
        show_all()
    elif cat == 2:
        show_all(None, 'name')
    elif cat == 3:
        show_all(None, 'description')
    elif cat == 4:
        show_all(None, 'creating_date')
    elif cat == 5:
        show_all(None, 'status')
    elif cat == 6:
        show_all(None, 'task_priority')


def show_all(filter = None, sort = 'id'):
    query = "SELECT * FROM todo_list ORDER BY {0}".format(sort)
    cur.execute(query)
    records = cur.fetchall()
    print('ID,\t Tytuł,\t Opis, \tData, \tStatus, \tPriorytet')
    for i in records:   # print(records) #tablica toupli
        if filter is None or (isinstance(filter, Status) and i[4] == filter.name):
            formatted_date = i[3].strftime('%d-%m-%Y %H:%M:%S')
            formatted_record = (i[0], i[1], i[2], formatted_date, i[4], i[5])
            print(formatted_record)

def edit_task():
    show_all()
    id = input('Podaj id zadania do edycji: ')
    query = "SELECT * FROM todo_list WHERE id = {0}".format(id)
    cur.execute(query)
    id = cur.fetchone()[0]

    if id is None:
        print('Brak rekordu o takim id')
    else:
        print('\n1. Tytuł')
        print('2. Opis')
        print('3. Status')
        choice = int(input('\nPodaj które pole chcesz dytować: '))
        value = None
        if choice == 1:
            value = input('\nPodaj jaką wartość chcesz nadać: ')
            query = "UPDATE todo_list SET name = '{0}' WHERE id = {1}".format(value, id)
            print(query)
        elif choice == 2:
            value = input('\nPodaj jaką wartość chcesz nadać: ')
            query = "UPDATE todo_list SET description = '{0}' WHERE id = {1}".format(value, id)
        elif choice == 3:
            print('\n1. DO_ZROBIENIA')
            print('2. W_TRAKCIE')
            print('3. ZAKONCZONE')
            choice = int(input('\nWybierz status: '))
            for stat in Status:
                if stat.value == choice:  value = stat.name
                print(value)
            query = "UPDATE todo_list SET status = '{0}' WHERE id = {1}".format(value, id)
            print(query)
        cur.execute(query)
        con.commit()

def login():
    #Logowanie i łączenie z bazą
    connected = False
    global con
    global cur
    while connected == False:
        try:
            login = input('Podaj numer studenta (sXXXXX): ')

            con = oracledb.connect('{}/oracle12@db-oracle02.pjwstk.edu.pl:1521/baza.pjwstk.edu.pl'.format(login))
            cur = con.cursor()
            connected = True
        except:
            print('Nie udało połączyć się z bazą danych')
            connected = False

def menu():
    print('\n--- MENU ---')
    print('1. Wyświetlanie zadań')
    print('2. Nowe zadanie')
    print('3. Edytuj zadanie')
    print('4. Usuń zadanie')
    print('0. Wyjście')
    print('----------')

    try:
        choice = int(input('\nWybierz opcję: '))
    except:
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe")

    if choice not in range(5):
        raise InvalidInputException("Podano nieprawidłowe dane wejściowe") 
    
    while choice != 0:  # match case nie działa na interpreterze 3.9, a na 3.12 nie działa oracledb :((

        if choice == 1:
            show_tasks()
        elif choice == 2:
            print()
            add_task()
        elif choice == 3:
            edit_task()
        elif choice == 4:
            delete_task()
            print()
        elif choice == 0:
            break

        print('\n--- MENU ---')
        print('1. Wyświetlanie zadań')
        print('2. Nowe zadanie')
        print('3. Edytuj zadanie')
        print('4. Usuń zadanie')
        print('0. Wyjście')
        print('----------')
        
        choice = int(input('Wybierz opcję: '))

while True:
    try:
        login()
        break
    except DatabaseConnectionProblemException as e:
        print(e)

while True:
    try:
        menu()
        break
    except InvalidInputException as e:
        print(e)

cur.close()
con.close()
