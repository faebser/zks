var index = 0;

var funShitThatYouNeedToRun = function($) {
    // fix dropcap
    var thatP;
    if( (thatP = $('.article-content > *').first()).is('p')) {
    	console.log(thatP);
	    	var thatChar = thatP.html().substring(0, 1);
	    	console.log(thatChar);
	    	thatP.html(thatP.html().substring(1));
	    	thatP.prepend($('<span/>').addClass('dropcap').html(thatChar));
    }
    index += 1;
    console.log('run: ' + index);
};

$(document).ready(function(){
    funShitThatYouNeedToRun($);
});