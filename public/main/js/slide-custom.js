(function ($) {
    "use strict";
    jQuery(document).ready(function() {
        jQuery('#rev_slider_1').show().revolution({
            
            responsiveLevels: [1200, 992, 768, 480],
            gridwidth:[1200, 992, 768, 480],
            gridheight:[515, 515, 515, 515],
            delay: 7000,

            spinner: 'spinner2',
            disableProgressBar:"on",
            
            sliderLayout: 'fullwidth',
            /*stopLoop: 'on',
            stopAfterLoops: 0,
            stopAtSlide: 1,*/

            navigation: {

                keyboardNavigation: 'on',
                keyboard_direction: 'horizontal',
                onHoverStop: 'off',

                touch: {
 
                    touchenabled: 'on',
                    swipe_threshold: 75,
                    swipe_min_touches: 1,
                    swipe_direction: 'horizontal',
                    drag_block_vertical: true
             
                },
 
                arrows: {
                    enable: false,
                    style: 'persephone',
                    hide_onleave: true,
                    left: {
                        container: 'slider',
                        h_align: 'left',
                        v_align: 'center',
                        h_offset: 40,
                        v_offset: 0
                    },
             
                    right: {
                        container: 'slider',
                        h_align: 'right',
                        v_align: 'center',
                        h_offset: 40,
                        v_offset: 0
                    }
                },
 
                bullets: {
                    enable: false,
                    style: 'hermes',
                    tmp: '<span class="tp-bullet-inner"></span>',
                    hide_onleave: false,
                    h_align: 'center',
                    v_align: 'bottom',
                    h_offset: 0,
                    v_offset: 40,
                    space: 10
                }
            }
        });
    });

})(jQuery);