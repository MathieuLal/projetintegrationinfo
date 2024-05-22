import base58
import base64
import json

from solders import message
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

from solana.rpc.types import TxOpts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed

from jupiter_python_sdk.jupiter import Jupiter

import asyncio

# Ce code retour plein de Token différent listé sur Jupiter Station, leur source, leur adresse,  leur ticker  ...

private_key = Keypair.from_bytes(base58.b58decode("Mettre la private key du wallet"))
async_client = AsyncClient("Mettre votre RPC")
#async_client = AsyncClient("RPC (devnet)")

jupiter = Jupiter(async_client, private_key)

async def get_tokens_list():   
    token_data = await jupiter.get_tokens_list()
    print(f"token_data: {token_data}")

if __name__ == "__main__":
    asyncio.run(get_tokens_list())