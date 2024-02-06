from typing import Iterable
from collections import deque
from math import *
from fractions import Fraction

ANSWER = 'ans'
BINARY_OPERATORS = '+-*/'
LEFT_PARENTHESIS = '('
RIGHT_PARENTHESIS = ')'
PARENTHESES = LEFT_PARENTHESIS + RIGHT_PARENTHESIS
OPERATOR_PRECEDENCE = {
    '*': 1,
    '/': 1,
    '+': 2,
    '-': 2,
}
OPERATOR_FUNCTION = {
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
}
 
def tokenize(formula: str) -> Iterable[str]:
    '''
    Converts input string into sequence of tokens.
    '''
    formula = formula.replace(' ', '')
    token = ""
    for symbol in formula:
        if symbol.isdigit():
            token += symbol
        elif symbol in BINARY_OPERATORS or symbol in PARENTHESES:
            if len(token) > 0:
                yield token
                token = ""
            yield symbol
        elif symbol in ANSWER:
            token += symbol
            if token == ANSWER:
                yield token
                token = ""
        else:
            raise ValueError('Unexpected symbol in formula: ', symbol)
    if len(token) > 0:
        yield token

def parse(tokens: Iterable[str]) -> Iterable[str]:
    '''
    Converts sequence of tokens into sequence
    of tokens that represents formula in postfix
    notation.
    '''
    stack = deque()
    for token in tokens:
        if token.isdigit() or token == ANSWER:
            yield token
        elif token in BINARY_OPERATORS:
            while is_not_left_parenthesis_on_top(stack) and is_precending(token, stack):
                yield stack.pop()
            stack.append(token)
        elif token == LEFT_PARENTHESIS:
            stack.append(token)
        elif token == RIGHT_PARENTHESIS:
            while is_not_left_parenthesis_on_top(stack):
                yield stack.pop()
            if len(stack) > 0 and stack[-1] != LEFT_PARENTHESIS:
                raise ValueError('Mismatched right parenthesis')
            stack.pop()      
    
    while len(stack) > 0:
        if stack[-1] == LEFT_PARENTHESIS:
            raise ValueError('Mismatched left parenthesis')
        yield stack.pop()

def is_not_left_parenthesis_on_top(stack: deque) -> bool:
    return len(stack) > 0 and stack[-1] != LEFT_PARENTHESIS

def is_precending(operator: str, stack: deque) -> bool:
    return OPERATOR_PRECEDENCE[stack[-1]] < OPERATOR_PRECEDENCE[operator]

def evaluate(formula: Iterable[str], prev_answer: Fraction) -> Fraction:
    '''
    Evaluates formula in postfix notation.
    '''
    stack = deque()
    for token in formula:
        if token.isdigit():
            fraction = Fraction(int(token), 1)
            stack.append(fraction)
        elif token == ANSWER:
            stack.append(prev_answer)
        elif token in BINARY_OPERATORS:
            op2, op1 = stack.pop(), stack.pop()
            result = OPERATOR_FUNCTION[token](op1, op2)
            stack.append(result)
    if len(stack) != 1:
        raise ValueError('Syntax error in formula')
    return stack.pop()

def extract_integer_part(frac: Fraction) -> str:
    '''
    Returns a string representation of fraction of form k+n/m,
    where k is integer and n and m are natural numbers and n < m
    '''
    integer_part = int(modf(frac)[1])
    if (integer_part != 0):
        new_numerator = abs(frac.numerator) - (frac.denominator * abs(integer_part))
        new_fraction = Fraction(new_numerator, frac.denominator)
        return f'{integer_part}+{new_fraction}' if integer_part > 0 else f'-({abs(integer_part)}+{new_fraction})'
    else:
        return frac

def calculate(frac_input: str, prev_answer: Fraction):
    tokens = tokenize(frac_input)
    formula = parse(tokens)
    return evaluate(formula, prev_answer)
    
def main():
    ans = Fraction(0, 1)
    while True:
        frac_input = input('> ')
        if not frac_input:
            continue
        if frac_input == 'exit':
            return
        extract = False
        if (frac_input.startswith('i ')):
            extract = True
        frac_input = frac_input.removeprefix('i ')
        ans = calculate(frac_input, ans)
        print(extract_integer_part(ans) if extract else ans)

if __name__ == '__main__':
    main()