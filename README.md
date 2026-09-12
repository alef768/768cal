# 768cal
(PROPER README.MD UPON RELEASE)

## What is 768cal?
768cal is a lightweight interpreted programming language written in Python. It is still in the works, so expect some bugs and missing features.

## Usage
For now, the main file is a Python file and pre-built executables will be available upon first stable release. 

### To run your first script:

1. Make sure you have Python 3.14.0 or later installed. (the Python version used to develop 768cal)
2. Download `768cal.py`.
3. Now anywhere in your computer, create a text file with the `.768cal` file extension.
    * This will serve as your script.
4. Now you can start writing code!
5. To run your code, run `768cal.py` that you have downloaded using Python.
6. Simply input the filepath of your script.
7. The program will then ask whether you want to view processing details.
    * (Enter none to skip or enter any other value to display them)
8. The program will proceed to run your script.

## Programming 768cal
Now, we will talk about the features, and keywords (available as of day 3) in this programming language.

### Comments
Turns the line into a comment, which the program ignores during runtime.

`* This is a comment!`

### TXTOUT
`TXTOUT` is the `print()` equivalent of 768cal.

`TXTOUT "Hello world!"`

### TEMPVAL
`TEMPVAL` serves as the temporary value buffer used by 768cal. It stores values as strings, and operations convert those values to the required datatype when necessary.

`TEMPVAL "Value"`

### TEMPSET
`TEMPSET` assigns the current value of `TEMPVAL` to a variable. If the variable does not already exist, it is created. This also allows creation of variables.

```
TEMPVAL "USD30"
TEMPSET "PRICE"
```

### Variable substitution
Now is probably a good time to talk about this. Variable substitution allows variables to be inserted into most argument inputs. It is indicated by `&VARIABLE_NAME&`. The example involving `TXTOUT`:

```
TEMPVAL "USD30"
TEMPSET "PRICE"
TXTOUT "The price is &PRICE&."
```
Outputs `The price is USD30.`

In this second example, variable substitution can also be used in assigning a value to `TEMPVAL`:

```
TEMPVAL "5"
TEMPSET "VAR_A"
TEMPVAL 8
TEMPVAL &VAR_A&
TEMPSET "VAR_B"
```

`VAR_B`'s value is 5, instead of 8.

### TXTIN
`TXTIN` is the `input()` equivalent of 768cal. The user's input will then be recorded to `TEMPVAL`.

```
TXTIN "What is your name? "
TEMPSET "name"
TXTOUT "It's nice to meet you, &name&!"
```

### Math operations
#### SUM
`SUM` returns the sum of all provided arguments (two or more), which will be recorded to `TEMPVAL`.

```
TEMPVAL "5"
TEMPSET "yourvar_a"
TEMPVAL 7
TEMPSET "yourvar_b"
SUM 5 10 &yourvar_a& 15 &yourvar_b&
TXTOUT &TEMPVAL&
```

Outputs `42.0`

Even though `TEMPVAL "5"` stores 5 as a string, it can still be used in calculations because math operations automatically convert values to the appropriate numeric type.

#### DIFF
`DIFF` returns the difference of all provided arguments (two or more), which will be recorded to `TEMPVAL`. It subtracts each argument from the previous result, from left to right.

```
TEMPVAL "5"
TEMPSET "yourvar_a"
TEMPVAL 7
TEMPSET "yourvar_b"
DIFF 5 10 &yourvar_a& 15 &yourvar_b&
TXTOUT &TEMPVAL&
```

Outputs `-32.0` 

#### PROD
`PROD` returns the product of all provided arguments (two or more), which will be recorded to `TEMPVAL`.

```
TEMPVAL "5"
TEMPSET "yourvar_a"
TEMPVAL 7
TEMPSET "yourvar_b"
PROD 5 10 &yourvar_a& 15 &yourvar_b&
TXTOUT &TEMPVAL&
```

Outputs `26250.0`

#### QUOT
`QUOT` returns the quotient of all provided arguments (two or more), which will be recorded to `TEMPVAL`. It divides the previous result by each argument, from left to right.

```
TEMPVAL "5"
TEMPSET "yourvar_a"
TEMPVAL 7
TEMPSET "yourvar_b"
QUOT 5 10 &yourvar_a& 15 &yourvar_b&
TXTOUT &TEMPVAL&
```

Outputs `0.0009523809523809525`

#### POW
`POW` returns the first argument raised to the power of the second argument. It only requires 2 arguments, and the result will be recorded to `TEMPVAL`.

```
TEMPVAL 4
POW &TEMPVAL& 2
TXTOUT "&TEMPVAL&"
```

Outputs `16.0`

#### ROOT
`ROOT` returns the root of the first argument with the second argument specifying root degree. Similarly, it also requires 2 arguments, and the result is recorded to `TEMPVAL`.

```
TEMPVAL 27
ROOT &TEMPVAL& 3
TXTOUT "&TEMPVAL&"
```

Outputs `3.0`

### WAIT
`WAIT` pauses the runtime for the specified amount of seconds. In this example:

```
TXTOUT "0 seconds"
WAIT 1
TXTOUT "1 second"
```

The program waits for 1 second before displaying `1 second`.

### @
`@` allows the program to jump to the specified line number. It also accepts variable substitution.

```
1: TXTOUT "Line 1"
2: @ 7
3: * This will not be displayed
4: TXTOUT "Line 4"
5: TXTOUT "Line 5"
6: * The following text will be displayed
7: TXTOUT "Line 7"
```

Outputs

```
Line 1
Line 7
```

Lines 3 - 6 are skipped because the program jumps from line 2 to line 7.

### Points
Points are labels assigned to specific lines. It is generally easier to use than line number-based jumps.

#### @<, @>
`@<` assigns a label to the following line, and `@>` jumps to the specified point. In this example:

```
1: TXTOUT "Line 1"
2: @> "point1"
3: * This will not be displayed
4: TXTOUT "Line 4"
5: TXTOUT "Line 5"
6: @< "point1"
7: TXTOUT "Line 7"
```

The `@< "point1"` in line 6 stores `"point1"` as a point, pointing towards line 7.

#### @GET
`@GET` returns the current line number, and is recorded to `TEMPVAL`.

```
1: @GET
2: TXTOUT "&TEMPVAL&"
```

Outputs `1`

### Conditionals
#### @IF
`@IF` compares the value stored in `TEMPVAL` with the specified value. If the condition is true, it jumps to the specified destination. It supports 6 comparison operators:
1. `==` / `TEMPVAL` exactly equal to
2. `!=` / `TEMPVAL` not exactly equal to
3. `>` / `TEMPVAL` is greater than
4. `<` / `TEMPVAL` is less than
5. `>=` / `TEMPVAL` is greater than or equal to
6. `<=` / `TEMPVAL` is less than or equal to

Its structure is as follows:

`@IF <operator> <value> <destination>`

Points in the destination argument are written as `@pointname`.

In this example using the equal operator `==`:

````
1: TXTIN "Y or N? "
2: 
3: @IF == "N" 6
4: TXTOUT "You said yes."
5: @ 7
6: TXTOUT "You said no."
7: TXTOUT "Line 7"
8: TXTOUT "END"
````

The user is asked to input Y or N, and the input is stored to `TEMPVAL`. The `@IF == "N" 6` in line 3 then evaluates whether `TEMPVAL` is equal to `"N"`. If it is true, the program jumps to line 6. If not, it does not jump and proceeds to line 4.

In this second example involving variable substitution and points:

````
TXTIN "How much is your budget? "
TEMPSET "budget"
TXTIN "How much is the price? "

@IF > &budget& @Notenoughbudget
TXTOUT "You can proceed to buy."
@> END
@< Notenoughbudget
TXTOUT "You don't have enough budget!"

@< END
````

`@IF` evaluates if `TEMPVAL` (containing the price) is greater than `budget`. In this case, the program automatically compares numerically (by converting to numerical) but if it fails to do so, it falls back to lexicographical comparison.

#### @IF!
`@IF!` is essentially `@IF`, but negates the result.

In this example:

````
TXTIN "How much is your budget? "
TEMPSET "budget"
TXTIN "How much are you going to buy? "

@IF! > &budget& @Enoughbudget
TXTOUT "You don't have enough budget!"
@> END
@< Enoughbudget
TXTOUT "You can proceed to buy."

@< END
````

If `TEMPVAL` is not greater than the budget, the program jumps to `Enoughbudget`.

### What's next?

768cal is still being developed, and more features, improvements, and changes will be implemented in the future. The features mentioned above are the ones currently in 768cal. As new changes are added, this README will update accordingly... occasionally.

As of now, planned features are about expanding math operations (+INV/*INV, ROUND/FLOOR/CEIL, MIN/MAX), and implementing string manipulation (STRLEN, STRCHAR, STRUP, STRLOW, etc.).

For now, expect bugs and, likely, changes to the language's syntax and behaviour.

Thanks for checking out 768cal!
