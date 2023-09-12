from flask import Flask, jsonify
import requests

app = Flask(__name__)

currentBalances = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'
key = 'b4a4552e-1eac-44ac-8fcc-91acca085b98-f94b74ce-aa17-48f5-83e2-8b8c30509c18'
headers = {
    'x-api-key' : key
}
# Get current balance
response = requests.get(currentBalances,headers = headers)
if response.status_code == 200:
    balance = response.json()
    print(balance['amount'])
else: 
    print(f'Error :{response.status_code}')

# Get past transactions
transactions = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/transactions'
response = requests.get(transactions,headers=headers)
if response.status_code == 200:
    transactions = response.json()
else:
    print(f'Error: {response.status_code}')

record = transactions['transactions'] 
processed = [i for i in record if i['status']=='PROCESSED']

def new():
        # task 
    # create and return 
    @app.route('/historical-balances?from=2022-01-03&to=2022-01-05&sort=desc', methods = ['GET'])
    def get_resource():
        # user logic
        resource_data = {"key": "value"}
        return jsonify(resource_data)

    if __name__ == 'main':
        app.run(debug=True)
