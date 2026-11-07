"""Convert photos to WebP at most 800px wide. Needs Pillow. Keeps transparency. Safe to rerun."""
import glob,os,sys
from PIL import Image
n=0;bad=0
for f in glob.glob(sys.argv[1]+"/data/catalog/images/*/*"):
    if f.endswith(".webp"): continue
    o=os.path.splitext(f)[0]+".webp"
    try:
        im=Image.open(f); im=im.convert("RGBA" if im.mode in("RGBA","LA","P") else "RGB")
        im.thumbnail((800,1100)); im.save(o,"WEBP",quality=76,method=4); os.remove(f); n+=1
    except Exception as e: bad+=1; print("bad",f,e)
print("converted",n,"bad",bad)
