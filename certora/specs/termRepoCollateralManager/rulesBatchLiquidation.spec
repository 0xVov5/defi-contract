import "../methods/erc20Methods.spec";
import "../methods/emitMethods.spec";
import "./liquidations.spec";
import "../common/isTermContractPaired.spec";
import "../complexity.spec";
import "./accessRoles.spec";
import "./auction.spec";
import "./externalLocking.spec";
import "./stateVariables.spec";

ghost mapping(address => mapping(uint256 => uint256)) tokenPricesPerAmount;

ghost mapping(address => uint256) tokenPrices;

function usdValueCVL(address token, uint256 amount) returns ExponentialNoError.Exp {
    ExponentialNoError.Exp result;
    require result.mantissa == tokenPricesPerAmount[token][amount];
    return result;
}

methods {
    // TermAuctionBidLocker
    function _.termAuctionId() external => DISPATCHER(true);
    function _.termRepoServicer() external => DISPATCHER(true);
    function _.dayCountFractionMantissa() external => DISPATCHER(true);
    function _.lockRolloverBid(uint256) external => DISPATCHER(true);
    function _.auctionEndTime() external => DISPATCHER(true);
    function _.purchaseToken() external => DISPATCHER(true);
    function _.collateralTokens(address) external => DISPATCHER(true);
    function _.termAuction() external => DISPATCHER(true);
    function _.termRepoId() external => DISPATCHER(true);

    // TermController
    function _.isTermDeployed(address) external => PER_CALLEE_CONSTANT;
    function _.getProtocolReserveAddress() external => CONSTANT;

    // TermPriceOracle
    function _.usdValueOfTokens(address token, uint256 amount) external => usdValueCVL(token, amount) expect (ExponentialNoError.Exp);
}

// use rule TEMPbatchLiquidationSuccessfullyLiquidatesTEMP;
use rule batchLiquidationSuccessfullyLiquidates;
use rule batchLiquidationRevertsIfInvalid;
use rule batchLiquidationDoesNotAffectThirdParty;
