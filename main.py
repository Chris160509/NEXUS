from flask import Flask, render_template, request
import pyttsx3
import random
import json
import os

app = Flask(__name__)

# Initialiseer spraaksynthese (offline)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english')  # Pas aan als nodig

# Onthoud de laatste 10 berichten
gespreksgeschiedenis = []

# Laad bestaande kennis of maak een nieuwe kennisdatabase aan
KENNISBESTAND = "kennis_database.json"
if os.path.exists(KENNISBESTAND):
    with open(KENNISBESTAND, "r") as f:
        kennis_database = json.load(f)
else:
    kennis_database = {
        "wat is de hoofdstad van nederland": "De hoofdstad van Nederland is Amsterdam.",
        "wie is de president van de vs": "Op dit moment weet ik dat niet zeker, maar je kunt het opzoeken!",
        "hoeveel continenten zijn er": "Er zijn 7 continenten: Afrika, Antarctica, Azië, Europa, Noord-Amerika, Oceanië en Zuid-Amerika.",
    }

# Grappige reacties
grappige_reacties = [
    "Waarom had de computer honger? Omdat hij te veel bytes had!",
    "Ik vertelde een grap over elektriciteit... maar het sloeg niet in.",
    "Waarom kan een skelet niet liegen? Omdat je er zo doorheen kijkt!"
]

# Functie om Nexus te laten spreken
def spreken(tekst):
    print(f"Nexus: {tekst}")
    engine.say(tekst)
    engine.runAndWait()

@app.route("/", methods=["GET", "POST"])
def home():
    antwoord = ""
    user_input = ""
    if request.method == "POST":
        user_input = request.form["user_input"].lower()

        # Onthoud de laatste 10 berichten
        gespreksgeschiedenis.append(user_input)
        if len(gespreksgeschiedenis) > 10:
            gespreksgeschiedenis.pop(0)

        # Algemene kennisvragen
        if user_input in kennis_database:
            antwoord = kennis_database[user_input]
        # Grappige reacties
        elif "grap" in user_input or "vertel iets grappigs" in user_input:
            antwoord = random.choice(grappige_reacties)
        else:
            antwoord = "Sorry, ik weet niet het antwoord op dat."

        # Laat Nexus spreken
        spreken(antwoord)

    return render_template("./index.html", antwoord=antwoord, user_input=user_input)

if __name__ == "__main__":
    if __name__ == "__main__":
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)

