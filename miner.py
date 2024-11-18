import requests

NODE_URL = "http://localhost:5000/mine"

def start_mining(miner_address):
    while True:
        response = requests.post(NODE_URL, json={"miner": miner_address})
        print(response.json())

if __name__ == '__main__':
    miner_address = input("Enter your miner address: ")
    start_mining(miner_address)
