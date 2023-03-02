import sqlite3

# Connection to database
connection = sqlite3.connect('transaction.db')
cursor = connection.cursor()

# Create table, if not exists
sql_anweisung = """
CREATE TABLE IF NOT EXISTS xrptransaction (
id INTEGER PRIMARY KEY AUTOINCREMENT,
sender text,
receiver text
);"""

cursor.execute(sql_anweisung)

# Define the network client
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html
from xrpl.wallet import generate_faucet_wallet
test_wallet = generate_faucet_wallet(client, debug=True)
print(test_wallet)

# Prepare payment
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
my_tx_payment = Payment(
    account=test_wallet.classic_address,
    amount=xrp_to_drops(10),
    destination="rKhHrN57pVs41rk96ZpVojy2QapQE7R8uU",
)

# Sign the transaction
from xrpl.transaction import safe_sign_and_autofill_transaction
my_tx_payment_signed = safe_sign_and_autofill_transaction(my_tx_payment, test_wallet, client)

# Submit and send the transaction
from xrpl.transaction import send_reliable_submission
tx_response = send_reliable_submission(my_tx_payment_signed, client)
print(tx_response)

# Insert in db
cursor.execute("INSERT INTO xrptransaction (id, sender, receiver) VALUES (?, ?, ?)",
    (id, test_wallet ,'rKhHrN57pVs41rk96ZpVojy2QapQE7R8uU'))

connection.commit()

# Close connection
connection.close()
