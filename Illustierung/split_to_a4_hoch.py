#!/usr/bin/env python3
"""
split_to_a4_hoch.py

Nimmt ein PDF, bei dem jede Seite eine Doppelseite (Spread) im Querformat
enthält, teilt jede Seite in der Mitte und erzeugt daraus ein neues PDF mit
A4-Hochformat-Seiten.

Abhängigkeit: PyMuPDF (fitz)
    pip install pymupdf
"""

import argparse
import sys
from pathlib import Path

import fitz

# A4 Hochformat in PostScript-Punkten (1 pt = 1/72 Zoll)
A4_WIDTH_PT = 595.276
A4_HEIGHT_PT = 841.89


def _destination_rect(clip_rect, mode):
    """
    Berechnet das Ziel-Rechteck auf der A4-Seite.

    mode == "fit":   Seitenverhältnis beibehalten, in die A4-Seite einpassen
                    und zentrieren (evtl. weiße Ränder).
    mode == "fill":  Clip füllt die gesamte A4-Seite aus (kann leicht
                    verzerren, wenn das Seitenverhältnis nicht passt).
    """
    if mode == "fill":
        return fitz.Rect(0, 0, A4_WIDTH_PT, A4_HEIGHT_PT)

    scale = min(A4_WIDTH_PT / clip_rect.width, A4_HEIGHT_PT / clip_rect.height)
    dw = clip_rect.width * scale
    dh = clip_rect.height * scale
    dx = (A4_WIDTH_PT - dw) / 2
    dy = (A4_HEIGHT_PT - dh) / 2
    return fitz.Rect(dx, dy, dx + dw, dy + dh)


def split_pdf_to_a4_portrait(input_path, output_path, order="left-first", mode="fit"):
    src = fitz.open(input_path)
    if src.page_count == 0:
        raise ValueError("Eingabe-PDF enthält keine Seiten.")

    out = fitz.open()

    for pno in range(src.page_count):
        page = src[pno]
        rect = page.rect
        w = rect.width
        h = rect.height
        mid = w / 2

        left_clip = fitz.Rect(0, 0, mid, h)
        right_clip = fitz.Rect(mid, 0, w, h)

        if order == "right-first":
            sides = [("rechts", right_clip), ("links", left_clip)]
        else:
            sides = [("links", left_clip), ("rechts", right_clip)]

        for side_name, clip in sides:
            dst_rect = _destination_rect(clip, mode)
            out_page = out.new_page(width=A4_WIDTH_PT, height=A4_HEIGHT_PT)
            out_page.show_pdf_page(dst_rect, src, pno, clip=clip)
            print(f"  Seite {pno + 1}/{src.page_count} – {side_name}e Hälfte -> A4")

    out.save(output_path, garbage=4, deflate=True)
    out.close()
    src.close()


def main():
    parser = argparse.ArgumentParser(
        description="PDF-Doppelseiten in der Mitte teilen und auf A4 Hochformat bringen."
    )
    parser.add_argument("input", help="Eingabe-PDF mit Doppelseiten")
    parser.add_argument(
        "output",
        nargs="?",
        help="Ausgabe-PDF (Standard: <Eingabe>_A4.pdf)",
    )
    parser.add_argument(
        "--order",
        choices=["left-first", "right-first"],
        default="left-first",
        help=(
            'Reihenfolge der Hälften pro Seite. "left-first" = linke Hälfte zuerst, '
            '"right-first" = rechte Hälfte zuerst.'
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["fit", "fill"],
        default="fit",
        help=(
            '"fit": Seitenverhältnis beibehalten und auf A4 zentrieren '
            '(kann weiße Ränder ergeben). '
            '"fill": gesamte A4-Seite füllen (leichte Verzerrung möglich).'
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
        output_path = input_path.parent / f"{input_path.stem}_A4.pdf"

    print(f"Eingabe:  {input_path}")
    print(f"Ausgabe:  {output_path}")
    print(f"Modus:    {args.mode} (A4 Hochformat)")
    print(f"Reihenfolge: {args.order}")
    print()

    split_pdf_to_a4_portrait(str(input_path), str(output_path), args.order, args.mode)

    print(f"\nFertig: {output_path}")


if __name__ == "__main__":
    main()
