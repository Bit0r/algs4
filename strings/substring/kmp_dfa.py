import typer


class KMP:
    def __init__(self, pattern: str, radix=127) -> None:
        self._dfa = [[0] * radix for _ in pattern]
        prefix = 0
        for matched, char in enumerate(pattern):
            self._dfa[matched] = self._dfa[prefix].copy()
            prefix = self._dfa[prefix][ord(char)]
            self._dfa[matched][ord(char)] = matched + 1

    def find(self, text: str):
        matched = 0
        for idx, char in enumerate(text):
            matched = self._dfa[matched][ord(char)]
            if matched == len(self._dfa):
                return idx - matched + 1
        else:
            return -1


def main(pattern: str, text: str):
    kmp = KMP(pattern)
    assert kmp.find(text) == text.find(pattern)
    print(kmp.find(text))


if __name__ == '__main__':
    typer.run(main)
