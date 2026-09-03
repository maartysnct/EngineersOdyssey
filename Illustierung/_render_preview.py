import fitz
src = r"C:\Users\Lars\Documents\GitHub\Wisskomm\Inseln\1_Anleitung\Spielanleitung (3).pdf"
out = r"C:\Users\Lars\Documents\GitHub\Wisskomm\Inseln\1_Anleitung\Spielanleitung (3)_A4.pdf"
for label, path in [("input", src), ("output", out)]:
    doc = fitz.open(path)
    page = doc[0]
    pix = page.get_pixmap(dpi=72)
    pix.save(f"C:/Users/Lars/AppData/Local/Temp/preview_{label}.png")
    print(label, page.rect, "rendered")
