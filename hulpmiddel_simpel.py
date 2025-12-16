import requests
import os
import googletrans
import json
import webbrowser
import cv2


install_url = {"discord": "https://stable.dl2.discordapp.net/distro/app/stable/win/x64/1.0.9218/DiscordSetup.exe",
               "firefox": "https://download-installer.cdn.mozilla.net/pub/firefox/releases/146.0/win32/nl/Firefox%20Installer.exe",
               "virtualbox": "https://download.virtualbox.org/virtualbox/7.2.4/VirtualBox-7.2.4-170995-Win.exe",
               "obs": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-32.0.4-Windows-x64-Installer.exe",
               "vlc":" https://videolan.nl.mirrors.airvpn.org/vlc/3.0.21/win32/vlc-3.0.21-win32.exe",
               "google earth": "https://dl.google.com/tag/s/appguid%3D%7B65E60E95-0DE9-43FF-9F3F-4F7D2DFF04B5%7D%26iid%3D%7B65E60E95-0DE9-43FF-9F3F-4F7D2DFF04B5%7D%26lang%3Dnl%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Earth%2520Pro%26needsadmin%3DTrue%26brand%3DGGGE/earth/client/GoogleEarthProSetup.exe",
               "epic games": "https://epicgames-download1.akamaized.net/Builds/UnrealEngineLauncher/Installers/Windows/EpicInstaller-19.0.0.msi?launcherfilename=EpicInstaller-19.0.0.msi",
               "spotify": "https://download.scdn.co/SpotifySetup.exe",
               "steam": "https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe",
               }


def scherm_leeg():
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
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    lat, lon = data['lat'], data['lon']
    print(f"land: {data['country']}\nregio: {data['regionName']}\nstad: {data['city']}\ngoogle maps: https://maps.google.com/?q={lat},{lon}")



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
    
    stad = input("De stad waarvan je het weer wilt weten: ")
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={stad}")
    data = response.json()
    lat, lon = data['results'][0]['latitude'], data['results'][0]['longitude']
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m"
    response = requests.get(url)
    data = response.json()
    print(f"temperatuur: {data['current']['temperature_2m']} °C\nwindsnelheid: {data['current']['wind_speed_10m']} km/h\nregen: {data['current']['rain']} mm")

def foto():
    """
    This function will take a picture and save it if you press enter. If you press q then it will quit without saving.
    """
    
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
    

def vertaal(tekst: str, resultaat: str="en"):
    """
    This function translates the given text and returns the translation.
    
    :param tekst: The text to translate.
    :type tekst: str
    :param resultaat: The language to translate to.
    :type resultaat: str
    """
    
    vertaler = googletrans.Translator()
    vertaling = vertaler.translate(tekst, dest=resultaat)
    return f"{tekst} --> {vertaling.text}"

def recept(eten: str):
    """
    This function will print the food, ingridients and instructions based on the input.
    
    :param eten: The food to give its recept
    :type eten: str
    """
    
    ver_eten = vertaal(eten).replace(f"{eten} --> ", "")
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={ver_eten}"
    response = requests.get(url)
    data = response.json()
    print(f"{eten} \ningredient: ")
    for i in range(20):
        if data['meals'][0][f'strIngredient{i+1}'] != "":
            print(f"{i+1}: {vertaal(data['meals'][0][f'strIngredient{i+1}'], "nl").replace(f"{data['meals'][0][f'strIngredient{i+1}']} --> ", "")}; aantal: {vertaal(data['meals'][0][f'strMeasure{i+1}'], "nl").replace(f"{data['meals'][0][f'strMeasure{i+1}']} --> ", "")}")
        else:
            break
    print(vertaal(data['meals'][0]["strInstructions"], "nl").replace(f"{data['meals'][0]["strInstructions"]} --> ", ""))

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
    actie: int = 0
    try:
        with open("nummer.json", "r") as nummerlijst:
            nummer_dir = json.load(nummerlijst)
    except FileNotFoundError:
        nummer_dir = {}
    while not (actie in [1,2,3]):
        try:
            actie = int(input("Opslaan(1), lezen(2), verwijderen(3): "))
            if not (actie in [1,2,3]):
                raise ValueError
        except ValueError:
            print("Het nummer moet 1 of 2 zijn.")
    if actie == 1:
        naam = input("de naam: ").lower()
        nummer = input("het nummer: ")
        nummer_dir[naam] = nummer
    elif actie == 2:
        try:
            naam = input("de naam: ").lower()
            print(f"{naam}: {nummer_dir[naam]}")
        except KeyError:
            print("Deze naam is nog niet opgeslagen.")
    else:
        try:
            naam = input("de naam: ")
            nummer_dir.pop(naam)
        except KeyError:
            print("Deze naam is nog niet opgeslagen.")
    with open("nummer.json", "w") as nummerlijst:
        nummerlijst.write(json.dumps(nummer_dir))

def reken():
    """
    This is a function to calculate.
    """
    
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


def verander_kleur():
    """
    This function will change the color of the terminal.
    """
    
    kleuren = {
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
        for element in kleuren:
            print(element)
    else:
        for element in kleuren:
            if element in ai:
                os.system(f"color {kleuren[element]}")
                break
        else:
            print("Niet gevonden.")
    


while True:    
    ai = input("wat wil je doen? ")
    ai = ai.lower()
    if "stop" in ai:
        exit()
    elif ("clear" in ai) or ("cls" in ai):
        scherm_leeg()
    elif "weer" in ai:
        weer()
    elif "vertaal" in ai:
        tekst = input("De tekst die je wilt vertalen: ")
        taal = input("taal waar je in wilt vertalen (leeg is gelijk aan engels)")
        if taal == "":
            print(vertaal(tekst))
        else:
            print(vertaal(tekst, taal))
    elif "foto" in ai:
        print("Om te stoppen klik op de knop 'q' en om het te accepteren klik op de enter-knop")
        foto()
    elif "install" in ai:
        installeer()
    elif "reken" in ai:
        reken()
    elif ("verander" in ai) and ("kleur" in ai):
        verander_kleur()
    elif "eten" in ai:
        eten = input("Van welk eten wil je het recept weten? ")
        recept(eten) 
    elif "ip" in ai:
        ip = input("Welk IP-adres wil je tracken? ")
        ip_tracker(ip)
    else:
        print("Niet gevonden.")
        


