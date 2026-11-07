"""Normalize women's Shopify feed samples into women_candidates.json."""
import json,glob,os,re,html,collections,sys
ROOT=sys.argv[1]
BRAND={"www.birdygrey.com":"Birdy Grey","www.staud.clothing":"Staud","www.ullajohnson.com":"Ulla Johnson","www.showmeyourmumu.com":"Show Me Your Mumu","www.mmlafleur.com":"M.M.LaFleur","www.cuyana.com":"Cuyana","www.aninebing.com":"Anine Bing","www.agolde.com":"Agolde","www.motherdenim.com":"Mother","jennikayne.com":"Jenni Kayne","www.naadam.co":"Naadam","www.aloyoga.com":"Alo","www.beyondyoga.com":"Beyond Yoga","www.outdoorvoices.com":"Outdoor Voices","www.lspace.com":"L*Space","www.solidandstriped.com":"Solid & Striped","www.vitaminaswim.com":"Vitamin A","www.sarahflint.com":"Sarah Flint","www.dolcevita.com":"Dolce Vita","birdies.com":"Birdies","www.loefflerrandall.com":"Loeffler Randall","gorjana.com":"Gorjana","kith.com":"Kith"}
EXCL=re.compile(r"swatch|sample|gift ?card|e-gift|\bmen'?s\b|\bmens\b|\bkids?\b|\bgirls?\b|\bboys?\b|\bbaby\b|toddler|mini me|\bmen:|furniture|textiles|decor|\bhome\b|ooak|candle|pajama|intimates|underwear|\bthong\b|cheeky hipster|\bpanty|shipping|protection|insurance|readers|charm\b|\bcharms\b|piercing|bead|cleaner|care kit|shoe tree|\blaces?\b|\bpillow|\bblanket|\btowel|\bmug\b|\bset of\b|bundle|gift box|pouch|\bdog\b|\bpet\b|ski\b",re.I)
SHOE=r"pumps?|heels?|flats?|sandals?|boots?|sneakers?|loafers?|slides?|shoes|mules?|ballet|slingback|clogs?"
R=[
("Bags","Clutch",r"clutch|minaudiere"),
("Bags","Tote",r"\btote\b"),
("Bags","Handbag",r"\|(fashion handbags|handbags|bags)$|\bbag\b|shoulder bag|crossbody|\bhobo\b|satchel|baguette"),
("Jewelry","Earrings",r"earrings?|\bhoops?\b|\bstuds?\b(?! belt)|\|earrings$"),
("Jewelry","Necklaces",r"necklace|\|necklaces$|pendant|choker"),
("Jewelry","Bracelets",r"bracelet|bangle|\|bracelets$"),
("Jewelry","Rings",r"\brings?\b.*\|(rings|jewelry)|\|rings$"),
("Swim","Cover-Up",r"cover.?up|sarong|kaftan|caftan|pareo"),
("Swim","One-Piece",r"one.?piece(?!.*dress)"),
("Swim","Bikini Top",r"bikini top|swim top|bralette top|\|bikini tops$"),
("Swim","Bikini Bottom",r"bikini bottom|swim bottom|\|bikini bottoms$"),
("Shoes","Heels",r"\|(pumps|heel sandals|heels)$|\bpumps?\b|stiletto|slingback|\bheels?\b"),
("Shoes","Boots",r"\|(boots|ankle boots|tall boots)$|\bboots?\b|\bbooties?\b"),
("Shoes","Loafers",r"\|loafers$|\bloafers?\b"),
("Shoes","Sandals",r"\|(sandals|slides)$|\bsandals?\b|\bslides?\b"),
("Shoes","Sneakers",r"\|sneakers?$|\bsneakers?\b"),
("Shoes","Flats",r"\|flats$|\bflats?\b|ballet|\bmules?\b"),
("Dresses","Jumpsuit",r"(jumpsuit|romper|playsuit)[^|]*\|"),
("Dresses","Gown",r"bridesmaid dress|\bgown\b"),
("Dresses","Maxi Dress",r"maxi\b.*dress|\bmaxi\b.*\|dress|\|maxi dress"),
("Dresses","Midi Dress",r"midi\b.*dress|\bmidi\b.*\|dress"),
("Dresses","Mini Dress",r"mini\b.*dress|\bmini\b.*\|dress"),
("Dresses","Dress",r"\bdress\b(?! pant| shirt)|\|dresses$|\|dress$|knit dresses"),
("Outerwear","Blazer",r"blazer"),
("Outerwear","Coat",r"\bcoat\b|trench|overcoat"),
("Outerwear","Jacket",r"jacket|bomber|\|jackets$|women:outerwear:jackets"),
("Activewear","Sports Bra",r"sports? bra|\|women:bras$|\|bras$|\bbra\b"),
("Activewear","Leggings",r"legging|bike short"),
("Bottoms","Shorts",r"\bshorts?\b(?! sleeve)"),
("Bottoms","Jeans",r"\bjeans?\b|\bdenim\b.*\|(pants|bottoms|apparel)"),
("Bottoms","Skirts",r"skirt|skort"),
("Bottoms","Joggers",r"jogger|sweatpant"),
("Bottoms","Trousers",r"trouser|\bpants?\b|\|pants$|\|bottoms$"),
("Tops","Sweatshirt",r"hood|sweatshirt|pullover.*\|women:outerwear"),
("Tops","Knitwear",r"sweater|cardigan|\bknit\b|cashmere|pullover|\|sweaters|\|crew neck sweaters$|turtleneck"),
("Tops","Bodysuit",r"bodysuit"),
("Tops","Tank",r"\btank\b|\bcami\b|camisole|\|women:tops:tanks$"),
("Tops","Tee",r"\btee\b|t-shirt|\|t-shirts$"),
("Tops","Blouse",r"blouse|shirt|\btop\b|\|tops$|\|knit tops$"),
("Accessories","Belts",r"\bbelts?\b"),
("Accessories","Scarves",r"scarf|scarves"),
("Accessories","Hats",r"\bhat\b|\bcap\b|beanie|visor"),
("Accessories","Sunglasses",r"sunglass"),
]
R=[(c,s,re.compile(x,re.I)) for c,s,x in R]
def classify(t,p):
    x=f"{t}|{p}".strip()
    for c,s,r in R:
        if r.search(x): return c,s
    return None,None
def clean(h):
    h=h or ""
    h=re.sub(r"<(style|script)[^>]*>.*?</\1>"," ",h,flags=re.S|re.I)
    li=[re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",x))).strip() for x in re.findall(r"<li[^>]*>(.*?)</li>",h,re.S|re.I)]
    b=re.sub(r"<li[^>]*>.*?</li>"," ",h,flags=re.S|re.I)
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",b))).strip(),[x for x in li if x]
out=[];drop=collections.Counter();seen=set()
files=[(s,ROOT+f"/data/raw/women_probe/{s}.json") for s in BRAND if s!="kith.com"]+[("kith.com",f) for f in sorted(glob.glob(ROOT+"/data/raw/feeds/kith.com.p*.json"))]
for s,f in files:
    for p in json.load(open(f))["products"]:
        if (s,p["id"]) in seen: continue
        seen.add((s,p["id"]))
        tags=p["tags"] if isinstance(p["tags"],list) else []
        if s=="kith.com" and not re.search(r"wom[ae]n|wmns",p["title"]+" "+p["product_type"]+" "+" ".join(tags),re.I): continue
        if EXCL.search(p["title"]+"|"+p["product_type"]): drop["excl"]+=1; continue
        pt=p["product_type"]
        if s=="www.aloyoga.com": pt=pt.split(":")[-1]
        c,sub=classify(p["title"],pt)
        if not c: drop["uncat:"+s]+=1; continue
        d,li=clean(p.get("body_html"))
        if len(d)<40 and li: d=". ".join(x.rstrip(".") for x in li[:4])+"."
        pr=[float(v["price"]) for v in p["variants"] if float(v["price"])>0]
        if not pr: continue
        out.append(dict(src=s,src_id=str(p["id"]),url=f"https://{s}/products/{p['handle']}",title=p["title"],brand=BRAND[s],ptype=p["product_type"],category=c,subcategory=sub,description=d,details=li,images=[i["src"] for i in p["images"]],options={o["name"].lower():o["values"] for o in p["options"]},price=min(pr)))
json.dump(out,open(ROOT+"/data/women_candidates.json","w"))
print(len(out),drop.most_common(10))
g=[x for x in out if len(x["images"])>=3 and len(x["description"])>=40]
print("quality",len(g))
for k,v in sorted(collections.Counter((x["category"],x["subcategory"]) for x in g).items()):
    print(k,v,collections.Counter(x["brand"] for x in g if (x["category"],x["subcategory"])==k).most_common(5))
