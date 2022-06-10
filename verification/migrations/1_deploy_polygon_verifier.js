const VerifierNFT = artifacts.require("VerifierNFT");

module.exports = function (deployer) {
  deployer.deploy(VerifierNFT);
};
