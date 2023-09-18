# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"question_msg": "GET_QUESTION",
"answer_msg": "SEND_ANSWER",
"score_msg": "MY_SCORE",
"highscore_msg": "HIGHSCORE",
"see_logged" : "LOGGED",
"ERORR_MASSAGE":"ERROR"

} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"logged_msg": "LOGGED_ANSWER",
"your_question_msg": "YOUR_QUESTION",
"correct_answer_msg": "CORRECT_ANSWER",
"wrong_answer_msg": "WRONG_ANSWER",
"your_score_msg": "YOUR_SCORE",
"all_score_msg": "ALL_SCORE",
"no_question_msg": "NO_QUESTIONS"

} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """Gets command name (str) and data field (str) and creates a valid protocol message
      Returns: str, or None if error occured
    """

    if (len(cmd) <= CMD_FIELD_LENGTH) and (MAX_DATA_LENGTH >= len(data)) and ((cmd in PROTOCOL_CLIENT.values()) or (cmd in PROTOCOL_SERVER.values())):

        prot_cmd = cmd + " " * (CMD_FIELD_LENGTH - len(cmd))
        len_of_data = "%04d" % len(data)
        pre_full = [prot_cmd, len_of_data, data]
        full_msg = DELIMITER.join(pre_full)
        if ((cmd  in PROTOCOL_CLIENT.values()) or (cmd  in PROTOCOL_SERVER.values())) and (len(cmd) <= 16) and (len(data) <= MAX_DATA_LENGTH):
            return full_msg
        else:
            return ERROR_RETURN








def get_number(number):
    num = number.strip()
    for dig in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']:
        if dig in num:
            return ERROR_RETURN

    #print('num is: ' + num)
    final = num.lstrip('0')
    if len(final) == 0:

        return 0
    else:

        return int(final)




def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """

    parts = data.split(DELIMITER, maxsplit=3)


    if data.count(DELIMITER) < 2:
        return None, None
    cmd = parts[0].strip()
    msg = "".join(parts[2:])
    len_of_data = get_number(parts[1])
    if len_of_data == ERROR_RETURN:
        return None, None

    if (MAX_MSG_LENGTH >= len(data)) and (len(str(get_number(parts[1]))) <= 4) and (len(parts[2]) <= MAX_DATA_LENGTH):
        if len_of_data == len(msg):
            return cmd, msg
        else:
            return None, None


    else:
        return None, None
# The function should return 2 values


#parse_message("LOGIN           |   4|data")
def split_data(msg, expected_fields):
    """
	Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
    num_of_parts = msg.split(DATA_DELIMITER)
    if len(num_of_parts) == expected_fields:
        return num_of_parts
    else:
        return ERROR_RETURN





def join_data(msg_fields):
    """
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""
    string_fields = [str(i) for i in msg_fields]
    join_msg = DATA_DELIMITER.join(string_fields)
    return join_msg



#build_message('LOGIN','user#pass')


