import glob, os
import hashlib
import json
from web3 import Web3


class File():
    def __init__(self, path, dimension, hash, datetime):
        self.path = path
        self.dimension = dimension
        self.hash = hash
        self.datetime = datetime


def sha256(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()


def alert():
    print(
        'Anomaly detected! If nothing extraordinary as a blackout happened, the chances that you were hacked are very high.')


print('Attention: someone could be able to change the source code of this tool.')
print(
    'Please, upload a new version of this tool each time you need to check the integrity of your system. Thank you.\n')

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/8f283916dfab4e8e8fc2adf4c4a94127'))  # testnet
configurationFile = 'gianoConfiguration.json'

with open(configurationFile) as jsonFile:
    data = json.load(jsonFile)
files = {}
logs = glob.glob("%s/*.json" % (data['logsPath']))
counter = 1
previousLogHash = None
for number in range(len(logs), 0, -1):
    log = 'logs/%s.json' % (number)
    print("Checking (%s/%s)" % (counter, len(logs)))
    if previousLogHash and previousLogHash != sha256(log):
        alert()
        break
    with open(log) as jsonFile:
        data = json.load(jsonFile)
        previousLogTx = data['previousLogTx']
        if previousLogTx:
            transaction = w3.eth.getTransaction(previousLogTx)
            logHash = transaction['input'][3:]
            logHash = logHash[0:len(logHash) - 3]
            previousLogHash = data['previousLogHash']
            if logHash != previousLogHash:
                alert()
                break

    counter += 1

alert = False
files = {}
print("")
for log in logs:
    with open(log) as jsonFile:
        data = json.load(jsonFile)
        for file in data['files']:

            if file['path'] in files:
                if files[file['path']].dimension > file['dimension']:
                    print('ALERT - File size is decreased (%s) | %s' % (file['path'], data['datetime']))
                    print('Please check %s\n' % (log))
                    alert = True

            files[file['path']] = File(
                path=file['path'],
                datetime=data['datetime'],
                hash=file['hash'],
                dimension=file['dimension']
            )

if counter >= len(logs) and alert == False:
    print('\nYour system is safe.\n')