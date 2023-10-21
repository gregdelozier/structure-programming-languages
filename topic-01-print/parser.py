# Assuming the tokens are generated and stored in a list called 'tokens'.
# We'll use a global pointer 'current_token_index' to keep track of the current token being processed.

tokens = []  # Example: ["print", ["NUMBER", 1], "+", ["NUMBER", 2], ";", "{", ...]
current_token_index = 0

def get_current_token():
    global current_token_index
    if current_token_index < len(tokens):
        return tokens[current_token_index]
    return None

def consume_token():
    global current_token_index
    current_token_index += 1

def parse(program_tokens):
    global tokens
    global current_token_index
    current_token_index = 0
    tokens = program_tokens
    statements = []
    while get_current_token() is not None:
        statements.append(parse_statement())
    # return {"type": "program", "statements": statements}
    return ["program", statements]

def parse_statement():
    current_token = get_current_token()
    if current_token == "print":
        consume_token()  # Consume 'print'
        expr = parse_expression()
        if get_current_token() != ";":
            raise Exception("Expected ';'")
        consume_token()
        # return {"type": "print", "expression": expr}
        return ["print", expr]
    elif current_token == "{":
        return parse_block()
    else:
        raise Exception("Unexpected token in statement")

def parse_block():
    consume_token()  # Consume '{'
    statements = []
    while get_current_token() != "}":
        statements.append(parse_statement())
    consume_token()  # Consume '}'
    # return {"type": "block", "statements": statements}
    return ["block", statements]

def parse_expression():
    left_term = parse_term()
    while get_current_token() in ["+", "-"]:
        op = get_current_token()
        consume_token()
        right_term = parse_term()
        # left_term = {"type": "binary", "left": left_term, "operator": op, "right": right_term}
        left_term = [op, left_term, right_term, 1]
    return left_term

def handle_number_signs():
    multiplier = 1
    while get_current_token() in ["+", "-"]:
        if get_current_token() == "-":
            multiplier *= -1
        consume_token()
    return multiplier

def parse_term():
    left_factor = parse_factor()
    while get_current_token() in ["*", "/"]:
        op = get_current_token()
        consume_token()
        right_factor = parse_factor()
        left_factor = [op, left_factor, right_factor, 1]
        #left_factor = {"type": "binary", "left": left_factor, #"operator": op, "right": right_factor}
    return left_factor

def parse_factor():
    multiplier = handle_number_signs()
    current_token = get_current_token()
    if isinstance(current_token, list) and current_token[0] == "NUMBER":
        consume_token()
        #return {"type": "number", "value": current_token[1]}
        return ["NUMBER", multiplier * float(current_token[1])]
    elif current_token == "(":
        consume_token()  # Consume '('
        expr = parse_expression()
        if expr[0] != "NUMBER":
            expr[3] *= multiplier
        if get_current_token() != ")":
            raise Exception("Expected ')'")
        consume_token()  # Consume ')'
        return expr
    else:
        raise Exception("Unexpected token in factor")

# Example usage:

def test_parse():
    print("testing parse")
    program_tokens = ["print", ["NUMBER", 1], "+", ["NUMBER", 2], ";", "{", "print", ["NUMBER", 3], ";", "}"]
    ast = parse(program_tokens)
    assert ast == ['program', [['print', ['+', ['NUMBER', 1], ['NUMBER', 2]]], ['block', [['print', ['NUMBER', 3]]]]]]

    program_tokens = ['print', ['NUMBER', 3], '+', ['NUMBER', 4], '*', '(', ['NUMBER', 5], '-', ['NUMBER', 2], ')', ';']
    ast = parse(program_tokens)
    assert ast == ['program', [['print', ['+', ['NUMBER', 3], ['*', ['NUMBER', 4], ['-', ['NUMBER', 5], ['NUMBER', 2]]]]]]]

if __name__ == "__main__":
    test_parse
    print(parse(['print', '-', ['NUMBER', 3], '+', '-', ['NUMBER', 4], '*', '(', '-', '+', '-', '+', '-', '-', '-', '-', '-', '+', ['NUMBER', 5], '-', '-', ['NUMBER', 2], ')', '+', ['NUMBER', 3], '*', ['NUMBER', 2], '-', ['NUMBER', 1], '+', ['NUMBER', 0], ';']))
    print(parse(['print', ['NUMBER', 3], '+', '(', '-', ['NUMBER', 4], '*', ['NUMBER', 3], ')', '+', '-', '(', ['NUMBER', 4], '*', ['NUMBER', 5], ')', ';']))