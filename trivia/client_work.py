import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    mag_protocol = chatlib.build_message(code, data)
    conn.send(mag_protocol.encode())
    #print("the massage is: " + mag_protocol)


def play_question(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["question_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["your_question_msg"]:

        data_parts = chatlib.split_data(data, 6)
        id = data_parts[0]
        question = data_parts[1]
        answers = "\n".join(data_parts[2:])

        print("the question is: " + question + "\n----answers----\n" + answers)
        your_answer = input("\npleas enter your answer: ")
        answer_shield = id + '#' + your_answer
        answer_cmd, answer_data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["answer_msg"], answer_shield)
        if answer_cmd == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
            print("your correct!\nthe answer is: " + your_answer + "\nyour score is: ")

        elif answer_cmd == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
            print("your wrong :(\n the correct answer is:" + answer_data)
        get_score(conn)
    elif msg_code == chatlib.PROTOCOL_SERVER["no_question_msg"]:
        print("there is no more question left")
    else:
        return

def get_logged_users(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["see_logged"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["logged_msg"]:
        print("the member are:\n" + data)
    else:
        print("error")
        return

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
    if cmd == "ERROR":
        error_and_exit(data)
    return cmd, data


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    pass
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit()



def login(conn):
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    status =True
    while status:
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username + '#' + password)
        cmd, data = recv_message_and_parse(conn)
        print('cmd: ' + cmd, '\ndata: ' + data)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("your login succeed!\nwelcome " + username)
            return
        else:
            print("ERROR with LOGIN")
            username = input("Please enter username again: \n")
            password = input("Please enter password again: \n")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")

def build_send_recv_parse(conn,cmd,data):
    build_and_send_message(conn, cmd, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data

def get_highscore(conn):
    msg_code, data =build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["highscore_msg"],'')
    if msg_code == chatlib.PROTOCOL_SERVER["all_score_msg"]:
        print(data)
    else:
        print("ERROR WITH DATA")


def get_score(conn):
    msg_code, data =build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["score_msg"],'')
    if msg_code == chatlib.PROTOCOL_SERVER["your_score_msg"]:
        print("my score is: ", data)
    else:
        print("ERROR WITH DATA")




def main():
 the_socket =connect()
 login(the_socket)

 print("\n\nMENU\n\nthis numbers are command for the script\n1-to see your score.\n2-to see the score table.\n3-to ask a question.\n4-to see onlinr members.\n5-to quit the game.\nyour command: ")
 chose = input()
 while chose != "5":
     if chose == '1':
         get_score(the_socket)
     elif chose == '2':
         get_highscore(the_socket)
     elif chose == '3':
         play_question(the_socket)
     elif chose == '4':
         get_logged_users(the_socket)
     print("insert another command: ")
     chose = input()
 logout(the_socket)
 the_socket.close()



if __name__ == '__main__':
    main()
