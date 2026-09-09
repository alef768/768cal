import shlex

### DECLARE VARS
CAL768_TEMPVAL = 0

### OPEN SCRIPT
while True:
    # request script path
    path = "E://python//Projects//768cal//script.768cal"
    
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

# print content
print("\nRaw contents:")
print(content)

### READ SCRIPT
code = content.splitlines()
print("\nCode list:")
print(code)
print()

### FUNCTIONS
def comment(args, args2):
    print(f"@ Line {args2} This is a comment")

def txtout(args, args2):
    print(args[1])

### KEYWORDS
run = {
    "//": {
        "func": comment,
        },
    "TXTOUT": {
        "func": txtout,
        },
    }

### PARSE
print(f"Running...\n")
for no, line in enumerate(code, start=1):
    try:
        args = shlex.split(line)

        if not args:
            continue

        if args[0] not in run:
            print(f"Error at line {no}")
            break
        run[args[0]]["func"](args, no)
    except ValueError:
        print(f"Error at line {no}")
        break
    
input()
