import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    pattern = r'(' + '|'.join([f'{field}=[^\\{separator}]*' for field in fields]) + r')'
    return re.sub(pattern, lambda x: x.group(0).split('=')[0] + '=' + redaction, message)
