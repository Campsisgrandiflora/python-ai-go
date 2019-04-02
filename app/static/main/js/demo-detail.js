
        function good(obj) {
            $(obj).children('span').css({
                color: 'red'
            });
        }
        window.addEventListener('load', function() {
            $('#detail').click(function(event) {
                $(this).addClass('my-active');
                $('#comment').removeClass('my-active');
                $('.info-dd').show();
                $('.comment-dd').hide();
                $('.reply-hoster').hide();

                $('.resolve-detail').show();
            });
            $('#comment').click(function(event) {
                $(this).addClass('my-active');
                $('#detail').removeClass('my-active');
                $('.info-dd').hide();
                $('.comment-dd').show();
                $('.reply-hoster').show();

                $('.resolve-detail').hide();
            });
            $('#score').click(function(event) {
                $('.score-area').toggle();
            });
        });