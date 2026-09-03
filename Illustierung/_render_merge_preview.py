import fitz
p = r"C:\Users\Lars\Documents\GitHub\Wisskomm\Inseln\1_Anleitung\Spielanleitung (4)_A4_A4quer.pdf"
doc = fitz.open(p)
page = doc[0]
pix = page.get_pixmap(dpi=72)
pix.save("C:/Users/Lars/AppData/Local/Temp/preview_merge.png")
print("rendered", page.rect)
