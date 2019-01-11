
    jQuery(document).ready(function($){
        $('.votings').on('click', function() {
            var voting = parseInt($('#voting').text());
            var reward = parseFloat($('#reward').text());
            var posts_id = {{ posts.posts_id }}
            console.log(voting)
            console.log(reward)

            voting = voting + parseInt(1);

//            $('#voting').text(voting)

            if (voting % 1 == 0)
			     reward = reward + parseFloat(0.1);
                 reward = reward.toFixed(1);
//			     $("#reward").text(reward);
			     console.log(voting)
			     console.log(reward)

            $.ajax({
                    type: 'POST',
                    url: "../unid/voting/",
                    data :{
                        id: posts_id,
                        voting: voting,
                        reward: reward,
                        csrfmiddlewaretoken: '{{ csrf_token }}'
                        },
                     success : function(res) {
                        alert(res.Ans);

                        }

                    });

            });
        });