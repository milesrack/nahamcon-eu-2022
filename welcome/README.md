# Welcome

## Description
Author: Ferran Celades (HALBORN)

This challenge is provided by HALBORN. Check the Info page for more tips on how you might solve this task! Note, as this challenge is developed and provided by an external sponsor, there will be limited support for this challenge.

Send me some funds!

Press the Start button on the top-right to begin this challenge.

## Solve
This challenge was new to me because I had never done web3. First I had to install [Brownie](https://eth-brownie.readthedocs.io), a python library to interact with ethereum smart contracts.
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
npm install ganache --globa
```
Starting the challenge gives us these deployment details:
```
Deploy Details:

{
  "Welcome": [
    "0x0cB8C2Fe5f94B3b9a569Df43a9155AC008c9884b"
  ]
}

Private RPC URL:

https://ctf.nahamcon.com/challenge/39/f997a07c-75b6-42c1-88b3-f5972901b6dc

Mnemonic:

test test test test test test test test test test test junk
```
If we read `scripts/challenge.py` we will see the program is checking if it has a balance greater than 0. So we need to figure out how to transfer some coins to the `0x0cB8C2Fe5f94B3b9a569Df43a9155AC008c9884b` address.

Since this is running on a private RPC URL I had to add it into brownie first.
```
user@arch:~/cyber/ctf/nahamcon-2022/welcome$ brownie networks add Ethereum nahamcon host=https://ctf.nahamcon.com/challenge/39/f997a07c-75b6-42c1-88b3-f5972901b6dc chainid=1
Brownie v1.19.2 - Python development framework for Ethereum

SUCCESS: A new network 'nahamcon' has been added
  └─nahamcon
    ├─id: nahamcon
    ├─chainid: 1
    └─host: https://ctf.nahamcon.com/challenge/39/f997a07c-75b6-42c1-88b3-f5972901b6dc

```

Then I started the `brownie` console with the custome network set.
```
user@arch:~/cyber/ctf/nahamcon-2022/welcome$ brownie console --network nahamcon
Brownie v1.19.2 - Python development framework for Ethereum

EthWelcomeProject is the active project.
Brownie environment is ready.
>>> accounts
[<Account '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'>, <Account '0x70997970C51812dc3A010C7d01b50e0d17dc79C8'>, <Account '0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC'>, <Account '0x90F79bf6EB2c4f870365E785982E1f101E93b906'>, <Account '0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65'>, <Account '0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc'>, <Account '0x976EA74026E726554dB657fA54763abd0C3a0aa9'>, <Account '0x14dC79964da2C08b23698B3D3cc7Ca32193d9955'>, <Account '0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f'>, <Account '0xa0Ee7A142d267C1f36714E4a8F75612F20a79720'>]
>>> accounts[0]
<Account '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'>
>>> accounts[0].balance()
10000000000000000000000
>>> accounts[0].transfer(to='0x0cB8C2Fe5f94B3b9a569Df43a9155AC008c9884b', amount=1)
Transaction sent: 0xead297f17bd20de0e5d9efd49e75d24ba3d64b72b4c4a4a4d31d4d52c13019de
  Gas price: 1.0 gwei   Gas limit: 24546   Nonce: 0
  Transaction confirmed   Block: 2   Gas used: 21033 (85.69%)

<Transaction '0xead297f17bd20de0e5d9efd49e75d24ba3d64b72b4c4a4a4d31d4d52c13019de'>
```
After doing this I checked solution and the account had recieved the funds!