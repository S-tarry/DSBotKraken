import re


def clean_role_name(role_name: str):
    cleaned = re.sub(r"[^\w]", "", role_name)
    return cleaned.lower()