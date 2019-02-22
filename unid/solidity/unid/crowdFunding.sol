pragma solidity ^0.4.25;


contract nidcoin {

	// 상태 변수를 선언
    string public name; // 코인 이름 (nidcoin)
    string public symbol; // 코인 단위 (nid)
    uint8 public decimals; // 소수점 이하 자리수 (0)
    int256 public totalSupply; // 전체 발행량 (10000)

	// 계정별 잔액
    // balanceOf[eth.accounts[0]] = 1000; // 첫번째 계정에 1000nid를 할당
    // balance = balanceOf[eth.accounts[0]]; // 첫번째 계정의 잔액을 조회
	mapping (address => int256) public balanceOf;


	// 이벤트 정의
	event EvtTransfer(address indexed from, address indexed to, int256 value);


	// 생성자
	// 일반적으로 생성자에서는 상태변수 초기화를 처리
	constructor (int256 _supply, string _name, string _symbol, uint8 _decimals) public {
		name = _name;
		symbol = _symbol;
		decimals = _decimals;
		totalSupply = _supply;
		// balanceOf[msg.sender] => 생성자를 호출한 사용자의 잔액
		// 생성자를 호출한 사용자에게 전체 코인을 할당
		balanceOf[msg.sender] = _supply;
	}


	// 송금
	// 함수를 호출한 계정에서 _to 계정으로 _value 만큼의 nid를 전송
	function transfer1(address _from, address _to, int256 _value) public {
		// 검증을 통한 부정 방지
		if (_value < 0) revert("마이너스는 송금할 수 없습니다.");
		if (balanceOf[_from] < _value) revert("잔액 보다 많은 금액은 송금할 수 없습니다.");
		balanceOf[_from] -= _value;
		balanceOf[_to] += _value;
		emit EvtTransfer(_from, _to, _value);
    }

    function getBalance (address account) public returns (int256) {
        return balanceOf[account];
    }



}
contract CrowdFunding {
    struct Investor {
        address addr;
        uint amount;
    }
    address public owner;
    uint public numInvestors;
    uint public deadline;
    string public status;
    bool public ended;
    uint public goalAmount;
    uint public totalAmount;
    constructor (address fundCreater, uint deadline1, int256 goalAmount1) public {
        owner = fundCreater;
        deadline = deadline1;
        goalAmount = goalAmount1;
    }
    mapping (uint => Investor) public investors;

    modifier onlyOwner () {
        require(msg.sender == owner);
        _;
    }
    function getOwner() public view returns (address) {
        return owner;
    }

    function getDeadline() public view returns (uint) {
        return deadline;
    }
    function getNumInvestors() public view returns (uint) {
        return numInvestors;
    }
    function getEnded() public view returns (bool) {
        return ended;
    }
    function getGoalAmount() public view returns (uint) {
        return goalAmount;
    }
    function getTotalAmount() public view returns (uint) {
        return totalAmount;
    }

    function fund(uint fundAmount) public {
        require(!ended);


        Investor inv = investors[numInvestors++];
        inv.addr = funder;
        inv.amount = fundAmount;
        totalAmount = totalAmount + inv.amount;

        nidcoin nd = nidcoin(0x956199801a6c15687641ba8b357c91ee8dea3f68);
        nd.transfer(inv.addr, this, inv.amount);

    }

    function checkGoalReached () public onlyOwner {
        require(!ended);
        require(now >= deadline);

        if(totalAmount >= goalAmount) {
            status = "Campaign Succeeded";
            ended = true;
            nidcoin nd = nidcoin(0x956199801a6c15687641ba8b357c91ee8dea3f68);
            nd.transfer(this, owner, totalAmount);
        } else {
            uint i = 0;
            status = "Campaign Failed";
            ended = true;
            while(i <= numInvestors) {
                nd.transfer(this, investors[i].addr, totalAmount);
                i++;
            }
        }
    }
    function kill() public onlyOwner {
        selfdestruct(owner);
    }
}

contract CrowdFundMaster {
    mapping (address => CrowdFunding) public crowdfunding;
    address[] private addressList;

    event EventCreatFunding(address owner);

    function creatFunding(address fundCreater, uint deadline1, int256 goalAmount1) public {
        CrowdFunding c = new CrowdFunding(fundCreater, deadline1, goalAmount1);
        addressList.push(address(c));
        crowdfunding[address(c)] = c;

        emit EventCreatFunding(address(c));
    }

    function getContentsAddressList() public view returns (address[]
    contentsAddressList) {
        contentsAddressList = addressList;
    }
}
