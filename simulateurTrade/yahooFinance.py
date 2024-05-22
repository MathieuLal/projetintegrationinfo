import yfinance as yf
from datetime import datetime
import pytz
import time

# Vérifie si le titre boursier que l'utilisateur
# a rentré est valide
def verifer_Nom_Ticker_valide(ticker):
    try:
        stock_info = yf.Ticker(ticker)
        historical_data = stock_info.history(period="1d")
        last_close_price = historical_data["Close"].iloc[-1]
        if last_close_price:
            return True, last_close_price
        else:
            return False, None
    except IndexError as e:
        return False, None
    except Exception as e:
        return False, None

# retour une string écrit d'un façon spécifique 
def format_valeur_symbole(valeur, symbole):
    valeur_formater = '{:.2f}{}'.format(valeur, symbole)
    return valeur_formater

# regard si l'utilisateur a mis un nombre
def est_nombre(valeur):
    try:
        float(valeur)
        return True
    except ValueError:
        return False

# regarde si le marché boursier est ouvert
def market_is_open():
    heure_actuelle = time.localtime().tm_hour
    aujourd_hui = datetime.now()

    if heure_actuelle >= 10 and heure_actuelle <= 16 and aujourd_hui != 5 and aujourd_hui != 6:
        return True
    return False

# return le prix d'un titre boursier 
def get_Prix_Stock(ticker):
    stock = yf.Ticker(ticker)
    typeInfo = stock.get_info()

    marcherOuvert = market_is_open()

    if 'quoteType' in typeInfo and typeInfo['quoteType'] == 'CRYPTOCURRENCY' or not marcherOuvert:
        historical_data = stock.history(period="1d")
        price = historical_data["Close"].iloc[-1]
    else:
        price = stock.info['ask']
    
    return price

def moment_du_trade():
    fuseau_horaire_canada = pytz.timezone('Canada/Eastern')

    heure_utc = datetime.utcnow()
    heure_canadienne = heure_utc.replace(tzinfo=pytz.utc).astimezone(fuseau_horaire_canada)
    # renvoie le moment de l'action
    temps = heure_canadienne.strftime('%Y-%m-%d')
    return temps