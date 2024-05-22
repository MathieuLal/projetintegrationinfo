from flask import Flask, request
from termcolor import colored
from collections import Counter
from datetime import datetime
import pytz
from io import StringIO

class Transaction:
    def __init__(self, ticker, prix, temps, action):
        self.ticker = ticker
        self.prix = prix
        self.temps = temps
        self.action = action

class BotInfo:
    def __init__(self, capital_initial, capital_non_investi, capital_investi, capital_totale,
                 pourcentage_investir, commission_fee, nbr_fee, nbTrade,
                 trade_perdant, trade_gagnant, pourcentage_gagnant, pourcentage_perdant,
                 capital_perdu, capital_gagner):
        self.positions = []
        self.gains = []
        self.capital_initial = capital_initial
        self.capital_non_investi = capital_non_investi
        self.capital_investi = capital_investi
        self.capital_totale = capital_totale
        self.pourcentage_investir = pourcentage_investir
        self.commission_fee = commission_fee
        self.nbr_fee = nbr_fee
        self.nbTrade = nbTrade
        self.trade_perdant = trade_perdant
        self.trade_gagnant = trade_gagnant
        self.pourcentage_gagnant = pourcentage_gagnant
        self.pourcentage_perdant = pourcentage_perdant
        self.capital_perdu = capital_perdu
        self.capital_gagner = capital_gagner
        self.average_W = []
        self.average_L = []
    
    def ajouter_positions(self, position):
        self.positions.append(position)

    def ajouter_gain(self, gain):
        self.gains.append(gain)

    def ajouter_average_W(self, gain):
        self.average_W.append(gain)

    def ajouter_average_L(self, perte):
        self.average_L.append(perte)


app = Flask(__name__)

# debut des methodes
def moment_du_trade():
    fuseau_horaire_canada = pytz.timezone('Canada/Eastern')

    heure_utc = datetime.utcnow()
    heure_canadienne = heure_utc.replace(tzinfo=pytz.utc).astimezone(fuseau_horaire_canada)
    # renvoie le moment de l'action
    return colored(heure_canadienne.strftime('%Y-%m-%d %H:%M:%S'), "blue")

def format_valeur_et_symbole(valeur, symbole):
    valeur_formater = '{:.2f}{}'.format(valeur, symbole)
    return valeur_formater

def mettre_a_jour_capital_totale(capital_investi, capital_non_investi):
    return capital_investi + capital_non_investi

def jumeller_les_recurrences(tickers, qtAcheter, valeur, botInfo):

    tickers = [transaction['ticker'] for transaction in botInfo.positions]

    # compte les occurrences de chaque ticker
    occurrences = Counter(tickers)
    
    # crée un list avec juste les tickers qui apparaisse >1
    tickers_multiples = [ticker for ticker, count in occurrences.items() if count > 1]

    # Pour chaque ticker multiple, traitez les positions correspondantes
    for ticker in tickers_multiples:
        transactions_multiples = [transaction for transaction in botInfo.positions if transaction['ticker'] == ticker]
        valeurCombiner = 0
        qtAcheterCombiner = 0
        premiereValeurRecuperee = False
        valeurPremierAchat = 0
        
        for transaction in transactions_multiples:
            # addition les valeurs et les Qt acheter
            valeurCombiner = transaction.get('valeur', None) + valeurCombiner
            qtAcheterCombiner = transaction.get('qtAcheter', None) + qtAcheterCombiner

            if not premiereValeurRecuperee: # regarde si c'est le premier pour faire le calcul d'investissement
                valeurPremierAchat = transaction.get('valeur', None)
                premiereValeurRecuperee = True
        
        coutMoyen = valeurCombiner / qtAcheterCombiner
        # efface toutes les positions avec le ticker
        botInfo.positions = [transaction for transaction in botInfo.positions if transaction['ticker'] != ticker]

        botInfo.positions.append({# crée un nouvelle position avec les valeurs jumellées
                'ticker': ticker,
                'qtAcheter': qtAcheterCombiner,
                'valeur': valeurCombiner,
                'prixAchat': coutMoyen,
                'action': 'buy'
            })
        # ajuste les valeurs de capital investi pour être sur qu'on puisse faire d'autre achat ou non
        botInfo.capital_non_investi = botInfo.capital_non_investi + valeurPremierAchat - valeurCombiner
        botInfo.capital_investi = botInfo.capital_investi - valeurPremierAchat + valeurCombiner
        return qtAcheterCombiner, valeurCombiner
    
    # Pour réduire si autre alert buy et regard combien est investi
    botInfo.capital_non_investi = botInfo.capital_non_investi - valeur
    botInfo.capital_investi = botInfo.capital_investi + valeur
    return qtAcheter, valeur

def calcule_rentabiliter_trade(gain_individuel, botInfo): 
    #calcule toutes les infos sur qualite de tes trades

    if gain_individuel > 0:
        botInfo.trade_gagnant += 1
        botInfo.capital_gagner += gain_individuel
        botInfo.average_W.append(gain_individuel)
    else:
        botInfo.trade_perdant += 1
        botInfo.capital_perdu += gain_individuel
        botInfo.average_L.append(gain_individuel)

    botInfo.nbTrade += 1

    botInfo.pourcentage_gagnant = (botInfo.trade_gagnant/botInfo.nbTrade)*100
    botInfo.pourcentage_perdant = (botInfo.trade_perdant/botInfo.nbTrade)*100

def ecrireDansFichier(result_string, numeroBot):
    if numeroBot == 1:
        with open("Bot1", "a") as fichier:
            fichier.write(result_string)        
    elif numeroBot == 2:
        with open("Bot2", "a") as fichier:
            fichier.write(result_string)  
    elif numeroBot == 3:
        with open("Bot3", "a") as fichier:
            fichier.write(result_string)  
    elif numeroBot == 4:
        with open("Bot4", "a") as fichier:
            fichier.write(result_string) 

def botMessage(position_actuel_instance, botInfo, numeroBot, droitPerdre):

    botInfo.capital_totale = mettre_a_jour_capital_totale(botInfo.capital_investi, botInfo.capital_non_investi)

    qtAcheter = 0
    valeur = 0

    if position_actuel_instance.action == 'buy' and botInfo.capital_non_investi > 8:
        #regarde combien pas investi et investi un pourcentage et le tranforme en stock
        qtAcheter = (botInfo.pourcentage_investir * botInfo.capital_non_investi) / float(position_actuel_instance.prix)
        valeur = qtAcheter * float(position_actuel_instance.prix)

        # Stocker les informations de la transaction dans la liste
        botInfo.positions.append({
            'ticker': position_actuel_instance.ticker,
            'qtAcheter': qtAcheter,
            'valeur': valeur,
            'prixAchat': float(position_actuel_instance.prix),
            'action': 'buy'
        })
                
        qtAcheter, valeur = jumeller_les_recurrences(position_actuel_instance.ticker, qtAcheter, valeur, botInfo)
        botInfo.nbr_fee += 1

        string_builder_buy = StringIO()
        string_builder_buy.write(colored("===================================================================", "magenta") + "\n")
        string_builder_buy.write(moment_du_trade() + " Robot : " + str(numeroBot) + ",  temps  " + str(position_actuel_instance.temps) + "\n")
        string_builder_buy.write("Ticker: " + str(position_actuel_instance.ticker) + ", Prix Actuel: " + str(position_actuel_instance.prix) + "$, Action: " + colored(position_actuel_instance.action, "light_yellow") + "\n")
        string_builder_buy.write("QT acheter: " + str(qtAcheter) + ", valeur : " + format_valeur_et_symbole(valeur, '$') + "\n")
        string_builder_buy.write("Valeur du compte: " + format_valeur_et_symbole(botInfo.capital_totale, '$') + "\n")
        string_builder_buy.write("Capitale non investi: "+ format_valeur_et_symbole(botInfo.capital_non_investi, '$') +", Capitale investi: "+ format_valeur_et_symbole(botInfo.capital_investi,'$') + "\n")
        string_builder_buy.write(colored("===================================================================", "magenta") + "\n")

        result_string_buy = string_builder_buy.getvalue()
        print(result_string_buy)

        ecrireDansFichier(result_string_buy, numeroBot)

        string_builder_buy.truncate(0)
        string_builder_buy.seek(0)

    else:
        # Trouver la transaction d'achat correspondante dans la liste
        transactions_achat = next((t for t in botInfo.positions if t['ticker'] == position_actuel_instance.ticker and t['action'] == 'buy'), None)

        if transactions_achat:
            # btc lors sell - btc lors achat * qt = $$
            botInfo.nbr_fee += 1

            gain_individuel = (float(position_actuel_instance.prix) - transactions_achat['prixAchat']) * transactions_achat['qtAcheter'] - botInfo.commission_fee * botInfo.nbr_fee

            
            if gain_individuel > 0 or droitPerdre:
                calcule_rentabiliter_trade(gain_individuel, botInfo)
                botInfo.nbr_fee = 0

                botInfo.gains.append({# liste avec tous les gains pour calculer le PnL
                    "gain": gain_individuel
                })
                somme_totale = sum(transaction["gain"] for transaction in botInfo.gains)

                moyenne_W = 0
                moyenne_L = 0
                if len(botInfo.average_W) != 0:
                    moyenne_W = sum(botInfo.average_W) / len(botInfo.average_W)
                if len(botInfo.average_L) != 0:
                    moyenne_L = sum(botInfo.average_L) / len(botInfo.average_L)

                # Afficher la progression du capital initial
                botInfo.capital_non_investi = gain_individuel + botInfo.capital_non_investi + transactions_achat['valeur']
                botInfo.capital_investi = botInfo.capital_investi - transactions_achat['valeur']
                botInfo.capital_totale = mettre_a_jour_capital_totale(botInfo.capital_investi, botInfo.capital_non_investi)

                # enlève la transaction pour quel ne soit plus compter
                botInfo.positions.remove(transactions_achat)
                string_builder = StringIO()
                string_builder.write(colored("===================================================================", "magenta") + "\n")
                string_builder.write(moment_du_trade() + " Robot : " + str(numeroBot) + ", temps:  " + str(position_actuel_instance.temps) + "\n")
                string_builder.write("Ticker: " + str(position_actuel_instance.ticker) + ", Prix Actuel: " + str(position_actuel_instance.prix) + "$, QT acheter : " +  
                      str(transactions_achat['qtAcheter']) +", Action: " + colored(position_actuel_instance.action, "light_yellow") + "\n")
                string_builder.write("Capital Initial: " +format_valeur_et_symbole(botInfo.capital_initial,'$') + ", Capital Actuel: " + format_valeur_et_symbole(botInfo.capital_totale,'$') + "\n")
                string_builder.write("Gain du dernier trade: " + format_valeur_et_symbole(gain_individuel,'$') +", PnL: " + format_valeur_et_symbole(somme_totale,'$') + "\n")
                string_builder.write("Capitale non investi: "+ format_valeur_et_symbole(botInfo.capital_non_investi,'$') +", Capitale investi: "+ format_valeur_et_symbole(botInfo.capital_investi,'$') + "\n")
                string_builder.write(colored("===================================================================", "cyan") + "\n")
                string_builder.write("Trade gagnant: " + str(botInfo.trade_gagnant) + ", % win: " + format_valeur_et_symbole(botInfo.pourcentage_gagnant,'%') + 
                      ", QT d'argent gagner : " + format_valeur_et_symbole(botInfo.capital_gagner, '$') + "\n")
                string_builder.write("Trade perdant: " + str(botInfo.trade_perdant) + ", % loss: " + format_valeur_et_symbole(botInfo.pourcentage_perdant,'%') + 
                      ", QT d'argent perdu :" + format_valeur_et_symbole(botInfo.capital_perdu, '$') + "\n")
                string_builder.write(colored("Moyenne Trade gagnant :" + format_valeur_et_symbole(moyenne_W, '$'), "green") + " // " +
                      colored("Moyenne Trade perdant :" + format_valeur_et_symbole(moyenne_L, '$'), "red") + "\n")
                string_builder.write(colored("===================================================================", "cyan") + "\n")
                string_builder.write(colored("===================================================================", "magenta") + "\n")

                result_string = string_builder.getvalue()
                print(result_string)

                ecrireDansFichier(result_string, numeroBot)

                string_builder.truncate(0)
                string_builder.seek(0)
            else :
                print(colored("Soit Pas de position ou la position est dans le negatif" + str(numeroBot), "red"))


#capital_initial, capital_non_investi, capital_investi, capital_totale,
#pourcentage_investir, commission_fee, nbr_fee, nbTrade,
#trade_perdant, trade_gagnant, pourcentage_gagnant, pourcentage_perdant,
#capital_perdu, capital_gagner
Bot1 = BotInfo(100, 100, 0, 0, 0.8, 0.05, 0, 0, 0, 0, 0, 0, 0, 0)
Bot2 = BotInfo(100, 100, 0, 0, 0.5, 0.05, 0, 0, 0, 0, 0, 0, 0, 0)
Bot3 = BotInfo(100, 100, 0, 0, 0.8, 0.05, 0, 0, 0, 0, 0, 0, 0, 0)
Bot4 = BotInfo(100, 100, 0, 0, 0.5, 0.05, 0, 0, 0, 0, 0, 0, 0, 0)

@app.route("/tradingview-to-webhook", methods=['POST'])
def tradingview_webhook():
    global Bot1
    global Bot2
    global Bot3
    global Bot4

    json_data = request.get_json()
    position_actuel_instance = Transaction(**json_data)

    if position_actuel_instance.temps == "30": # les appels qui arrivent du WebHook de 30 minutes
        botMessage(position_actuel_instance, Bot1, 1, True) # peut vendre a perte
        botMessage(position_actuel_instance, Bot2, 2, False)# ne peut pas vendre a perte
    elif position_actuel_instance.temps == "4": # les appels qui arrivent du WebHook de 4 heures
        botMessage(position_actuel_instance, Bot3, 3, True) # peut vendre a perte
        botMessage(position_actuel_instance, Bot4, 4, False)# ne peut pas vendre a perte

    return "AAAAAA"