import re

stopwords = set(
    [
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        ">>",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "}",
        "~",
        " ",
        "。",
        "、",
    ]
)

stopwords_reg = "(" + "|".join([re.escape(s) for s in stopwords]) + ")"
stopwords_pattern = re.compile(stopwords_reg)
stopwords_between_hanzi_pattern = re.compile((r"([\u4e00-\u9fa5]{1})" + stopwords_reg + "+" + r"([\u4e00-\u9fa5]{1})"))


def search_sensitive_words(text, sensitive_pattern):
    """
    Search sensitive words in text.
    """

    if sensitive_pattern is None:
        return []

    text = stopwords_pattern.sub(" ", text)
    for i in range(3):
        text = stopwords_between_hanzi_pattern.sub(r"\1\3", text)
        pass
    ret = []
    for m in sensitive_pattern.finditer(text):
        tmp_str = m.group(0).strip()
        if len(tmp_str):
            ret.append(tmp_str)
        pass

    return ret
