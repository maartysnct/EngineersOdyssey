import fitz, os
p = r"C:\Users\Lars\Documents\GitHub\Wisskomm\Inseln\1_Anleitung\Spielanleitung (4)_A4_A4quer.pdf"
print("exists:", os.path.exists(p))
if os.path.exists(p):
    print("size:", os.path.getsize(p))
    doc = fitz.open(p)
    print("Seiten:", doc.page_count)
    for i in [0, 1, 2, doc.page_count - 1]:
        r = doc[i].rect
        print(f"Seite {i+1}: {r.width:.2f} x {r.height:.2f}")
