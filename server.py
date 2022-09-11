import socket
from enum import Enum

# create tcp socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define server port
ip = ''
port = 50000
tcp.bind((ip, port))
tcp.listen(1)

# accept connection
conn, addr = tcp.accept()


class OperationOptions(Enum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4
    EXIT = 5


class DataTypes(Enum):
    STRING = 1
    INTEGER = 2
    FLOAT = 3


# array of data
db_data = []

# last_id
last_id = 1


# receive size of message
def get_data():
    data_type = int.from_bytes(conn.recv(1), 'big')

    data = []

    while data_type != 0:
        key = unpack_string()
        value = ''

        if data_type == DataTypes.STRING.value:
            value = unpack_string()
        elif data_type == DataTypes.INTEGER.value:
            value = int.from_bytes(conn.recv(1), 'big')

        data.append({key: value})
        data_type = int.from_bytes(conn.recv(1), 'big')

    return data


def unpack_string():
    size_bytes = conn.recv(2)
    size_message = int.from_bytes(size_bytes, 'big')
    return conn.recv(size_message).decode()


def create_data():
    global last_id
    data = get_data()
    data.insert(0, {'id': last_id})
    last_id += 1
    db_data.append(data)
    conn.send((201).to_bytes(1, 'big'))


def read_data():
    print(db_data)
    conn.send((200).to_bytes(1, 'big'))


# def update_data(id, data):
#     find = False
#     for data in db_data:
#         if data[0]['id'] == id:
#             find = True
#             db_data.remove(data)
#             conn.send((200).to_bytes(1, 'big'))
#             return
#     if not find:
#         conn.send((404).to_bytes(2, 'big'))


def delete_data(id):
    pos = find_data_pos(id)
    if pos != -1:
        db_data.pop(pos)
        conn.send((200).to_bytes(1, 'big'))
    else:
        conn.send((404).to_bytes(2, 'big'))


def find_data_pos(id):
    for i in range(len(db_data)):
        if db_data[i][0]['id'] == id:
            return i
    return -1


while True:
    option = int.from_bytes(conn.recv(1), 'big')
    if option == OperationOptions.CREATE.value:
        create_data()
    elif option == OperationOptions.READ.value:
        read_data()
    # elif option == OperationOptions.UPDATE.value:
    #     update_data()
    elif option == OperationOptions.DELETE.value:
        data = get_data()
        id_to_delete = data[0]['id']
        delete_data(id_to_delete)
    elif option == 5:
        print('Exit')
        break

# close connection
conn.close()
