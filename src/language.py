import re


def detect_language(text):
    text = str(text).lower()

    # -----------------------------
    # 🔥 SCRIPT DETECTION (strong)
    # -----------------------------
    for char in text:
        code = ord(char)

        if 0x0900 <= code <= 0x097F:
            return "hi"
        if 0x0B80 <= code <= 0x0BFF:
            return "ta"
        if 0x0C00 <= code <= 0x0C7F:
            return "te"
        if 0x0D00 <= code <= 0x0D7F:
            return "ml"
        if 0x0980 <= code <= 0x09FF:
            return "bn"
        if 0x4E00 <= code <= 0x9FFF:
            return "zh"
        if 0x3040 <= code <= 0x30FF:
            return "ja"
        if 0xAC00 <= code <= 0xD7AF:
            return "ko"

    # -----------------------------
    # 🔥 HINDI BOOST (CRITICAL FIX)
    # -----------------------------
    hindi_keywords = [
        "arijit", "shreya", "sonu", "kk",
        "pritam", "atif", "jubin", "neha",
        "mohit chauhan", "rahat fateh ali",
        "amit trivedi", "anu malik", "alka yagnik"
    ]

    if any(k in text for k in hindi_keywords):
        return "hi"

    # -----------------------------
    # 🌍 OTHER LANGUAGE HINTS
    # -----------------------------
    if re.search(r"\b(el|amor|vida)\b", text):
        return "es"

    # -----------------------------
    # ⚠️ DEFAULT
    # -----------------------------
    return "en"


def add_language_column(df):
    print("Adding language column...")

    df["lang"] = (
        df["track_name"].astype(str) + " " +
        df["artists"].astype(str)
    ).apply(detect_language)

    return df