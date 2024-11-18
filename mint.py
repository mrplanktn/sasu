from blockchain import Blockchain
from wallet import Wallet

# Inisialisasi blockchain
sasu_chain = Blockchain()

# Masukkan public key penerima
recipient_public_key = input("Masukkan public key penerima: ")

# Jumlah token yang ingin dicetak
amount = int(input("Masukkan jumlah token yang ingin dicetak: "))

# Mint token
result = sasu_chain.mint_token(amount, recipient_public_key)
print(result)

# Cek saldo
print("Transaksi Pending:", sasu_chain.pending_transactions)
