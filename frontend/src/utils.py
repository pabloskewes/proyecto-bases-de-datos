def fix_name(name: str) -> str:
    name = name.lower()
    words = name.split(" ")
    for i, word in enumerate(words):
        words[i] = word.replace("?", "ñ").capitalize()
    return " ".join(words)
