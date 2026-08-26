"""Convert a CSV of point facilities into a GeoJSON FeatureCollection."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_COLUMNS = {
    "Facility_ID",
    "Facility_Type",
    "Location_Name",
    "Operator",
    "Status",
    "Latitude",
    "Longitude",
}


def parse_coordinates(row: dict[str, str], row_number: int) -> tuple[float, float]:
    """Return validated coordinates in GeoJSON longitude/latitude order."""
    try:
        latitude = float(row["Latitude"])
        longitude = float(row["Longitude"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Row {row_number}: invalid latitude or longitude") from exc

    if not -90 <= latitude <= 90:
        raise ValueError(f"Row {row_number}: latitude must be between -90 and 90")
    if not -180 <= longitude <= 180:
        raise ValueError(f"Row {row_number}: longitude must be between -180 and 180")

    return longitude, latitude


def csv_to_geojson(input_csv: Path, output_geojson: Path) -> int:
    """Convert CSV rows to GeoJSON and return the number of created features."""
    features: list[dict[str, object]] = []

    with input_csv.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        for row_number, row in enumerate(reader, start=2):
            longitude, latitude = parse_coordinates(row, row_number)
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude],
                    },
                    "properties": {
                        "Facility_ID": row["Facility_ID"].strip(),
                        "Facility_Type": row["Facility_Type"].strip(),
                        "Location_Name": row["Location_Name"].strip(),
                        "Operator": row["Operator"].strip(),
                        "Status": row["Status"].strip(),
                    },
                }
            )

    feature_collection = {"type": "FeatureCollection", "features": features}
    output_geojson.write_text(
        json.dumps(feature_collection, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return len(features)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_csv",
        nargs="?",
        type=Path,
        default=Path("texas_energy_infrastructure.csv"),
        help="Input CSV path",
    )
    parser.add_argument(
        "output_geojson",
        nargs="?",
        type=Path,
        default=Path("texas_energy_infrastructure.geojson"),
        help="Output GeoJSON path",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    count = csv_to_geojson(args.input_csv, args.output_geojson)
    print(f"Converted {count} records to {args.output_geojson}")


if __name__ == "__main__":
    main()

