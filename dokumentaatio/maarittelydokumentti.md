# Määrittelydokumentti
## Shakkibotti

Projektin tarkoituksena on kehittää shakkipeli ja shakkia mahdollisimman hyvin pelaava tekoäly, joka pystyy navigoimaan erilaisia pelitilanteita soveltaen sille kehitettyä heuristiikkafunktiota. Shakkipeliin kuuluu sisältyä ainakin tornittaminen, ohestalyönti ja sotilaan korotus, sekä ehkä myös toistuvaan asemaan perustuva tasapeli. Heuristiikkafunktion on tarkoitus arvioida pelitilannetta materiaalin määrän ja laadun lisäksi nappuloiden sijoittumisen mukaan, esim. avoimen diagonaalin näkevä lähetti on parempi kuin vain omat moukat näkevä lähetti. **Tekoäly on projektin ydin.** 

Tekoälyn on tarkoitus suorittaa ainakin osa seuraavista:
 + tunnistaa ja osata hyödyntää erilaisia taktisia liikkeitä; kiinnitykset, haarukka, paljastushyökkäys, deflektio
 + tunnistaa ja osata voittaa peli, jos laudalla on jokin tunnettu pakotettu matti
 + tunnistaa puolustaessa ja hyökätessä tietyt loppupelin periaatteet ja pelata optimaalisesti, esim. oppositio
 + yrittää saada aikaiseksi pattitilanne epäedullisissa asemissa

Projektissa käytetään [kurssisivulla tarjottua tekoälyalustaa](https://algolabra-hy.github.io/aiplatform-fi). Tekoäly kommunikoi alustan kanssa saaden informaation vastustajan tekemästä siirrosta ja komennon tehdä oman siirtonsa, jonka tekoäly kommunikoi alustalle tulostaen komennon ja laillisen siirron standardimuodossa.

## Kurssi-info

Käytän projektin tekemiseen pythonia, hallitsen javaa riittävän hyvin vertaisarvioidakseni javalla tehtyjä projekteja. Koodin dokumentointiin käytetään docstringeja.
Kuulun tietojenkäsittelytieteen kandidaattiohjelmaan.