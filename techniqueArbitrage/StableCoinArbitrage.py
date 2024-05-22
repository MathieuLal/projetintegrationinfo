import streamlit as st
from pycoingecko  import  CoinGeckoAPI

"""
Regarde s'il y a un possiblité d'arbitrage entre les différents stablecoin(Pour cette exemple :token qui suit le prix d'une money) sur la blockchain
même si les stablecoin sont supposés de suivre le prix de 1 USD = 1 USDC/USDT/DAI... cela n'est pas toujours le cas, donc tu peux changer entre les 
stablecoin pour avoir plus de token.
"""

if 'cg' not in st.session_state:
    st.session_state.cg = CoinGeckoAPI()

def get_coin_price(TypeCoin):
    price = st.session_state.cg.get_price(ids=TypeCoin, vs_currencies='usd')
    return price[TypeCoin]['usd']

listeStableCoin = ['usd-coin', 'tether', 'dai', 'uxd-stablecoin']

ChoisirCoinActuel= st.selectbox(" ", listeStableCoin)

st.write(ChoisirCoinActuel + " : " + str(get_coin_price(ChoisirCoinActuel))  + "$ ")

QTCoin = st.number_input("QT de  Coin", 0.0, step=10.0)

valeur = float(QTCoin) * float(get_coin_price(ChoisirCoinActuel))
st.write("La valeur de tes coins : " + str(valeur) + "$")
st.write(" ")
st.write("  ")

listeStableCoinRestant = listeStableCoin
if ChoisirCoinActuel in listeStableCoin:
    listeStableCoinRestant.remove(ChoisirCoinActuel)

column_names = [listeStableCoinRestant[0] + " vs" + ChoisirCoinActuel, listeStableCoinRestant[1] + " vs" + ChoisirCoinActuel, listeStableCoinRestant[2] + " vs" + ChoisirCoinActuel]

column_names[0], column_names[1], column_names[2] = st.columns([2, 2, 2])



with column_names[0]:
    st.write(listeStableCoinRestant[0] + " : " + str(get_coin_price(listeStableCoinRestant[0])) + "$")
    nbToken1 = float(valeur)/get_coin_price(listeStableCoinRestant[0])
    st.write("Nombre de Token : " + str(nbToken1))
    st.write("Valeur de Token : " + str(float(nbToken1) * float(get_coin_price(listeStableCoinRestant[0]))))
    if nbToken1 > QTCoin:
        st.write("opportunité")

with column_names[1]:
    st.write(listeStableCoinRestant[1] + " : " + str(get_coin_price(listeStableCoinRestant[1])) + "$")
    nbToken2 = float(valeur)/get_coin_price(listeStableCoinRestant[1])
    st.write("Nombre de Token : " + str(nbToken2))
    st.write("Valeur de Token : " + str(float(nbToken2) * float(get_coin_price(listeStableCoinRestant[1]))))
    if nbToken2 > QTCoin:
        st.write("opportunité")

with column_names[2]:
    st.write(listeStableCoinRestant[2] + " : " + str(get_coin_price(listeStableCoinRestant[2])) + "$")
    nbToken3 = float(valeur)/get_coin_price(listeStableCoinRestant[2])
    st.write("Nombre de Token : " + str(nbToken3))
    st.write("Valeur de Token : " + str(float(nbToken3) * float(get_coin_price(listeStableCoinRestant[2]))))
    if nbToken3 > QTCoin:
        st.write("opportunité")

st.button("reset")