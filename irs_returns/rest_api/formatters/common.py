import re


def to_paragraph_case(value: str | None) -> str | None:
    if not value:
        return value

    value = value.strip()
    value = value.lower()

    sentences = re.split(r"(?<=[.!?])\s+", value)
    result = []
    for i in range(0, len(sentences), 2):
        # Capitalize the current sentence part and append the terminator
        sentence_part = sentences[i].strip()
        if sentence_part:
            result.append(sentence_part.capitalize())
        if i + 1 < len(sentences):
            result.append(sentences[i + 1])  # Append the actual punctuation
    return "".join(result)
