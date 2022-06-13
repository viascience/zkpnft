Zero Knowledge Proofs, ZKPs, is a method that allows a prover to proof a statement to a verifier without having to reveal it.


The following repository defines a:

Visual ZKP proof generator 

 + Main script (Python):  main.py
 
 + Sequence verification generator (Python): verification_hash.py
 
 + A Polygon smart contract (https://polygon.technology/) with the NFT verification logic /verification
 

# main.py

ZKP visual proof generator given two sequences of uint[5] created by two different users.
The outputs of the script are:

* A 5 by 5 image with pixels correspond to sha256(sequence) mod 255.

* Noise is added to each user's sequence before the hash creation.

The script can be triggered by runnning: 

`docker build . -t zkp`

`docker run -v $(pwd)/image:/hash_mechanism/image -it zkp bash`  

The previous command will exec you into the created Docker container.

`python main.py '{"user1": [6, 7, 9, 10, 12], "user2": [1, 2, 3, 8, 7]}'`

{}: Dictionary of users' sequences

It will save the proof.png at current_directory/image in the host computer.

# verification_hash.py

Cryptographic verification sequence generator given the original image and the noise used by main.py (central oracle able to generate the global proof).


The script can be triggered by runnning: 

`docker build . -t zkp`

`docker run -v $(pwd)/image:/hash_mechanism/image -it zkp bash`

The previous command will exec you into the created Docker container.

`python verification_hash.py '[6, 7, 9, 10, 12]' 1`

[]: Sequence

Int: Noise of the user

It will save the proof.png at current_directory/image in the host computer.

# /verification 


NFT ERC721 verification smart contract on Polygon.

Main two functionalities of the smart contract are:

* creation and minting of an NFT with its corresponding uint[5][5] values per pixel.
* verification of a given sequence over a token.
 
 Smart contract support libraries:
 
 + `npm install -g truffle`
 
 + `npm install @openzeppelin/contracts`
 
 
 For local development mnemonic seed phrase: .env 
 
 
 ## LOCAL DEVELOPMENT WITH GANACHE
 
  + Install Ganache for local development: `npm install -g ganache-cli`
  
  `ganache-cli`
  
  + Truffle migrate (Deploys smart contract on local test network)
  
  `truffle migrate --config=truffle-config.polygon.js --network=development`


  + Truffle local console 
  
  `truffle console --config=truffle-config.polygon.js --network=development`
  
  + Steps in console for test:
  
  `let instance = await VerifierNFT.at("YOUR_CONTRACT_ADDRESS_HERE")`
  
  Mint NFT:
  
  `await instance.mint("YOUR_WALLET_ADDRESS", "YOUR_METADATA_URI", uint[5][5] sequences)`
  
  Verify sequence on a given NFT id:
  
  `await instance.verify(sequenceToVerify, tokenID)`
  
  TokenID points to the NFT with the global proof.
    
  Reference tutorial to deploy on testnet instead of local net: 
  `https://blog.paulmcaviney.ca/how-to-mint-an-nft-on-polygon`
  
 ## MUMBAI POLYGON TESTNET DEVELOPMENT 
 
  + Define .secret with wallet secret key to create the contract and do NOT commit the information online, as the key could be stolen.
  
  + Define Polygon scan token under truffle-config.json
  
  + To obtain tokens for deployment on the Mumbai Polygon testnet please go to: 
    
      https://faucet.polygon.technology/
 
  + `truffle compile`
  
  + Deployment on the Mumbai testnet: `truffle migrate --network polygon`
  
  + Console to mint and verify over deployed contract on Mumbai testnet: `truffle console --network polygon`
  
  Steps to test: 
  
  `let instance = await VerifierNFT.at("YOUR_CONTRACT_ADDRESS_HERE")`
  
  Mint NFT:
  
  `await instance.mint("YOUR_WALLET_ADDRESS", "YOUR_METADATA_URI", uint[5][5] sequences)`
  
  Verify sequence on a given NFT id:
  
  `await instance.verify(sequenceToVerify, tokenID)`
  
  
 ## For development, steps to execute Python unittest tests:
 
  `poetry shell`
  
  `pytest -vs`
  




