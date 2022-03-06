class KMP:
    def __init__(self, pattern: str, radix=127) -> None:
        self._dfa = [[0] * radix for _ in pattern]
        prefix = 0
        for matched, char in enumerate(pattern):
            self._dfa[matched] = self._dfa[prefix].copy()
            prefix = self._dfa[prefix][ord(char)]
            self._dfa[matched][ord(char)] = matched + 1

    def find(self, text='', file: str = None):
        if file is None:
            return self._find_text(text)
        else:
            return self._find_file(file)

    def _find_file(self, file):
        with open(file, 'rb') as f:
            matched, idx = 0, 0
            for char in f.read1():
                idx += 1
                matched = self._dfa[matched][char]
                if matched == len(self._dfa):
                    return idx - matched
            else:
                return -1

    def _find_text(self, text):
        matched = 0
        for idx, char in enumerate(text):
            matched = self._dfa[matched][ord(char)]
            if matched == len(self._dfa):
                return idx - matched + 1
        else:
            return -1

    def find_all(self, text: str = None):
        while (x := self.find(text)) != -1:
            yield x
            text = text[x + 1:]

    def count(self, text: str):
        return len(list(self.find_all(text)))


def main(pattern: str, text: str = None, file: str = None):
    kmp = KMP(pattern)
    if file is None:
        assert kmp.find(text) == text.find(pattern)
        print(kmp.find(text),
              list(kmp.find_all(text)),
              kmp.count(text),
              sep='\n')
    else:
        print(kmp.find(file=file))


if __name__ == '__main__':
    import typer
    typer.run(main)
