pragma solidity ^0.4.25;

contract Contents {
    string contentsWriter;
    string public contentsHashdata;

    constructor (string name, string hash) public {
        contentsWriter = name;
        contentsHashdata = hash;
    }
    
    function getContentsWriter() public view returns (string) {
        return contentsWriter;
    }

    function getcontentsHashdata() public view returns (string) {
        return contentsHashdata;
    }

}

contract ContentsMaster {
    mapping (address => Contents) public contents;
    address[] private addressList;

    event EventAddContents(string name);

    function addContents(string name, string hash) public {
        Contents c = new Contents(name, hash);
        addressList.push(address(c));
        contents[address(c)] = c;

        emit EventAddContents(name);
    }

    function getContentsAddressList() public view returns (address[]
    contentsAddressList) {
        contentsAddressList = addressList;
    }
}
	