from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

# --- Helper Functions (Define ALL functions first) ---

# Binary to other number system convertions.
def binary_to_decimal(binary_input):
    if binary_input is None:
        return "Binary input missing!"
    binary_input = str(binary_input).strip()
    if binary_input == "":
        return "Binary input missing!"

    result = 0

    if '.' in binary_input:
        try:
            # Check for multiple decimal points
            if binary_input.count('.') > 1:
                return "Invalid binary input!"
                
            integer_part, fractional_part = binary_input.split('.')
            
            # Handle empty parts like ".101" or "101."
            if not integer_part:
                integer_part = "0"
            if not fractional_part:
                fractional_part = "0"

            for digit in integer_part + fractional_part:
                if digit not in ['0', '1']:
                    return "Binary inputs can only be 0s and 1s"
            
            # Convert integer part
            for i in range(len(integer_part)):
                digit = int(integer_part[i])
                power = len(integer_part) - i - 1
                result = result + digit * (2 ** power)
            
            # Convert fractional part
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

    if '.' in binary_input:
        if binary_input.count('.') > 1:
            return "Invalid binary input!"
        integer_part, fractional_part = binary_input.split('.')
        if not integer_part:
            integer_part = "0"
        if not fractional_part:
            fractional_part = "0"
    else:
        integer_part = binary_input
        fractional_part = ''

    for ch in integer_part + fractional_part:
        if ch not in ('0', '1', ''):
            return "Binary inputs can only be 0s and 1s"

    # Pad integer part
    while len(integer_part) % 4 != 0:
        integer_part = '0' + integer_part
    if not integer_part: # Handle case of just ".101"
        integer_part = "0000"

    hex_integer = ''
    for i in range(0, len(integer_part), 4):
        four_bit_group = integer_part[i:i+4]
        hex_integer += hexadecimal_values.get(four_bit_group, '?')
    
    # Remove leading zeros unless it's the only digit
    if len(hex_integer) > 1 and hex_integer.startswith('0'):
       hex_integer = hex_integer.lstrip('0')

    hex_fraction = ''
    if fractional_part:
        # Pad fractional part
        while len(fractional_part) % 4 != 0:
            fractional_part = fractional_part + '0'
        for i in range(0, len(fractional_part), 4):
            four_bit_group = fractional_part[i:i+4]
            hex_fraction += hexadecimal_values.get(four_bit_group, '?')
        # Remove trailing zeros from fraction
        hex_fraction = hex_fraction.rstrip('0')

    if hex_fraction:
        return hex_integer + '.' + hex_fraction
    else:
        return hex_integer

def decimal_to_binary(decimal_input):
    if decimal_input is None:
        return "Decimal input missing!"
    decimal_input = str(decimal_input).strip()
    try:
        decimal_number = float(decimal_input)
    except ValueError:
        return "Invalid decimal input!"

    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part
    remainders = []

    if integer_part == 0:
        binary_number = "0"
    else:
        while integer_part > 0:
            remainder = integer_part % 2
            remainders.append(str(remainder))
            integer_part //= 2
        binary_number = ''.join(reversed(remainders))

    if fractional_part > 0:
        binary_fraction = []
        count = 0
        # Limit precision to avoid infinite loops
        while fractional_part > 0 and count < 10:
            fractional_part = fractional_part * 2
            binary_bit = int(fractional_part)
            binary_fraction.append(str(binary_bit))
            fractional_part -= binary_bit
            count += 1
        binary_number = binary_number + '.' + ''.join(binary_fraction)
    
    return binary_number

def decimal_to_octal(decimal_input):
    try:
        decimal_number = float(decimal_input)
    except ValueError:
        return "Invalid decimal input!"
        
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

    if fractional_part > 0:
        octal_fraction = []
        count = 0
        while fractional_part > 0 and count < 10: # Limit precision
            fractional_part *= 8
            digit = int(fractional_part)
            octal_fraction.append(str(digit))
            fractional_part -= digit
            count += 1
        octal_number = octal_number + '.' + ''.join(octal_fraction)
    return octal_number

def decimal_to_hexadecimal(decimal_input):
    try:
        decimal_number = float(decimal_input)
    except ValueError:
        return "Invalid decimal input!"
        
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

    if fractional_part > 0:
        hex_fraction = []
        count = 0
        while fractional_part > 0 and count < 10: # Limit precision
            fractional_part *= 16
            digit = int(fractional_part)
            hex_fraction.append(hex_digits[digit])
            fractional_part -= digit
            count += 1
        hex_number = hex_number + '.' + ''.join(hex_fraction)
    return hex_number

def octal_to_decimal(octal_input):
    if octal_input is None:
        return "Invalid octal input!"
    octal_input = str(octal_input).strip()
    try:
        if octal_input.count('.') > 1:
            return "Invalid octal input!"
        
        integer_part = octal_input
        fractional_part = ""
        
        if '.' in octal_input:
            integer_part, fractional_part = octal_input.split('.')
            if not integer_part:
                integer_part = "0"
            if not fractional_part:
                fractional_part = "0"

        for ch in integer_part + fractional_part:
            if ch not in '01234567':
                return "Invalid octal input!"

        result = 0
        # Convert integer part
        for i in range(len(integer_part)):
            result += int(integer_part[i]) * (8 ** (len(integer_part) - i - 1))
        # Convert fractional part
        for j in range(len(fractional_part)):
            result += int(fractional_part[j]) * (8 ** -(j + 1))
        return result
        
    except Exception:
        return "Conversion error!"

def hexadecimal_to_decimal(hex_input):
    if hex_input is None:
        return "Invalid hexadecimal input!"
    hex_input = str(hex_input).upper().strip()
    
    try:
        hex_digits = '0123456789ABCDEF'
        
        integer_part = hex_input
        fractional_part = ""

        if '.' in hex_input:
            if hex_input.count('.') > 1:
                return "Invalid hexadecimal input!"
            integer_part, fractional_part = hex_input.split('.')
            if not integer_part:
                integer_part = "0"
            if not fractional_part:
                fractional_part = "0"

        for ch in integer_part + fractional_part:
            if ch not in hex_digits:
                return "Invalid hexadecimal input!"
        
        result = 0
        # Convert integer part
        for i in range(len(integer_part)):
            result += hex_digits.index(integer_part[i]) * (16 ** (len(integer_part) - i - 1))
        # Convert fractional part
        for j in range(len(fractional_part)):
            result += hex_digits.index(fractional_part[j]) * (16 ** -(j + 1))
        return result
    except Exception:
        return "Invalid hexadecimal input!"

# --- REFACTORED/DRY Functions ---
# These functions reuse the ones above

def binary_to_octal(binary_input):
    """
    Refactored to be DRY (Don't Repeat Yourself).
    Converts Binary -> Decimal -> Octal.
    """
    if binary_input is None:
        return "Binary input missing!"
    binary_input = str(binary_input).strip()
    
    # 1. First, convert binary to decimal
    decimal_value = binary_to_decimal(binary_input)
    
    if isinstance(decimal_value, str):
        # This means binary_to_decimal returned an error message
        return decimal_value
        
    # 2. Now, reuse your existing function to convert decimal to octal
    return decimal_to_octal(str(decimal_value))

def octal_to_binary(octal_input):
    """
    Converts Octal -> Decimal -> Binary.
    """
    if octal_input is None:
        return "Octal input missing!"
    octal_input = str(octal_input).strip()
    try:
        decimal_value = octal_to_decimal(octal_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_binary(str(decimal_value))
    except Exception:
        return "Conversion error!"

def octal_to_hexadecimal(octal_input):
    """
    Converts Octal -> Decimal -> Hexadecimal.
    """
    if octal_input is None:
        return "Invalid Octal Input!"
    octal_input = str(octal_input).strip()
    try:
        decimal_value = octal_to_decimal(octal_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_hexadecimal(str(decimal_value))
    except Exception:
        return "Conversion error!"

def hexadecimal_to_binary(hex_input):
    """
    Converts Hexadecimal -> Decimal -> Binary.
    (Note: Direct conversion is often faster, but this reuses code)
    """
    if hex_input is None:
        return "Invalid hexadecimal input!"
    hex_input = str(hex_input).strip()
    try:
        decimal_value = hexadecimal_to_decimal(hex_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_binary(str(decimal_value))
    except Exception:
        return "Conversion error!"


def hexadecimal_to_octal(hex_input):
    """
    Converts Hexadecimal -> Decimal -> Octal.
    (FIXED TYPO: hex_input)
    """
    if hex_input is None: # Fixed typo here
        return "Invalid hexadecimal input!"
    hex_input = str(hex_input).strip()
    try:
        decimal_value = hexadecimal_to_decimal(hex_input)
        if isinstance(decimal_value, str):
            return decimal_value
        return decimal_to_octal(str(decimal_value))
    except Exception:
        return "Conversion error!"

# --- CONVERSION_MAP (Must be defined AFTER functions) ---

CONVERSION_MAP = {
    ('binary', 'decimal'): binary_to_decimal,
    ('binary', 'octal'): binary_to_octal,
    ('binary', 'hexadecimal'): binary_to_hexadecimal,
    ('decimal', 'binary'): decimal_to_binary,
    ('decimal', 'octal'): decimal_to_octal,
    ('decimal', 'hexadecimal'): decimal_to_hexadecimal,
    ('octal', 'binary'): octal_to_binary,
    ('octal', 'decimal'): octal_to_decimal,
    ('octal', 'hexadecimal'): octal_to_hexadecimal,
    ('hexadecimal', 'binary'): hexadecimal_to_binary,
    ('hexadecimal', 'decimal'): hexadecimal_to_decimal,
    ('hexadecimal', 'octal'): hexadecimal_to_octal,
}

# --- Flask Routes ---

@app.route('/')
def home():
    # This route still renders the full page, which is correct
    return render_template('index.html', from_option='binary', to_option='decimal')

@app.route('/calculate', methods=['POST'])
def check_convertion():
    from_option = request.form.get('from-option')
    to_option = request.form.get('to-option')
    input_number = request.form.get('input-number')
    result = "" # Default result

    # Basic guards
    if input_number is None or str(input_number).strip() == "":
        result = "Please enter a number to convert."
        # *** CHANGED ***
        # Instead of rendering a template, return JSON
        return jsonify({'result': result})
        
    elif from_option == to_option:
        result = "You chose the same convertion! Try different one."
        return jsonify({'result': result})
        
    else:
        # Use the dispatch map
        conversion_key = (from_option, to_option)
        
        if conversion_key in CONVERSION_MAP:
            # Look up the correct function from the map
            conversion_function = CONVERSION_MAP[conversion_key]
            # Call it
            input_val = str(input_number).strip()
            result = conversion_function(input_val)
        else:
            # This should ideally not be reachable
            result = "Error: Conversion type not supported."
    # Return the final result as JSON
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)