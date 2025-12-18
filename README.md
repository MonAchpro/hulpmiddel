## Beschrijving



Dit programma is een hulpmiddel met verschillende functies, inclusief het weer, vertalen, en meer. Het gebruikt verschillende bibliotheken, zodat de gebruiker verschillende taken kan uitvoeren met de CLI.

---

## Belangrijke delen

### Geïmporteerde bibliotheken

- **requests**: Om met API's te communiceren.
- **os**: Om met bestanden te werken en het scherm leeg te maken.
- **googletrans**: Om tekst te vertalen.
- **json**: Om json te lezen en schrijven.
- **webbrowser**: Om websites te openen.
- **cv2**: Om foto's te maken.
- **asyncio**: Dit was nodig om ter vertalen.
- **typing**: Om de functies duidelijker te maken


### Extra bestanden

- **urls.json**: Bevat de urls en de naam om apps te installeren. Als je een eigen app toe wilt voegen, dan voeg je het toe in dit formaat: ```"app naam": "https://exe-url"``` 
- **sites.json**: Bevat de urls en de naam om websites te openen. Als je een eigen website toe wilt voegen, dan voeg je het toe in dit formaat: ```"website naam": "https://website-url"``` 
- **nummer.json**: Een json bestand dat nummers en namen bevat.
- **todo.json**: Een json bestand om todo's te volgen.
- **expenses.json**: Een json bestand om uitgavenyy te tracken.


### Functies

- **stop**: Dit stopt het programma. Dit is de veiligste weg om het programma te stoppen. 
- **clear** of **cls**: Dit maakt het scherm leeg. 
- **weer**: Geeft het weer van een stad naar keuze. 
- **vertaal**: vertaalt een tekst van keuze naar een taal van keuze 
- **foto**: maakt een foto 
- **install**: installeert een programma 
- **reken**: voert een bewerking uit 
- **verander kleur**: verandert de kleur van het tekst 
- **recept**: krijg het recept van een gerecht naar keuze 
- **ip**: track een IP adres naar keuze 
- **telefoonnummer**: een adresboek (lees schrijf en verwijder nummers) 
- **verklein url**: verkleint een url naar keuze 
- **open "site"**: verander site met de naam van een site en het opent die site 
- **todo**: een todo boek 
- **help**: geeft alle commandos en hun uitleg


### Installatie
1. Zorg ervoor dat python en pip geinstalleerd is.
2. Ga naar [hulpmiddel](https://github.com/MonAchpro/hulpmiddel) en klik op de code knop en dan download ZIP.
 - Breng het ZIP bestand naar waar je het wilt en pak het uit.
3. Of gebruik git
 - Open een terminal en schrijf dit 
```
git clone https://github.com/MonAchpro/hulpmiddel.git
cd hulpmiddel
```
 4. Schrijf dit in de terminal: 
```
pip install -r requirements.txt
```
5. Open het python bestand en profiteer.

### Gebruik

Dit programma vraagt je om een actie (kies uit een van deze: [hier](#Functies)) en voert een actie uit op basis van de functies.