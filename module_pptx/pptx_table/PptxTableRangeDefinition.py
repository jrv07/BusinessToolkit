

class PptxTableRangeDefinition:
    def __init__(self, expression):
        self._expression = expression

    def is_in_expression(self, value):
        if ":" not in self._expression:
            return value == int(self._expression)
        else:
            exp_split = self._expression.split(":")
            exp_min = exp_split[0]
            exp_max = exp_split[1]
            if exp_max == "":
                if exp_min == "":
                    return True
                else:
                    if value >= int(exp_min):
                        return True
            else:
                if exp_min == "":
                    if value <= int(exp_max):
                        return True
                else:
                    if int(exp_min) <= value <= int(exp_max):
                        return True
        return False
