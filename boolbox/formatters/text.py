from boolbox.formatters.base import Formatter


class TextFormatter(Formatter):
    """
    Standard text formatter for polynomials
    """

    def format(self, polys: dict[int, str]) -> str:
        data = []

        for idx, poly in polys.items():
            data.append(f"x_{idx} -> S_{idx} = {poly}")

        return "\n".join(data)
