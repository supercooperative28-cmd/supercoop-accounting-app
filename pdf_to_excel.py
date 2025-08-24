#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import subprocess
from typing import List

# Use venv if invoked via system python


def run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def find_pdfs(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() == ".pdf":
            files.append(path.resolve())
        elif path.is_dir():
            files.extend([q.resolve() for q in path.rglob("*.pdf")])
        else:
            # allow globbing patterns
            for q in Path().glob(p):
                if q.is_file() and q.suffix.lower() == ".pdf":
                    files.append(q.resolve())
    # unique while preserving order
    seen = set()
    unique = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def camelot_extract(pdf_path: Path, out_xlsx: Path) -> bool:
    try:
        import camelot
        import pandas as pd
    except Exception as e:
        return False
    try:
        tables = camelot.read_pdf(str(pdf_path), pages="all", flavor="lattice")
        if tables.n == 0:
            tables = camelot.read_pdf(str(pdf_path), pages="all", flavor="stream")
        if tables.n == 0:
            return False
        with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
            for i, table in enumerate(tables):
                df = table.df
                sheet_name = f"table_{i+1}"
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        return True
    except Exception:
        return False


def tabula_extract(pdf_path: Path, out_xlsx: Path) -> bool:
    try:
        import tabula
        import pandas as pd
    except Exception:
        return False
    try:
        dfs = tabula.read_pdf(str(pdf_path), pages="all", multiple_tables=True, lattice=True, stream=True)
        if not dfs:
            return False
        with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
            for i, df in enumerate(dfs):
                sheet_name = f"table_{i+1}"
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert tables from PDF to Excel (.xlsx)")
    parser.add_argument("inputs", nargs="*", default=["."], help="PDF files or directories to search")
    parser.add_argument("--output-dir", default="/workspace/outputs", help="Directory to place Excel files")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pdfs = find_pdfs(args.inputs)
    if not pdfs:
        print("No PDF files found in inputs.")
        return 2

    successes = 0
    for pdf in pdfs:
        out_name = pdf.stem + ".xlsx"
        out_path = out_dir / out_name
        print(f"Converting {pdf} -> {out_path}")
        ok = camelot_extract(pdf, out_path)
        if not ok:
            ok = tabula_extract(pdf, out_path)
        if ok:
            print(f"✔ Wrote {out_path}")
            successes += 1
        else:
            print(f"✖ Failed to extract tables from {pdf}")
    print(f"Done. {successes}/{len(pdfs)} succeeded. Outputs: {out_dir}")
    return 0 if successes > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
