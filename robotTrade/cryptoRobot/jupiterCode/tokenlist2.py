import asyncio

from solana.rpc.api import Client
from solana.rpc.types import MemcmpOpts
from solders.pubkey import Pubkey

from typing import List, Union


BTC_address = "3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh"
USDC_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

user_wallet = "Mettre votre wallet"
rpc = "Mettre votre RPC"
token_program = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"

# Ce code avec l'aide de  l'adresse  d'un token fourni regarde s'il y en a dans ton wallet et si oui, il te retour la quantité que tu as.

memcmp_opts = MemcmpOpts(offset=32, bytes=user_wallet)
pubkey = Pubkey.from_string(token_program)
filters: List[Union[int, MemcmpOpts]] = [165, memcmp_opts]
solana_client = Client(rpc)

async def get_tokens_list(address):
    
    for x in solana_client.get_program_accounts_json_parsed(pubkey, filters=filters).value: # regarde dans ton wallet
        # response payload
        # print(x)
        if (x.account.data.parsed["info"]["mint"] == address):
            print(x.account.data.parsed["info"]["mint"])
            print(x.account.data.parsed["info"]["tokenAmount"]["uiAmountString"])
            break;

if __name__ == "__main__":
    asyncio.run(get_tokens_list(BTC_address))
    asyncio.run(get_tokens_list(USDC_address))
    