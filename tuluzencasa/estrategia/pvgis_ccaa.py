"""Producción fotovoltaica anual por kWp instalado en la capital de cada comunidad (PVGIS 5.3, JRC).
Sistema: 1 kWp, pérdidas 14 %, inclinación y orientación óptimas (optimalangles=1). Sin clave."""
import json,time,urllib.request
CAP=[('Andalucía','Sevilla',37.389,-5.984),('Aragón','Zaragoza',41.649,-0.889),('Asturias','Oviedo',43.361,-5.849),
('Illes Balears','Palma',39.570,2.650),('Canarias','Las Palmas de Gran Canaria',28.124,-15.430),('Canarias','Santa Cruz de Tenerife',28.464,-16.251),
('Cantabria','Santander',43.462,-3.810),('Castilla-La Mancha','Toledo',39.863,-4.027),('Castilla y León','Valladolid',41.652,-4.724),
('Cataluña','Barcelona',41.385,2.173),('Comunitat Valenciana','Valencia',39.470,-0.376),('Extremadura','Mérida',38.916,-6.344),
('Galicia','Santiago de Compostela',42.878,-8.544),('Comunidad de Madrid','Madrid',40.417,-3.704),('Región de Murcia','Murcia',37.992,-1.131),
('Navarra','Pamplona',42.812,-1.646),('País Vasco','Vitoria-Gasteiz',42.847,-2.672),('La Rioja','Logroño',42.465,-2.445),
('Ceuta','Ceuta',35.889,-5.321),('Melilla','Melilla',35.292,-2.938)]
out=[]
for ca,ci,la,lo in CAP:
    u=f'https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat={la}&lon={lo}&peakpower=1&loss=14&optimalangles=1&outputformat=json'
    d=json.load(urllib.request.urlopen(u,timeout=60))
    t=d['outputs']['totals']['fixed']; m=d['inputs']['mounting_system']['fixed']
    out.append({'comunidad':ca,'ciudad':ci,'kwh_kwp_ano':round(t['E_y']),'inclinacion':m['slope']['value'],'azimut':m['azimuth']['value']})
    time.sleep(1.2)
json.dump(out,open('pvgis_ccaa.json','w'),ensure_ascii=False,indent=1)
for o in sorted(out,key=lambda o:-o['kwh_kwp_ano']): print(o)
