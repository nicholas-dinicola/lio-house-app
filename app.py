import pywebio
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import argparse
import numpy as np
import pandas as pd
from joblib import load
from geopy.geocoders import Nominatim

application = Flask(__name__)

# Load the model in
model = load("Optimised_Xgb.joblib")

# Main Function
def predict():

    # Markdown text

    put_markdown(
        """# Predicting House Price - by *Lio Capital Srl*
    
    * The algorithm has been built utilizing real estate data collected  on various sources. 
    * This model is specific for  the cities of Pomezia, Ardea, Anzio, Ostia e Roma.
    
    ### Instructions
    Just fill up the form below and hit **Submit**. For repeated generation, just reload the page which will bring back this interface. Default values are provided in the form.  
    """,
        strip_indent=4,
    )

    # Variables to get
    #Spese_Condominio = input("Inserisci le spese di condominio:", type=NUMBER)
    Spese_Condominio = 86
    Superficie_MQ = input("Property size (Sqm)", type=FLOAT)
    Locali = input("Number of rooms:", type=FLOAT)
    Bagni = input("Number of bathrooms:", type=FLOAT)
    Piano = input("Floor:", type=FLOAT)
    #Anno_Costruzione = input("Inserire l'anno di costruzione:", type=NUMBER)
    Anno_Costruzione = 1970
    Totale_Piani = input("Building total number of floors:", type=NUMBER)

    """
    Ascensore = input("Fornito di ascensore: 'Si' - 'No'", type=TEXT)
    if(Ascensore=="si" or Ascensore=="SI"):
        Ascensore=1
    else:
        Ascensore=0
    """
    Ascensore=1

    """"
    Posti_Auto = input(
        "Fornito di posti auto: 'Si' - 'No'", type=TEXT
    )
    if(Posti_Auto=="Si" or Posti_Auto=="SI" or Posti_Auto=="si"):
        Posti_Auto=1
    else:
        Posti_Auto=0
    """
    Posti_Auto=0

    """"
    Terrazza = input("Fornito di terrazza: 'Si' - 'No'", type=TEXT)
    if(Terrazza=="si" or Terrazza=="SI" or Terrazza=="Si"):
        Terrazza=1
    else:
        Terrazza=0
    """

    Balcone = input("Balcony: 'Yes' - 'No'", type=TEXT)
    if(Balcone=="yes" or Balcone=="Yes" or Balcone=="YES"):
        Balcone=1
    else:
        Balcone=0

    """"
    Giardino_Privato = input(
        "Fornito di giardino privato: 'Si' - 'No'", type=TEXT
    )
    if(Giardino_Privato=="si" or Giardino_Privato=="SI" or Giardino_Privato=="Si"):
        Giardino_Privato=1
    else:
        Giardino_Privato=0
    """
    Giardino_Privato=0

    """"
    Giardino_Comune = input(
        "Fornito di giardino comune: 'Si' - 'No'", type=TEXT
    )
    if(Giardino_Comune=="Si" or Giardino_Comune=="SI" or Giardino_Comune=="si"):
        Giardino_Comune=1
    else:
        Giardino_Comune=0
    """
    Giardino_Comune=0

    """
    Arredato = input("Fornito di arredamento:  'Si' - 'No'", type=TEXT)
    if(Arredato=="Si" or Arredato=="si" or Arredato=="SI"):
        Arredato=1
    else:
        Arredato=0
    """
    Arredato=0

    """"
    Cantina = input("Fornito di cantina: 'Si' - 'No'", type=TEXT)
    if(Cantina=="Si" or Cantina=="si" or Cantina=="SI"):
        Cantina=1
    else:
        Cantina=0
    """
    Cantina = 0

    """
    Piscina = input("Fornito di piscina: 'Si' - 'No'", type=TEXT)
    if(Piscina=="Si" or Piscina=="SI" or Piscina=="si"):
        Piscina=1
    else:
        Piscina=0
    """
    Piscina=0



    ### Inserire un checkbox ai sottostanti
    # Città = input("Inserie il nome della città:", type=TEXT, datalist=["Roma", "Pomezia", "Ardea", "Nettuno"])
    Città = select("City:", options=[
        ("Roma"),
        ("Pomezia"),
        ("Ardea"),
        ("Nettuno")
    ])

    Indirizzo = input("Address of the property:", type=TEXT)

    # Stato = input("Inserie lo stato dell'immobile:", type=TEXT)
    Stato = select("Conditions of the property:", options=[
        ("Buono / Abitabile"),
        ("Ottimo / Ristrutturato"),
        ("Da ristrutturare"),
        ("Nuovo / In costruzione")
    ])

    # Riscaldamento = input("Inserie il tipo di riscaldamento dell'immobile:", type=TEXT)
    """"
    Riscaldamento = select("Inserie il tipo di riscaldamento dell'immobile:", options=[
        ("Autonomo"),
        ("Centralizzato")
    ])
    """
    Riscaldamento="Autonomo"

    # Climatizzazione = input(
    #     "Inserie il tipo di climatizazione dell'immobile:", type=TEXT
    # )
    """"
    Climatizzazione = select("Inserie il tipo di climatizazione dell'immobile:", options=[
        ("Autonomo"),
        ("Predisposizione impianto"),
        ("Centralizzato")
    ])
    """
    Climatizzazione = "Autonomo"

    # Tipologia = input("Inserire la tipologia dell'immobile:", type=TEXT)
    Tipologia = select("Typology of the property:", options=[
        ("Appartamento"),
        ("Villa"),
        ("Attico"),
        #("Rustico")
    ])

    if Tipologia == "Attico":
        Terrazza = 1
    else:
        Terrazza= 0

    # Cucina = input("Inserire la tipologia di cucina:", type=TEXT)
    """"
    Cucina = select("Inserire la tipologia di cucina:", options=[
        ("cucina abitabile"),
        ("cucina angolo cottura"),
        ("cucina semi abitabile"),
        ("cucina a vista"),
        ("cucina cucinotto")
    ])
    """
    Cucina="cucina abitabile"

    # Efficienza_Energitica = input("Inserire l'efficienza energetca:", type=TEXT)
    """
    Efficienza_Energitica = select("Inserire l'efficienza energetca:", options=[
        ("G"),
        ("F"),
        ("A"),
        ("E"),
        ("A+"),
        ("D"),
        ("B"),
        ("C"),
        ("A4"),
        ("A1"),
        ("A3"),
        ("A2")
    ])
    """
    Efficienza_Energitica = "A"

    ### Street and City Lat Long
    # Latitudine = input("Inserire la latitudine:", type=FLOAT)
    # Longitudine = input("Inserire la longitudine:", type=FLOAT)

    def get_location(Indirizzo, Città):
        geolocator = Nominatim(user_agent="skr")
        location = geolocator.geocode(f"{Indirizzo} {Città}")
        lat = location.latitude
        lon = location.longitude
        return lat, lon

    Latitudine, Longitudine = get_location(Indirizzo, Città)
    # Enter Street and City

    X = pd.DataFrame(
        np.array(
            [
                [
                    Spese_Condominio,
                    Superficie_MQ,
                    Locali,
                    Bagni,
                    Piano,
                    Anno_Costruzione,
                    Totale_Piani,
                    Ascensore,
                    Posti_Auto,
                    Terrazza,
                    Balcone,
                    Giardino_Privato,
                    Giardino_Comune,
                    Arredato,
                    Cantina,
                    Piscina,
                    Città,
                    Stato,
                    Riscaldamento,
                    Climatizzazione,
                    Tipologia,
                    Cucina,
                    Efficienza_Energitica,
                    Latitudine,
                    Longitudine,
                ]
            ]
        ),
        columns=[
            "Spese condominio/mese",
            "Superficie(sqm)",
            "Locali",
            "Bagni",
            "Piano",
            "Anno di costruzione",
            "Totale piani",
            "Ascensore",
            "Posti auto",
            "Terrazza",
            "Balcone",
            "Giardino privato",
            "Giardino comune",
            "Arredato",
            "Cantina",
            "Piscina",
            "Città",
            "Stato",
            "Riscaldamento",
            "Climatizzazione",
            "Tipologia",
            "Cucina",
            "Efficienza energetica",
            "Latitudine",
            "Longitudine",
        ],
    )

    prediction = model.predict(X)

    # output_price = np.round(prediction, 2)
    output_priceMQ = np.round((prediction[0]/Superficie_MQ), 2)

    # Print the predicted price
    # output_price = int(output_price)
    # put_text("Price:", output_price, " €")
    put_text("Price per SQ meters: ", output_priceMQ, " €")

    # Print the predicted price
    # put_text("Price per square meter:", output_priceMQ)


# if __name__ == "__main__":

application.add_url_rule(
    "/", "webio_view", webio_view(predict), methods=["GET", "POST", "OPTIONS"]
)

if __name__ == '__main__':
    #application.run(port=5000, debug=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)