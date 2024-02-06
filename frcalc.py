from typing import Iterable
from collections import deque
from math import *
from fractions import Fraction
from dataclasses import dataclass

ANSWER = 'ans'
MINUS = '-'
EXPONENT = '^'
OPERATORS = '^*/+-'
LEFT_PARENTHESIS = '('
RIGHT_PARENTHESIS = ')'
PARENTHESES = LEFT_PARENTHESIS + RIGHT_PARENTHESIS
OPERATOR_PRECEDENCE = {
    '^': 1,
    '*': 2,
    '/': 2,
    '+': 3,
    '-': 3,
}
OPERATOR_FUNCTION = {
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '^': lambda x, y: x ** y,
}

UNARY_OPERATOR_FUNCTION = {
    '-': lambda x: -x,
}

@dataclass
class Token():
    value: str
    arity: int
 
def tokenize(formula: str) -> Iterable[Token]:
    '''
    Converts input string into sequence of tokens.
    '''
    formula = formula.replace(' ', '')
    digits = ""
    previous_symbol = ''
    for symbol in formula:
        if symbol.isdigit():
            digits += symbol
        elif symbol in OPERATORS or symbol in PARENTHESES:
            if symbol == MINUS and (previous_symbol == '' or previous_symbol in OPERATORS or previous_symbol == LEFT_PARENTHESIS):
                yield Token(symbol, 1)
            else:
                if len(digits) > 0:
                    yield Token(digits, 0)
                    digits = ""
                yield Token(symbol, 2)
        elif symbol in ANSWER:
            digits += symbol
            if digits == ANSWER:
                yield Token(digits, 0)
                digits = ""
        else:
            raise ValueError('Unexpected symbol in formula: ', symbol)
        previous_symbol = symbol
    if len(digits) > 0:
        yield Token(digits, 0)

def parse(tokens: Iterable[Token]) -> Iterable[Token]:
    '''
    Converts sequence of tokens into sequence
    of tokens that represents formula in postfix
    notation.
    '''
    stack = deque[Token]()
    for token in tokens:
        value = token.value
        if value.isdigit() or value == ANSWER:
            yield token
        elif value in OPERATORS:
            while is_not_left_parenthesis_on_top(stack) and is_precending(token, stack):
                yield stack.pop()
            stack.append(token)
        elif value == LEFT_PARENTHESIS:
            stack.append(token)
        elif value == RIGHT_PARENTHESIS:
            while is_not_left_parenthesis_on_top(stack):
                yield stack.pop()
            if len(stack) > 0 and stack[-1].value != LEFT_PARENTHESIS:
                raise ValueError('Mismatched right parenthesis')
            stack.pop()    
    
    while len(stack) > 0:
        if stack[-1].value == LEFT_PARENTHESIS:
            raise ValueError('Mismatched left parenthesis')
        yield stack.pop()

def is_not_left_parenthesis_on_top(stack: deque) -> bool:
    return len(stack) > 0 and stack[-1].value != LEFT_PARENTHESIS

def is_precending(operator: Token, stack: deque) -> bool:
    precedence1 = 0 if stack[-1].arity == 1 else OPERATOR_PRECEDENCE[stack[-1].value]
    precedence2 = 0 if operator.arity == 1 else OPERATOR_PRECEDENCE[operator.value]
    return precedence1 < precedence2 or (precedence1 == precedence2 and operator.value != EXPONENT)

def evaluate(formula: Iterable[Token], prev_answer: Fraction) -> Fraction:
    '''
    Evaluates formula in postfix notation.
    '''
    stack = deque()
    for token in formula:
        value = token.value
        if value.isdigit():
            fraction = Fraction(int(value), 1)
            stack.append(fraction)
        elif value == ANSWER:
            stack.append(prev_answer)
        elif value in OPERATORS and token.arity == 1:
            op = stack.pop()
            result = UNARY_OPERATOR_FUNCTION[token.value](op)
            stack.append(result)
        elif value in OPERATORS:
            op2, op1 = stack.pop(), stack.pop()
            result = OPERATOR_FUNCTION[token.value](op1, op2)
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