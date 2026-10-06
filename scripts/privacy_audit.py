"""Fail-closed release audit for the small real-data teaching subset."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from PIL import Image
from shapely import wkt


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    field_path = DATA_DIR / "field_plots.csv"
    event_path = DATA_DIR / "field_events.csv"
    cnn_path = DATA_DIR / "cnn_model_outputs.csv"
    manifest_path = DATA_DIR / "TEACHING_DATA_MANIFEST.json"
    early_rgb = ASSET_DIR / "rgb_early_512.jpg"
    late_rgb = ASSET_DIR / "rgb_late_512.jpg"

    required = (field_path, event_path, cnn_path, manifest_path, early_rgb, late_rgb)
    for path in required:
        if not path.is_file():
            fail(f"missing required release file: {path.relative_to(ROOT)}")

    approved_data_files = {
        "README.md", "field_plots.csv", "field_events.csv", "cnn_model_outputs.csv",
        "TEACHING_DATA_MANIFEST.json",
    }
    unexpected_data = {
        path.name for path in DATA_DIR.iterdir() if path.is_file()
    } - approved_data_files
    if unexpected_data:
        fail(f"unexpected file(s) in data/: {sorted(unexpected_data)}")

    approved_binary_files = {
        "assets/rgb_early_512.jpg", "assets/rgb_late_512.jpg",
    }
    forbidden_suffixes = {
        ".gpkg", ".shp", ".dbf", ".shx", ".geojson",
        ".tif", ".tiff", ".png", ".jpeg",
        ".npy", ".npz", ".pkl", ".pickle", ".pt", ".pth", ".onnx",
    }
    forbidden_files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in forbidden_suffixes and relative not in approved_binary_files:
            forbidden_files.append(relative)
        if path.suffix.lower() == ".jpg" and relative not in approved_binary_files:
            forbidden_files.append(relative)
    if forbidden_files:
        fail(f"unapproved raw/binary release file(s): {sorted(set(forbidden_files))}")

    field = pd.read_csv(field_path)
    events = pd.read_csv(event_path)
    cnn = pd.read_csv(cnn_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if len(field) != 12:
        fail(f"field subset must contain exactly 12 rows, found {len(field)}")
    if len(events) != 10:
        fail(f"event table must contain exactly 10 rows, found {len(events)}")
    if len(cnn) != 24:
        fail(f"CNN table must contain exactly 24 rows, found {len(cnn)}")
    if manifest.get("research_rows_included") != 12:
        fail("manifest must declare exactly 12 included research rows")

    expected_field_columns = {
        "plot_id", "block", "treatment", "early_green_share", "late_green_share",
        "severity_sep04", "root_weight", "sugar_content_pct", "pixel_x", "pixel_y",
        "polygon_early_px", "polygon_late_px",
    }
    if set(field.columns) != expected_field_columns:
        fail("field table schema differs from the approved release schema")

    expected_event_columns = {
        "event_id", "event_type", "event_label", "date", "days_after_sowing",
        "display_group", "source_category",
    }
    if set(events.columns) != expected_event_columns:
        fail("event table schema differs from the approved release schema")

    forbidden_column_patterns = [
        r"experiment", r"unit_id", r"source", r"filename", r"epsg",
        r"latitude", r"longitude", r"easting", r"northing", r"crs",
    ]
    all_columns = [str(column).lower() for column in [*field.columns, *cnn.columns]]
    for pattern in forbidden_column_patterns:
        if any(re.search(pattern, column) for column in all_columns):
            fail(f"forbidden linkage/georeferencing column pattern: {pattern}")

    if list(field["plot_id"]) != [f"P{i:02d}" for i in range(1, 13)]:
        fail("plot identifiers are not the approved anonymous sequence")
    if list(events["event_id"]) != [f"E{i:02d}" for i in range(1, 11)]:
        fail("event identifiers are not the approved anonymous sequence")
    if list(cnn["sample_id"]) != [f"S{i:02d}" for i in range(1, 25)]:
        fail("CNN sample identifiers are not the approved anonymous sequence")
    if set(field["treatment"]) != {"Control", "Fungicide", "Inoculated"}:
        fail("unexpected treatment labels")
    if set(cnn["date"]) != {"2020-06-26", "2020-09-03"}:
        fail("unexpected CNN dates")
    if set(events.loc[events["event_type"].eq("image"), "date"]) != {
        "2020-06-26", "2020-09-03",
    }:
        fail("unexpected image dates in event table")
    if set(events.loc[events["event_type"].eq("fungicide"), "date"]) != {
        "2020-06-26", "2020-08-05", "2020-09-01",
    }:
        fail("unexpected fungicide dates in event table")

    event_dates = pd.to_datetime(events["date"], errors="raise")
    sowing_rows = events["event_id"].eq("E01")
    if sowing_rows.sum() != 1:
        fail("event table must contain exactly one E01 sowing row")
    sowing_date = event_dates.loc[sowing_rows].iloc[0]
    if not (event_dates.sub(sowing_date).dt.days == events["days_after_sowing"]).all():
        fail("event dates and days_after_sowing disagree")
    if not field.groupby(["block", "treatment"], observed=True).size().eq(1).all():
        fail("subset is not balanced across block and treatment")

    if not field["pixel_x"].between(0, 512).all() or not field["pixel_y"].between(0, 512).all():
        fail("pixel centroids fall outside the approved 512-pixel preview")
    for column in ("polygon_early_px", "polygon_late_px"):
        for text in field[column]:
            geometry = wkt.loads(text)
            x0, y0, x1, y1 = geometry.bounds
            if geometry.is_empty or geometry.area <= 0:
                fail(f"invalid pixel geometry in {column}")
            if not (0 <= x0 <= x1 <= 512 and 0 <= y0 <= y1 <= 512):
                fail(f"pixel geometry outside preview bounds in {column}")

    csv_text = (
        field_path.read_text(encoding="utf-8")
        + event_path.read_text(encoding="utf-8")
        + cnn_path.read_text(encoding="utf-8")
    )
    forbidden_text = [
        r"SE0\d", r"Plot_\d+",
        # Projected-coordinate-like integers. The negative look-behind avoids
        # treating harmless decimals such as 0.565749 as six-digit eastings.
        r"(?<![.\d])56\d{4,}(?!\d)", r"(?<![.\d])57\d{5,}(?!\d)",
        r"\.tif\b", r"\.gpkg\b",
    ]
    for pattern in forbidden_text:
        if re.search(pattern, csv_text, flags=re.IGNORECASE):
            fail(f"source-like content found in released tables: {pattern}")

    for image_path in (early_rgb, late_rgb):
        with Image.open(image_path) as image:
            if image.size != (512, 512) or image.mode != "RGB":
                fail(f"unexpected image format: {image_path.name}")
            if len(image.getexif()) != 0:
                fail(f"EXIF metadata present: {image_path.name}")

    # The private release builder is deliberately stored outside this public
    # folder. Fail if known private workspace/linkage markers are copied back.
    private_markers = [
        "2020-" + "SE01",
        "PRISM_" + "MANUSCRIPT",
        "DEPOSIT_" + "CANDIDATE",
        "RGB_" + "ORTHO",
        "F0_" + "I0",
        "F1_" + "I0",
        "F0_" + "I1",
    ]
    absolute_path_patterns = [
        re.compile(r"[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]", re.IGNORECASE),
        re.compile(r"(?:^|[\s\"'=])/" + r"home/[^/\s]+/", re.IGNORECASE),
        re.compile(r"(?:^|[\s\"'=])/" + r"Users/[^/\s]+/", re.IGNORECASE),
    ]
    text_suffixes = {".md", ".py", ".csv", ".json", ".txt", ".ipynb"}
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or path.suffix.lower() not in text_suffixes
            or ".git" in path.parts
            or "__pycache__" in path.parts
        ):
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for marker in private_markers:
            if marker.lower() in content.lower():
                fail(
                    f"private source/linkage marker found in "
                    f"{path.relative_to(ROOT).as_posix()}"
                )
        for pattern in absolute_path_patterns:
            if pattern.search(content):
                fail(
                    f"absolute local path found in "
                    f"{path.relative_to(ROOT).as_posix()}"
                )

    for relative, entry in manifest["files"].items():
        path = ROOT / relative
        if not path.is_file() or sha256(path) != entry["sha256"]:
            fail(f"manifest hash mismatch: {relative}")

    print("PASS: approved small real-data teaching release")
    print("  field rows:         12 (balanced by block and treatment)")
    print("  field events:       10 (dates and DAS cross-checked)")
    print("  RGB images:         2 real previews at 512 x 512 pixels")
    print("  CNN predictions:    24 grouped-CV cases")
    print("  projected/GPS data: none")
    print("  source identifiers: none in released tables")


if __name__ == "__main__":
    main()
