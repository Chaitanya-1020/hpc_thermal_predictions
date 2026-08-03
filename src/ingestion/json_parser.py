import json
import re
from json import JSONDecoder


def iter_json_records(file_path):
    """
    Generic parser for valid telemetry files.

    Works with:
    - temp.json
    - frequency.json
    - power.json
    - energy.json
    """

    decoder = JSONDecoder()

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    idx = 0
    length = len(text)

    while idx < length:

        while idx < length and text[idx].isspace():
            idx += 1

        if idx >= length:
            break

        obj, end = decoder.raw_decode(text, idx)

        yield obj

        idx = end


def iter_cpu_usage_records(file_path):
    """
    Special parser for mentor's cpu_usage.json.

    The dataset contains entries like:

        "core": 12:40:17

    which is not valid JSON.

    We repair it IN MEMORY only.
    """

    with open(file_path, "r", encoding="utf-8") as file:

        buffer = ""
        braces = 0

        for line in file:

            # Repair malformed core field
            line = re.sub(
                r'"core"\s*:\s*([0-9]{2}:[0-9]{2}:[0-9]{2})',
                r'"core":"\1"',
                line,
            )

            buffer += line

            braces += line.count("{")
            braces -= line.count("}")

            if braces == 0 and buffer.strip():

                yield json.loads(buffer)

                buffer = ""