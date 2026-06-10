import re
from pathlib import Path


def test_parameter_file_has_no_direct_parameter_aliases() -> None:
    source = Path("dih_models/parameters.py").read_text(encoding="utf-8")

    parameter_names = set(re.findall(r"^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\(", source, re.M))
    alias_candidates = [
        (line_no, match.group(1), match.group(2))
        for line_no, line in enumerate(source.splitlines(), start=1)
        if (match := re.match(r"^([A-Z][A-Z0-9_]+)\s*=\s*([A-Z][A-Z0-9_]+)\s*$", line))
    ]

    aliases = []
    known_parameter_names = set(parameter_names)
    changed = True
    while changed:
        changed = False
        for line_no, alias_name, target_name in alias_candidates:
            if alias_name not in known_parameter_names and target_name in known_parameter_names:
                aliases.append((line_no, alias_name, target_name))
                known_parameter_names.add(alias_name)
                changed = True

    assert aliases == []
