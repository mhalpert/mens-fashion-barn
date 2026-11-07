#!/bin/bash
# Sample one feed page per store. Honest user agent, slow pace, no retries.
UA='fashion-hackathon-catalog/0.1 (non-commercial hackathon demo)'
OUT="$1"
for s in www.birdygrey.com www.showmeyourmumu.com www.staud.clothing www.hillhousehome.com www.cuyana.com www.mmlafleur.com jennikayne.com www.tuckernuck.com www.rhode-resort.com www.faithfullthebrand.com realisationpar.com www.petalandpup.com www.princesspolly.com www.hellomolly.com www.meshki.us www.ohpolly.com www.outdoorvoices.com girlfriend.com www.beyondyoga.com www.aloyoga.com summersalt.com www.andieswim.com www.vitaminaswim.com www.solidandstriped.com www.sarahflint.com birdies.com www.dolcevita.com www.loefflerrandall.com www.stevemadden.com www.rothys.com www.baublebar.com gorjana.com www.mejuri.com www.senreve.com www.motherdenim.com www.paige.com www.agolde.com www.naadam.co www.ullajohnson.com www.marahoffman.com www.lovestitch.com www.lspace.com www.aninebing.com www.vince.com; do
  r=$(curl -s -m 12 -A "$UA" "https://$s/robots.txt" | awk 'tolower($1)=="user-agent:"{a=($2=="*")} a&&tolower($1)=="disallow:"' | grep -c -E 'products\.json|^[Dd]isallow: /\*?\.json|^[Dd]isallow: /products/?$')
  c=$(curl -s -m 25 -A "$UA" -o "$1/$s.json" -w '%{http_code}' "https://$s/products.json?limit=250")
  echo "$s robots=$r http=$c"
  [ "$c" = 200 ] || rm -f "$1/$s.json"
  sleep 5
done
echo DONE
