import yfinance as yf
import schedule
import time
from datetime import datetime
from termcolor import colored

"""
    Ce code regarde le prix de crypto choisi le vendredi quand la bourse
    ferme et le lundi avant que le marcher ouvre et regarde s'il y a un divergence
    entre les prix car les cryptos sont ouvert toujours, mais pas la bourse
"""

def get_bitcoin_ethereum_price(ticker):
    
    prix_data = yf.download(ticker, start="2020-01-01", end="2024-12-31")
    prix = prix_data['Close'].iloc[-1]
    return prix

def verif_difference_majeur(crypto_diff, crypto_nom):
    if abs(crypto_diff) < 2:
        print(crypto_nom + " mouvement minimale : " + crypto_diff)
    elif abs(crypto_diff) < 5:
        if crypto_diff < 0:
            print(colored(crypto_nom + " mouvement majeur : " + crypto_diff, 'red'))
        else : 
            print(colored(crypto_nom + " mouvement majeur : " + crypto_diff, 'green'))
    else :
        if crypto_diff < 0:
            print(colored(crypto_nom + " mouvement ultra majeur : " + crypto_diff, 'red'))
        else : 
            print(colored(crypto_nom + " mouvement ultra majeur : " + crypto_diff, 'green'))     

def actions_planifiees():
    heure_actuelle = time.localtime().tm_hour
    aujourd_hui = datetime.now()

    if heure_actuelle == 16 and aujourd_hui.weekday() == 4:
        BTC_Vendredi_Fermeture = get_bitcoin_ethereum_price("BTC-USD")
        ETH_Vendredi_Fermeture = get_bitcoin_ethereum_price("ETH-USD")

    if heure_actuelle == 7 and aujourd_hui.weekday() == 0:
        BTC_Dimanche_Fermeture = get_bitcoin_ethereum_price("BTC-USD")
        ETH_Dimanche_Fermeture = get_bitcoin_ethereum_price("ETH-USD")

        BTC_Difference = ((BTC_Dimanche_Fermeture - BTC_Vendredi_Fermeture) / BTC_Vendredi_Fermeture) * 100
        ETH_Difference = ((ETH_Dimanche_Fermeture - ETH_Vendredi_Fermeture) / ETH_Vendredi_Fermeture) * 100
    
        verif_difference_majeur(BTC_Difference, "BTC")
        verif_difference_majeur(ETH_Difference, "ETH")

schedule.every(1).minutes.do(actions_planifiees)

while True:
    schedule.run_pending()
    time.sleep(1)