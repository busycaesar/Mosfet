from config import DELIMITER

def build_content_file(description, content):
    return f"""\
{DELIMITER}
description: {description}
{DELIMITER}

{content}
"""
