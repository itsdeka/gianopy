import time
import datetime
import os
import hashlib
import random
import json
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/8f283916dfab4e8e8fc2adf4c4a94127'))
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

if not os.path.exists('logs'):
    os.makedirs('logs')


class Deamon():
    def __init__(self):
        self.configurationFile = 'gianoConfiguration.json'
        self.pid = os.getpid()
        self.paths = self.readJson()['paths']
        self.logsPath = self.readJson()['logsPath']
        self.address = self.readJson()['address']
        self.privateKey = self.readJson()['privateKey']
        self.latestLogHash = None
        self.latestLogTx = None
        self.nonce = w3.eth.getTransactionCount(self.address)
        self.delay = self.readJson()['delay']
        self.counter = 1

    def readJson(self):
        with open(self.configurationFile) as jsonFile:
            data = json.load(jsonFile)
            return (data)

    def sha256(self, path):
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            file = {}
            file['path'] = path
            file['dimension'] = os.path.getsize(path)
            file['hash'] = sha256_hash.hexdigest()
            return (file)

    def createTx(self, dataHash):
        proceed = False
        while (not proceed):
            try:
                latestLogTxId = '000'
                if self.latestLogTx:
                    latestLogTxId = self.latestLogTx[-3:]

                signed_txn = w3.eth.account.signTransaction(dict(
                    nonce=self.nonce,
                    gasPrice=w3.eth.generateGasPrice(),
                    gas=5514150,
                    to='0x0000000000000000000000000000000000000000',
                    value=w3.toWei(0, 'ether'),
                    data='%s%s' % (dataHash, latestLogTxId)
                ), self.privateKey)

                tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                txId = w3.toHex(tx)
                print(txId)
                self.nonce += 1
                return (txId)
            except Exception as error:
                print (error)
                self.nonce += 1

    def checkIntegrity(self):
        data = {}
        dt = datetime.datetime.now()
        unixDt = str(dt.timestamp()).split('.')[0]
        data['datetime'] = str(dt)
        data['pid'] = self.pid
        data['files'] = []
        data['previousLogHash'] = self.latestLogHash
        data['previousLogTx'] = self.latestLogTx

        for path in self.paths:
            file = self.sha256(path)
            data['files'].append(file)

        with open('logs/%s.json' % (self.counter), 'w') as outfile:
            json.dump(data, outfile, indent=4)

        dataHash = self.sha256('logs/%s.json' % (self.counter))['hash']
        self.latestLogHash = dataHash
        self.counter += 1

        self.latestLogTx = self.createTx(dataHash)

    def run(self):
        while True:
            self.checkIntegrity()
            time.sleep(self.delay)


if __name__ == "__main__":
    deamon = Deamon()
    deamon.run()