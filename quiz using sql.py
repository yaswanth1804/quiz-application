import mysql.connector
import time

conn = mysql.connector.connect(
    host='localhost',
    user='root',        
    password='yaswanth@4412',    
    database='quiz_app'
)
cursor = conn.cursor(dictionary=True)


def admin_login():
    admin_user = input('Enter admin username: ')
    admin_pass = input('Enter admin password: ')
    if admin_user == 'yaswanth' and admin_pass == 'yaswanth@123':  
        print('Admin login successful!\n')
        return True
    else:
        print('Invalid Admin credentials\n')
        return False



def add_technology():
    tech = input('Enter technology name: ').strip().lower()

    cursor.execute("SELECT * FROM technologies WHERE name=%s", (tech,))
    existing = cursor.fetchone()

    if existing:
        print("Technology already exists!")
        return

    cursor.execute("INSERT INTO technologies (name) VALUES (%s)", (tech,))
    conn.commit()
    print("Technology added successfully")



def add_question():
    tech = input('Enter technology name: ').strip().lower()
    cursor.execute('SELECT number FROM technologies WHERE name=%s', (tech,))
    row = cursor.fetchone()
    if not row:
        print('Technology not found')
        return
    tech_id = row['number']

    ques = input('Enter question: ')
    a = input('Option A: ')
    b = input('Option B: ')
    c = input('Option C: ')
    d = input('Option D: ')
    correct = input('Correct option (a/b/c/d): ').lower()

    cursor.execute('''
        INSERT INTO questions (technology_id, question, option_a, option_b, option_c, option_d, correct_option)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    ''', (tech_id, ques, a, b, c, d, correct))
    conn.commit()
    print('Question added successfully')


def modify_question():
    tech = input('Enter technology name: ').strip().lower()
    cursor.execute('SELECT number FROM technologies WHERE name=%s', (tech,))
    row = cursor.fetchone()
    if not row:
        print('Technology not found')
        return
    tech_id = row['number']

    cursor.execute('SELECT * FROM questions WHERE technology_id=%s', (tech_id,))
    questions= cursor.fetchall()
    if not questions:
        print('No questions found')
        return

    for q in questions:
        print(str(q['number']) + '. ' + q['question'])

    qid = input('Enter Question number to modify: ')
    cursor.execute('SELECT * FROM questions WHERE number=%s', (qid,))
    question = cursor.fetchone()
    if not question:
        print('Invalid Question number')
        return

    ques = input('Enter new question: ')
    a = input('Option A: ')
    b = input('Option B: ')
    c = input('Option C: ')
    d = input('Option D: ')
    correct = input('Correct option (a/b/c/d): ').lower()

    cursor.execute('''
        UPDATE questions SET question=%s, option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s
        WHERE number=%s
    ''', (ques, a, b, c, d, correct, qid))
    conn.commit()
    print('Question modified successfully')


def delete_question():
    tech = input('Enter technology name: ').strip().lower()
    cursor.execute('SELECT number FROM technologies WHERE name=%s', (tech,))
    row = cursor.fetchone()
    if not row:
        print('Technology not found')
        return
    tech_id = row['number']

    cursor.execute('SELECT * FROM questions WHERE technology_id=%s', (tech_id,))
    questions = cursor.fetchall()
    if not questions:
        print('No questions found')
        return

    for q in questions:
        print(str(q['number']) + '. ' + q['question'])

    qid = input('Enter Question number to delete: ')
    cursor.execute('DELETE FROM questions WHERE number=%s', (qid,))
    conn.commit()
    print('Question deleted successfully')

def view_questions():
    cursor.execute("SELECT number, name FROM technologies")
    techs = cursor.fetchall()

    if not techs:
        print("No technologies available.")
        return

    print("Available Technologies:")
    for t in techs:
        print(str(t['number']) + ". " + t['name'])
    tech_id = input("Enter technology number to view questions: ")
    cursor.execute("SELECT name FROM technologies WHERE number=%s", (tech_id,))
    tech = cursor.fetchone()

    if not tech:
        print("Invalid technology.")
        return

    cursor.execute("""
        SELECT number, question, option_a, option_b, option_c, option_d, correct_option
        FROM questions WHERE technology_id=%s
    """, (tech_id,))
    questions = cursor.fetchall()

    if not questions:
        print("No questions present in this technology.")
        return

    print("Questions for " + tech['name'] + ":\n")
    for q in questions:
        print("Q" + str(q['number']) + ". " + q['question'])
        print("   A) " + str(q['option_a']))
        print("   B) " + str(q['option_b']))
        print("   C) " + str(q['option_c']))
        print("   D) " + str(q['option_d']))
        print("  Correct Answer: " + q['correct_option'])
def view_technologies():
    cursor.execute('SELECT * FROM technologies')
    rows = cursor.fetchall()
    for t in rows:
        print('- ' + t['name'])


def view_users_and_scores():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print('Users:')
    for u in users:
        print(u['username'] + ' | ' + u['mobile'])
   
    cursor.execute('SELECT * FROM scores')
    scores = cursor.fetchall()
    print('Scores:')
    for s in scores:
        print(s['username'] + ' | ' + s['mobile'] + ' | ' + s['technology'] + ' | ' + str(s['score']) + ' in ' + str(s['time_taken']) + ' sec')



def register_user():
    uname = input('Enter username: ')
    mobile = input('Enter mobile (10 digits): ')
    pwd = input('Enter password (must be same as mobile): ')

    if not (mobile.isdigit() and len(mobile) == 10 and mobile[0] in '6789'):
        print('Invalid mobile number (must start with 6/7/8/9 and be 10 digits)')
        return


    if pwd != mobile:
        print("Password must be the same as mobile number")
        return

    cursor.execute("SELECT * FROM users WHERE username=%s OR mobile=%s", (uname, mobile))
    existing = cursor.fetchone()

    if existing:
        print("Username or mobile already exists")
        return

    cursor.execute(
        "INSERT INTO users (username, mobile, password) VALUES (%s, %s, %s)",
        (uname, mobile, pwd)
    )
    conn.commit()
    print("User registered successfully")

def login_user():
    uname = input('Enter username: ')
    pwd = input('Enter password: ')

    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (uname, pwd))
    user = cursor.fetchone()
    if not user:
        print('Invalid credentials')
        return

    print('Welcome ' + uname + '!')
    while True:
        print('1. Start Quiz')
        print('2. View Top 3 Scores')
        print('3. Logout')
        choice= input('Enter choice: ')

        if choice == '1':
            start_quiz(cursor, conn, user['username'], user['mobile'])
        elif choice == '2':
            show_top_scores()
        elif choice == '3':
            break
        else:
            print('Invalid choice')


def start_quiz(cursor, conn, username, mobile):

    cursor.execute("SELECT number, name FROM technologies")
    techs = cursor.fetchall()
    if not techs:
        print("No technologies present")
        return

    print("Available Technologies are:")
    for row in techs:
        print(str(row['number']) + ". " + row['name'])

    tech_choice = input("Choose technology number: ")
    cursor.execute("SELECT * FROM technologies WHERE number=%s", (tech_choice,))
    tech = cursor.fetchone()
    if not tech:
        print("Invalid technology choice")
        return


    cursor.execute("SELECT * FROM questions WHERE technology_id=%s", (tech_choice,))
    questions = cursor.fetchall()
    if not questions:
        print(" No questions found in this technology")
        return

    score = 0
    start_time = time.time()

    for q in questions:
        print(q['question'])
        print("A:", q['option_a'])
        print("B:", q['option_b'])
        print("C:", q['option_c'])
        print("D:", q['option_d'])
        ans = input("Your answer (A/B/C/D): ").upper()

        if ans == q['correct_option'].upper():
            score += 1

    end_time = time.time()
    time_taken = int(end_time - start_time)

   
    cursor.execute(
        "INSERT INTO scores (username, mobile, technology, score, time_taken) VALUES (%s, %s, %s, %s, %s)",
        (username, mobile, tech['name'], score, time_taken)
    )
    conn.commit()

    print("Quiz Completed! Score:", score, "/", len(questions))
    print("Time Taken:", time_taken, "seconds")



def show_top_scores():
    tech = input('Enter technology name: ').strip().lower()
    cursor.execute('SELECT username,mobile,score,time_taken FROM scores WHERE technology=%s ORDER BY score DESC, time_taken ASC LIMIT 3', (tech,))
    rows = cursor.fetchall()
    print('Top 3 Scores:')
    for r in rows:
        print(r['username'] + ' | ' + r['mobile'] + ' | Score: ' + str(r['score']) + ' | Time: ' + str(r['time_taken']) + ' sec')


def admin_menu():
    while True:
        print('*************** ADMIN MENU ******************')
        print('1. Add Technology')
        print('2. Add Question')
        print('3. Modify Question')
        print('4. Delete Question')
        print('5. View Questions')
        print('6. View Technologies')
        print('7. View Users and Scores')
        print('8. Exit from this Menu')
        admin_choice= input('Enter choice: ')

        if admin_choice == '1':
            add_technology()
        elif admin_choice == '2':
            add_question()
        elif admin_choice== '3':
            modify_question()
        elif admin_choice== '4':
            delete_question()
        elif admin_choice == '5':
            view_questions()
        elif admin_choice == '6':
            view_technologies()
        elif admin_choice == '7':
            view_users_and_scores()
        elif admin_choice == '8':
            print('Exited from admin menu')
            break
        else:
            print('Invalid choice')


def user_menu():
    while True:
        print('*************** USER MENU ******************')
        print('1. Register for quiz')
        print('2. Login to start quiz')
        print('3. Exit')
        user= input('Enter choice: ')

        if user == '1':
            register_user()
        elif user == '2':
            login_user()
        elif user == '3':
            print('Exited from user menu')
            break
        else:
            print('Invalid choice')


while True:
        print('*************** MAIN MENU ******************')
        print('1. Admin')
        print('2. User')
        print('3. Exit')
        choice = input('Enter choice: ')

        if choice == '1':
            if admin_login():
                admin_menu()
        elif choice == '2':
            user_menu()
        elif choice == '3':
            print('Thank you for choosing us!!')
            break
        else:
            print('Invalid choice')
