from math import isfinite, pi


def analyze(data):
    diameter, density, available, waste = (data[k] for k in
        ("diameterMm", "densityGramsPerCm3", "availableGrams", "wasteFraction"))
    if not all(type(n) in (int, float) and isfinite(n) and n >= 0 for n in (diameter, density, available, waste)):
        raise ValueError("Provide finite nonnegative inputs")
    if diameter <= 0 or density <= 0 or waste > 1:
        raise ValueError("Diameter and density must be positive, with waste between 0 and 1")
    grams_per_meter = pi * (diameter / 2) ** 2 * density
    rows = []
    total = 0
    for label, length in data["jobs"]:
        if not isinstance(label, str) or not label.strip() or type(length) not in (int, float) or not isfinite(length) or length < 0:
            raise ValueError("Each job needs a name and a finite nonnegative length")
        mass = length * grams_per_meter
        total += mass
        rows.append({"job": label, "grams": round(mass, 3)})
    planned = total * (1 + waste)
    return {"filamentGrams": round(total, 3), "budgetedGrams": round(planned, 3),
            "remainingGrams": round(available - planned, 3), "fits": planned <= available, "jobs": rows}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
