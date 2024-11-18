from wallet import Wallet

# Buat wallet baru
my_wallet = Wallet()

# Simpan kunci
with open("private_key.pem", "w") as f:
    f.write(my_wallet.private_key)

with open("public_key.pem", "w") as f:
    f.write(my_wallet.public_key)

print("Wallet berhasil dibuat!")
print("Public Key:", my_wallet.public_key)
