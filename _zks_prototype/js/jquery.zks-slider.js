$.fn.zksSlider = function() {

    return this.each(function() {
    	var slider = $(this),
			w = slider.width(),
			mInit = 0,
			img = slider.find(".img-slide"),
			imgNr = img.length,
			imgClass = "imgactive",
			container = $(this).find(".slider-container"),
			next = slider.find(".next"),
			prev = slider.find(".prev"),
			slide = function(sLink) {
	        	if(sLink.hasClass("next")) {
			        mInit = (mInit==(imgNr-1)) ? 0 : mInit+1;
		        	diff = -mInit*w;
		        } else {
		        	mInit = (mInit==0) ? imgNr-1 : mInit-1;
		        	diff = -mInit*w;
		        }
		        container.css({
				  '-webkit-transform' : 'translateX(' + diff + 'px)',
				  '-moz-transform'    : 'translateX(' + diff + 'px)',
				  '-ms-transform'     : 'translateX(' + diff + 'px)',
				  '-o-transform'      : 'translateX(' + diff + 'px)',
				  'transform'         : 'translateX(' + diff + 'px)'
				});
				img.removeClass(imgClass);
		        img.eq(mInit).addClass(imgClass);
	        }
	        
        img.eq(mInit).addClass(imgClass);

        container.width(imgNr*w);
        
        /* Next/Prev */
        next.add(prev).on('click', function(e) {
			e.preventDefault()
			slide($(this));
        });
        /* Next/Prev Keynav */
		$("body").keydown(function(e) {
			if(e.which == 37) { // left     
				e.preventDefault();
				if(slider.isOnScreen(0.3, 0.3)) {
					prev.trigger("click");
				}
			}
			else if(e.which == 39) { // right     
				e.preventDefault();
				if(slider.isOnScreen(0.3, 0.3)) {
					next.trigger("click");
				}
			}
		});
 
         /* Resize Events */       
        function resSlider() {
	    	w = slider.width();
	    	img.width(w-(2*(parseInt(img.css('padding-left')))));
	    	container.width(imgNr*w);
	    	container.css({
				  '-webkit-transform' : 'translateX(' + -mInit*w + 'px)',
				  '-moz-transform'    : 'translateX(' + -mInit*w + 'px)',
				  '-ms-transform'     : 'translateX(' + -mInit*w + 'px)',
				  '-o-transform'      : 'translateX(' + -mInit*w + 'px)',
				  'transform'         : 'translateX(' + -mInit*w + 'px)'
				});
        }
        
        $(window).resize(function() {
		    if(this.resizeTO) clearTimeout(this.resizeTO);
		    this.resizeTO = setTimeout(function() {
		        $(this).trigger('resizeEnd');
		    }, 500);
		});
		$(window).bind('resizeEnd', function() {
			resSlider();
		});	        

        resSlider();

    });
};

/*	Check if Slider is in Viewport 
	https://github.com/moagrius/isOnScreen
*/

(function ($) {

    $.fn.isOnScreen = function(x, y){

        if(x == null || typeof x == 'undefined') x = 1;
        if(y == null || typeof y == 'undefined') y = 1;

        var win = $(window);

        var viewport = {
            top : win.scrollTop(),
            left : win.scrollLeft()
        };
        viewport.right = viewport.left + win.width();
        viewport.bottom = viewport.top + win.height();

        var height = this.outerHeight();
        var width = this.outerWidth();

        if(!width || !height){
            return false;
        }

        var bounds = this.offset();
        bounds.right = bounds.left + width;
        bounds.bottom = bounds.top + height;

        var visible = (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));

        if(!visible){
            return false;
        }

        var deltas = {
            top : Math.min( 1, ( bounds.bottom - viewport.top ) / height),
            bottom : Math.min(1, ( viewport.bottom - bounds.top ) / height),
            left : Math.min(1, ( bounds.right - viewport.left ) / width),
            right : Math.min(1, ( viewport.right - bounds.left ) / width)
        };

        return (deltas.left * deltas.right) >= x && (deltas.top * deltas.bottom) >= y;

    };

})(jQuery);