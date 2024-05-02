import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip = '127.0.0.1'
port = 8000

server.bind((ip,port))
server.listen()

list_of_clients = []
nicknames  = []

questions = [
    "What is the Italian word for PIE? \n A.Mozarella\n B.Pasty\n C.Patty\n D.Pizza",
    "Water boils at 212 Units at which scale? \n A.Fahrenheit\n B.Celsius\n C.Rankine\n D.Kelvin",
    "Which sea creature has 3 hearts? \n A.Dolphin\n B.Octopus\n C.Walrus\n D.Seal",
    "How many bones does an adult human have? \n A.206\n B.208\n C.201\n D.196",
    "What element does not exist? \n A.Xf\n B.Re\n C.Si\n D.Pa",
    "How many states are there in India? \n A.24\n B.29\n C.30\n D.31",
    "How many wonders are there in the world? \n A.7\n B.8\n C.10\n D.4"    
    ]

answers = ['D','A','B','A','A','B','A']

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index,random_question,random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clientthread(conn):
    print("Hello")
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question.The answer to that question should be one of a,b,c or d!\n".encode('utf-8'))
    conn.send("Good luck!\n\n".encode('utf-8'))

    index,questions,answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1] == answer:
                    score += 1
                    conn.send(f"Bravo!Your score is {score} \n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer!Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index,questions,answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
        except:
            continue

while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + "connected")
    new_thread = Thread(target = clientthread,args=(conn,))
    new_thread.start()

