import requests
import os
import googletrans
import json
import webbrowser
import cv2
import asyncio


with open("urls.json", "r") as file:
    install_url = json.load(file)


with open("sites.json", "r") as file:
    sites = json.load(file)

help_description = ["stop: stopt het programma",
        "clear of cls: maakt het scherm leeg",
        "weer: geeft het weer van een stad naar keuze",
        "vertaal: vertaalt een tekst van keuze naar een taal van keuze",
        "foto: maakt een foto",
        "install: installeert een programma", 
        "reken: voert een bewerking uit",
        "verander kleur: verandert de kleur van het tekst",
        "recept: krijg het recept van een gerecht naar keuze",
        "ip: track een IP adres naar keuze",
        "telefoonnummer: een adresboek (lees, schrijf en verwijder nummers)",
        "verklein url: verkleint een url naar keuze",
        "open SITE: verander site met de naam van een site en het opent die site",
        "todo: een todo boek",
        "help: geeft dit help scherm weer" ]

def clear_screen():
    """
    This function clears the screen.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def ip_tracker(ip: str):
    """
    A function to track IP's
    
    :param ip: The IP adres to track
    :type ip: str
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        lat, lon = data['lat'], data['lon']
        print(f"land: {data['country']}\nregio: {data['regionName']}\ncity: {data['city']}\ngoogle maps: https://maps.google.com/?q={lat},{lon}")
    except KeyError:
        print("Er was een error.")



def install_file(url: str, naam: str):
    """
    A function to install a file based on an url and saves it in a name
    
    :param url: the url
    :param naam: The name of the file
    """
    response = requests.get(url)
    content = response.content
    with open(naam, "wb") as file:
        file.write(content)


def installeer():
    """
    A function that uses the install_file function to install apps
    """
    
    ai = input("Welke app wil je installeren( lijst voor de mogelijkheden)? ")
    if ai == "lijst":
        for element in install_url:
            print(element)
    else:
        for element in install_url:
            if element in ai:
                install_file(install_url[element], f"{element}.exe")
                os.startfile(f"{element}.exe")
                print("File is installing")
                break
        else:
            print("Not found")



def nieuws():
    """
    A function that give news
    """
    # Still in development. I have to find a good API or site to scrape.
    pass



def weer():
    """
    This function prints the weather based on the city that is given.
    """
    try:
        city = input("De stad waarvan je het weer wilt weten: ")
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
        data = response.json()
        lat, lon = data['results'][0]['latitude'], data['results'][0]['longitude']
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m"
        response = requests.get(url)
        data = response.json()
        print(f"temperatuur: {data['current']['temperature_2m']} °C\nwindsnelheid: {data['current']['wind_speed_10m']} km/h\nregen: {data['current']['rain']} mm")
    except KeyError:
        print("Er was een error")
        return

def foto():
    """
    This function will take a picture and save it if you press enter. If you press q then it will quit without saving.
    """
    try:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            key = cv2.waitKey(1)
            cv2.imshow("test", frame)
            if key == ord('q'):
                cv2.destroyAllWindows()
                cap.release()
                break
            elif key == 13:
                cv2.destroyAllWindows()
                cv2.imwrite(f"{input("Naam van de foto: ")}.jpg", frame)
                cv2.imshow("foto", frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cap.release()
                break
    except Exception:
        print("Er was een error.")
    

async def vertaal(text: str, result: str="en"):
    """
    This function translates the given text and returns the translation.
    
    :param text: The text to translate.
    :type text: str
    :param resultaat: The language to translate to.
    :type result: str
    """
    try:
        vertaler = googletrans.Translator()
        vertaling = await vertaler.translate(text, dest=result)
        return f"{text} --> {vertaling.text}"
    except ValueError:
        print("De taal is niet in onze catalogus.")

def recept(food: str):
    """
    This function will print the food, ingridients and instructions based on the input.
    
    :param food: The food to give its recept
    :type food: str
    """
    
    try:
        translated_food = vertaal(food).replace(f"{food} --> ", "")
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={translated_food}"
        response = requests.get(url)
        data = response.json()
        print(f"{food} \ningredient: ")
        for i in range(20):
            if data['meals'][0][f'strIngredient{i+1}'] != "":
                print(f"{i+1}: {vertaal(data['meals'][0][f'strIngredient{i+1}'], "nl").replace(f"{data['meals'][0][f'strIngredient{i+1}']} --> ", "")}; aantal: {vertaal(data['meals'][0][f'strMeasure{i+1}'], "nl").replace(f"{data['meals'][0][f'strMeasure{i+1}']} --> ", "")}")
            else:
                break
        print(vertaal(data['meals'][0]["strInstructions"], "nl").replace(f"{data['meals'][0]["strInstructions"]} --> ", ""))
    except KeyError:
        print("Er was een error")

def verklein_url(url: str):
    """
    This function will print a shorter url for the same domain.
    
    :param url: Description
    :type url: str
    """

    url = f"https://ulvis.net/api.php?url={url}"
    print(requests.get(url).text)

def telefoonnummer():
    """
    This function will save phone numbers and retrieve them from a json file.
    """
    action: int = 0
    try:
        with open("nummer.json", "r") as nummerlijst:
            number_dir = json.load(nummerlijst)
    except FileNotFoundError:
        number_dir = {}
    while not (action in [1,2,3]):
        try:
            action = int(input("Opslaan(1), lezen(2), verwijderen(3): "))
            if not (action in [1,2,3]):
                raise ValueError
        except ValueError:
            print("Het nummer moet 1 of 2 zijn.")
    try:
        if action == 1:
            name = input("de naam: ").lower()
            number = input("het nummer: ")
            number_dir[name] = number
        elif action == 2:
            name = input("de naam: ").lower()
            print(f"{name}: {number_dir[name]}")
        else:
            name = input("de naam: ")
            number_dir.pop(name)
    except KeyError:
        print("Deze naam is nog niet opgeslagen.")
    with open("nummer.json", "w") as nummerlijst:
        nummerlijst.write(json.dumps(number_dir))

def reken():
    """
    This is a function to calculate.
    """
    
    try:
        reken = input("Welke bewerking wilt u doen? \n1) optellen \n2) aftrekken \n3) delen \n4) vermenigvuldigen\n5) machten \n6)vierkantswortel\n")
        if reken == "1":
            getal1 = float(input("Wat is het eerste getal? "))
            getal2 = float(input("Wat is het tweede getal? "))
            print(f"{getal1} + {getal2} = {getal1 + getal2}")
        elif reken == "2":
            getal1 = float(input("Wat is het eerste getal? "))
            getal2 = float(input("Wat is het tweede getal? "))
            print(f"{getal1} - {getal2} = {getal1 - getal2}")
        elif reken == "3":
            getal1 = float(input("Wat is het deeltal? "))
            getal2 = float(input("Wat is de deler? "))
            print(f"{getal1} / {getal2} = {getal1/getal2}")
        elif reken == "4":
            getal1 = float(input("Wat is het eerste getal? "))
            getal2 = float(input("Wat is het tweede getal? "))
            print(f"{getal1} * {getal2} = {getal1 * getal2}")
        elif reken == "5":
            getal1 = float(input("Wat is het grondtal? "))
            getal2 = float(input("Wat is exponent? "))
            print(getal1 ** getal2)
        elif reken == "6":
            getal1 = float(input("Wat is het getal? "))
            print(getal1 ** 0.5)
    except ValueError:
        print("Er was een error")


def verander_kleur():
    """
    This function will change the color of the terminal.
    """
    
    colors = {
    "zwart": "0",
    "blauw": "1",
    "groen": "2",
    "aqua": "3",
    "rood": "4",
    "paars": "5",
    "geel": "6",
    "wit": "7",
    "grijs": "8",
    "licht bluaw": "9",
    "licht groen": "A",
    "licht aqua": "B",
    "licht rood": "C",
    "licht paars": "D",
    "licht geel": "E",
    "helder geel": "F"
}
    ai = input("Welke kleur wil je?( lijst voor mogelijkheden) ")
    if ai == "lijst":
        for element in colors:
            print(element)
    else:
        for element in colors:
            if element in ai:
                os.system(f"color {colors[element]}")
                break
        else:
            print("Niet gevonden.")


def todo():
    if os.path.exists("todo.json"):
        with open ("todo.json", "r") as file:
            todo = json.load(file)
    else:
        with open("todo.json", "w") as file:
            todo = {}
            file.write("{}")
    keuze = input("Typ 1 voor een nieuwe TODO.\nTyp 2 voor een lijst van TODO.\nTyp 3 om een todo te verwijderen.\nTyp 4 om de status van je todo te veranderen\n")
    if keuze == "1":
        naam = input("Wat zal de naam van de nieuwe todo zijn? ").lower()
        beschrijving = input("Een korte beschrijving: ")
        todo[naam] = [beschrijving, "ongedaan"]
    elif keuze == "2":
        for element in todo:
            print(f"naam: {element} \nbeschrijving: {todo[element][0]} \nstatus: {todo[element][1]} \n")
    elif keuze == "3":
        naam = input("Wat was de naam van de todo? ").lower()
        try:
            del todo[naam]
        except KeyError:
            print("Deze todo is niet gevonden.")
    elif keuze == "4":
        naam = input("Wat was de naam van de todo? ").lower()
        try:
            if todo[naam][1] == "gedaan":
                todo[naam][1] = "ongedaan"
            else:
                todo[naam][1] = "gedaan"
        except KeyError:
            print("Deze todo bestaat nog niet.")
    with open("todo.json", "w") as file:
        json.dump(todo, file)
    



while True:    
    ai = input("wat wil je doen? ")
    ai = ai.lower()
    if "stop" in ai:
        exit()
    elif ("clear" in ai) or ("cls" in ai):
        clear_screen()
    elif "weer" in ai:
        weer()
    elif "vertaal" in ai:
        tekst = input("De tekst die je wilt vertalen: ")
        taal = input("taal waar je in wilt vertalen (leeg is gelijk aan engels): ")
        if taal == "":
            result = asyncio.run(vertaal(tekst))
        else:
            result = asyncio.run(vertaal(tekst, taal))
        print(result)
    elif "foto" in ai:
        print("Om te stoppen klik op de knop 'q' en om het te accepteren klik op de enter-knop")
        foto()
    elif "install" in ai:
        installeer()
    elif "reken" in ai:
        reken()
    elif ("verander" in ai) and ("kleur" in ai):
        verander_kleur()
    elif "recept" in ai:
        eten = input("Van welk eten wil je het recept weten? ")
        recept(eten) 
    elif "ip" in ai:
        ip = input("Welk IP-adres wil je tracken? ")
        ip_tracker(ip)
    elif ("telefoon" in ai) and ("nummer" in ai):
        telefoonnummer()
    elif ("klein" in ai) and ("url" in ai):
        url = input("Welke url wil je verkleinen (vergeet geen https)? ")
        verklein_url(url)
    elif "open" in ai:
        for site in sites:
            if site in ai:
                webbrowser.open(sites[site])
                break
        else:
            print("Niet gevonden.")
    elif "todo" in ai:
        todo()
    elif "help" == ai:
        for element in help_description:
            print(element)
    elif ai == "":
        continue
    else:
        print("Niet gevonden.")
        


