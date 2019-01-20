

(function ($) {
    // USE STRICT
    "use strict";

        /*==================================================================
        [ Slick 1 ]*/
        var itemSlick1 = $('.js-slick-1').find('.item-slick-1');

        $('.js-slick-1').on('init', function(){
            $(itemSlick1[0]).children('.para-slide-slick-1').addClass('vi-vi-slick fadeInDown');
            $(itemSlick1[0]).children('.wrap-person').addClass('zoomIn vi-vi-slick');
        });

        $('.js-slick-1').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: false,
            infinite: false,
            autoplay: true,
            autoplaySpeed: 5000,
            appendArrows: $('.wrap-slide-slick-1'),
            prevArrow:'<span class="arrow-slide-slick-1 prev-slide-1"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
            nextArrow:'<span class="arrow-slide-slick-1 next-slide-1"><i class="fa fa-angle-right" aria-hidden="true"></i></span>',
        });

        $('.js-slick-1').on('afterChange', function(event, slick, currentSlide){
            $(itemSlick1[currentSlide]).children('.para-slide-slick-1').addClass('fadeInDown vi-vi-slick');

            setTimeout(function(){
                $(itemSlick1[currentSlide]).children('.wrap-person').addClass('zoomIn vi-vi-slick');
            },800);

            for(var i=0; i<itemSlick1.length; i++) {
                if (i != currentSlide) {
                    $(itemSlick1[i]).find('.para-slide-slick-1').removeClass('fadeInDown vi-vi-slick');
                    $(itemSlick1[i]).find('.wrap-person').removeClass('zoomIn vi-vi-slick');
                }
            }
        });

        /*==================================================================
        [ Slick 2 ]*/
        $('.js-slick-2').slick({
            slidesToShow: 3,
            slidesToScroll: 3,
            dots: false,
            infinite: true,
            autoplay: false,
            appendArrows: $('.container-slick-2'),
            prevArrow:'<span class="arrow-slick-2 prev-slide-2"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
            nextArrow:'<span class="arrow-slick-2 next-slide-2"><i class="fa fa-angle-right" aria-hidden="true"></i></span>',
            responsive: [
                {
                  breakpoint: 1200,
                  settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                  }
                },
                {
                  breakpoint: 992,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 576,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                  }
                }
            ]    
        });

        var x = $('.wrap-pic-b4').height();
        $('.arrow-slick-2').css('top',x/2-17);
        $(window).resize(function(){
            x = $('.wrap-pic-b4').height();
            $('.arrow-slick-2').css('top',x/2-17);
        });


        /*==================================================================
        [ Slide 3 ]*/
        var itemSlick3 = $('.js-slick-3').find('.item-slick-3');

        $('.js-slick-3').on('init', function(){
            $(itemSlick3[0]).find('.para-slide-slick-3').addClass('vi-vi-slick fadeInDown');
            $(itemSlick3[0]).find('.wrap-person-slick-3').addClass('zoomIn vi-vi-slick');
        });

        $('.js-slick-3').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: false,
            autoplay: true,
            autoplaySpeed: 5000,
            dots: true,
            appendDots: $('.wrap-slick3-dots'),
            dotsClass:'slick3-dots',
            appendArrows: $('.wrap-slide-slick-3'),
            prevArrow:'<span class="arrow-slide-slick-3 prev-slide-3"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
            nextArrow:'<span class="arrow-slide-slick-3 next-slide-3"><i class="fa fa-angle-right" aria-hidden="true"></i></span>',
            customPaging: function(slick, index) {
                var linkIMG = $(slick.$slides[index]).data('thumb');
                return '<img src=" ' + linkIMG + ' "/>';
            },  
        });

        $('.js-slick-3').on('afterChange', function(event, slick, currentSlide){
            $(itemSlick3[currentSlide]).find('.para-slide-slick-3').addClass('fadeInDown vi-vi-slick');

            setTimeout(function(){
                $(itemSlick3[currentSlide]).find('.wrap-person-slick-3').addClass('zoomIn vi-vi-slick');
            },800);

            for(var i=0; i<itemSlick3.length; i++) {
                if (i != currentSlide) {
                    $(itemSlick3[i]).find('.para-slide-slick-3').removeClass('fadeInDown vi-vi-slick');
                    $(itemSlick3[i]).find('.wrap-person-slick-3').removeClass('zoomIn vi-vi-slick');
                }
            }
        });


        /*[ Slick 4 ]
        ===========================================================*/
        $('.js-slick-4').slick({
            slidesToShow: 3,
            slidesToScroll: 3,
            dots: false,
            infinite: true,
            autoplay: false,
            appendArrows: $('.container-slick-4'),
            prevArrow:'<span class="arrow-slick-4 prev-slide-4"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
            nextArrow:'<span class="arrow-slick-4 next-slide-4"><i class="fa fa-angle-right" aria-hidden="true"></i></span>',
            responsive: [
                {
                  breakpoint: 1200,
                  settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                  }
                },
                {
                  breakpoint: 992,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 576,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                  }
                }
            ]    
        });


        /*[ Slick 5 ]
        ===========================================================*/
        $('.js-slick-5').slick({
            slidesToShow: 4,
            slidesToScroll: 4,
            dots: false,
            infinite: true,
            autoplay: false,
            appendArrows: $('.container-slick-5'),
            prevArrow:'<span class="arrow-slick-5 prev-slide-5"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
            nextArrow:'<span class="arrow-slick-5 next-slide-5"><i class="fa fa-angle-right" aria-hidden="true"></i></span>',
            responsive: [
                {
                  breakpoint: 1200,
                  settings: {
                    slidesToShow: 4,
                    slidesToScroll: 4
                  }
                },
                {
                  breakpoint: 992,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 576,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                  }
                }
            ]    
        });
        

        /*==================================================================
        [ Slick 6 ]*/
        var itemSlick6 = $('.js-slick-6').find('.item-slick-6');

        $('.js-slick-6').on('init', function(){
            $(itemSlick6[0]).find('.para-slide-slick-6').addClass('vi-vi-slick fadeInDown');
            $(itemSlick6[0]).find('.wrap-person-slick-6').addClass('zoomIn vi-vi-slick');
        });

        $('.js-slick-6').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            infinite: false,
            autoplay: true,
            autoplaySpeed: 5000,
            appendArrows: $('.wrap-slide-slick-6'),
            prevArrow:'<span class="arrow-slide-slick-6 prev-slide-6"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
            nextArrow:'<span class="arrow-slide-slick-6 next-slide-6"><i class="fa fa-angle-right" aria-hidden="true"></i></span>',
            appendDots: $('.wrap-slick6-dots'),
            dotsClass:'slick6-dots',
            customPaging: function(slick, index) {
                var linkIMG = $(slick.$slides[index]).data('thumb');
                return '<img src=" ' + linkIMG + ' "/>';
            },  
        });

        $('.js-slick-6').on('afterChange', function(event, slick, currentSlide){
            $(itemSlick6[currentSlide]).find('.para-slide-slick-6').addClass('fadeInDown vi-vi-slick');

            setTimeout(function(){
                $(itemSlick6[currentSlide]).find('.wrap-person-slick-6').addClass('zoomIn vi-vi-slick');
            },800);

            for(var i=0; i<itemSlick6.length; i++) {
                if (i != currentSlide) {
                    $(itemSlick6[i]).find('.para-slide-slick-6').removeClass('fadeInDown vi-vi-slick');
                    $(itemSlick6[i]).find('.wrap-person-slick-6').removeClass('zoomIn vi-vi-slick');
                }
            }
        });

})(jQuery);