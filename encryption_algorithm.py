def encrypt(value):
    value_as_string = str(value)
    while len(value_as_string) < 5:
        value_as_string = "0" + value_as_string
    binary_string = convert_chars_to_binary(value_as_string)
    encrypted_string = order_bits(binary_string)
    return encrypted_string

def convert_chars_to_binary(value_as_string):
    binary_string = ""
    for char in value_as_string:
        binary_string += format(int(char), "04b")
    return binary_string

def order_bits(binary_string_len_20):
    ordered_bits = ""
    encrypt_index_order = [25, 25, 8, 9, 10, 19, 7, 1, 2, 11, 18, 6, 0, 3, 25, 17, 5, 4, 25, 12, 16, 25, 15, 14, 13]
    twenty_five_bit_index = 0
    for index in encrypt_index_order:
        if twenty_five_bit_index == 0:
            ordered_bits += xor(binary_string_len_20[18], binary_string_len_20[19])
        elif twenty_five_bit_index == 1:
            ordered_bits += xor(binary_string_len_20[6], binary_string_len_20[7])
        elif twenty_five_bit_index == 14:
            ordered_bits += xor(binary_string_len_20[10], binary_string_len_20[11])
        elif twenty_five_bit_index == 18:
            ordered_bits += xor(binary_string_len_20[2], binary_string_len_20[3])
        elif twenty_five_bit_index == 21:
            ordered_bits += xor(binary_string_len_20[14], binary_string_len_20[15])
        else:
            ordered_bits += binary_string_len_20[index]
        twenty_five_bit_index += 1
    return ordered_bits

def xor(char_0, char_1):
    if char_0 == "0" and char_1 == "0":
        return "0"
    if char_0 == "1" and char_1 == "1":
        return "0"
    return "1"

def print_for_easy_read(binary_message):
    for (index, char) in enumerate(binary_message):
        if (index % 5 == 4):
            print(char)
        else:
            print(char, end="")

def convert_to_decimal(binary_string):
    decimal_string = ""
    decimal_string += str(int(binary_string[0:4], 2))
    decimal_string += str(int(binary_string[4:8], 2))
    decimal_string += str(int(binary_string[8:12], 2))
    decimal_string += str(int(binary_string[12:16], 2))
    decimal_string += str(int(binary_string[16:20], 2))
    return decimal_string
    
def decrypt(encrypted_binary_string):
    reordered_string = ""
    decrypt_index_order = [12, 7, 8, 13, 17, 16, 11, 6, 2, 3, 4, 9, 19, 24, 23, 22, 20, 15, 10, 5]
    for index in decrypt_index_order:
        reordered_string += encrypted_binary_string[index]
    decrypted_value = convert_to_decimal(reordered_string)
    decrypted_value_without_leading_zeros = decrypted_value
    for char in decrypted_value:
        if char == "0":
            decrypted_value_without_leading_zeros = decrypted_value_without_leading_zeros[1:]
        else:
            break
    return decrypted_value_without_leading_zeros

encrypted_value = encrypt(7)
print_for_easy_read(encrypted_value)

print(decrypt(encrypted_value))