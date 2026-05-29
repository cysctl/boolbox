import os
from boolbox.formatters.latex import LaTeXFormatter

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


class ImageFormatter:
    def __init__(self, output_path: str = "anf_equations.png"):
        self.latex_formatter = LaTeXFormatter()

        # Check and enforce the .png extension
        #
        if not output_path.lower().endswith(".png"):
            output_path += ".png"
            
        self.output_path = output_path

    def format(self, polys: list[str]) -> str:
        """
        Renders the polynomials as a PNG image using matplotlib's mathtext
        """

        if plt is None:
            raise ImportError("The 'matplotlib' library is required to render images")

        equations = []
        for i, poly in polys.items():
            # Replace XOR with LaTeX \oplus
            #
            latex_poly = poly.replace("XOR", r"\oplus")
            equations.append(f"$x_{{{i}}} \\rightarrow S_{{{i}}} = {latex_poly}$")

        # Join the equations with double newlines for spacing
        #
        full_text = "\n\n".join(equations)

        # Dynamically calculate the figure height
        #
        fig = plt.figure(figsize=(6, len(equations) * 0.8))

        # Center the text
        #
        fig.text(0.1, 0.5, full_text, fontsize=16, va="center", ha="left")

        # Hide the axes
        #
        plt.axis("off")

        # Save the image
        #
        plt.savefig(
            self.output_path,
            format="png",
            bbox_inches="tight",
            dpi=300,
            facecolor="white",
        )

        # Clean up the memory
        #
        plt.close(fig)

        return (
            f"Image successfully saved to: file://{os.path.abspath(self.output_path)}"
        )
