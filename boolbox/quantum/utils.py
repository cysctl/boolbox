import sys

def require_qiskit() -> None:
    """
    Checks if Qiskit is installed?
    Raises a clean SystemExit if not, guiding the user to install the optional dependency
    """

    try:
        import qiskit
    except ImportError:
        print("Error: The quantum module requires 'qiskit'.", file=sys.stderr)
        print("Please install it using the optional dependency flag:", file=sys.stderr)
        print("    pip install boolbox[quantum]", file=sys.stderr)
        print("Or manually:", file=sys.stderr)
        print("    pip install qiskit", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    require_qiskit()