import sys

sys.setrecursionlimit(10000)


def char_match(regex: chr, char: chr) -> bool:
    return regex == char or regex in (".", "")


def zero_or_one(regex: str, string: str) -> bool:
    chr_match = char_match(regex[0], string[0])
    return string_match(regex[2], string[chr_match:])


def zero_or_more(regex: str, string: str) -> bool:
    chr_match = char_match(regex[0], string[0])
    if regex[0] == "." and char_match(regex[2], string[0]) and string.count(string[0]) == 1:
        return string_match(regex[2:], string[0:])
    return string_match(regex[int(not chr_match) * 2:], string[chr_match:])


def one_or_more(regex: str, string: str) -> bool:
    chr_match = char_match(regex[0], string[0])
    if chr_match:
        next_index = 0
        for i in range(len(string)):
            if regex[0] != "." and not char_match(regex[0], string[i]):
                next_index = i
                break
            elif len(regex) > 2 and char_match(regex[2], string[i]):
                next_index = i
                break
        return string_match(regex[2:], string[next_index:])
    else:
        return False


def meta_char(regex: str, string: str) -> bool:
    if regex[1] == "?":
        return zero_or_one(regex, string)
    if regex[1] == "*":
        return zero_or_more(regex, string)
    if regex[1] == "+":
        return one_or_more(regex, string)


def string_match(regex: str, string: str) -> bool:
    if regex in ("", ".*", ".?") or (regex == "$" and not string):
        return True
    elif not string:
        return False
    elif regex[0] == "\\" and len(regex) > 1:
        if char_match(regex[1], string[0]):
            return string_match(regex[1], string[0])
    elif len(regex) > 1 and regex[1] in ("?", "*", "+"):
        return meta_char(regex, string)
    elif not char_match(regex[0], string[0]):
        return False
    else:
        return string_match(regex[1:], string[1:])


def any_match(regex: str, string: str) -> bool:
    for i in range(len(string)):
        if string_match(regex, string[i:]):
            return True
    return False


def regex_match(regex: str, string: str) -> bool:
    if not regex:
        return True
    if regex[0] == "^":
        return string_match(regex[1:], string)
    else:
        return any_match(regex, string)


result = regex_match(*input().split("|"))
print(result)