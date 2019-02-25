pragma solidity ^0.4.25;


contract nidcoin {

   // 상태 변수를 선언
    string public name; // 코인 이름 (nidcoin)
    string public symbol; // 코인 단위 (nid)
    uint8 public decimals; // 소수점 이하 자리수 (0)
    int256 public totalSupply; // 전체 발행량 (10000)

   // 계정별 잔액
   mapping (address => int256) public balanceOf;

   // 이벤트 정의
   event EvtTransfer(address indexed from, address indexed to, int256 value);


   // 생성자
   constructor (int256 _supply, string _name, string _symbol, uint8 _decimals) public {
      name = _name;
      symbol = _symbol;
      decimals = _decimals;
      totalSupply = _supply;
      balanceOf[msg.sender] = _supply;
   }


   // 송금
   function transfer(address _from, address _to, int256 _value) public {
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
        int256 amount;
    }
    address public owner;
    uint public numInvestors;
    uint public deadline;
    string public status;
    bool public ended;
    int256 public goalAmount;
    int256 public totalAmount;
    
    nidcoin nd = nidcoin(0x956199801a6c15687641ba8b357c91ee8dea3f68); 
    
    constructor (address fundCreater, uint deadline1, int256 goalAmount1) public {
        owner = fundCreater;
        deadline = deadline1;
        goalAmount = goalAmount1;
    }
    mapping (uint => Investor) public investors;

    modifier onlyAdmin () {
        require(msg.sender == 0xab8348cc337c3a807b21f7655cae0769d79c3772);
        _;
    }

    

    function getOwner() public view returns (address) {
        return owner;
    }
    function getNow() public view returns (uint) {
        return now;
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
    function getGoalAmount() public view returns (int256) {
        return goalAmount;
    }
    function getTotalAmount() public view returns (int256) {
        return totalAmount;
    }

    function fund(int256 fundAmount, address funder) public {
        require(!ended);

        Investor inv = investors[numInvestors++];
        inv.addr = funder;
        inv.amount = fundAmount;
        totalAmount = totalAmount + inv.amount;

        nd.transfer(inv.addr, address(this), inv.amount);

    }

    function checkGoalReached () public onlyAdmin {
        require(!ended);
        require(now >= deadline);
        if (totalAmount >= goalAmount) {
            nd.transfer(this, owner, totalAmount);
            status = "Campaign Succeeded";
            ended = true;
            totalAmount = 0;
        } else {
            uint i = 0;
            while(i < numInvestors) {
                nd.transfer(this, investors[i].addr, totalAmount);
                i++;
            }
            status = "Campaign Failed";
            ended = true;
            totalAmount = 0;
        }
    }
    
    function kill() public onlyAdmin {
        selfdestruct(owner);
    }
}

contract CrowdFundMaster {
    mapping (address => CrowdFunding) public crowdfunding;
    address[] private addressList;

    event EventCreatFunding(address CA);

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