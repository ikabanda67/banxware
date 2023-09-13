from flask import Flask, jsonify, request
import requests
from datetime import datetime,date

def past_transactions(fromdate,todate,sort=True):
    '''
    return a sorted list of transactions fromdate to todate with default sorting set to descending order.
    '''
    # adjust the date format
    # day = datetime.strptime(fromdate,'%Y-%m-%d')
    # fromdate = day.strftime('%d/%m/%Y')
    # day = datetime.strptime(todate,'%Y-%m-%d')
    # todate = day.strftime('%d/%m/%Y')
    
    currentBalances = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'
    key = 'b4a4552e-1eac-44ac-8fcc-91acca085b98-f94b74ce-aa17-48f5-83e2-8b8c30509c18'
    headers = {
        'x-api-key' : key
    }
    # Get current balance
    response = requests.get(currentBalances,headers = headers)
    if response.status_code == 200:
        balance = response.json()

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
    today = {'amount': balance['amount'], 'currency': 'EUR','date': '30/06/2022','status': 'PROCESSED'}
    processed.append(today)
    dailyBalances = []
    # reduce the date length
    for data in processed:
        for key,value in data.items():
            if key == 'date':
                data[key] = value[:10]
                # day = datetime.strptime(data[key],'%Y-%m-%d')
                # data[key] = day.strftime('%d/%m/%Y')
        
    # calculate daily balances
    truth = 0
    for u in processed:
        new = {'date': '', 'amount': 0, 'currency': 'EUR'}
        truth = 0
        if  fromdate <= u['date'] <= todate:
            if u['date'] in [k['date'] for k in dailyBalances]:

                # replace its entry in dailybalances dont create a new one use indexing.
                for y in processed:
                    if u != y and u['date'] == y['date']:
                        new['date'] = y['date']
                        new['amount'] = u['amount'] + y['amount'] 
                        truth = 1
            else:
                new['date'] = u['date']
                new['amount'] = u['amount']    
                truth = 1
                        
            if truth:
                dailyBalances.append(new)
    result = sorted(dailyBalances,key=lambda x :x['date'],reverse= sort)
    print(f'final array {result}')
    return result


## creating endpoint.
    
# task 
app = Flask(__name__)

# create and return 
@app.route('/historical-balances', methods = ['GET'])
def get_transactions():
    # user logic
    today = '2022-06-30'
    frm = request.args.get('date')
    to = request.args.get('date')
    sorting = request.args.get('sort')
    if frm is None or to is None:
        return jsonify({'error': 'Invalid format for date frm  or to.'}), 400
    if to < today or frm > to: return jsonify({'error':'Invalid values for frm and to '}), 300
    if sorting is None: sorting = 'dec'
    if sorting == 'asc': sort = True 
    elif sorting == 'desc': sort = False

    return jsonify(past_transactions(frm,to,sort=sort))

if __name__ == 'main':
    app.run(debug=True)
