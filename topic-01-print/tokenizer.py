import re

patterns = [
    [r"print", "print"],
    [r"number", "number"],
    [r"\d+(\.\d*)?", "NUMBER"],
    [r"\+", "+"],
    [r"-", "-"],
    [r"\*", "*"],
    [r"/", "/"],
    [r"\(", "("],
    [r"\)", ")"],
    [r"\{", "{"],
    [r"\}", "}"],
    [r"\;", ";"],
]


WHITESPACE = [" ", "\t", "\n"]


# general numeric literal conversion
def number(s):
    if "." in s:
        return float(s)
    else:
        return int(s)


# The lex function
def tokenize(characters):
    result = []
    pos = 0
    while pos < len(characters):
        if characters[pos] in WHITESPACE:
            pos += 1
            continue
        t = None
        for regex, token in patterns:
            pattern = re.compile(regex)
            match = pattern.match(characters, pos)
            if match:
                if token in ["NUMBER"]:
                    t = [token, number(match.group(0))]
                else:
                    t = token
                pos = match.end()
                break
        if t:
            result.append(t)
        else:
            raise Exception(f"Invalid character: {characters[pos]}")
    return result


def test_individual_tokens():
    print("testing individual tokens")
    for s in ["1", "22", "12.1", "0", "12.", "123145"]:
        assert tokenize(s) == [
            ["NUMBER", number(s)]
        ], f"Expected {[['NUMBER', s]]}, got {tokenize(s)}."
    examples = "+,-,*,/,(,),{,},;".split(",")
    for example in examples:
        assert tokenize(example) == [example]


def test_whitespace():
    print("testing whitespace")
    for s in ["1", "1  ", "  1", "  1  "]:
        assert tokenize(s) == [["NUMBER", 1]]


def test_multiple_tokens():
    print("testing multiple tokens")
    assert tokenize("1+2") == [["NUMBER", 1], "+", ["NUMBER", 2]]
    assert tokenize("1+2-3") == [["NUMBER", 1], "+", ["NUMBER", 2], "-", ["NUMBER", 3]]
    assert tokenize("3+4*(5-2)") == [
        ["NUMBER", 3],
        "+",
        ["NUMBER", 4],
        "*",
        "(",
        ["NUMBER", 5],
        "-",
        ["NUMBER", 2],
        ")",
    ]

    assert tokenize("-3+4*(-5--2)") == [
        "-",
        ["NUMBER", 3],
        "+",
        ["NUMBER", 4],
        "*",
        "(",
        "-",
        ["NUMBER", 5],
        "-",
        "-",
        ["NUMBER", 2],
        ")",
    ]
    assert tokenize("3+4*(5-2)") == tokenize("3 + 4 * (5 - 2)")
    assert tokenize("3+4*(5-2)") == tokenize("  3  +  4 * (5 - 2)  ")
    assert tokenize("3+4*(5-2)") == tokenize(" 3 + 4 * (5 - 2) ")


def test_multiple_sequential_signed_numbers():
    print("testing multiple sequential signed numbers")
    assert tokenize("1--2") == [["NUMBER", 1], "-", "-", ["NUMBER", 2]]
    assert tokenize("1---2") == [["NUMBER", 1], "-", "-", "-", ["NUMBER", 2]]
    assert tokenize("print -3+-4*(-+-+-----+5--2);") == [
        "print",
        "-",
        ["NUMBER", 3],
        "+",
        "-",
        ["NUMBER", 4],
        "*",
        "(",
        "-",
        "+",
        "-",
        "+",
        "-",
        "-",
        "-",
        "-",
        "-",
        "+",
        ["NUMBER", 5],
        "-",
        "-",
        ["NUMBER", 2],
        ")",
        ";",
    ]


def test_keywords():
    print("testing keywords")
    for keyword in ["print"]:
        assert tokenize(keyword) == [keyword]


if __name__ == "__main__":
    test_individual_tokens()
    test_whitespace()
    test_multiple_tokens()
    test_keywords()
    test_multiple_sequential_signed_numbers()
    print(tokenize("print -3+-4*(-+-+-----+5--2)+3*2-1+0;"))
    print(tokenize("print 3 + (-4 * 3) + -(4 * 5);"))
