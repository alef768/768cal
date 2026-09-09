import shlex
import sys

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

# MATH FUNCS
def diff(args, line_no):
    args0 = mathargs(args)
    while len(args0) != 1:
        args0[0] = args0[0] - args0[1]
        args0.pop(1)
    variables["TEMPVAL"] = args0[0]
    return

def pow0(args, line_no):
    args = sub_vars(args[1:])
    try:
        variables["TEMPVAL"] = pow(float(args[0]), float(args[1]))
        return
    except ValueError:
        raise ValueError("All math arguments must be numeric!")

def prod(args, line_no):
    args0 = mathargs(args)
    while len(args0) != 1:
        args0[0] = args0[0] * args0[1]
        args0.pop(1)
    variables["TEMPVAL"] = args0[0]
    return

def quot(args, line_no):
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
        variables["TEMPVAL"] = float(args[0]) ** (1 / float(args[1]))
        return
    except ValueError:
        raise ValueError("All math arguments must be numeric!")
    except ZeroDivisionError:
        raise ZeroDivisionError("Root degree cannot be zero!")

def sum0(args, line_no):
    args0 = mathargs(args)
    while len(args0) != 1:
        args0[0] = args0[0] + args0[1]
        args0.pop(1)
    variables["TEMPVAL"] = args0[0]
    return

def tempset(args, line_no):
    if " " not in args[1]:
        variables[args[1]] = variables["TEMPVAL"]
        return
    raise ValueError(
        f"Invalid variable name!"
        )

def tempval(args, line_no):
    variables["TEMPVAL"] = sub_vars(args[1])
    return

def txtin(args, line_no):
    variables["TEMPVAL"] = input(sub_vars(args[1]))
    return

def txtout(args, line_no):
    print(sub_vars(args[1]))
    return

### KEYWORDS
# argsno as 0 means no fixed amount of inputs
run = {
    "*": {
        "func": comment,
        "argsno": 0,
        },
    "DIFF": {
        "func": diff,
        "argsno": 0,
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
    }

### PARSE
print(f"Running {path}\n")
for no, line in enumerate(code, start=1):
    try:
        args0 = shlex.split(line)

        if not args0:
            continue
        keyword = args0[0]

        if keyword not in run:
            raise ValueError(
                f"Unknown keyword {keyword}"
            )
        args0no = run[keyword]["argsno"]
        
        if keyword == "*":
            continue
        
        if args0no and args0no != len(args0):
            raise ValueError(
                f"{keyword} requires {args0no} arguments!"
            )
        run[keyword]["func"](args0, no)

    except KeyError as e:
        print(f"Error at line {no}: Invalid variable {e}")
    except Exception as e:
        print(f"Error at line {no}: {e}")

input(f"\nProgram finished... Press ENTER to exit...")
