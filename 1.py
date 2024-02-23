import psycopg2

def connect():
    conn = psycopg2.connect(database='Student', user='postgres', password='postgres', host='localhost', port='5432')
    return conn

def read(student_number):
    conn = connect()
    cur = conn.cursor()
    sql = 'SELECT * FROM student WHERE sno = %s'
    cur.execute(sql, (student_number,))
    info = cur.fetchall()
    cur.close()
    conn.close()

    return info

def insert(number, name, age, gender, department):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM student WHERE sno = %s", (number,))
        if cur.fetchone() is not None:
            print("Student number already exists. Please enter a different student number.\n")
            return
        cur.execute("INSERT INTO student (sno, sname, sage, sgender, sdept) VALUES (%s, %s, %s, %s, %s)",
                    (number, name, age, gender, department))
        conn.commit()
        print("New student information inserted successfully.\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def update():
    student_number = input("Enter student number: \n")
    info = read(student_number)
    if info:
        print("Current student information:")
        for row in info:
            print(row)
    else:
        print("No student found with the given student number.\n")
        return

    conn = connect()
    cur = conn.cursor()

    new_name = input("Enter new name: ")
    new_age = input("Enter new age: ")
    new_gender = input("Enter new gender: ")
    new_department_name = input("Enter new department name: ")
    cur.execute("UPDATE student SET sname = %s, sage = %s, sgender = %s, sdept = %s WHERE sno = %s",
                (new_name, new_age, new_gender, new_department_name, student_number))
    print("Student information updated successfully.\n")

    conn.commit()
    cur.close()
    conn.close()

    info = read(student_number)
    print("Updated student information:")
    for row in info:
        print(row)

def delete():
    conn = connect()
    cur = conn.cursor()
    student_number = input("Enter student number: \n")
    try:
        cur.execute("SELECT * FROM sc WHERE sno = %s", (student_number,))
        if cur.fetchone() is not None:
            print("Student cannot be deleted because they are enrolled in courses.\n")
            return
        cur.execute("DELETE FROM student WHERE sno = %s", (student_number,))
        conn.commit()
        print("Student deleted successfully. \n")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()



def menu():
    while True:
        print("\nMenu:")
        print("1. Read student information")
        print("2. Insert new student information")
        print("3. Update student information")
        print("4. Delete student information")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            read_student()
        elif choice == '2':
            insert_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def read_student():
    student_number = input("Enter student number: ")
    info = read(student_number)
    if info:
        for row in info:
            print(row)
            print(' ')
    else:
        print("No student found with the given student number.")

def insert_student():
    while True:
        number = input("Enter student number: ")
        info = read(number)
        if info:
            print("Student number already exists. Please enter a different student number.")
        else:
            name = input("Enter the student's name: ")
            age = int(input("Enter the student's age: "))
            gender = input("Enter the student's gender (F/M): ")
            department = input("Enter the student's department name: ")
            insert(number, name, age, gender, department)
            break

def update_student():
    update()

def delete_student():
    delete()

# 主程序开始
if __name__ == "__main__":
    menu()

