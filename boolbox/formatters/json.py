import json
from boolbox.formatters.base import Formatter


class JSONFormatter(Formatter):
    """
    JSON formatter for polynomials
    """

    def format(self, polys: dict[int, str]) -> str:
        # Create a structured dict scheme
        #
        structured_data = {
            "metadata": {"type": "ANF Polynomials", "bit_count": len(polys)},
            "equations": [
                {"bit_index": bit, "polynomial": poly} for bit, poly in polys.items()
            ],
        }

        # Convert to JSON string
        #
        return json.dumps(structured_data, indent=4)
