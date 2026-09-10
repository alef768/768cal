import math
import shlex
import sys
import time

### OPEN SCRIPT
content = ""
while True:
    # request script path
    path = input("Script path: ")

    # process script path
    try:
        if not path.lower().endswith(".768cal"):
            # except invalid extension
            print(f"Invalid file type! (Expected .768cal)")
            continue
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            break
    except FileNotFoundError:
        print(f"File not found!")
    except PermissionError:
        print(f"File cannot be accessed!")
    except OSError as e:
        if e.errno == 22:
            print("Path contains invalid arguments!")
            continue
        print(f"Error: {e}")
    except Exception as e:
        print(f"File error: {e}")

# print content
verbose = input("Display processed details of script? NONE/ANY: ")
if verbose:
    print("Raw contents:")
    print(content)

### READ SCRIPT
code = content.splitlines()
if verbose:
    print("\nCode list:")
    print(code)
    print()

### VARIABLES
variables = {
    "TEMPVAL": "0",
    }

### FUNCTIONS
## HELPER FUNCS
def check_linetarget(linetarget):
    try:
        linetarget = int(linetarget)
    except ValueError:
        raise ValueError("Number argument must be numeric!")

    if not 1 <= linetarget <= len(code):
        raise ValueError(f"Invalid line number {linetarget}!")
    return linetarget

def compare(left, operator, right):
    # left usually TEMPVAL
    try:
        left = float(left)
        right = float(right)
    except (ValueError, TypeError):
        left = str(left)
        right = str(right)

    match operator:
        case "==":
            return left == right
        case "!=":
            return left != right
        case ">":
            return left > right
        case "<":
            return left < right
        case ">=":
            return left >= right
        case "<=":
            return left <= right
        case _:
            raise ValueError(f"Unknown operator: {operator}")

def eval_if(args, negate=False):
    args = sub_vars(args[1:])
    operator = args[0]
    subject = args[1]
    linetarget = check_linetarget(args[2])
    
    result = compare(variables["TEMPVAL"], operator, subject)

    if negate:
        result = not result

    if result:
        return linetarget

def sub_vars(text):
    if isinstance(text, str):
        for name, val in variables.items():
            placeholder = f"&{name}&"
            
            text = text.replace(placeholder, str(val))
        return text

    if isinstance(text, list):
        text = [sub_vars(item) for item in text]
        return text

    return text

def mathargs(args):
    # applicable to operations w/ multiple inputs
    args = sub_vars(args[1:])
    try:
        args = [float(x) for x in args]
    except ValueError:
        raise ValueError("All math arguments must be numeric!")
    return args

## MAIN FUNCS
def comment(args, line_no):
    pass

def goto(args, line_no):
    return check_linetarget(args[1])

def diff(args, line_no):
    if len(args) < 3:
        raise ValueError(
            f"{args[0]} requires at least 3 arguments!"
        )
    args0 = mathargs(args)
    while len(args0) != 1:
        args0[0] = args0[0] - args0[1]
        args0.pop(1)
    variables["TEMPVAL"] = args0[0]
    return

def if0(args, line_no):
    return eval_if(args)

def ifnot(args, line_no):
    return eval_if(args, True)

def pow0(args, line_no):
    args = sub_vars(args[1:])
    try:
        base = float(args[0])
        exponent = float(args[1])
    except ValueError:
        raise ValueError("All math arguments must be numeric!")

    if base < 0 and not exponent.is_integer():
        raise ValueError("Negative bases require integer exponents!")

    variables["TEMPVAL"] = pow(float(args[0]), float(args[1]))

def prod(args, line_no):
    if len(args) < 3:
        raise ValueError(
            f"{args[0]} requires at least 3 arguments!"
        )
    args0 = mathargs(args)
    while len(args0) != 1:
        args0[0] = args0[0] * args0[1]
        args0.pop(1)
    variables["TEMPVAL"] = args0[0]
    return

def quot(args, line_no):
    if len(args) < 3:
        raise ValueError(
            f"{args[0]} requires at least 3 arguments!"
        )
    args0 = mathargs(args)
    try:
        while len(args0) != 1:
            args0[0] = args0[0] / args0[1]
            args0.pop(1)
    except ZeroDivisionError:
        raise ZeroDivisionError("Cannot divide by zero!")
    variables["TEMPVAL"] = args0[0]
    return

def root(args, line_no):
    args = sub_vars(args[1:])
    try:
        number = float(args[0])
        degree = float(args[1])
    except ValueError:
        raise ValueError("All math arguments must be numeric!")

    if degree == 0:
        raise ZeroDivisionError("Root degree cannot be zero!")
    
    if number < 0:
        if not degree.is_integer():
            raise ValueError("Negative numbers require odd integer root degrees!")
        if int(degree) % 2 == 0:
            raise ValueError("Even root degrees of negative numbers are complex!")
        variables["TEMPVAL"] = -(abs(number) ** (1 / degree))
        return

    variables["TEMPVAL"] = number ** (1 / degree)
    return

def sum0(args, line_no):
    if len(args) < 3:
        raise ValueError(
            f"{args[0]} requires at least 3 arguments!"
        )
    args0 = mathargs(args)
    while len(args0) != 1:
        args0[0] = args0[0] + args0[1]
        args0.pop(1)
    variables["TEMPVAL"] = args0[0]
    return

def tempset(args, line_no):
    if not args[1].isidentifier():
        raise ValueError("Invalid variable name!")

    variables[args[1]] = variables["TEMPVAL"]

def tempval(args, line_no):
    variables["TEMPVAL"] = sub_vars(args[1])
    return

def txtin(args, line_no):
    variables["TEMPVAL"] = input(sub_vars(args[1]))
    return

def txtout(args, line_no):
    print(sub_vars(args[1]))
    return

def wait(args, line_no):
    try:
        time.sleep(float(args[1]))
        return
    except ValueError:
        raise ValueError("Number argument must be numeric!")

### KEYWORDS
# argsno as 0 means no fixed amount of inputs
run = {
    "*": {
        "func": comment,
        "argsno": 0,
        },
    "@": {
        "func": goto,
        "argsno": 2,
        },
    "DIFF": {
        "func": diff,
        "argsno": 0,
        },
    "@IF": {
        "func": if0,
        "argsno": 4,
        },
    "@IF!": {
        "func": ifnot,
        "argsno": 4,
        },
    "POW": {
        "func": pow0,
        "argsno": 3,
        },
    "PROD": {
        "func": prod,
        "argsno": 0,
        },
    "QUOT": {
        "func": quot,
        "argsno": 0,
        },
    "ROOT": {
        "func": root,
        "argsno": 3,
        },
    "SUM": {
        "func": sum0,
        "argsno": 0,
        },
    "TEMPSET": {
        "func": tempset,
        "argsno": 2,
        },
    "TEMPVAL": {
        "func": tempval,
        "argsno": 2,
        },
    "TXTIN": {
        "func": txtin,
        "argsno": 2,
        },
    "TXTOUT": {
        "func": txtout,
        "argsno": 2,
        },
    "WAIT": {
        "func": wait,
        "argsno": 2,
        },
    }

### PARSE
print(f"Running {path}\n")

no = 1
while no <= len(code):
    line = code[no - 1]

    try:
        args0 = shlex.split(line)

        if not args0:
            no += 1
            continue
        keyword = args0[0]

        if keyword not in run:
            raise ValueError(
                f"Unknown keyword {keyword}"
            )

        args0no = run[keyword]["argsno"]
        
        if keyword == "*":
            no += 1
            continue
        
        if args0no and args0no != len(args0):
            raise ValueError(
                f"{keyword} requires {args0no} arguments!"
            )
        lineto = run[keyword]["func"](args0, no)
        if lineto is None:
            no += 1
            continue
        no = lineto

    except KeyError as e:
        print(f"Error at line {no}: Invalid variable {e}")
        break
    except Exception as e:
        print(f"Error at line {no}: {e}")
        break

input(f"\nProgram finished... Press ENTER to exit...")
