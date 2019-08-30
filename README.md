# Giano - DLTs based utility for security and data integrity
Giano allows to effortlessly exploit the potentialities of decentralized ledgers to improve
the overall level of security of IT infrastructures.
## Abstract
Giano is an open-source utility that permits to effortlessly exploit the potentialities of
DLTs to improve the overall level of security of IT infrastructures. It was designed to
detect in real-time security breach attempts, offering an unprecedented degree of
reliability. Today, in most cases, the victims of cyber-attacks do not know that they have
been affected. When an attacker succeeds in violating a device, his first action is to
manipulate the system registers to hide his traces. This action exposes the data of
millions of people to significant risks. To solve this massive problem, Giano takes
advantage of the immutability of the information registered on DLTs, leaving a
permanent footprint of any suspected attempt of a data breach. Designed to be agnostic
about a specific blockchain, Giano represents an incredible novelty, sufficiently
customizable, and scalable to be used by any company in the world. Indeed, being able to use all the DLTs, Giano can work on blockchains that do not require to pay network
commissions to execute transactions, allowing small organizations to adopt such a
powerful solution for free.
## How it works

To understand how Giano exploits the potentialities of DLTs, one needs to have a clear
vision of the general principles of its functioning. Giano acts as a simple routine that
checks at a configured interval of time a list of files. These files are usually called logs
and are registers where it is reported what happened on the device. They are
automatically created by the operating system or other security softwares. In the
situation of an attack, hackers try immediately to delete or manipulate logs to hide their
tracks. Also, in most cases, they can do it. The result is that companies do not realize in
time that they have been the victim of a security breach. If there were a way to be sure
of the integrity of the logs, this scenario would be impractical, and any attack could be
quickly identified. Giano leverages DLTs to obtain this, today. If the proof of the
existence of logs is stored on an immutable ledger, the fact itself that the files in
question are not found or have been altered constitutes enough evidence of
unauthorized access. On a practical level, at a programmable time interval, Giano
obtains a unique deterministically calculated identifier for each log under surveillance.
The identifiers and other information, as the logs&#39; size, are reported in a data structure
similar to a Merkle Tree. Then they are stored in a file.

![](https://i.imgur.com/e7kBo84.png)

After, Giano calculates the identifier of the file itself, and stores this information in a
transaction on the blockchain. After the first transaction, the information will be
composed, in addition to the file identifier, also by the last three characters of the
previous transaction identifier.

![](https://i.imgur.com/GCJbetj.png)

Once the chain of transactions is created, it becomes sufficient to check if the
transaction reported in each generated file exists and has in it the identifier specified in
the field previousLogTx, to be sure that no log has been altered. Controlling the size of
the files is another relevant passage: the size of a log file should never decrease unless
someone has manipulated it. This control can take place automatically, and the system
sends an alert in case of anomalies. While this is a check that can only be done by the
administrators of the system on which Giano is installed, it is, however, possible to
monitor third-party devices to which you do not have access if you are aware of the
public address set in the configuration file. An anomaly or a security breach can be
identified if the timing of the transmission of the transactions performed by the specific
address is not respected or the sequence is interrupted. An example of routines that
perform these audits is available in this repository.

![](https://i.imgur.com/SpZlxHa.png)


It should now be clear why Giano needs DLTs to work correctly. It is an innovation that
would have been not possible to achieve otherwise. For the first time in the history of
cybersecurity, it is possible to be sure that a security breach can never happen without
anyone noticing it.
## About this version
Giano can be rewritten in whatever programming language and use every kind of
decentralized ledgers. In this version, however, I decided to use Python and leverage
the blockchain of Ethereum to reach the highest number of persons possible. In the
standard configuration, you will find set the Ropsten testnet; this choice implies that, by
using a faucet, you can freely charge your account balance and use Giano for free in
your project.
A possible attack on the testnet would indeed be more likely, but it is equally valid that it
would be noticed immediately. If so, restarting Giano on a different testnet, or on the
official mainnet, is sufficient to continue being protected. It is essential to consider that
the cost of an attack on the testnet would still require a very considerable expense,
especially if Giano had been running long enough and therefore had created a very long
hash sequence that extends over several blocks. Even if the attack succeeded, Giano
would immediately report the anomaly and the possibility of having been the victim of an
attack.

## Installation

To use Giano you will need to install Web3.Py

Web3.py can be installed (preferably in a virtualenv) using pip as follows

```bash
pip install web3
```

After the installation is complete, you can move the files of this repository on your
server.

## Usage

Before launching Giano, you will need to configure it. You can find an example of configuration already prepared in the file *gianoConfiguration*.

```
{
  "address": "YOUR_ETHEREUM_ADDRESS",
  "privateKey": "YOUR_PRIVATE_KEY",
  "delay": 120,
  "logsPath": "logs",
  "paths": [
    "giano.py",
    "gianoConfiguration.json",
    "example.txt"
  ]
}


```

```
{
    "datetime": "2019-08-21 16:13:45.581824",
    "pid": 13037,
    "files": [
        {
            "path": "giano.py",
            "dimension": 3386,
            "hash": "79502d1ac6eb91065181779fb9f47ba6b0f585b0dda3e638cda195cc4cd99f0a"
        },
        {
            "path": "gianoConfiguration.json",
            "dimension": 266,
            "hash": "b99b52fe160215580805246618a5225967b74b85567f2d5ec4d99110095892ce"
        },
        {
            "path": "auth.logs",
            "dimension": 2343,
            "hash": "a2c2339691fc48fbd14fb307292dff3e21222712d9240810742d7df0c6d74dfb"
        }
    ],
    "previousLogHash": "4d1b6c8b39d8f20cf50edaa1ebc30649d22135d02925b43658dbbab417521bc8",
    "previousLogTx": "0xe272ff92e3858a3534f3971a517f0645868add1f7259a6f4e9b49900d8270ef8"
}

```

*address* - Your ethereum ropsten account address

*privateKey* - The private key of your address

*delay* - Seconds of delay between the storage on the chain

*logsPath* - Name of the folders that will contain the logs file

*paths* - The paths of each files that you want to protect

## How to create an account on Ropsten
You can easily create an account on the Ethereum Ropsten Testnet using Metamask, a popular Google Chrome extension.
To obtain the private key of your account, you will need to open the *Account Details* section as shown in the screenshots below.

![](https://i.imgur.com/grmeuBp.png)
![](https://i.imgur.com/L4mwhcj.png)

To charge your account freely, you can use one of the faucets available online at
https://faucet.metamask.io.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT License

Copyright (c) [2019] [Dario Moceri]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*
