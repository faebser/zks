$(document).ready(function() {
	var	nav = $("#nav-wrapper"),
		trigger = $("#mobile"),
		note = $(".detail .lead"),
		cNode = note.text().split(' ').length-9;
		
	note.nthWord(cNode+"n").addClass("dropcap-top");
	
	trigger.on("click", function(e) {
		e.preventDefault();
		$("body").toggleClass("nav-open");
	});

	
});
