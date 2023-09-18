##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import select
import random
import json
import requests
# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def load_questions_from_web():
    url = "https://opentdb.com/api.php?amount=50&type=multiple"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        print("succes load")
        num_quest = 1
        for question in json_data["results"]:
            correct = question["correct_answer"]
            answers = [correct] + question["incorrect_answers"][:4]
            random.shuffle(answers)
            questions[num_quest] = {"question": question["question"].replace('#',""), "answers": [string.replace("#","") for string in answers], "correct": correct.replace("#","")}
            num_quest += 1
    else:
        print("error")
        exit

def build_and_send_message(conn, code, msg):
    """
       Builds a new message using chatlib, wanted code and message.
       Prints debug info, then sends it to the given socket.
       Paramaters: conn (socket object), code (str), data (str)
       Returns: Nothing
       """
    full_msg = chatlib.build_message(code, msg)
    conn.send(full_msg.encode())
    print("[SERVER] ", full_msg)  # Debug print


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()

    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT] ", full_msg)  # Debug print
    return cmd, data

# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """

    users = {
        "test"	:	{"password" :"test" ,"score" :0 ,"questions_asked" :[]},
        "yossi"		:	{"password" :"123" ,"score" :50 ,"questions_asked" :[]},
        "master"	:	{"password" :"master" ,"score" :200 ,"questions_asked" :[]}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    return server_socket




def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    msg_protocol = chatlib.build_message("ERROR",error_msg)
    conn.send(msg_protocol.encode())
    print("[SERVER]", msg_protocol)





##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    if username in users:
        score = users[username]["score"]
        build_and_send_message(conn,"YOUR_SCORE", score)
    else:
        send_error(conn, "wrong user name")
# Implement this in later chapters



def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    print("[CLIENT] ", conn.recv(1024).decode())
    logged_users.pop(conn.getpeername())
    conn.close()


# Implement code ...


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later
    login_data = chatlib.split_data(data,2)
    if login_data[0] in users.keys():
        user = login_data[0]
        password = users[user]["password"]
        if login_data[1] == password:
            build_and_send_message(conn,"LOGIN_OK","")
            logged_users[conn.getpeername()] = user
            return
        else:
            send_error(conn, "wrong password\n exit, goodbuye")
    send_error(conn,"LOGIN ERROR")



def handle_logged_message(conn):
    #get a socket object and send list of logged online user
    key_list = list(logged_users.values())
    msg = ','.join(key_list)
    build_and_send_message(conn, "LOGGED_ANSWER", msg)


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later
    id_q =-1
    if conn.getpeername() not in logged_users.keys():
        if cmd == "LOGIN":
            handle_login_message(conn, data)
        else:
            send_error(conn,"failed logg")
    username = logged_users[conn.getpeername()]
    if cmd == "LOGOUT":
        handle_logout_message(conn)
    elif cmd == "LOGGED":
        handle_logged_message(conn)
    elif cmd == "GET_QUESTION":
        ls = list(questions.keys())
        question_left = list(set(ls) - set(users[username]["questions_asked"]))
        if len(question_left):
            id_q = random.choice(question_left)
            users[username]["questions_asked"].append(id_q)
            question= questions[id_q]["question"]
            answer = chatlib.join_data(questions[id_q]["answers"])
            msg = chatlib.join_data([id_q,question,answer])
            build_and_send_message(conn, "YOUR_QUESTION", msg )
        else:
            build_and_send_message(conn, "NO_QUESTIONS","")
    elif cmd == "SEND_ANSWER":
        answer_data = chatlib.split_data(data, 2)
        id_q, choice = answer_data[0], answer_data[1]
        question = questions[int(id_q)]
        answer = question["correct"]
        answer_number = {question["answers"][0]:1,question["answers"][1]:2, question["answers"][2]:3,question["answers"][3]:4}
        if answer_number[answer] == int(choice):
            build_and_send_message(conn,"CORRECT_ANSWER","")
            users[username]["score"] += 5
        else:
            build_and_send_message(conn, "WRONG_ANSWER", str(answer))
    elif cmd == "MY_SCORE":
        username = logged_users[conn.getpeername()]
        build_and_send_message(conn,"YOUR_SCORE", str(users[username]["score"]))
    elif cmd == "HIGHSCORE":
        data_score = build_score_table()
        build_and_send_message(conn, "ALL_SCORE", data_score)

    else:
        send_error(conn,ERROR_MSG)


def build_score_table():
    "sort the score lable and contruct a data of ALL SCORE by protocol"
    score_table = dict(sorted(users.items(), key=lambda score: score[1]["score"],reverse= True))
    data_score = []
    for user in score_table.keys():
        data_score.append(user + ":" + str(score_table[user]["score"]))
    return "\n".join(data_score)

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

def main():
    # Initializes global users and questions dicionaries using load functions, will be used later

    global users
    global questions
    load_questions_from_web()
    users = load_user_database()
    #questions = load_questions()
    print("Welcome to Trivia Server!")
    server_socket = setup_socket()
    client_sockets = []
    messages_to_send = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                cmd , data = recv_message_and_parse(client_socket)
                client_sockets.append(client_socket)
                handle_login_message(client_socket, data)

            else:
                print("new data from client")
                try:
                    cmd, data = recv_message_and_parse(current_socket)
                    messages_to_send.append((current_socket,cmd, data))
                except:
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print("client has been loged out")
                    print_client_sockets(client_sockets)
                    continue
                if data == "LOGOUT":
                    print("connection close")
                    client_sockets.remove(current_socket)
                    handle_logout_message(current_socket)
                    print_client_sockets(client_sockets)
                else:
                    print(data)
                    for message in messages_to_send:
                        current_socket, cmd, data = message
                        if current_socket in ready_to_write:
                            handle_client_message(current_socket,cmd, data)
                            messages_to_send.remove(message)


# Implement code ...



if __name__ == '__main__':
    main()

