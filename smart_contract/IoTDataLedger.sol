// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IoTDataLedger {
    struct Record {
        string dataHash;
        uint256 timestamp;
    }

    Record[] public records;
    address public owner;

    event RecordAdded(string dataHash, uint256 timestamp);

    constructor() {
        owner = msg.sender;
    }

    function storeHash(string memory _dataHash) public {
        Record memory newRecord = Record(_dataHash, block.timestamp);
        records.push(newRecord);
        emit RecordAdded(_dataHash, block.timestamp);
    }

function getRecord(uint256 index) 
    public 
    view 
    returns (string memory dataHash, uint256 timestamp) 
{
    require(index < records.length, "Index out of range");
    Record storage r = records[index];
    return (r.dataHash, r.timestamp);
}


    function totalRecords() public view returns (uint256) {
        return records.length;
    }

    // Allow the contract to safely reject or receive ETH transfers
    receive() external payable {}
    fallback() external payable{}
}