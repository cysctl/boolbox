from boolbox.formatters.base import Formatter


class LaTeXFormatter(Formatter):
    """
    LaTeX formatter for polynomials
    Replaces 'XOR' with '\\oplus'
    """

    def format(self, polys: dict[int, str]) -> str:
        data = []

        for idx, poly in polys.items():
            # Replace 'XOR' with '\\oplus'
            #
            new_poly_str = poly.replace(" XOR ", " \\oplus ")

            data.append(f"x_{idx} \\rightarrow S_{idx} = {new_poly_str}")

        return "\n".join(data)
