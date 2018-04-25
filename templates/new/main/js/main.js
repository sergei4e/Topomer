$(document).ready(function(){
	
	// CountTo
	$('.counter').countTo();

	// Tab
	$('.tab-content .tabs').slice(1).hide();
	$('.tab li').bind('click' , function (){
		$('.tab li a').removeClass('active-tab');
		$(this).find('a').addClass('active-tab');
		$('.tab-content .tabs:visible').fadeOut(100);
		$('.tab-content .tabs').eq($(this).index()).fadeIn(100);

		return false;
	});

	// Slide respond
    $('.respond-carousel').owlCarousel({
        nav: false,
        responsive:{
            0:{
                items:1,
                nav: false,
                dots: true
            },
            600:{
                items: 1,
                nav: false,
                dots: true
            },
            1000:{
                items: 1,
                nav: false,
                loop: true,
                dots: true
            }
        }
    });

    // Have promocode
    $('.have-promocode').click(function(){
        $(this).hide();
        $(this).closest('form').find('.price').hide();
        $(this).closest('form').find('.input-promocode').show();
        return false;
    });

    $('.remove-promocode').click(function(){
        $(this).closest('form').find('.input-promocode').hide();
        $(this).closest('form').find('.price').show();
        $('.have-promocode').show();
        return false;
    });

    // Add more url
    var i = 0;
    var price = 0;
    $('.add-more').click(function(){
        if (i <= 9) {
            $('.new-input').prepend('<p class="add-input">' + '<input type="text" name="" placeholder="Url для сравнения">' + '<a href="#" class="remove-input"><i class="fa fa-close"></i></a>' + '</p>');
            i++;
            price=price+0.2;
            $(this).closest('form').find('.price i').text(parseFloat(price).toFixed(1));
        } 
        if (i == 10) {
            $('.add-more').hide();
        }
        if (i == 1) {
            $(this).closest('form').find('.have-promocode').show();
        }

        return false;
    });

   $('.new-input').on('click', '.remove-input', function(e) {
        i--;
        price=price-0.2;
        $(this).closest('form').find('.price i').text(parseFloat(price).toFixed(1));
        if (i>=9) {
            $('.add-more').show();
            $(this).closest('form').find('.price').show();
        }

        if(i==0) {
            $(this).closest('form').find('.input-promocode').hide();
            $(this).closest('form').find('.have-promocode').hide();
        }

        e.preventDefault();
        $(this).parent().remove();
    });

});