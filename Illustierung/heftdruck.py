#!/usr/bin/env python3
"""
heftdruck.py

Bereitet ein PDF für den Heftdruck (Saddle-Stitch / Broschüre) vor.

Ausgangssituation:
- Die Eingabe-PDF enthält Doppelseiten (Spreads): jede PDF-Seite ist im
  Querformat und zeigt zwei Buchseiten nebeneinander.
- Die erste PDF-Seite enthält das Deckblatt.
- Das Skript teilt jede Doppelseite in der Mitte und ordnet die daraus
  entstehenden Einzelseiten so an, dass man das PDF duplexdrucken, die
  Blätter stapeln und in der Mitte falten kann.

Algorithmus (Kernidee):
1. Jede PDF-Seite wird in zwei "logische" Buchseiten zerlegt.
   Standard: rechte Hälfte = ungerade Seite, linke Hälfte = gerade Seite.
2. Die Gesamtzahl der logischen Seiten wird auf ein Vielfaches von 4
   mit Leerseiten aufgefüllt.
3. Für ein Heft mit P logischen Seiten und S = P/4 Bogen gilt:
   Bogen i (0-basiert):
     Vorderseite: links = P - 2*i, rechts = 2*i + 1
     Rückseite:   links = 2*i + 2, rechts = P - 2*i - 1
   Beim Falten und Stapeln ergibt sich dadurch die Lesereihenfolge 1..P.
"""

import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF


def physical_page_sources(spread_count, split_order):
    """
    Ordnet jeder logischen Buchseite (1-basiert) ihre Herkunft zu:
    (Eingabe-Spread-Index, Hälfte).

    split_order = "right-first":  rechte Hälfte zuerst -> Seite 1 ist rechts
    split_order = "left-first":   linke Hälfte zuerst  -> Seite 1 ist links
    """
    mapping = {}
    logical = 1
    mapping[1] = (0, "left")
    mapping[2] = (0, "right")
    for s in range(3, spread_count):
        mapping[logical] = (s - 1, "right")
        mapping[2*spread_count - logical] = (s - 1, "left")
        logical += 2

    for s in range(spread_count):
        if split_order == "right-first":
            mapping[logical] = (s, "right")
            mapping[logical + 1] = (s, "left")
            mapping_log.append((s, "right"))
            mapping_log.append((s, "left"))
        else:
            mapping[logical] = (s, "left")
            mapping[logical + 1] = (s, "right")
        logical += 2
    return mapping


def booklet_order(total_logical, mode):
    """
    Berechnet die Reihenfolge der Ausgabe-Spreads.

    Rückgabe: Liste von (l_links, l_rechts) für jede Ausgabe-Seite.
    Ein "Bogen" besteht aus zwei aufeinanderfolgenden Einträgen
    (Vorderseite, Rückseite).
    """
    if total_logical % 4 != 0:
        raise ValueError("Anzahl logischer Seiten muss ein Vielfaches von 4 sein.")

    sheets = []
    p = total_logical
    for i in range(p // 4):
        front = (p - 2 * i, 2 * i + 1)
        back = (2 * i + 2, p - 2 * i - 1)
        sheets.append((front, back))

    if mode == "duplex":
        # Druckreihenfolge für automatischen Duplexdruck (Bogen für Bogen).
        order = []
        for front, back in sheets:
            order.append(front)
            order.append(back)
        return order

    if mode == "manual":
        # Zuerst alle Vorderseiten im Stapel, dann die Rückseiten in
        # umgekehrter Reihenfolge (für das Wenden des Stapels um die
        # Längskante).
        fronts = [front for front, _ in sheets]
        backs = [back for _, back in sheets][::-1]
        return fronts + backs

    raise ValueError(f"Unbekannter Modus: {mode}")


def build_booklet(src_path, split_order="right-first", mode="duplex"):
    src = fitz.open(src_path)
    if src.page_count == 0:
        raise ValueError("Eingabe-PDF enthält keine Seiten.")

    spread_count = src.page_count
    logical_count = spread_count * 2

    # Auffüllen auf Vielfaches von 4
    remainder = logical_count % 4
    blanks_needed = (4 - remainder) % 4
    total_logical = logical_count + blanks_needed

    source = physical_page_sources(spread_count, split_order)
    for b in range(1, blanks_needed + 1):
        source[logical_count + b] = None

    first = src[0]
    spread_w = first.rect.width
    spread_h = first.rect.height
    half_w = spread_w / 2

    order = booklet_order(total_logical, mode)

    out = fitz.open()
    left_clip = fitz.Rect(0, 0, half_w, spread_h)
    right_clip = fitz.Rect(half_w, 0, spread_w, spread_h)

    for left_logical, right_logical in order:
        page = out.new_page(width=spread_w, height=spread_h)

        for dst_x, logical, clip in (
            (0, left_logical, left_clip),
            (half_w, right_logical, right_clip),
        ):
            src_info = source[logical]
            if src_info is None:
                continue
            spread_idx, side = src_info
            src_page = src[spread_idx]
            # clip auf die gewünschte Hälfte der Quell-Spread beschränken
            if side == "left":
                src_clip = fitz.Rect(0, 0, half_w, spread_h)
            else:
                src_clip = fitz.Rect(half_w, 0, spread_w, spread_h)
            dst_rect = fitz.Rect(dst_x, 0, dst_x + half_w, spread_h)
            page.show_pdf_page(dst_rect, src, spread_idx, clip=src_clip)

    return out, order, source


def main():
    parser = argparse.ArgumentParser(
        description="PDF-Doppelseiten für Heftdruck vorbereiten."
    )
    parser.add_argument("input", help="Eingabe-PDF mit Doppelseiten")
    parser.add_argument("output", help="Ausgabe-PDF")
    parser.add_argument(
        "--split-order",
        choices=["right-first", "left-first"],
        default="right-first",
        help=(
            'Reihenfolge beim Teilen einer Doppelseite. "right-first" bedeutet: '
            "rechte Hälfte zuerst (ungerade Seite = rechts, typisch für Bücher). "
            '"left-first" bedeutet: linke Hälfte zuerst.'
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["duplex", "manual"],
        default="duplex",
        help=(
            '"duplex": Vorder-/Rückseite abwechselnd pro Bogen (für Duplexdruck). '
            '"manual": alle Vorderseiten, dann alle Rückseiten in umgekehrter '
            "Reihenfolge (für manuelles Wenden des Stapels um die Längskante)."
        ),
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Nur den Aufschlagplan ausgeben, keine PDF erzeugen.",
    )
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Fehler: Datei nicht gefunden: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.info:
        src = fitz.open(args.input)
        if src.page_count == 0:
            print("Fehler: Eingabe-PDF enthält keine Seiten.", file=sys.stderr)
            sys.exit(1)

        spread_count = src.page_count
        logical_count = spread_count * 2
        remainder = logical_count % 4
        blanks_needed = (4 - remainder) % 4
        total_logical = logical_count + blanks_needed

        source = physical_page_sources(spread_count, args.split_order)
        for b in range(1, blanks_needed + 1):
            source[logical_count + b] = None

        order = booklet_order(total_logical, args.mode)

        print("Aufschlagplan:")
        print("Logische Seiten -> Eingabe-Spread, Hälfte")
        for logical in sorted(source):
            src_info = source[logical]
            if src_info is None:
                print(f"  {logical:3d}: [Leerseite]")
            else:
                spread, side = src_info
                print(f"  {logical:3d}: Spread {spread + 1}, {side}")
        print(f"\nDruckreihenfolge ({args.mode}):")
        for i, (left, right) in enumerate(order, start=1):
            print(f"  Ausgabe-Seite {i:2d}: links={left}, rechts={right}")
        return

    out, order, source = build_booklet(args.input, args.split_order, args.mode)
    out.save(args.output, garbage=4, deflate=True)
    out.close()

    print(f"Ausgabe geschrieben: {args.output}")
    print(f"  Eingabe-Spreads:   {fitz.open(args.input).page_count}")
    print(f"  Logische Seiten:   {len(source)}")
    print(f"  Ausgabe-Spreads:   {len(order)}")
    print(f"  Modus:             {args.mode}")
    print(f"  Teilung:           {args.split_order}")


if __name__ == "__main__":
    main()
