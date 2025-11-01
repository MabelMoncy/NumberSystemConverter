from flask import Flask, render_template, request, redirect, url_for  # importing neccessary modules and classes
app = Flask(__name__)  # app is the instance of the class 'Flask'

@app.route('/')  # Route for home screen
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def check_convertion():  # Check for the valid options
    from_option = request.form.get('from-option')  # alwyas binary in this case.
    to_option = request.form.get('to-option')
    input_number = request.form.get('input-number')

    # basic guard: ensure input exists (prevents crashes when input_number is None)
    if input_number is None or str(input_number).strip() == "":
        return render_template('index.html', result="Please enter a number to convert.")

    # normalize input string (but keep semantics same)
    input_number = str(input_number).strip()

    # All same system conversions are done:
    errMssg = "You chose the same convertion! Try different one."
    if from_option == "binary" and to_option == "binary":
        return render_template('index.html', result=errMssg)
    if from_option == "decimal" and to_option == "decimal":
        return render_template('index.html', result=errMssg)
    if from_option == "octal" and to_option == "octal":
        return render_template('index.html', result=errMssg)
    if from_option == "hexadecimal" and to_option == "hexadecimal":
        return render_template('index.html', result=errMssg)

    # All Binary conversions
    if from_option == "binary" and to_option == "decimal":  # "binary">>is taken from value=" "
        result = binary_to_decimal(input_number)
        return render_template('index.html', result=result)
    if from_option == "binary" and to_option == "octal":  # "octal">> is taken from value=" "
        result = binary_to_octal(input_number)
        return render_template('index.html', result=result)
    if from_option == "binary" and to_option == "hexadecimal":
        result = binary_to_hexadecimal(input_number)
        return render_template('index.html', result=result)

    # All Decimal conversions
    if from_option == "decimal" and to_option == "binary":
        result = decimal_to_binary(input_number)
        return render_template('index.html', result=result)
    if from_option == "decimal" and to_option == "octal":
        result = decimal_to_octal(input_number)
        return render_template('index.html', result=result)
    if from_option == "decimal" and to_option == "hexadecimal":
        result = decimal_to_hexadecimal(input_number)
        return render_template('index.html', result=result)

    # All Octal Conversions
    if from_option == "octal" and to_option == "binary":
        result = octal_to_binary(input_number)
        return render_template('index.html', result=result)
    if from_option == "octal" and to_option == "decimal":
        result = octal_to_decimal(input_number)
        return render_template('index.html', result=result)
    if from_option == "octal" and to_option == "hexadecimal":
        result = octal_to_hexadecimal(input_number)
        return render_template('index.html', result=result)

    # All Hexadecimal conversion
    if from_option == "hexadecimal" and to_option == "binary":
        result = hexadecimal_to_binary(input_number)
        return render_template('index.html', result=result)
    if from_option == "hexadecimal" and to_option == "decimal":
        result = hexadecimal_to_decimal(input_number)
        return render_template('index.html', result=result)
    if from_option == "hexadecimal" and to_option == "octal":
        result = hexadecimal_to_octal(input_number)
        return render_template('index.html', result=result)
    return None

# Binary to other number system convertions.
def binary_to_decimal(binary_input):
    # defensive: ensure string and strip spaces
    if binary_input is None:
        return "Binary input missing!"
    binary_input = str(binary_input).strip()
    if binary_input == "":
        return "Binary input missing!"

    result = 0

    if '.' in binary_input:
        try:
            integer_part, fractional_part = binary_input.split('.')
            # validate digits
            for digit in integer_part + fractional_part:
                if digit not in ['0', '1']:
                    return "Binary inputs can only be 0s and 1s"
            for i in range(len(integer_part)):
                digit = int(integer_part[i])
                power = len(integer_part) - i - 1
                result = result + digit * (2 ** power)
            for j in range(len(fractional_part)):
                digit = int(fractional_part[j])
                result = result + digit * (2 ** -(j + 1))
            return result
        except ValueError:
            return "Something went wrong!"
    else:
        integer_part = binary_input
        for digit in integer_part:
            if digit not in ['0', '1']:
                return "Binary inputs can only be 0s and 1s"
        for i in range(len(integer_part)):
            digit = int(integer_part[i])
            power = len(integer_part) - i - 1
            result = result + digit * (2 ** power)
        return result

def binary_to_octal(binary_input):
    if binary_input is None:
        return "Binary input missing!"
    binary_input = str(binary_input).strip()
    try:
        for digit in binary_input:
            if digit not in ['0', '1', '.']:
                return "Binary inputs can only be 0s and 1s"
        integer_part_remainder = []
        fractional_part_value = []
        decimal_value = binary_to_decimal(binary_input)
        # if binary_to_decimal returned an error string, propagate it
        if isinstance(decimal_value, str):
            return decimal_value

        # Since we have a decimal number here we cannot split it using the spilt() function instead we do:
        integer_part = int(decimal_value)  # This will convert the decimal number to integer removing the fractional part
        fractional_part = decimal_value - integer_part  # This will give the fractional part

        # integer part conversion
        if integer_part == 0:
            integer_part_remainder.append('0')
        else:
            while integer_part > 0:
                remainder = integer_part % 8
                integer_part_remainder.append(str(remainder))
                integer_part //= 8

        # Limit to 5 digits max for fractional part
        for _ in range(5):
            fractional_part *= 8
            digit = int(fractional_part)
            fractional_part_value.append(str(digit))
            fractional_part -= digit
            if fractional_part == 0:
                break

        if fractional_part_value:
            octal_number = ''.join(reversed(integer_part_remainder)) + '.' + ''.join(fractional_part_value)
        else:
            octal_number = ''.join(reversed(integer_part_remainder))
        return octal_number

    except ValueError:
        return "Something went wrong!"

def binary_to_hexadecimal(binary_input):
    if binary_input is None:
        return "Binary input missing!"
    binary_input = str(binary_input).strip()
    hexadecimal_values = {
        '0000': '0', '0001': '1', '0010': '2', '0011': '3',
        '0100': '4', '0101': '5', '0110': '6', '0111': '7',
        '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
        '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'
    }

    # Separate integer and fractional parts
    if '.' in binary_input:
        integer_part, fractional_part = binary_input.split('.')
    else:
        integer_part = binary_input
        fractional_part = ''

    # validate binary digits
    for ch in integer_part + fractional_part:
        if ch not in ('0', '1', ''):
            return "Binary inputs can only be 0s and 1s"

    # --- Integer part ---
    while len(integer_part) % 4 != 0:
        integer_part = '0' + integer_part

    hex_integer = ''
    for i in range(0, len(integer_part), 4):
        four_bit_group = integer_part[i:i+4]
        hex_integer += hexadecimal_values.get(four_bit_group, '?')

    # --- Fractional part ---
    hex_fraction = ''
    if fractional_part:
        while len(fractional_part) % 4 != 0:
            fractional_part = fractional_part + '0'
        for i in range(0, len(fractional_part), 4):
            four_bit_group = fractional_part[i:i+4]
            hex_fraction += hexadecimal_values.get(four_bit_group, '?')

    # Combine result
    if fractional_part:
        return hex_integer + '.' + hex_fraction
    else:
        return hex_integer

# Decimal to other number system conversion
def decimal_to_binary(decimal_input):
    if decimal_input is None:
        return "Decimal input missing!"
    decimal_input = str(decimal_input).strip()
    if '.' in decimal_input:
        try:
            decimal_number = float(decimal_input)
            integer_part = int(decimal_number)
            fractional_part = decimal_number - integer_part
            remainders = []

            if integer_part:
                while integer_part > 0:
                    remainder = integer_part % 2
                    remainders.append(str(remainder))
                    integer_part //= 2
                binary_number = ''.join(reversed(remainders))
            else:
                binary_number = "0"

            if fractional_part:
                binary_fraction = []
                count = 0
                while fractional_part > 0 and count < 10:
                    fractional_part = fractional_part * 2
                    binary_bit = int(fractional_part)
                    binary_fraction.append(str(binary_bit))
                    fractional_part -= binary_bit
                    count += 1
                binary_number = binary_number + '.' + ''.join(binary_fraction)
            return binary_number
        except ValueError:
            return "Error occured"
    else:
        try:
            integer_part = int(decimal_input)
        except ValueError:
            return "Error occured"
        remainders = []
        if integer_part:
            while integer_part > 0:
                remainder = integer_part % 2
                remainders.append(str(remainder))
                integer_part //= 2
            binary_number = ''.join(reversed(remainders))
            return binary_number
        else:
            return "0"

# ---------- Decimal to other number systems ----------

def decimal_to_octal(decimal_input):
    try:
        decimal_number = float(decimal_input)
        integer_part = int(decimal_number)
        fractional_part = decimal_number - integer_part
        remainders = []

        if integer_part == 0:
            octal_number = '0'
        else:
            while integer_part > 0:
                remainder = integer_part % 8
                remainders.append(str(remainder))
                integer_part //= 8
            octal_number = ''.join(reversed(remainders))

        if fractional_part:
            octal_fraction = []
            count = 0
            while fractional_part > 0 and count < 10:
                fractional_part *= 8
                digit = int(fractional_part)
                octal_fraction.append(str(digit))
                fractional_part -= digit
                count += 1
            octal_number = octal_number + '.' + ''.join(octal_fraction)
        return octal_number
    except ValueError:
        return "Invalid decimal input!"

def decimal_to_hexadecimal(decimal_input):
    try:
        decimal_number = float(decimal_input)
        integer_part = int(decimal_number)
        fractional_part = decimal_number - integer_part

        hex_digits = '0123456789ABCDEF'
        remainders = []

        if integer_part == 0:
            hex_number = '0'
        else:
            while integer_part > 0:
                remainder = integer_part % 16
                remainders.append(hex_digits[remainder])
                integer_part //= 16
            hex_number = ''.join(reversed(remainders))

        if fractional_part:
            hex_fraction = []
            count = 0
            while fractional_part > 0 and count < 10:
                fractional_part *= 16
                digit = int(fractional_part)
                hex_fraction.append(hex_digits[digit])
                fractional_part -= digit
                count += 1
            hex_number = hex_number + '.' + ''.join(hex_fraction)
        return hex_number
    except ValueError:
        return "Invalid decimal input!"

# ---------- Octal to other number systems ----------

def octal_to_binary(octal_input):
    if octal_input is None:
        return "Octal input missing!"
    octal_input = str(octal_input).strip()
    try:
        for digit in octal_input:
            if digit not in ['0','1','2','3','4','5','6','7','.']:
                return "Invalid Octal Input!"
        decimal_value = octal_to_decimal(octal_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_binary(str(decimal_value))
    except:
        return "Conversion error!"

def octal_to_decimal(octal_input):
    if octal_input is None:
        return "Invalid octal input!"
    octal_input = str(octal_input).strip()
    try:
        # validation: only digits 0–7 and optionally one '.'
        if octal_input.count('.') > 1:
            return "Invalid octal input!"
        for ch in octal_input:
            if ch == '.':
                continue
            if ch not in '01234567':
                return "Invalid octal input!"

        # conversion
        if '.' in octal_input:
            integer_part, fractional_part = octal_input.split('.')
            result = 0
            for i in range(len(integer_part)):
                result += int(integer_part[i]) * (8 ** (len(integer_part) - i - 1))
            for j in range(len(fractional_part)):
                result += int(fractional_part[j]) * (8 ** -(j + 1))
            return result
        else:
            result = 0
            for i in range(len(octal_input)):
                result += int(octal_input[i]) * (8 ** (len(octal_input) - i - 1))
            return result
    except Exception:
        return "Conversion error!"

def octal_to_hexadecimal(octal_input):
    if octal_input is None:
        return "Invalid Octal Input!"
    octal_input = str(octal_input).strip()
    try:
        decimal_value = octal_to_decimal(octal_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_hexadecimal(str(decimal_value))
    except:
        return "Conversion error!"

# ---------- Hexadecimal to other number systems ----------

def hexadecimal_to_binary(hex_input):
    if hex_input is None:
        return "Invalid hexadecimal input!"
    hex_input = str(hex_input).upper().strip()
    try:
        hex_digits = '0123456789ABCDEF'
        binary_map = {
            '0': '0000', '1': '0001', '2': '0010', '3': '0011',
            '4': '0100', '5': '0101', '6': '0110', '7': '0111',
            '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
            'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
        }

        # Validate characters
        for ch in hex_input:
            if ch == '.':
                continue
            if ch not in hex_digits:
                return "Invalid hexadecimal input!"

        if '.' in hex_input:
            integer_part, fractional_part = hex_input.split('.')
            bin_integer = ''.join([binary_map[d] for d in integer_part])
            bin_fraction = ''.join([binary_map[d] for d in fractional_part])
            return bin_integer + '.' + bin_fraction
        else:
            return ''.join([binary_map[d] for d in hex_input])
    except:
        return "Invalid hexadecimal input!"

def hexadecimal_to_decimal(hex_input):
    if hex_input is None:
        return "Invalid hexadecimal input!"
    hex_input = str(hex_input).upper().strip()
    try:
        hex_digits = '0123456789ABCDEF'
        if '.' in hex_input:
            integer_part, fractional_part = hex_input.split('.')
            result = 0
            for i in range(len(integer_part)):
                result += hex_digits.index(integer_part[i]) * (16 ** (len(integer_part) - i - 1))
            for j in range(len(fractional_part)):
                result += hex_digits.index(fractional_part[j]) * (16 ** -(j + 1))
            return result
        else:
            result = 0
            for i in range(len(hex_input)):
                result += hex_digits.index(hex_input[i]) * (16 ** (len(hex_input) - i - 1))
            return result
    except:
        return "Invalid hexadecimal input!"

def hexadecimal_to_octal(hex_input):
    if hex_input is None:
        return "Invalid hexadecimal input!"
    hex_input = str(hex_input).strip()
    try:
        decimal_value = hexadecimal_to_decimal(hex_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_octal(str(decimal_value))
    except:
        return "Conversion error!"

if __name__ == '__main__':
    app.run(debug=True)
