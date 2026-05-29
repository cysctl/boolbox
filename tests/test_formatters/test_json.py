import json
from boolbox.formatters.json import JSONFormatter


# Test for JSON formatter
#
def test_json_formatter_basic():
    formatter = JSONFormatter()

    sample_polys = {0: "x_0 XOR x_1", 1: "1 XOR x_2"}

    # Generate the JSON string
    #
    json_output = formatter.format(sample_polys)

    # Parse it back to a Python dictionary to verify its structure
    #
    parsed_output = json.loads(json_output)

    # Validate metadata
    #
    assert parsed_output["metadata"]["type"] == "ANF Polynomials"
    assert parsed_output["metadata"]["bit_count"] == 2

    # Validate equations array
    #
    assert len(parsed_output["equations"]) == 2

    # Validate specific items
    #
    assert parsed_output["equations"][0]["bit_index"] == 0
    assert parsed_output["equations"][0]["polynomial"] == "x_0 XOR x_1"

    assert parsed_output["equations"][1]["bit_index"] == 1
    assert parsed_output["equations"][1]["polynomial"] == "1 XOR x_2"
