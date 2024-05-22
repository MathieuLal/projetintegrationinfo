from flask import Flask, request
from solana.rpc.api import Client
from solana.rpc.types import MemcmpOpts
from solders.pubkey import Pubkey
from typing import List, Union

class Transaction:
    def __init__(self, ticker, prix, temps, action):
        self.ticker = ticker
        self.prix = prix
        self.temps = temps
        self.action = action

app = Flask(__name__)

BTC_address = "3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh"
USDC_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

user_wallet = "Mettre votre wallet"
rpc = "Mettre votre RPC"
token_program = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"


memcmp_opts = MemcmpOpts(offset=32, bytes=user_wallet)
pubkey = Pubkey.from_string(token_program)
filters: List[Union[int, MemcmpOpts]] = [165, memcmp_opts]
solana_client = Client(rpc)

enTrade = False

private_key = Keypair.from_bytes(base58.b58decode("Mettre la private key de votre wallet"))
async_client = AsyncClient(rpc)
jupiter = Jupiter(async_client, private_key)


async def faireSwap(input, output, Qt): # Fait un swap entre 2 tokens  
    transaction_data = await jupiter.swap(
        input_mint=input,
        output_mint=output,
        amount= Qt,
        slippage_bps=2000,
    )
    raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(transaction_data))
    signature = private_key.sign_message(message.to_bytes_versioned(raw_transaction.message))
    signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
    opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
    result = await async_client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

async def JupValeurBTC(input_mint, output_mint, amount, slippage_bps, divide): # Retour le prix d'un token voulu selon jupiter  
    quote_data = await jupiter.quote(
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount,
        slippage_bps=slippage_bps,
    )

    return (float(quote_data["outAmount"]) / divide)
        
def verifWallet(address): # regarde si le trade a été effectué, si oui retour la quantité de token reçu par ce trade

    for x in solana_client.get_program_accounts_json_parsed(pubkey, filters=filters).value:
        if (x.account.data.parsed["info"]["mint"] == address):
            QtToken = x.account.data.parsed["info"]["tokenAmount"]["uiAmountString"]

            if QtToken > 0:
                return True, QtToken
            break;
    return False, 0


def actionLorsAchat(prixBTCTradingView):

    enPossessionUSDC, QtToken = verifWallet(USDC_address) # regarde s'il y a de l'USDC dans le wallet
    if  enPossessionUSDC:
        prixJupiterBTC = JupValeurBTC(BTC_address, USDC_address, 100_000, 2000, 1000) # récupère le prix de BTC sur Jupiter

        valeurDeDivergence = (prixBTCTradingView-prixJupiterBTC)/prixJupiterBTC # regarde  la différence de prix du BTC entre Jupiter et TradingView

        if abs(valeurDeDivergence) < 5:    
            enPossessionBTC, QtToken = verifWallet(BTC_address)
            QT_BTC = QtToken * 100000000
            while(not enPossessionBTC):

                faireSwap(USDC_address, BTC_address, QT_BTC)
                enPossessionBTC, QtToken = verifWallet(BTC_address)

def actionLorsVente():

    enPossessionBTC, QtToken = verifWallet(BTC_address)

    if enPossessionBTC:
        QT_USDC = QtToken * 1000000
        while(not enPossessionUSDC):
            faireSwap(BTC_address, USDC_address, QT_USDC)
            enPossessionUSDC, QtToken = verifWallet(USDC_address)

# Lorsque le Webook reçoit un message ce fait des actiions par rapport 
@app.route("/tradingview-to-webhook", methods=['POST'])
def tradingview_webhook():
    global enTrade

    json_data = request.get_json()
    position_actuel_instance = Transaction(**json_data) # messege du tradiingview

    if position_actuel_instance.action == "buy":
        actionLorsAchat(position_actuel_instance.prix)
        enTrade = True

    if position_actuel_instance.action == "sell" and enTrade == True:
        actionLorsVente()
        enTrade = False

    return "AAAAAA"
