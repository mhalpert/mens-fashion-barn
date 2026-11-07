"""Select the women's catalog and outfits, add simulated fields. Deterministic."""
import json,re,sys,random,hashlib,collections,os
ROOT=sys.argv[1]; random.seed(77)
C=json.load(open(ROOT+"/data/women_candidates.json"))
bad=set(json.load(open(ROOT+"/data/exclude_women.json"))) if os.path.exists(ROOT+"/data/exclude_women.json") else set()
NOPE=re.compile(r"wgaca|chanel|14k|lab grown|sam edelman|steve madden|matisse|faithy|\bset\b|fur\b|mink|shearling|tennis dress|bag and mule",re.I)
P=[c for c in C if len(c["images"])>=3 and len(c["description"])>=40 and not NOPE.search(c["title"]) and c["src"]+c["src_id"] not in bad and not (c["brand"]=="Alo" and c["category"]=="Swim")]
for c in P: c["key"]=c["src"]+":"+c["src_id"]
def pick(sub,rx,brand=None,no=None):
    r=[c for c in P if c["subcategory"]==sub and re.search(rx,c["title"],re.I) and (not brand or c["brand"]==brand) and not (no and re.search(no,c["title"],re.I))]
    r.sort(key=lambda c:(-min(len(c["images"]),6),c["title"]))
    return r[0] if r else None
GOLD=("Earrings",r"gold",None,r"hoop.*huggie")
L=[
("formal-wedding","Black Tulle Gown","A full black gown for a black-tie evening.",[("Gown",r"Tulle Dress - Black$"),("Heels",r"black",  "Dolce Vita"),("Clutch",r"Paloma.*Noir"),("Earrings",r"Large Crystal Chandelier"),("Bracelets",r"Icon Tennis")]),
("formal-wedding","Emerald Satin","Deep green satin with gold at the ankle and ear.",[("Maxi Dress",r"Emerald|Moss Green"),("Heels",r"gold"),("Clutch",r"Paloma.*Oro"),("Earrings",r"Deco Pearl"),("Necklaces",r"Elowin.*Gold")]),
("formal-wedding","Burgundy Sequins","A sequin maxi for a wedding with a dance floor.",[("Maxi Dress",r"Burgundy Sequins"),("Heels",r"black"),("Clutch",r"Paloma.*Noir"),("Earrings",r"Ola Hoop")]),
("beach-wedding","Sunset Maxi","A light maxi that moves in the sea air.",[("Maxi Dress",r".","L*Space"),("Sandals",r"tan|natural"),("Clutch",r"raffia"),("Earrings",r"^Mini Hoop"),("Bracelets",r"Amara Tennis")]),
("beach-wedding","Garden Party Dress","A printed dress with raffia heels for an afternoon ceremony.",[("Dress",r".","Staud",r"black|sweater|knit"),("Heels",r"raffia"),("Clutch",r"natural|tan"),("Earrings",r"pearl")]),
("beach-wedding","Easy Jumpsuit","A jumpsuit for guests who would rather skip the dress.",[("Jumpsuit",r"Gigi Chiffon Jumpsuit - Sage"),("Sandals",r"DIXI"),("Clutch",r"IONE"),("Necklaces",r"^Roxie Necklace")]),
("beach-vacation","Poolside One-Piece","A one-piece, a wrap and a wide hat for a long day by the water.",[("One-Piece",r".","Solid & Striped"),("Cover-Up",r"Wrap Maxi"),("Sandals",r"natural|tan"),("Hats",r"straw|brim"),("Sunglasses",r".","Jenni Kayne"),("Tote",r"raffia|mesh|straw|canvas")]),
("beach-vacation","Bikini and Pareo","A bikini with a pareo that doubles as a skirt for lunch.",[("Bikini Top",r"^Zahara\ Bikini\ Top\ \-\ Nostalgia\ Playground$"),("Bikini Bottom",r"^Zahara\ Bikini\ Bottom\ \-\ Nostalgia\ Playground$"),("Cover-Up",r"pareo"),("Sandals",r"DIXI"),("Hats",r"straw|brim"),("Tote",r"mesh|raffia|canvas")]),
("beach-vacation","Boardwalk Mini","A simple mini dress for dinner after the beach.",[("Mini Dress",r".","L*Space"),("Sandals",r"DIXI"),("Sunglasses",r".","Jenni Kayne"),("Bracelets",r"Amara Tennis")]),
("business-casual","The Power Suit","A sharp blazer and wide-leg trouser for the big meeting.",[("Blazer",r"Kati.*Dark For"),("Trousers",r"Tinsley.*Dark For"),("Blouse",r"silk"),("Loafers",r"BODI LOAFERS BLACK"),("Tote",r".","Cuyana"),("Earrings",r"Gold/Pearl")]),
("business-casual","Knit and Trouser","A fine knit over a straight trouser for everyday work.",[("Knitwear",r"crew|cashmere","Naadam"),("Trousers",r"Straight-Leg Trouser"),("Loafers",r"BODI LOAFERS BLACK"),("Tote",r".","Cuyana"),("Necklaces",r"Elowin.*Gold")]),
("business-casual","Workday Dress","One dress, one jacket, and the morning is solved.",[("Dress",r"Aditi.*Charcoal"),("Blazer",r"Priscilla.*Knit Suiting.*Charcoa"),("Heels",r"RAMIA HEELS BLACK"),("Handbag",r".","Cuyana"),("Earrings",r"Estelle")]),
]
looks=[];forced={};miss=[]
for theme,name,desc,slots in L:
    it=[]
    for s in slots:
        c=pick(s[0],s[1],*s[2:])
        if not c: miss.append((name,s[:2])); continue
        forced[c["key"]]=c; it.append((s[0],c["key"]))
    looks.append(dict(theme=theme,name=name,description=desc,items=it,gender="women"))
print("MISSING",miss)
Q={"Gown":22,"Maxi Dress":18,"Midi Dress":6,"Mini Dress":14,"Dress":26,"Jumpsuit":10,"Blouse":28,"Tank":12,"Tee":14,"Knitwear":24,"Sweatshirt":12,"Bodysuit":6,"Jeans":16,"Trousers":22,"Skirts":16,"Shorts":12,"Joggers":8,"Leggings":14,"Sports Bra":10,"Blazer":14,"Jacket":14,"Coat":8,"Bikini Top":10,"Bikini Bottom":8,"One-Piece":14,"Cover-Up":10,"Heels":20,"Flats":10,"Sandals":14,"Boots":10,"Sneakers":10,"Loafers":6,"Handbag":14,"Clutch":6,"Tote":6,"Earrings":10,"Necklaces":10,"Bracelets":6,"Rings":4,"Belts":6,"Scarves":5,"Hats":8,"Sunglasses":6}
def base(t): return re.sub(r"\s*(\| | - | ~ | :: ).*$","",t).strip().lower()
sel=dict(forced)
for sub,q in Q.items():
    have=[c for c in sel.values() if c["subcategory"]==sub]
    by=collections.defaultdict(list)
    for c in P:
        if c["subcategory"]==sub and c["key"] not in sel: by[c["brand"]].append(c)
    for b in by: random.shuffle(by[b]); by[b].sort(key=lambda c:len(c["images"])<4)
    used=collections.Counter(base(c["title"]) for c in have)
    while len(have)<q and any(by.values()):
        for b in sorted(by):
            while by[b]:
                c=by[b].pop(0)
                if used[base(c["title"])]<3:
                    used[base(c["title"])]+=1; sel[c["key"]]=c; have.append(c); break
            if len(have)>=q: break
def colors(c):
    o=c["options"]; v=next((o[k] for k in o if "color" in k or "colour" in k),None)
    if v and v[0].lower()!="default title": return v[:8],"feed"
    m=re.search(r"(?: - | \| | ~ | :: )([^-|~:]+)$",c["title"])
    if m: return [m.group(1).strip().title()],"title"
    return ["Assorted"],"title"
SIM={"numeric":[str(x) for x in range(0,18,2)],"denim":[str(x) for x in range(24,35)],"shoe":[str(x/2).rstrip("0").rstrip(".") for x in range(10,23)],"alpha":["XS","S","M","L","XL"],"one":["One Size"]}
def stype(c):
    if c["category"] in("Bags","Jewelry") or c["subcategory"] in("Scarves","Sunglasses","Hats","Belts"): return "one"
    if c["category"]=="Shoes": return "shoe"
    if c["subcategory"]=="Jeans": return "denim"
    if c["category"]=="Dresses" or c["subcategory"] in("Blazer","Trousers","Skirts"): return "numeric"
    return "alpha"
def sizes(c):
    t=stype(c); o=c["options"]; v=next((o[k] for k in o if k=="size" or "size" in k),None)
    if v and v[0].lower() not in("default title","os","one size") and len(v)>1:
        if v[0].upper() in("XXS","XS","S","M","L","XL"): t="alpha"
        return t,v[:16],"feed"
    return t,SIM[t],"simulated"
def style(c):
    b,cat,s=c["brand"],c["category"],c["subcategory"]
    if b in("Alo","Beyond Yoga","Outdoor Voices") or cat=="Activewear": return "Athletic"
    if b=="Kith": return "Streetwear"
    if cat=="Swim" or b in("L*Space","Solid & Striped","Vitamin A"): return "Resort"
    if b in("Birdy Grey","Show Me Your Mumu") or s in("Gown","Clutch","Heels"): return "Formal"
    if b in("M.M.LaFleur","Cuyana","Sarah Flint") or s in("Blazer","Trousers","Loafers"): return "Business Casual"
    return "Casual"
OCC={"Formal":["wedding","black tie","party"],"Business Casual":["office","client meeting","dinner"],"Casual":["weekend","everyday"],"Streetwear":["everyday","weekend"],"Athletic":["gym","yoga","travel"],"Resort":["beach","vacation","pool"]}
items=sorted(sel.values(),key=lambda c:(c["category"],c["subcategory"],c["title"]))
out=[];idm={}
for i,c in enumerate(items,1):
    pid=f"WW-{i:04d}"; idm[c["key"]]=pid; col,cs=colors(c); st,sz,ss=sizes(c)
    h=int(hashlib.md5(c["key"].encode()).hexdigest(),16); r=random.Random(h)
    price=float(int(c["price"])) if c["price"]>=20 else round(c["price"],2)
    sale=r.random()<.15; disc=r.choice([.15,.2,.25,.3]); sty=style(c)
    txt=(c["title"]+" "+c["description"]).lower(); tags=[]
    if re.search(r"linen|swim|short|sandal|raffia|bikini",txt): tags.append("summer")
    if c["category"]=="Swim" or c["subcategory"]=="Sandals": tags.append("vacation")
    out.append(dict(id=pid,gender="women",title=c["title"],brand=c["brand"],category=c["category"],subcategory=c["subcategory"],style=sty,occasions=OCC[sty],season_tags=tags,description=c["description"],details=c["details"],colors=col,color_source=cs,size_type=st,sizes=sz,size_source=ss,images=[],image_dir=hashlib.md5(c["key"].encode()).hexdigest()[:12],source_images=c["images"][:5],source_url=c["url"],source=c["src"],source_id=c["src_id"],
      simulated=dict(price=price if not sale else round(price*(1-disc),2),compare_at_price=price if sale else None,on_sale=sale,sku=f"{pid}-{hashlib.md5(c['title'].encode()).hexdigest()[:5].upper()}",rating=round(r.uniform(3.8,4.9),1),review_count=r.randint(4,380),inventory={s:r.choice([0,2,3,5,8,12,20]) for s in sz})))
for l in looks: l["items"]=[dict(slot=s,product_id=idm[k]) for s,k in l["items"]]
json.dump(out,open(ROOT+"/data/catalog/women_products.json","w"),ensure_ascii=False,indent=1)
json.dump(looks,open(ROOT+"/data/catalog/women_outfits.json","w"),ensure_ascii=False,indent=1)
print(len(out),"items; forced",len(forced)); print(collections.Counter(x["style"] for x in out)); print(collections.Counter(x["brand"] for x in out).most_common(25)); print(collections.Counter(x["category"] for x in out).most_common())
by={x["id"]:x for x in out}
for l in looks:
    print("\n"+l["theme"],"/",l["name"])
    for i in l["items"]: x=by[i["product_id"]]; print("   ",i["slot"],"->",x["brand"],"|",x["title"][:60],"|",x["simulated"]["price"])
