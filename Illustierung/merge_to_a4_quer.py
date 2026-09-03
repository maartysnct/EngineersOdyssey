#!/usr/bin/env python3
"""
merge_to_a4_quer.py

Fügt jeweils zwei aufeinanderfolgende Seiten zu einer A4-Querformat-Seite
zusammen (2 Seiten pro Blatt).

Abhängigkeit: PyMuPDF (fitz)
    pip install pymupdf
"""

import argparse
import sys
from pathlib import Path

import fitz

# A4 Querformat in Punkten
A4L_WIDTH = 841.89
A4L_HEIGHT = 595.276
HALF_W = A4L_WIDTH / 2


def _fit_rect(container, src_rect, mode):
    """
    Passt src_rect in container ein.

    mode == "fit":   Seitenverhältnis beibehalten und im Container zentrieren.
    mode == "fill":  Container komplett ausfüllen (evtl. verzerren).
    """
    if mode == "fill":
        return container

    scale = min(container.width / src_rect.width, container.height / src_rect.height)
    new_w = src_rect.width * scale
    new_h = src_rect.height * scale
    x = container.x0 + (container.width - new_w) / 2
    y = container.y0 + (container.height - new_h) / 2
    return fitz.Rect(x, y, x + new_w, y + new_h)


def merge_pdf_to_a4_landscape(
    input_path, output_path, order="left-right", mode="fit", orphan="center"
):
    src = fitz.open(input_path)
    if src.page_count == 0:
        raise ValueError("Eingabe-PDF enthält keine Seiten.")

    out = fitz.open()
    n = src.page_count

    left_half = fitz.Rect(0, 0, HALF_W, A4L_HEIGHT)
    right_half = fitz.Rect(HALF_W, 0, A4L_WIDTH, A4L_HEIGHT)
    full_page = fitz.Rect(0, 0, A4L_WIDTH, A4L_HEIGHT)

    for i in range(0, n, 2):
        out_page = out.new_page(width=A4L_WIDTH, height=A4L_HEIGHT)

        if i + 1 < n:
            # Normales Paar
            if order == "left-right":
                placements = [(i, left_half, "links"), (i + 1, right_half, "rechts")]
            else:
                placements = [(i + 1, left_half, "links"), (i, right_half, "rechts")]
        else:
            # Ungerade Seitenzahl: letzte Seite einzeln platzieren
            if orphan == "left":
                placements = [(i, left_half, "links (letzte Seite)")]
            elif orphan == "right":
                placements = [(i, right_half, "rechts (letzte Seite)")]
            else:
                placements = [(i, full_page, "zentriert (letzte Seite)")]

        for pno, container, label in placements:
            src_page = src[pno]
            dst_rect = _fit_rect(container, src_page.rect, mode)
            out_page.show_pdf_page(dst_rect, src, pno)
            print(f"  Seite {pno + 1}/{n} – {label} auf A4-Quer")

    out.save(output_path, garbage=4, deflate=True)
    out.close()
    src.close()


def main():
    parser = argparse.ArgumentParser(
        description="Zwei Seiten nebeneinander auf eine A4-Querformat-Seite legen."
    )
    parser.add_argument("input", help="Eingabe-PDF")
    parser.add_argument(
        "output",
        nargs="?",
        help="Ausgabe-PDF (Standard: <Eingabe>_A4quer.pdf)",
    )
    parser.add_argument(
        "--order",
        choices=["left-right", "right-left"],
        default="left-right",
        help=(
            '"left-right": Erste Seite links, zweite rechts (Standard). '
            '"right-left": Erste Seite rechts, zweite links.'
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["fit", "fill"],
        default="fit",
        help=(
            '"fit": Seitenverhältnis beibehalten und in die Hälfte einpassen '
            '(kann kleine weiße Ränder ergeben). '
            '"fill": Hälfte komplett füllen (leichte Verzerrung möglich).'
        ),
    )
    parser.add_argument(
        "--orphan",
        choices=["left", "right", "center"],
        default="center",
        help=(
            "Wo eine einzelne übrig gebliebene Seite bei ungerader Seitenzahl "
            "platziert wird: links, rechts oder zentriert (Standard)."
        ),
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Fehler: Datei nicht gefunden: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_A4quer.pdf"

    print(f"Eingabe:  {input_path}")
    print(f"Ausgabe:  {output_path}")
    print(f"Modus:    {args.mode}")
    print(f"Reihenfolge: {args.order}")
    print(f"Letzte Seite: {args.orphan}")
    print()

    merge_pdf_to_a4_landscape(
        str(input_path), str(output_path), args.order, args.mode, args.orphan
    )

    print(f"\nFertig: {output_path}")


if __name__ == "__main__":
    main()
