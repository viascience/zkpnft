

The following repository defines a:

Visual ZKP proof generator 

 + Main script (Python):  main.py
 
 The pixel colours define the sequences given by the users

 + Environment: environment.yml


Polygon smart contract verification.

Input:
 
 + NFT image
 
 + User given hash sequence

Output:

 + True or False
 
 Installation:
 
 + `npm install -g truffle`
 
 + `npm install @openzeppelin/contracts`
 
 mnemonic seed phrase: .env 
 
 (DO NOT USE EXISTING .env VALUE AS IT IS ONLY AN EXAMPLE)
 
 ## GANACHE LOCAL DEVELOPMENT
 
  + Install Ganache for local development: `npm install -g ganache-cli`
  
  `ganache-cli`
  
  + Truffle migrate
  
  `truffle migrate --config=truffle-config.polygon.js --network=development`


  + Truffle local console 
  
  `truffle console --config=truffle-config.polygon.js --network=development`
  
  + Steps in console for test:
  
  `let instance = await VerifierNFT.at("YOUR_CONTRACT_ADDRESS_HERE")`
  
  `await instance.mint("YOUR_WALLET_ADDRESS", "YOUR_METADATA_URI", uint[5][5] sequences)`
  
  `await instance.verify(sequenceToVerify, tokenID)`
  
  TokenID correspond to the proof.
    
  Reference tutorial to deploy on testnet instead of local net 
  `https://blog.paulmcaviney.ca/how-to-mint-an-nft-on-polygon`
  
 ## POLYGON TEST NET DEVELOPMENT 
  
  + To obtain tokens for deployment on Mumbai Polygon testnet please go to: 
    
      https://faucet.polygon.technology/
 
  + truffle compile
  
  + truffle migrate --network polygon
  

