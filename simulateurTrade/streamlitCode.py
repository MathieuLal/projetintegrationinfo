import streamlit as st
import matplotlib.pyplot as plt
import yahooFinance 

st.set_page_config(layout="wide")

optionTrade, ActionPrise, Statistique = st.columns([1, 2, 1])
ticker = ""
nombre_action_acheter = 0

# initialise les valeurs que le code doit sa rappeler
if 'pourcentage_investir' not in st.session_state:
    st.session_state.pourcentage_investir = 50
if 'pourcentage_divergence' not in st.session_state:
    st.session_state.pourcentage_divergence = 0
if 'frais_transaction' not in st.session_state:
    st.session_state.frais_transaction = 0
if 'capital_totale' not in st.session_state:
    st.session_state.capital_totale = 0
if 'capital_investi' not in st.session_state:
    st.session_state.capital_investi = 0
if 'capital_non_investi' not in st.session_state:
    st.session_state.capital_non_investi = 0
if 'capital_donner' not in st.session_state:
    st.session_state.capital_donner = 0
if 'PnL' not in st.session_state:
    st.session_state.PnL = 0
if 'NBRajout' not in st.session_state:
    st.session_state.NBRajout = 0

container = st.empty()

if 'nbTrade' not in st.session_state:
    st.session_state.nbTrade = 0
if 'trade_W' not in st.session_state:
    st.session_state.trade_W = 0
if 'trade_L' not in st.session_state:
    st.session_state.trade_L = 0
if 'pourcentage_rentabilite' not in st.session_state:
    st.session_state.pourcentage_rentabilite = 0
if 'premierFois' not in st.session_state:
    st.session_state.premierFois = 0

# s'assure que les fichiers sont vide
if st.session_state['premierFois'] == 0: 
    with open('titre_acheter.txt', 'w') as file:
        pass
    with open('GraphCapitalTransaction.txt', 'w') as file:
        pass
    with open('Position_Actuel.txt', 'w') as file:
        pass
    st.session_state['premierFois'] += 1

# lorsqu'un bouton est clicker
def on_click():
    destination = [[]]
        
    with open('titre_acheter.txt', 'r') as file:
        fichierDeTransactions = file.readlines()
                
    for ligne in fichierDeTransactions:
        ligneTransaction = ligne.split()                   
        if len(destination) <= 0:
            destination.append(ligneTransaction)
        else:
            for ligneDestination in destination: # fusion les mêmes achats
                if len(ligneDestination) > 0:
                    if  ligneTransaction[0] == ligneDestination[0] :
                        nouvelleLigne = False
                        ligneDestination[1] = yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ligneTransaction[0]),' ') # prix actuel
                        if ligneTransaction[8] == "achat" and ligneDestination[8] == "achat":                            
                            ligneDestination[2] = yahooFinance.format_valeur_symbole((float(ligneTransaction[5]) + float(ligneDestination[5]))/(float(ligneTransaction[3]) + float(ligneDestination[3])), ' ') # prix achat moyen                                                    
                            ligneDestination[3] = yahooFinance.format_valeur_symbole(float(ligneTransaction[3]) + float(ligneDestination[3]), ' ') # QT acheter
                            ligneDestination[4] = yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ligneTransaction[0]) * float(ligneDestination[3]), ' ') #valeur actuel
                            ligneDestination[5] = yahooFinance.format_valeur_symbole(float(ligneTransaction[5]) + float(ligneDestination[5]), ' ') # valeur achat
                            ligneDestination[6] = yahooFinance.format_valeur_symbole(float(ligneTransaction[6]) + float(ligneDestination[6]), ' ') # frais de commission
                            ligneDestination[7] = yahooFinance.format_valeur_symbole(float(ligneDestination[4]) - float(ligneDestination[5]) - float(ligneDestination[6]), ' ') # gain
                        
                        elif ligneTransaction[8] == "vente" and ligneDestination[8] == "achat": 
                            ligneDestination[3] = yahooFinance.format_valeur_symbole(float(ligneDestination[3]) - float(ligneTransaction[3]), ' ')# QT acheter
                            ligneDestination[4] = yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ligneTransaction[0]) * float(ligneDestination[3]), ' ')#valeur actuel
                            ligneDestination[5] = yahooFinance.format_valeur_symbole(float(ligneDestination[2]) * float(ligneDestination[3]), ' ') # valeur achat
                            ligneDestination[6] = yahooFinance.format_valeur_symbole(float(ligneTransaction[6]) + float(ligneDestination[6]), ' ')# frais de commission
                            ligneDestination[7] = yahooFinance.format_valeur_symbole(float(ligneDestination[4]) - float(ligneDestination[5]) - float(ligneDestination[6]), ' ') # gain

                        elif ligneTransaction[8] == "achat" and ligneDestination[8] == "vente":          
                            ligneDestination[2] = yahooFinance.format_valeur_symbole(float(ligneTransaction[2]), ' ') # prix achat moyen                                                    
                            ligneDestination[3] = yahooFinance.format_valeur_symbole(float(ligneTransaction[3]) - float(ligneDestination[3]), ' ') # QT acheter
                            ligneDestination[4] = yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ligneTransaction[0]) * float(ligneDestination[3]), ' ') #valeur actuel
                            ligneDestination[5] = yahooFinance.format_valeur_symbole(float(ligneDestination[2]) * float(ligneDestination[3]), ' ') # valeur achat
                            ligneDestination[6] = yahooFinance.format_valeur_symbole(float(ligneTransaction[6]) + float(ligneDestination[6]), ' ') # frais de commission
                            ligneDestination[7] = yahooFinance.format_valeur_symbole(float(ligneDestination[4]) - float(ligneDestination[5]) - float(ligneDestination[6]), ' ') # gain

                        else:
                            ligneDestination[2] = yahooFinance.format_valeur_symbole( 0 , ' ') # prix achat moyen                                                    
                            ligneDestination[3] = yahooFinance.format_valeur_symbole(-float(ligneTransaction[3]) - float(ligneDestination[3]), ' ') # QT acheter
                            ligneDestination[4] = yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ligneTransaction[0]) * float(ligneDestination[3]), ' ') #valeur actuel
                            ligneDestination[5] = yahooFinance.format_valeur_symbole(0, ' ') # valeur achat
                            ligneDestination[6] = yahooFinance.format_valeur_symbole(float(ligneTransaction[6]) + float(ligneDestination[6]), ' ') # frais de commission
                            ligneDestination[7] = yahooFinance.format_valeur_symbole(float(ligneDestination[7]) + float(ligneDestination[7]) - float(ligneDestination[6]), ' ') # gain    
                else:
                    nouvelleLigne = True
            if nouvelleLigne:                
                destination.append(ligneTransaction)

    with open('Position_Actuel.txt', 'w') as file:
        for i in range(len(destination)):# toutes les positions combinés
            chaine = " ".join(destination[i])
           
            if chaine != "":
                if float(destination[i][3]) > 0:
                    file.write(chaine + "\n")    

# récupère les informations pour faire l'affichage
def Position_Actuel_ou_Historique_Liste(Fichier, UpdateValeur):
    with open(Fichier, 'r') as file:
        fichierDeTransactions = file.readlines()
    
    Positions = []
    for ligne in fichierDeTransactions:
        ligneTransaction = ligne.split()
        if len(ligneTransaction) > 1 and ligneTransaction != "":
            if UpdateValeur:
                ligneTransaction[1] = yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ligneTransaction[0]), ' ')
                ligneTransaction[4] = yahooFinance.format_valeur_symbole(float(ligneTransaction[1]) * float(ligneTransaction[3]), ' ')
                ligneTransaction[7] = yahooFinance.format_valeur_symbole(float(ligneTransaction[4]) - float(ligneTransaction[5]), ' ')
            
            Positions.append(ligneTransaction)

    return Positions

# première colonne 
with optionTrade:
    optionstrade = ['Hands picking']

    option_selectionner = st.radio(" ", optionstrade, index=0)

    # option Hands picking
    if option_selectionner == 'Hands picking':
        colonneText,colonneEntreUtilisateur = st.columns([1.5, 1])
        container.empty()

        # colonne de text
        with colonneText:
            st.write("Choisir: Action, etf ou crypto")
            st.write("")
            st.write("")
            st.write("Ticker:")
        
        # colonne où l'utilisateur rentre des données
        with colonneEntreUtilisateur:
            st.write("")
            st.write("")
            ticker = st.text_input("", value=ticker)

        # vérifie le ticker et retour le prix
        tickerValid, prixActuel = yahooFinance.verifer_Nom_Ticker_valide(ticker)
        
        if tickerValid:
            
            colonneText,colonneEntreUtilisateur = st.columns([1.5, 1])
            # colonne de text
            with colonneText:
                st.write("")
                st.write("Valeur Actuel: " + ticker)
                st.write("")     
                st.write("")           
                st.write("Quantité à acheter: ")
                st.write("")
                st.write("")
                st.write("Valeur : ")

            # colonne où l'utilisateur rentre des données
            with colonneEntreUtilisateur:
                
                st.write("")
                st.write(yahooFinance.format_valeur_symbole(prixActuel,'$'))# affiche le prix
                nombre_action_acheter = st.number_input("  ",min_value=0.0, max_value=100.0, step=0.1)
            
                valeur = nombre_action_acheter * prixActuel
                st.write("")
                st.write(yahooFinance.format_valeur_symbole(valeur, '$'))
                
            acheter = st.button("Acheter")

            # regarde si l'utilisateur à de l'argent et s'il veut acheter 
            if acheter and st.session_state['capital_non_investi'] >= valeur:
                st.session_state['capital_non_investi'] -= valeur
                st.session_state['capital_investi'] += valeur
                with open('titre_acheter.txt', 'a') as fichier:
                    
                    temps = yahooFinance.moment_du_trade() 
                    # crée un trade
                    # ticker, prix actuel, prix d'achat, Quantité acheter, valeur actuel, valeur d<achat, Frais de commission et gain 
                    fichier.write(
                                str(ticker).upper() + " " +
                                yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ticker), ' ') + " " +
                                yahooFinance.format_valeur_symbole(prixActuel, ' ') + " " +
                                yahooFinance.format_valeur_symbole(nombre_action_acheter, ' ') + " " +
                                yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ticker) * nombre_action_acheter, ' ') + " " +
                                yahooFinance.format_valeur_symbole(valeur, ' ') + " " +
                                yahooFinance.format_valeur_symbole(st.session_state['frais_transaction'], ' ') + " " +
                                yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(ticker) * nombre_action_acheter - valeur - st.session_state['frais_transaction'], ' ') + " " + 
                                "achat" + " " + str(temps)+ "\n"
                                )
                on_click() 
            elif acheter and st.session_state['capital_non_investi'] <= valeur: # message d'erreur
                st.markdown("<span style='color:red'>**Vous n<avez pas assez d<argent**</span>", unsafe_allow_html=True)
        elif not tickerValid:
            if ticker != "":
                st.markdown("<span style='color:red'>**Ticker non valide**</span>", unsafe_allow_html=True)

    vendre =  st.checkbox("Vendre des titres:")
    # récupère les positions ouvertes
    positionsActuel = Position_Actuel_ou_Historique_Liste("Position_Actuel.txt", True) 

    if vendre and len(positionsActuel) > 0:

        colonneTextVente,colonneEntreUtilisateurVente = st.columns([1.5, 1])
        with colonneTextVente:
            st.write("  ")
            st.write("  ")
            st.write("Quel titre, voulez-vous vendre?")
            st.write("  ")
            st.write("  ")
            st.write("Quel quantité, voulez-vous vendre?")

        # crée un widget avec tous les positions actuel
        with colonneEntreUtilisateurVente:
            tableauTickerActif = []
            for element in positionsActuel:
                tableauTickerActif.append(element[0])

            tickerVendre = st.selectbox(" ", tableauTickerActif)

            tickerChoisiVendre = []
            for element in positionsActuel:
                if tickerVendre == element[0]:
                    tickerChoisiVendre = element
            
            QT_Vendre = st.number_input("   ", min_value=0.01, max_value= float(tickerChoisiVendre[3]), step=0.10)
            
        
        comfirmerVente = st.button("Vendre")
        if comfirmerVente:
            with open('titre_acheter.txt', 'a') as fichier:
                    
                temps = yahooFinance.moment_du_trade() 
                # s'il vend crée une nouvelle position
                # ticker, prix actuel, prix d'achat, Quantité acheter, valeur actuel, valeur d'achat, Frais de commission et gain 
                fichier.write(
                            str(tickerChoisiVendre[0]).upper() + " " +
                            yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(tickerChoisiVendre[0]), ' ') + " " +                                
                            yahooFinance.format_valeur_symbole(0, ' ') + " " +
                            yahooFinance.format_valeur_symbole(QT_Vendre, ' ') + " " +
                            yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(tickerChoisiVendre[0]) * float(tickerChoisiVendre[3]), ' ') + " " +
                            yahooFinance.format_valeur_symbole(0, ' ') + " " +
                            yahooFinance.format_valeur_symbole(st.session_state['frais_transaction'], ' ') + " " +
                            yahooFinance.format_valeur_symbole(yahooFinance.get_Prix_Stock(tickerChoisiVendre[0]) * float(QT_Vendre) - float(tickerChoisiVendre[2])*float(QT_Vendre) - st.session_state['frais_transaction'], ' ') + " " + 
                            "vente" + " " + str(temps)+ "\n"
                            )
            # calcule les informations de la colonne 3
            st.session_state['PnL'] += yahooFinance.get_Prix_Stock(tickerChoisiVendre[0])* float(QT_Vendre) - float(tickerChoisiVendre[2])*float(QT_Vendre)
            st.session_state['nbTrade'] += 1
            if float(tickerChoisiVendre[7]) > 0 : 
                st.session_state['trade_W'] += 1
            else:
                st.session_state['trade_L'] += 1

            st.session_state['pourcentage_rentabilite'] = (st.session_state['trade_W']/st.session_state['nbTrade'])*100

            st.session_state['capital_investi'] -= float(tickerChoisiVendre[2])*float(QT_Vendre)
            st.session_state['capital_non_investi']  += float(tickerChoisiVendre[2])*float(QT_Vendre)
            st.session_state['capital_totale'] = float(st.session_state.capital_investi) + float(st.session_state.capital_non_investi) + st.session_state.PnL

            # information pour les graphiques
            with open('GraphCapitalTransaction.txt', 'a') as fichier:
                fichier.write(  "Trade"+str(st.session_state['nbTrade']) + " " + str(yahooFinance.format_valeur_symbole(st.session_state['capital_totale'], ' ')) + " " + str(temps) + " " + str(yahooFinance.format_valeur_symbole(st.session_state['capital_totale'], ' ')) +"\n")

            on_click()             

# colonne 2
with ActionPrise:
    optionsGraphique = ['Capital/Temps', 'Capital/transaction', 'Pas de Graphique']
    option_selectionner_Graphique = st.radio("Sélectionnez une option de Graphique:", optionsGraphique, index=2)
    
    # les graphiques options
    if option_selectionner_Graphique == 'Capital/Temps':
        tableauInfo = Position_Actuel_ou_Historique_Liste("GraphCapitalTransaction.txt" , False)
        tableauTransaction = []
        tableauCapital = []
        
        for i in range(len(tableauInfo)):
            tableauTransaction.append(tableauInfo[i][2])
            tableauCapital.append(float(tableauInfo[i][3]))
        
        print(tableauCapital)

        if len(tableauTransaction) > 0 and len(tableauCapital) > 0:
            fig, ax = plt.subplots()
            ax.plot(tableauTransaction, tableauCapital, marker='o', linestyle='-', markersize=5)

            ax.set_xlabel('Transaction')
            ax.set_ylabel('Capital ($)')

            st.pyplot(fig)
    elif option_selectionner_Graphique == 'Capital/transaction':

        st.title("Graphique selon le capital et les transactions faites")
        
        tableauInfo = Position_Actuel_ou_Historique_Liste("GraphCapitalTransaction.txt" , False)
        tableauTransaction = []
        tableauCapital = []
        
        for i in range(len(tableauInfo)):
            tableauTransaction.append(tableauInfo[i][0])
            tableauCapital.append(float(tableauInfo[i][1]))

        if len(tableauTransaction) > 0 and len(tableauCapital) > 0:
            fig, ax = plt.subplots()
            ax.plot(tableauTransaction, tableauCapital, marker='o', linestyle='-', markersize=5)

            ax.set_xlabel('Transaction')
            ax.set_ylabel('Capital ($)')

            st.pyplot(fig)

        else:
            st.markdown("<span style='color:red'>**Aucune donner**</span>", unsafe_allow_html=True)



    optionsVisuelPosition = ['Historique de transaction', 'Position Actuel']
    option_selectionner = st.radio("Sélectionnez une option:", optionsVisuelPosition, index=1)
    
    # positions actuel avec leurs informations
    if option_selectionner == 'Position Actuel':
        TickerNom, Prix_actuel, Prix_achat, QT_acheter, Valeur_Actuel, Valeur_achat, fraisCommisson, gain   = st.columns(8)

        with TickerNom:
             st.write("Ticker:")

        with Prix_actuel:
             st.write("Prix Actuel:")
        
        with Prix_achat:
             st.write("Prix Achat:")
        
        with QT_acheter:
            st.write("QT Acheter:")

        with Valeur_Actuel:
             st.write("Valeur Actuel:")
        
        with Valeur_achat:
            st.write("Valeur Achat:")

        with fraisCommisson:
            st.write("Frais Commisson:")

        with gain:
            st.write("Gain:")

        listePositionActuel = Position_Actuel_ou_Historique_Liste("Position_Actuel.txt", True)

        for ligne in listePositionActuel:

            with TickerNom:
                st.write(ligne[0])

            with Prix_actuel:
                st.write(str(ligne[1]) + "$")
        
            with Prix_achat:
                st.write(str(ligne[2])+ "$")
        
            with QT_acheter:
                st.write(ligne[3])

            with Valeur_Actuel:
                st.write(str(ligne[4])+ "$")

            with Valeur_achat:
                st.write(str(ligne[5])+ "$")

            with fraisCommisson:
                st.write(str(ligne[6])+ "$")

            with gain:
                if float(ligne[7]) > 0:
                    st.write(f'<span style="color:green">{str(ligne[7] + " $")}</span>', unsafe_allow_html=True)
                elif float(ligne[7]) < 0:
                    st.write(f'<span style="color:red">{str(ligne[7]) + " $"}</span>', unsafe_allow_html=True)
                else :
                    st.write(str(ligne[7]) + " $")

    # list d'information sur toutes les trades prix
    elif option_selectionner == 'Historique de transaction':
        Date, TickerNom, Action, QT_acheter, Valeur_achat, fraisCommisson, gain   = st.columns(7)

        with Date:
            st.write("Date")

        with TickerNom:
            st.write("Ticker:")
        
        with Action:
            st.write("Action:")
        
        with QT_acheter:
            st.write("QT Acheter:")

        with Valeur_achat:
            st.write("Valeur de l'Action:")
        
        with fraisCommisson:
            st.write("Frais Commisson:")

        with gain:
            st.write("Profit:")

        listePositionActuel = Position_Actuel_ou_Historique_Liste("titre_acheter.txt", False)

        for ligne in listePositionActuel:
            with Date:
                st.write(str(ligne[9]))

            with TickerNom:
                st.write(str(ligne[0]))
        
            with Action:
                if ligne[8] == "achat":
                    st.write(f'<span style="color:green">{str(ligne[8])}</span>', unsafe_allow_html=True)
                else:
                    st.write(f'<span style="color:red">{str(ligne[8])}</span>', unsafe_allow_html=True)
        
            with QT_acheter:
                st.write(str(ligne[3]))

            with Valeur_achat:
                st.write(str(ligne[4])+ " $")   

            with fraisCommisson:
                st.write(str(ligne[6])+ " $")

            with gain:
                if  ligne[8] == "vente":
                    if float(ligne[7]) > 0:
                        st.write(f'<span style="color:green">{str(ligne[7] + " $")}</span>', unsafe_allow_html=True)
                    elif float(ligne[7]) < 0:
                        st.write(f'<span style="color:red">{str(ligne[7]) + " $"}</span>', unsafe_allow_html=True)
                else:
                    st.write("0$")

# colonne 3 
with Statistique:
    # Capital que l'utilisateur se donne pour trader
    with st.form("Donnez-vous du capital"):
        rajoutCapital = st.number_input(" ", min_value=0.0, max_value=1000000.0, step=10000.0)
        rajoutArgent = st.form_submit_button("Rajouter $")

    if rajoutArgent:# ajuste les valeurs si l'utilisateur se donne de l'argent
        st.session_state['capital_non_investi'] += rajoutCapital
        st.session_state['capital_donner'] += rajoutCapital
        st.session_state['capital_totale'] = float(st.session_state.capital_investi) + float(st.session_state.capital_non_investi) + st.session_state.PnL
        st.session_state['NBRajout'] += 1
        with open('GraphCapitalTransaction.txt', 'a') as fichier:
            fichier.write("Rajout"+str(st.session_state['NBRajout'])+"$" + " " + str(yahooFinance.format_valeur_symbole(st.session_state['capital_totale'], ' ')) + " " + "Rajout"+str(st.session_state['NBRajout'])+"$" + " "+ str(yahooFinance.format_valeur_symbole(st.session_state['capital_totale'], ' ')) + "\n")
       
    colonneText,colonneInfromationStatistique = st.columns([1.5, 2])
    
    with colonneText:
        st.write("  ")
        st.write("  ")
        st.write("capitale actuel ($):")
        st.write("  ")
        st.write("  ")
        st.write("capitale investi ($):")
        st.write("capitale non investi ($):")
        st.write("  ")
        st.write("PnL : ")
        st.write("  ")
        st.write("Nombre de trade pris:")
        st.write("Statistique (W/L) : ")
        st.write("Pourcentage de Rentabilité (%):")
        st.write("  ")
        st.write("  ")
        st.write("  ")
        st.write("Choisir frais de transaction ($):")

    with colonneInfromationStatistique: # montre les informations du compte   
        st.metric(" ", value=yahooFinance.format_valeur_symbole(float(st.session_state.capital_totale), '$'), delta=yahooFinance.format_valeur_symbole(float(st.session_state.PnL), '$'))
        st.write(yahooFinance.format_valeur_symbole(float(st.session_state.capital_investi), '$'))
        st.write(yahooFinance.format_valeur_symbole(float(st.session_state.capital_non_investi), '$'))
        st.write("  ")
        st.write(yahooFinance.format_valeur_symbole(float(st.session_state.PnL), '$'))
        st.write("  ")
        st.write(str(st.session_state['nbTrade']))
        st.write(str(st.session_state['trade_W']) + " / " + str(st.session_state['trade_L']))
        st.write(yahooFinance.format_valeur_symbole(st.session_state['pourcentage_rentabilite'], '%')) 
        st.write("  ")               
        st.session_state['frais_transaction'] = st.number_input("   ", min_value=0.0, max_value=10.0, step=0.01)
        
        reset = st.checkbox("Reset") # si l'utilisateur veux reset sont compte. Cela réinitialise les valeurs et les tableaux
        if reset:
            sur = st.button("Click ce bouton pour Reset le simulateur")
            if sur:               
                with open('titre_acheter.txt', 'w') as file:
                    pass
                with open('GraphCapitalTransaction.txt', 'w') as file:
                    pass
                with open('Position_Actuel.txt', 'w') as file:
                    pass
                st.session_state.pourcentage_divergence = 0
                st.session_state.capital_totale = 0
                st.session_state.capital_investi = 0
                st.session_state.capital_donner = 0
                st.session_state.PnL = 0
                st.session_state.trade_W = 0
                st.session_state.trade_L = 0
                st.session_state.pourcentage_rentabilite = 0
                st.session_state.pourcentage_investir = 50
                st.session_state.frais_transaction = 0
                st.session_state.capital_non_investi = 0                
                st.session_state.nbTrade = 0
                st.write("Fermez le checkBox pour Reset")