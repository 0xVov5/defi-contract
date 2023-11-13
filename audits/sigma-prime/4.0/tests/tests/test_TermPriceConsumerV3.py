import brownie
import pytest

from brownie import (
    # Brownie helpers
    accounts,
    web3,
    reverts,
    Wei,
    chain,
    Contract
)
from helpers import get_encoded_termRepoId, make_term_auth

 ####################################################
 # +  TermPriceConsumerV3 (ITermPriceOracle, ITermPriceOracleErrors, Initializable, UUPSUpgradeable, AccessControlUpgradeable, ExponentialNoError)
 #    ✓ [Ext] initialize #
 #       - modifiers: initializer
 #    ✓ [Ext] addNewTokenPriceFeed #
 #       - modifiers: onlyRole
 #    ✓ [Ext] removeTokenPriceFeed #
 #       - modifiers: onlyRole
 #    ✓ [Ext] reOpenToNewTerm #
 #       - modifiers: onlyRole
 #    ✓ [Ext] reOpenToNewBidLocker #
 #       - modifiers: onlyRole
 #    - [Ext] usdValueOfTokens
 #       - modifiers: onlyRole
 #    ✓ [Int] _getLatestPrice
 #    ✓ [Int] _getDecimals
 #    ✓ [Int] _authorizeUpgrade
 #       - modifiers: onlyRole
 #
 #
 # ($) = payable function
 # # = non-constant function


def test_usdValueOfTokens(setup_protocol, owner):
    oracle = setup_protocol["oracle"]
    termRepoCollateralManager = setup_protocol["termRepoCollateralManager"]
    purchaseToken_usdc = setup_protocol["purchaseToken_usdc"]
    collateralToken_wbtc = setup_protocol["collateralToken_wbtc"]
    collateralToken_weth = setup_protocol["collateralToken_weth"]
    mockPurchaseFeed_usdc = setup_protocol["mockPurchaseFeed_usdc"]
    mockCollateralFeed_wbtc = setup_protocol["mockCollateralFeed_wbtc"]
    mockCollateralFeed_weth = setup_protocol["mockCollateralFeed_weth"]
    expScale = 10**18

    # Same as mainnet feed 0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6 (USDC/USD)
    # 1 USDC = 1 USD
    mockPurchaseFeed_usdc.setAnswer(1 * 10 ** purchaseToken_usdc.decimals())

    # 1 USDC token should equal 1 USD
    priceInUSD = 1
    amountTokens = 1 * 10 ** purchaseToken_usdc.decimals()
    valueInUSDExp = oracle.usdValueOfTokens(purchaseToken_usdc, amountTokens, {"from": termRepoCollateralManager})[0]
    assert valueInUSDExp == priceInUSD * expScale

    # Same as mainnet feed 0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c (BTC/USD)
    # 1 WBTC = 22,104 USD
    mockCollateralFeed_wbtc.setAnswer(22_104 * 10 ** purchaseToken_usdc.decimals())

    # 1 WBTC token should equal 22,104 USD
    priceInUSD = 22_104
    amountTokens = 1 * 10 ** collateralToken_wbtc.decimals()
    valueInUSDExp = oracle.usdValueOfTokens(collateralToken_wbtc, amountTokens, {"from": termRepoCollateralManager})[0]
    assert valueInUSDExp == priceInUSD * expScale

    # Same as mainnet feed 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 (ETH/USD)
    # 1 ETH = 1,548 USD
    mockCollateralFeed_weth.setAnswer(1_548 * 10 ** purchaseToken_usdc.decimals())

    # 1 WETH token should equal 1,548 USD
    priceInUSD = 1_548
    amountTokens = 1 * 10 ** collateralToken_weth.decimals()
    valueInUSDExp = oracle.usdValueOfTokens(collateralToken_weth, amountTokens, {"from": termRepoCollateralManager})[0]
    assert valueInUSDExp == priceInUSD * expScale
