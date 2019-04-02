'use strict';

	window.addEventListener('load', function () {
		var carousels = document.querySelectorAll('.carousel');

		for (var i = 0; i < carousels.length; i++) {
			carousel(carousels[i]);
		}
	});

	function carousel(root) {
		var figure = root.querySelector('figure'),
			nav = root.querySelector('nav'),
			images = figure.children,
			n = images.length,
			gap = root.dataset.gap || 0,
			bfc = 'bfc' in root.dataset,
			theta = 2 * Math.PI / n,
			currImage = 0;

		setupCarousel(n, parseFloat(getComputedStyle(images[0]).width));
		window.addEventListener('resize', function () {
			setupCarousel(n, parseFloat(getComputedStyle(images[0]).width));
		});
		
		setupNavigation();

		function setupCarousel(n, s) {
			var apothem = s / (2 * Math.tan(Math.PI / n));

			figure.style.transformOrigin = '50% 50% ' + -apothem + 'px';

			for (var i = 0; i < n; i++) {
				images[i].style.padding = gap + 'px';
			}for (i = 1; i < n; i++) {
				images[i].style.transformOrigin = '50% 50% ' + -apothem + 'px';
				images[i].style.transform = 'rotateY(' + i * theta + 'rad)';
			}
			if (bfc) for (i = 0; i < n; i++) {
				images[i].style.backfaceVisibility = 'hidden';
			}rotateCarousel(currImage);
		}
          
		function setupNavigation() {
			nav.addEventListener('click', onClick, true);
			function onClick(e) {
				e.stopPropagation();

				var t = e.target;
				if (t.tagName.toUpperCase() != 'BUTTON') return;

				if (t.classList.contains('next')) {
					currImage++;
				} else {
					currImage--;
				}

				rotateCarousel(currImage);
			}
		}

		function rotateCarousel(imageIndex) {
			figure.style.transform = 'rotateY(' + imageIndex * -theta + 'rad)';
		}
	}
	window.addEventListener('load',function(){
		$('#b1').mouseover(function(event) {
			$(this).parent().children().removeClass('myactive');
			$(this).parent().children().removeClass('mynoactive');
			$(this).parent().children().addClass('mynoactive');
			$(this).removeClass('mynoactive');
			$(this).addClass('myactive');
			$(".list1").show();
			$(".list2").hide();
			$(".list3").hide();
		});


		$('#b2').mouseover(function(event) {
			$(this).parent().children().removeClass('myactive');
			$(this).parent().children().removeClass('mynoactive');
			$(this).parent().children().addClass('mynoactive');
			$(this).removeClass('mynoactive');
			$(this).addClass('myactive');
			$(".list1").hide();
			$(".list2").show();
			$(".list3").hide();
		});


		$('#b3').mouseover(function(event) {
			$(this).parent().children().removeClass('myactive');
			$(this).parent().children().removeClass('mynoactive');
			$(this).parent().children().addClass('mynoactive');
			$(this).removeClass('mynoactive');
			$(this).addClass('myactive');
			$(".list1").hide();
			$(".list2").hide();
			$(".list3").show();
		});


		$('#b4').mouseover(function(event) {
			$(this).parent().children().removeClass('myactive');
			$(this).parent().children().removeClass('mynoactive');
			$(this).parent().children().addClass('mynoactive');
			$(this).removeClass('mynoactive');
			$(this).addClass('myactive');

			$(".list4").show();
			$(".list5").hide();
			$(".list6").hide();
		});


		$('#b5').mouseover(function(event) {
			$(this).parent().children().removeClass('myactive');
			$(this).parent().children().removeClass('mynoactive');
			$(this).parent().children().addClass('mynoactive');
			$(this).removeClass('mynoactive');
			$(this).addClass('myactive');

			$(".list4").hide();
			$(".list5").show();
			$(".list6").hide();
		});


		$('#b6').mouseover(function(event) {
			$(this).parent().children().removeClass('myactive');
			$(this).parent().children().removeClass('mynoactive');
			$(this).parent().children().addClass('mynoactive');
			$(this).removeClass('mynoactive');
			$(this).addClass('myactive');

			$(".list4").hide();
			$(".list5").hide();
			$(".list6").show();
		});

	});

	window.addEventListener('load',function(){
         $('#a1').mouseover(function(event) {
         	$(this).parent().children().removeClass('my-a-active');
			$(this).addClass('my-a-active');
         });

          $('#a2').mouseover(function(event) {
         	$(this).parent().children().removeClass('my-a-active');
			$(this).addClass('my-a-active');
         });

           $('#a3').mouseover(function(event) {
         	$(this).parent().children().removeClass('my-a-active');
			$(this).addClass('my-a-active');
         });
	});