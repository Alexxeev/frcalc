from math import *
from fractions import Fraction
import re
import sys

REGEX_DIV = re.compile(r'(?P<num>((\d+(\.\d*)?)|(\.\d+)))/(?P<denom>((\d+(\.\d*)?)|(\.\d+)))')

#TODO
# 1. save answer
# 2. maybe get rid of eval and use something more safe?

def extract_integer_part(frac: Fraction) -> str:
    integer_part = int(modf(frac)[1])
    if (integer_part != 0):
        new_numerator = abs(frac.numerator) - (frac.denominator * abs(integer_part))
        new_fraction = Fraction(new_numerator, frac.denominator)
        return f'{integer_part}+{new_fraction}' if integer_part > 0 else f'-({abs(integer_part)}+{new_fraction})'
    else:
        return frac

def calculate(frac_input: str):
    frac_output = re.sub(REGEX_DIV, r'Fraction(\g<num>,\g<denom>)', frac_input)
    extract = False
    if (frac_output.startswith('-i ')):
        extract = True
        frac_output = frac_output.removeprefix('-i ')
    result = eval(frac_output)
    print(extract_integer_part(result) if extract else result)

def input_and_calculate():
    while True:
        frac_input = input('> ')
        if not frac_input:
            continue
        calculate(frac_input)

def main():
    if len(sys.argv) < 2:
        input_and_calculate()
    frac_input = sys.argv[1].replace(' ', '')
    calculate(frac_input)
    

if __name__ == '__main__':
    main()