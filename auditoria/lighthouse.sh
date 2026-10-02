# Lighthouse (mismo motor que PageSpeed) en local. Requiere: npm i lighthouse@12 y la CA del proxy en ~/.pki/nssdb.
# Uso: bash auditoria/lighthouse.sh (desde una carpeta con node_modules/.bin/lighthouse)
export CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
for s in "" cuanto-consume-aire-acondicionado/ cuanto-consume-freidora-de-aire/ cuanto-consume-radiador-de-aceite/ cuanto-consume-termo-electrico/ cuanto-consume-una-nevera/ por-que-salta-el-diferencial/; do
  n=$(echo "${s:-portada}" | tr -d /)
  for i in 1 2 3; do node_modules/.bin/lighthouse "https://tuluzencasa.com/$s" --only-categories=performance,accessibility,best-practices,seo --form-factor=mobile --output=json --output-path="m-$n-$i.json" --quiet --chrome-flags="--headless=new --no-sandbox" >/dev/null 2>&1; done
  node_modules/.bin/lighthouse "https://tuluzencasa.com/$s" --only-categories=performance,accessibility,best-practices,seo --preset=desktop --output=json --output-path="d-$n.json" --quiet --chrome-flags="--headless=new --no-sandbox" >/dev/null 2>&1
  echo "hecho $n"
done
