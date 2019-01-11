
    jQuery(document).ready(function($){
        //open popup
        $('.cd-popup-trigger').on('click', function(event){
            event.preventDefault();
            $('.cd-popup').addClass('is-visible');

        });

        //close popup
        $('.cd-popup').on('click', function(event){
            if( $(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup') || $(event.target).is('.cd-popup-no')) {
                event.preventDefault();
                $(this).removeClass('is-visible');
            }
        });
        //close popup when clicking the esc keyboard button
        $(document).keyup(function(event){
            if(event.which=='27'){
                $('.cd-popup').removeClass('is-visible');
            }

        });
        $('#inputreply').on('click', function() {
            var reply = $('#inputreplytext').val();
            var post_id = {{ replys.posts_id }};
            $.ajax({
                type: 'POST',
                url: '../../mainreply/',
                data: {
                    id: posts_id,
                    reply: reply,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                    },
                success : function(res) {
                    alert(res.Ans);
                    location="{% url 'main_detail' posts.posts_id %}"
                }
            });
        });

    });

    var WEB3 = require('web3');
    var web3 = new WEB3();
    web3.setProvider(new web3.providers.HttpProvider("http://localhost:8545"));

    var contentsmasterContract = web3.eth.contract([{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"contents","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"price","type":"uint32"}],"name":"addContents","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"name","type":"string"}],"name":"EventAddContents","type":"event"}]);


    let cc = contentsmasterContract.at( "0xbf5f1204ba8ee3bc0096459e9b80099d4fee2a7a" );

    var contentsContract = web3.eth.contract([{"constant":false,"inputs":[],"name":"countUp","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getDownloadCount","outputs":[{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getContentsPrice","outputs":[{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getContentsName","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"name","type":"string"},{"name":"price","type":"uint32"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"count","type":"uint32"}],"name":"EventCountUp","type":"event"}]);

    $(function() {
        $('#enrollyes').click(function() {
            let contentsprice = $('#inputprice').val();
            let contentsname = $('#user_files').val();
            cc.addContents (
                contentsname,
                contentsprice,
                { from: web3.eth.coinbase, gas: 1000000 },
                function(err, res) {
                    if (!err) {
                        console.log(res);
                    } else {
                        console.error(err);
                    }
                }
            );
        });
    });
