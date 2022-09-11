import socket
from enum import Enum

# create tcp socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # define server address and port
ip = ''
port = 50000
dest = (ip, port)
tcp.connect(dest)


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


def package_info(data_type, key, value):
    if data_type == DataTypes.STRING.value:
        value = package_string(value)
    elif data_type == DataTypes.INTEGER.value:
        if value != '':
            value = package_int(int(value))
        else:
            data_type = DataTypes.STRING.value
            value = package_string(value)

    data_type = package_int(data_type)
    key = package_string(key)

    return data_type + key + value


def package_string(value):
    return converter_size(value) + value.encode()


def converter_size(value):
    return (len(value)).to_bytes(2, 'big')


def package_int(integer):
    return integer.to_bytes(1, 'big')


def send_package(data):
    tcp.send(data)


def create_message(op, infos):
    data = op
    for info in infos:
        data += info
    data += package_int(0)
    return data


def show_operation_options():
    print('')
    print('Select an option:')
    for operation_option in OperationOptions:
        print(f'{operation_option.value} - {operation_option.name}')


while True:
    show_operation_options()
    option = int(input())
    if option == OperationOptions.CREATE.value:
        op = package_int(OperationOptions.CREATE.value)

        infos = []

        info = package_info(DataTypes.STRING.value, 'name', input('Name of the pokemon: '))
        infos.append(info)

        info = package_info(DataTypes.STRING.value, 'type', input('Type of the pokemon: '))
        infos.append(info)

        info = package_info(DataTypes.INTEGER.value, 'HP', input('HP of the pokemon: '))
        infos.append(info)

        data = create_message(op, infos)
        send_package(data)

        response = tcp.recv(1)
        response = int.from_bytes(response, 'big')
        print(response)

    elif option == OperationOptions.READ.value:
        tcp.send(package_int(option))

        response = tcp.recv(1)

        response = int.from_bytes(response, 'big')

        print(response)

    elif option == OperationOptions.UPDATE.value:
        op = package_int(OperationOptions.UPDATE.value)

        infos = []

        info = package_info(DataTypes.INTEGER.value, 'id', input('Id of the pokemon: '))
        infos.append(info)

        info = package_info(DataTypes.STRING.value, 'name', input('Name of the pokemon: '))
        infos.append(info)

        info = package_info(DataTypes.STRING.value, 'type', input('Type of the pokemon: '))
        infos.append(info)

        info = package_info(DataTypes.INTEGER.value, 'HP', input('HP of the pokemon: '))
        infos.append(info)

        data = create_message(op, infos)
        send_package(data)

        response = tcp.recv(2)
        response = int.from_bytes(response, 'big')
        print(response)

    elif option == OperationOptions.DELETE.value:
        op = package_int(OperationOptions.DELETE.value)

        infos = []

        info = package_info(DataTypes.INTEGER.value, 'id', input('Id of the pokemon to delete: '))
        infos.append(info)

        data = create_message(op, infos)
        send_package(data)

        response = tcp.recv(2)
        response = int.from_bytes(response, 'big')
        print(response)

    elif option == OperationOptions.EXIT.value:
        tcp.send(package_int(option))
        break

    else:
        print('invalid option')
        continue
