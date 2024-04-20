def escape_special_chars(input_string):
    special_chars = ['-', '_', '|', '~',
                     '(', '[', '{', ')', ']', '}', '>', '`', '.','!']
    escaped_string = ''

    for char in input_string:
        if char in special_chars:
            escaped_string += '\\' + char
        else:
            escaped_string += char

    return escaped_string