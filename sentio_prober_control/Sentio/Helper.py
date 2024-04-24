import re

from typing import List


class Helper:
    def split_string(s : str, delimiter : str) -> List[str]:
        escaped_delimiter = re.escape(delimiter)
        pattern = rf'"[^"]*"|[^{escaped_delimiter}]+'
        matches = re.findall(pattern, s)

        return [match.strip('"') for match in matches]