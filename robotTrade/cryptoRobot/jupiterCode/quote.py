import base58
import base64
import json

from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from jupiter_python_sdk.jupiter import Jupiter
import asyncio

# should probably be in an env file
USDC_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
SOL_address = "So11111111111111111111111111111111111111112"
BTC_address = "3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh"
rpc = "Mettre votre RPC"
wallet_privkey = "Mettre votre clé privé"

# program start here
private_key = Keypair.from_bytes(base58.b58decode(wallet_privkey))
async_client = AsyncClient(rpc)
jupiter = Jupiter(async_client, private_key)

async def quote(input_mint, output_mint, amount, slippage_bps, divide):   
    quote_data = await jupiter.quote(
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount,
        slippage_bps=slippage_bps,
    )
    # response payload
    #print(f"quote_data: {quote_data}")
    
    print(quote_data["outAmount"])
    print(float(quote_data["outAmount"]) / divide)

if __name__ == "__main__":
    asyncio.run(quote(USDC_address, SOL_address, 300_000, 2000, 1000000000))
    asyncio.run(quote(BTC_address, USDC_address, 100_000, 2000, 1000))
    