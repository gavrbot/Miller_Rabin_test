import numpy
import random

dict_with_codes = {
    "001": "-1",
    "010": "-2",
    "011": "3",
    "100": "-3",
    "101": "0",
    "110": "2",
    "111": "1",
}

S_matrix = numpy.array([(1, 1, 0, 1),
                        (1, 0, 0, 1),
                        (0, 1, 1, 1),
                        (1, 1, 0, 0)])

P_matrix = numpy.array([(0, 1, 0, 0, 0, 0, 0),
                        (0, 0, 0, 1, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 1),
                        (1, 0, 0, 0, 0, 0, 0),
                        (0, 0, 1, 0, 0, 0, 0),
                        (0, 0, 0, 0, 0, 1, 0),
                        (0, 0, 0, 0, 1, 0, 1)])

hamming_matrix = numpy.array(
    [(1, 0, 0, 0, 1, 0, 1),
     (0, 1, 0, 0, 1, 1, 1),
     (0, 0, 1, 0, 1, 1, 0),
     (0, 0, 0, 1, 0, 1, 1)])

hamming_matrix_to_find_errors = numpy.array([(1, 0, 1),
                                             (1, 1, 1),
                                             (1, 1, 0),
                                             (0, 1, 1),
                                             (1, 0, 0),
                                             (0, 1, 0),
                                             (0, 0, 1)])


def generate_matrix(n):
    flag = False
    while not flag:
        matrix = numpy.zeros(n ** 2)
        for i in range(n ** 2):
            val = random.randint(0, 1)
            matrix[i] = val
        matrix = matrix.reshape(n, n)
        det = numpy.linalg.det(matrix) % 2
        flag = bool(det)
    return matrix


def generate_error():
    error = numpy.zeros(7)
    index = random.randint(0, 6)
    error[index] = 1
    return error


def encrypt(message, error):
    # S_matrix = generate_matrix(4)
    # P_matrix = generate_matrix(7)

    print("S matrix:")
    print(S_matrix)
    print("P matrix:")
    print(P_matrix)
    print("Message to encrypt:")
    print(message)
    print("Error:")
    print(error)

    new_G_matrix = numpy.dot(S_matrix, hamming_matrix) % 2
    new_G_matrix = numpy.dot(new_G_matrix, P_matrix) % 2

    c = numpy.dot(message, new_G_matrix) % 2
    c = (c + error) % 2
    return c, P_matrix, S_matrix


def decrypt(c):
    inverse_P_matrix = numpy.linalg.inv(P_matrix) % 2

    new_c = numpy.dot(c, inverse_P_matrix) % 2

    code = numpy.dot(new_c, hamming_matrix_to_find_errors) % 2
    code = code.astype('int8')

    code = ''.join([str(x) for x in code])

    for key in dict_with_codes.keys():
        if key == code:
            code = int(dict_with_codes.get(key))
            break

    if code != '000':
        new_c[code] += 1
        new_c[code] %= 2

    new_c = new_c[:4]
    inverse_S_matrix = numpy.linalg.inv(S_matrix) % 2
    message = numpy.dot(new_c, inverse_S_matrix) % 2
    return message


def group(iterable, count):
    return zip(*[iter(iterable)] * count)





if __name__ == '__main__':
    a_string = input()

    a_byte_array = bytearray(a_string, "utf8")

    byte_list = []

    for byte in a_byte_array:
        binary_representation = bin(byte)

        byte_list.extend(int(i) for i in binary_representation[2:])

    result = [int(x) for x in result]
    res_list = list(group(result, 4))
    encrypted_message = numpy.zeros(0)
    for block in res_list:
        encrypted_message = numpy.concatenate((encrypted_message, encrypt(block, generate_error())[0]), axis=0)

    encrypted_list = list(group(result, 7))

    decrypt_message = numpy.zeros(0)
    for block in encrypted_list:
        decrypt_message = numpy.concatenate((decrypt_message, decrypt(block)), axis=0)

    print(decrypt_message)
    while (len(decrypt_message) % 7) != 0:
        decrypt_message = numpy.append(decrypt_message, 0)

    res = ""
    count = int(len(decrypt_message) / 7)
    for i in range(count):
        res += '0b' + ''.join(str(int(j)) for j in decrypt_message[i * 7:i * 7 + 7])

    print(res)

    # P_matrix, S_matrix, c = encrypt(numpy.array([1, 0, 1, 0]), generate_error())
    # decrypt(c, P_matrix, S_matrix)
    # c = encrypt(m, z)
    # decrypt(c)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
