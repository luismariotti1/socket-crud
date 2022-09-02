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
    global last_id

    data_type = int.from_bytes(conn.recv(1), 'big')

    data = [{'id': last_id}]

    while data_type != 0:
        key = unpack_string()
        value = ''

        if data_type == DataTypes.STRING.value:
            value = unpack_string()
        elif data_type == DataTypes.INTEGER.value:
            value = int.from_bytes(conn.recv(1), 'big')

        data.append({key: value})
        data_type = int.from_bytes(conn.recv(1), 'big')

    last_id += 1

    return data


def unpack_string():
    size_bytes = conn.recv(2)
    size_message = int.from_bytes(size_bytes, 'big')
    return conn.recv(size_message).decode()


while True:
    option = int.from_bytes(conn.recv(1), 'big')
    if option == OperationOptions.CREATE.value:
        db_data.append(get_data())
        conn.send((201).to_bytes(1, 'big'))
    elif option == OperationOptions.READ.value:
        print(db_data)
    # elif option == 3:
    #     print('Update')
    # elif option == 4:
    #     # data.pop()
    #     print('Delete')
    elif option == 5:
        print('Exit')
        break

# close connection
conn.close()
