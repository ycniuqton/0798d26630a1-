import random
import string


def generate_customer_code(length=8):
    # Define the character pool: uppercase letters and digits
    char_pool = string.ascii_uppercase + string.digits
    # Generate a random code
    return ''.join(random.choice(char_pool) for _ in range(length))


def number(num):
    return '{:20,.2f}'.format(num)
