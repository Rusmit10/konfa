from lark import Lark, Transformer

grammar = r"""
    start: statement*

    statement: "const" NAME "=" value ";"

    ?value: NUMBER           -> number
          | array
          | expr

    array : "[" [value ("," value)*] "]"

    expr : "$" expr_item+ "$"

    expr_item : NAME        -> name
              | NUMBER      -> number
              | OP          -> op

    OP: "+" | "-" | "*" | "/" | "max"

    NAME: /[_a-zA-Z]+/
    NUMBER: /\d+/

    %ignore /\s+/
"""

class EvalTransformer(Transformer):
    def __init__(self):
        self.env = {}

    def number(self, items):
        return int(items[0])

    def name(self, items):
        return str(items[0])

    def op(self, items):
        return str(items[0])

    def array(self, items):
        return items

    def statement(self, items):
        name = items[0]
        value = items[1]
        self.env[name] = value

    def expr(self, items):
        stack = []

        for item in items:
            if isinstance(item, int):
                stack.append(item)

            elif isinstance(item, str):
                if item in self.env:
                    stack.append(self.env[item])

                elif item in {"+", "-", "*", "/", "max"}:
                    if len(stack) < 2:
                        raise ValueError("Ошибка в постфиксном выражении")

                    b = stack.pop()
                    a = stack.pop()

                    if item == "+":
                        stack.append(a + b)
                    elif item == "-":
                        stack.append(a - b)
                    elif item == "*":
                        stack.append(a * b)
                    elif item == "/":
                        stack.append(a // b)
                    elif item == "max":
                        stack.append(max(a, b))

                else:
                    raise ValueError(f"Неизвестный идентификатор: {item}")

        if len(stack) != 1:
            raise ValueError("Некорректное постфиксное выражение")

        return stack[0]

    def start(self, _):
        return self.env


def parse_and_translate(text: str) -> str:
    parser = Lark(grammar, parser="lalr")
    tree = parser.parse(text)
    result = EvalTransformer().transform(tree)

    return "\n".join(f"{k} = {v}" for k, v in result.items())
