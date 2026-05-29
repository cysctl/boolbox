import re
from boolbox.formatters.base import Formatter
from boolbox.formatters.text import TextFormatter

class UnicodeFormatter(Formatter):
    def __init__(self):
        self.text_formatter = TextFormatter()
        
        # Digits
        # 
        self.subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    def format(self, polys: list[str]) -> str:
        """
        Formats the ANF polynomials into a rendered Unicode text string
        """

        text_output = self.text_formatter.format(polys)
        
        if not text_output:
            return ""

        # Replace
        # 
        unicode_output = text_output.replace(" XOR ", " ⊕  ")
        unicode_output = unicode_output.replace("->", "→")
        
        unicode_output = re.sub(
            r'_(\d+)', 
            lambda match: match.group(1).translate(self.subscripts), 
            unicode_output
        )
        
        return unicode_output