def resolve(s, e):
    #return e.get(s, None)
    if s in e:
        return e[s]
    else:
        return None

def set_statement(v, e):
    assert len(v) == 3
    assert v[0] == "set"
    assert type(v[1]) is str
    e[v[1]] = evaluate(v[2], e)
    return None
def if_statement(v, e):
    assert len(v) == 4
    assert v[0] == "if"
    assert type(v[1]) is list

    if(evaluate(v[1], e)):
        return evaluate(v[2],e)
    else:
        return evaluate(v[3],e)

def while_statement(v, e):
    assert len(v) == 3
    assert v[0] == "while"
    assert type(v[1]) is list

    while(evaluate(v[1], e)):
        evaluate(v[2],e)
    return None

def begin_statement(v, e):
    assert len(v) == 3
    assert v[0] == "begin"
    for item in v[1:]:
        result = evaluate(item, e)
    return result


def evaluate(v, env):
    if type(v) is list:
        if len(v) == 0:
            return None
        assert type(v[0]) is str
        if v[0] == "set":
            return set_statement(v, env)
        if v[0] == "if":
            return if_statement(v, env)
        if v[0] == "while":
            return while_statement(v, env)
        if v[0] == "begin":
            return begin_statement(v, env)
        f = resolve(v[0], env)
        assert callable(f)
        values = [evaluate(value, env) for value in v[1:]]
        return f(values, env)
    if type(v) is str:
        return resolve(v, env) 
    return v 

env = {
    'x': 3,
    'y': 4,
    '+': lambda v, e: sum(v),
    '-': lambda v, e: v[0] - v[1],
    '*': lambda v, e: v[0] * v[1],
    '/': lambda v, e: v[0] / v[1],
    'print': lambda v, e: print(v),
    '<': lambda v, e: v[0] < v[1],
    '?': lambda v ,e: print(e),
}

def test_evaluate():
    print("test evaluate")
    assert evaluate(1, env) == 1
    assert evaluate(1.2, env) == 1.2
    assert evaluate('x', env) == 3
    assert evaluate(['+', 11, 22], env) == 33
    assert evaluate(['+', ['+', 11, 22], 22], env) == 55
    assert evaluate(['-', 33, 22], env) == 11
    assert evaluate(['*', 33, 2], env) == 66
    assert evaluate(['/', 33, 3], env) == 11
    assert evaluate(['set', 'q', 7], env) == None
    assert env['q'] == 7
    assert evaluate(['set', 'q', 77], env) == None
    assert env['q'] == 77
    assert evaluate(['set', 'q', ['+', 5, 6]], env) == None
    assert env['q'] == 11
    evaluate(['print', 2, 3, 4], env)

    assert evaluate(['if',['<',5,10],['+',2,1],['+',2,2]], env) == 3
    evaluate(['set','i',1], env)
    assert evaluate(['while',['<','i',10],['set','i',['+','i',1]]], env) == None
    assert evaluate('i', env) == 10

    evaluate(['?'],env)

    assert evaluate(['begin',['+',2,1],['+',2,2]], env) == 4

    assert evaluate(['if',['<',5,10],['begin',['+',2,1],['+',2,2]],['+',2,2]], env) == 4


def test_resolve():
    print("test resolve")
    env = {
        'x': 3,
        'y': 4
    }
    assert resolve('x', env) == 3
    assert resolve('y', env) == 4

if __name__ == "__main__":
    test_evaluate()
    test_resolve()
    print("done")