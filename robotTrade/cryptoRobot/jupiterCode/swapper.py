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

private_key = Keypair.from_bytes(base58.b58decode("Mettre votre clé privé"))
async_client = AsyncClient("Mettre votre RPC")
jupiter = Jupiter(async_client, private_key)

async def swap():   
    transaction_data = await jupiter.swap(
        input_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        output_mint="3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh",
        amount=100000,
        slippage_bps=2000,
    )
    # Returns str: serialized transactions to execute the swap.
    raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(transaction_data))
    signature = private_key.sign_message(message.to_bytes_versioned(raw_transaction.message))
    signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
    opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
    result = await async_client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
    print(result.to_json())
    transaction_id = json.loads(result.to_json())['result']
    print(f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")

if __name__ == "__main__":
    asyncio.run(swap())