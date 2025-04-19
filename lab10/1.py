import psycopg2
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Дерекқорға қосылу
conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="kbtu.aza_007"
)
cur = conn.cursor()


# CSV-тен дерек енгізу
def insert_from_csv(contacts):
    try:
        with open(contacts, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
        conn.commit()
        print("CSV файлдан деректер енгізілді.")
    except Exception as e:
        print("Қате:", e)


# Консоль арқылы дерек енгізу
def insert_from_console():
    name = input("Атыңызды енгізіңіз: ")
    phone = input("Телефон нөмірін енгізіңіз: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Дерек енгізілді.")


# Деректі жаңарту
def update_data():
    field = input("Қай өрісті өзгертесіз (name/phone): ").lower()
    if field not in ['name', 'phone']:
        print("Қате өріс!")
        return

    old_value = input(f"Ескі {field}: ")
    new_value = input(f"Жаңа {field}: ")

    query = f"UPDATE phonebook SET {field} = %s WHERE {field} = %s"
    cur.execute(query, (new_value, old_value))
    conn.commit()
    print("Дерек жаңартылды.")


def query_data():
    print("Фильтрді таңдаңыз: name, phone немесе all")
    filt = input("Фильтр: ").lower()
    if filt == 'name':
        val = input("Атын енгізіңіз: ")
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (val,))
    elif filt == 'phone':
        val = input("Телефон нөмірін енгізіңіз: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (val,))
    elif filt == 'all':
        cur.execute("SELECT * FROM phonebook")
    else:
        print("Қате фильтр!")
        return

    results = cur.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("Дерек табылмады.")


def delete_by_name():
    name = input("Жою үшін пайдаланушы атын енгізіңіз: ")
    cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    conn.commit()
    print("Дерек жойылды.")


def menu():
    while True:
        print("\n--- Телефон кітапшасы ---")
        print("1. CSV-тен дерек енгізу")
        print("2. Консоль арқылы дерек енгізу")
        print("3. Деректі жаңарту")
        print("4. Деректі сұрау")
        print("5. Деректі жою")
        print("6. Шығу")

        choice = input("Таңдауыңыз: ")

        if choice == '1':
            insert_from_csv("contacts.csv")
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_by_name()
        elif choice == '6':
            print("Бағдарлама аяқталды.")
            break
        else:
            print("Қате таңдау!")


menu()

cur.close()
conn.close()
