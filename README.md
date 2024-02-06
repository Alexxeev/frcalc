# frcalc - A simple fraction calculator
## Features
- Basic operations such as additition, substraction and multiplication
- Parentheses
- Integer part extraction
- Remember answer to use it in subsequent calculation

## Usage
Run `python frcalc.py` in the working folder to start a calculator.
- Use `/` symbol to denote a fraction:
```
> 5 + 1/3 + 12 + (1/4 + 1/3)
215/12
```
- Insert `i` symbol in the beginning of the expression to extract integer part:
```
> i 5 + 1/3 + 12 + (1/4 + 1/3)
17+11/12
```
- Use keyword `ans` to insert previously calculated answer
```
> 5 + 1/3 + 12 + (1/4 + 1/3)
215/12
> ans * (3/5 + 9/5)
43
```
- Use keyword `exit` to close the calculator.
