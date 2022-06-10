// URI will be overwritten by an array of arrays and instead of 
// minting, it will search for a sequence

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

// Import the OpenZeppelin contracts
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";


// Declare our contract and inherit from the OpenZeppelin ERC721 and Ownable contracts 
contract VerifierNFT is ERC721, Ownable {

    // Helpers for counting safely and converting data to strings
    using Counters for Counters.Counter;
    using Strings for uint256;

    // State variable for storing the current token Id
    Counters.Counter private _tokenIds;
    
    // Map token Ids to token URI
    mapping (uint256 => string) private _tokenURIs;    
    
    // Image sequence assignation
    mapping (uint256 => mapping(string => uint)) private _tokenSequences;
    
    // Input image sequence    
    mapping (uint => string) private mapSequences;
    
    // ERC721 requires a name for the NFT collection and a symbol
    constructor() ERC721("VerifierNFT", "ZKP NFTs") {}

    // Set the URI (metadata) for tokenId
    function _setTokenSequence(uint256 tokenId, mapping(uint => string) storage _tokenSequence)
        internal
        virtual
    {
       uint rowsInImage = 5;
       for(uint256 i; i < rowsInImage; i++) {
          uint key = i + 1;
          string memory sequence = _tokenSequence[i];
          _tokenSequences[tokenId][sequence] = key;
        }
    }

    // Verify sequence against proof
    function _verifySequence(uint256 tokenId, string memory sequence)
        internal
        returns (bool)
    {
        require(_exists(tokenId), "Token does not exist");
        uint value = _tokenSequences[tokenId][sequence];
        
        if(value > 0) return true;
        
        return false;

    }
    
    // Set the URI (metadata) for tokenId
    function _setTokenURI(uint256 tokenId, string memory _tokenURI)
        internal
        virtual
    {
        _tokenURIs[tokenId] = _tokenURI;
    }

    // Return the Token URI - Required for viewing properly on OpenSea
    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(_exists(tokenId), "Token does not exist");
        string memory _tokenURI = _tokenURIs[tokenId];

        return _tokenURI;
    }

    // Mint the NFT to the provided address, using the provided metadata URI and 
    // set the information as a map to allow for easy verification
    // Only the wallet address that deployed this contract can call this function
    function mint(address recipient, string memory URI, uint8[5][5] memory sequences )
        public
        onlyOwner
        returns (uint256)
    {


        for(uint j; j <5; j++){
          string memory stringSequence = "";

          for(uint i; i <5; i++){
          
            uint valueUint = sequences[j][i];
            string memory valueString = Strings.toString(valueUint);
            stringSequence =string(abi.encodePacked(stringSequence,"", valueString)); 
          
          }
          
          mapSequences[j] = stringSequence;

        }
        
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();

        _mint(recipient, newItemId);
        // Set proof with sequences as map
        _setTokenSequence(newItemId, mapSequences);
        // Set URI for proof NFT
        _setTokenURI(newItemId, URI);

        return newItemId;
    }

    function verify(uint[5] memory sequence, uint256 tokenId)
        public
        returns (bool)
    {
        // Convert sequence to string
        string memory sequenceString2Verify = '';
        
        for(uint i; i < 5; i++){
        
            uint valueUint = sequence[i];
            string memory valueString = Strings.toString(valueUint);
            sequenceString2Verify = string(abi.encodePacked(sequenceString2Verify,"", valueString));  
                  
        }
    
        // Return proof map
        bool result = _verifySequence(tokenId, sequenceString2Verify);
    
        // Search for sequence in map from Image
        return result;
    
    }
    
}
