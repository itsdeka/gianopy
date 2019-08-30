import requests
# CONFIGURATION
address = '0x26dc5859c654Ca9C177beB0759d5D79f8c5662A2'

import datetime
import operator

class Transaction():
    def __init__(self, nonce, txHash, txInput, timeStamp):
        self.nonce = nonce
        self.txHash = txHash
        self.txInput = txInput
        self.timeStamp = timeStamp


transactions = []

txs = requests.get('https://blockscout.com/eth/ropsten/api?module=account&action=txlist&address=%s' % (address)).json()

for tx in txs['result']:
    if tx['from'] == address.lower():
        transactions.append(Transaction(
            nonce=tx['nonce'],
            txHash=tx['hash'],
            txInput=tx['input'],
            timeStamp=tx['timeStamp']
        ))

latestTxHash = None
latestTxInput = None
counter = 1
flag = False
transactions = sorted(transactions, key=operator.attrgetter('timeStamp'))
for transaction in reversed(transactions):
    txHash = transaction.txHash
    txInput = transaction.txInput
    print('Checking transaction %s (%s/%s)' % (txHash, counter, len(transactions)))
    counter += 1
    if latestTxHash and latestTxInput:
        if latestTxInput[-3:] != txHash[-3:] and latestTxInput[-3:] != '000':
            unix = (transaction.timeStamp)
            date = datetime.datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')
            print('This system is safe since %s' % (date))
            print('Starting from this transaction: %s' % (txHash))
            flag = True
            break

    latestTxHash = txHash
    latestTxInput = txInput

if flag == False:
    print('This system is safe since its first transaction')

firstTxUnix = transactions[-1].timeStamp
date = datetime.datetime.utcfromtimestamp(int(firstTxUnix)).strftime('%Y-%m-%d %H:%M:%S')
print('The last transaction was executed on %s' % (date))