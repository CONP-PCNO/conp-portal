import json
from whoosh.analysis import Tokenizer, Token
from whoosh.compat import text_type
from whoosh.analysis import RegexTokenizer


class JsonTokenizer(RegexTokenizer):
    def __toString__(self, v):
        if isinstance(v, dict):
            return self.__toString__(list(v.values()))
        elif isinstance(v, list):
            if len(v) == 0:
                return ""
            if len(v) == 1:
                return self.__toString__(v[0])
            else:
                return self.__toString__(v[0]) + ',' + self.__toString__(v[1:])
        elif isinstance(v, str):
            return v

    def __call__(self, value, positions = False, chars = False,
                keeporiginal = False, removestops = True,
                start_pos = 0, start_char = 0,
                tokenize = True, mode = '', **kwargs):
        try:
            v = json.loads(value)
        except:
            v = value

        v = self.__toString__(v)

        return super().__call__(v, positions, chars,
                keeporiginal, removestops,
                start_pos, start_char,
                tokenize, mode, **kwargs)