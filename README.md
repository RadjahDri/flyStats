# FlyStats
## Description
Le script génère des statistiques de vols à partir de traces GPS au format KML.

## Informations obtenues
Deux types de statistiques sont générées: globales à tous les vols (Temps de vol total par exemple) ou spécifique à chaque vol.
### Informations globales
#### Types d'informations
- Période de réalisation des vols
- Nombre de vols
- Temps de vol
- Temps de vol minimum
- Temps de vol maximum
- Temps de vol moyen
- Vol le plus tôt
- Vol le plus tard
- Record de vitesse
- Record de force G
- Record d'altitude

#### Exemple de sortie
```
Du 12/08/17 au 19/09/17
26 vols
Temps de vol total:  8h29m04s
Temps de vol minimum:  0h03m45s
Temps de vol maximum:  1h29m05s
Temps de vol moyen:  0h19m34s
Le vol le plus tot:  8h10m00s
Le vol le plus tard: 18h45m00s
La plus haute vitesse: 53.42km/h
La plus haute force G: 2.45g
La plus haute altitude: 1764m
```

### Informations spécifiques
#### Types d'informations
- Date
- Durée
- Heure de décollage
- Heure d'attérissage
- Record de vitesse
- Record de force G
- Record d'altitude
- Altitude de décollage
- Altitude de l'attérissage

#### Exemple de sortie
```
|--------|---------|---------|---------|---------|-----|-----|-----|-----|
|  Date  |  Duree  |Decollage|Atterissa|  Vit M  |Max G|Alt M|Alt D|Alt A|
|--------|---------|---------|---------|---------|-----|-----|-----|-----|
|06/09/17| 0h03m45s|10h13m00s|10h30m00s|07.25km/h|1.67g| 431m| 430m| 430m|
|07/09/17| 0h24m20s|11h36m00s|12h00m00s|40.21km/h|1.33g|1276m|1223m| 469m|
|07/09/17| 0h29m25s|16h50m00s|17h19m00s|53.42km/h|1.26g|1241m|1221m| 465m|
|08/09/17| 0h07m45s| 9h59m00s|10h07m00s|35.11km/h|1.41g|1187m|1187m| 470m|
|08/09/17| 0h07m35s|12h27m00s|12h35m00s|40.26km/h|1.36g|1124m|1124m| 468m|
|08/09/17| 0h14m30s|14h02m00s|14h16m00s|36.84km/h|1.33g|1218m|1217m| 475m|
|08/09/17| 0h14m30s|15h13m00s|15h28m00s|39.68km/h|1.35g|1196m|1196m| 469m|
|08/09/17| 0h10m55s|18h34m00s|18h45m00s|44.55km/h|1.51g|1203m|1203m| 476m|
|12/09/17| 0h09m40s|11h38m00s|11h48m00s|41.78km/h|1.21g|1394m|1390m| 753m|
|13/09/17| 0h03m50s| 8h43m00s| 8h47m00s|36.13km/h|1.46g| 992m| 992m| 734m|
|13/09/17| 0h16m55s|10h13m00s|10h30m00s|43.50km/h|1.23g|1556m|1550m| 763m|
|14/09/17| 0h20m04s| 8h54m00s| 9h14m00s|46.70km/h|1.25g|1540m|1539m| 757m|
|14/09/17| 0h44m55s|10h07m00s|10h52m00s|52.56km/h|1.44g|1569m|1569m| 771m|
|16/09/17| 0h09m05s| 9h20m00s| 9h29m00s|37.73km/h|2.07g|1079m|1079m| 445m|
|16/09/17| 0h09m30s|10h42m00s|10h52m00s|39.53km/h|1.26g|1072m|1072m| 450m|
|17/09/17| 0h21m00s|11h30m00s|11h51m00s|46.77km/h|1.29g|1418m|1372m| 463m|
|19/09/17| 0h10m45s| 9h58m00s|10h09m00s|43.21km/h|1.46g|1151m|1142m| 458m|
|19/09/17| 0h30m45s|11h39m00s|12h09m00s|50.30km/h|2.45g|1533m|1211m| 473m|
|19/09/17| 0h47m20s|15h42m00s|16h29m00s|46.75km/h|1.42g|1764m|1200m| 459m|
|--------|---------|---------|---------|---------|-----|-----|-----|-----|
```

## Utilisation
```
usage: flyStats.py -d DIR [-r]
```
- -d DIR: Chemin vers le dossier contenant les fichiers KML
- -r: Etend la recherche de fichiers KML aux sous dossiers
