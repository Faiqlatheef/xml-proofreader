import re

def find_all_occurrences(text, substring):
    return [m.start() for m in re.finditer(re.escape(substring), text)]
