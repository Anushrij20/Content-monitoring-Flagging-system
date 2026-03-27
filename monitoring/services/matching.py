import re


def normalize(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_match_score(keyword, title, body):
    keyword = normalize(keyword)
    title = normalize(title)
    body = normalize(body)

    if not keyword:
        return 0

    # Exact keyword phrase in title
    if keyword in title:
        return 100

    # Partial keyword token match in title
    keyword_parts = keyword.split()
    if any(part in title for part in keyword_parts):
        return 70

    # Match only in body
    if keyword in body or any(part in body for part in keyword_parts):
        return 40

    return 0
