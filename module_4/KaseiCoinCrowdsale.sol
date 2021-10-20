pragma solidity ^0.5.5;

import "./KaseiCoin.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

contract KaseiCoinCrowdsale is Crowdsale, MintedCrowdsale{
    constructor(
        uint256 rate, // rate in TKNbits
        address payable wallet, // sale beneficiary
        KaseiCoin token // the deployed token contract 
    ) Crowdsale(rate, wallet, token) public {// invoke parent constructor
        
        
    }
}

contract KaseiCoinDeployer{
    address public kaseiCoin_address;
    address public kaseiCoinCrowdsale_address;
    
    constructor(
        string memory name, 
        string memory symbol, 
        address payable wallet) 
    public
    {
        /* Instanciate the token and save its address*/
        KaseiCoin kaseiCoin_deployed = new KaseiCoin(name, symbol, 100000);
        kaseiCoin_address = address(kaseiCoin_deployed);
        
        
        /* Instanciate the token crowdsale contract*/
        KaseiCoinCrowdsale kaseiCoinCrowdsale_deployed = new KaseiCoinCrowdsale(1, wallet, kaseiCoin_deployed);
        kaseiCoinCrowdsale_address = address(kaseiCoinCrowdsale_deployed);
        
        
        /* Set the crowdsale contract as the minter */
        kaseiCoin_deployed.addMinter(kaseiCoinCrowdsale_address);
        
        /* Have this deployer contract renounce its mint  */
        kaseiCoin_deployed.renounceMinter();
    }
}