"""Check women's photos, merge both catalogs into products.json and outfits.json. Safe to rerun."""
import json,glob,os,sys,csv,shutil,collections
ROOT=sys.argv[1]; D=ROOT+"/data/catalog"
W=json.load(open(D+"/women_products.json")); WL=json.load(open(D+"/women_outfits.json"))
M=[p for p in json.load(open(D+"/products.json")) if p.get("gender")!="women"]
ML=[l for l in json.load(open(D+"/outfits.json")) if l.get("gender")!="women"]
for p in M: p["gender"]="men"
for l in ML: l["gender"]="men"
SIG=(b"\xff\xd8\xff",b"\x89PNG",b"RIFF",b"GIF8")
short=[]
for p in W+M:
    fs=[]
    for f in sorted(glob.glob(f"{D}/images/{p['image_dir']}/*")):
        h=open(f,"rb").read(12)
        if h.startswith(SIG) or h[4:8]==b"ftyp": fs.append(os.path.relpath(f,D))
        else: os.remove(f)
    p["images"]=fs
    if len(fs)<3: short.append(p)
print("women",len(W),"men",len(M),"photos",sum(len(p["images"]) for p in W+M),"under3",len(short))
for p in short[:15]: print("  ",p["id"],p["brand"],p["title"][:50],len(p["images"]))
if short:
    ex=ROOT+"/data/exclude_women.json"; old=json.load(open(ex)) if os.path.exists(ex) else []
    json.dump(old+[p["source"]+p["source_id"] for p in short if p["gender"]=="women"],open(ex,"w")); sys.exit(2)
P=W+M
json.dump(P,open(D+"/products.json","w"),ensure_ascii=False,indent=1)
json.dump(WL+ML,open(D+"/outfits.json","w"),ensure_ascii=False,indent=1)
keep={p["image_dir"] for p in P}
for d in os.listdir(D+"/images"):
    if d not in keep: shutil.rmtree(f"{D}/images/{d}")
with open(D+"/products.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow("id gender title brand category subcategory style colors size_type sizes price compare_at_price on_sale description image_1 image_2 image_3 source_url".split())
    for p in P:
        s=p["simulated"]; i=p["images"]
        w.writerow([p["id"],p["gender"],p["title"],p["brand"],p["category"],p["subcategory"],p["style"],"|".join(p["colors"]),p["size_type"],"|".join(p["sizes"]),s["price"],s["compare_at_price"],s["on_sale"],p["description"],i[0],i[1],i[2],p["source_url"]])
