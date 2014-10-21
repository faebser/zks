/*
 * jQuery 'nth-word' plugin (c) Keith Clark
 * Freely distributable under the terms of the MIT license.
 * 
 * twitter.com/keithclarkcouk
 * www.keithclark.co.uk
 */

(function($) {

	var RE_WORD =		/[\S]+/g;
	var RE_ARGUMENT =	/^(?:([-+])?(\d*)n([-+]\d+)?|([+-]?\d+|odd|even))$/;

	// Parses CSS3 selector formula: 'an+b', 'a', 'odd' and 'even'
	function parseArgument( arg ) {
		var a, b = 0, repeat = true, data = RE_ARGUMENT.exec(arg);
		if (!data) {
			throw "Error '"+arg+"' is not a valid argument.";
		}
		if (data[4]) {
			if (data[4] === "odd" || data[4] === "even") {
				a = 2;
				b = data[4] === "odd" | 0;
			} else {
				a = parseInt(data[4],10);
				repeat = false;
			}
		} else {
			a = parseInt((data[1] || "") + (data[2] || 1), 10);
			b = parseInt(data[3],10) || 0;
		}
		return {
			a: a,
			b: b,
			repeat: repeat
		};
	}

	// Splits the passed text node (node) in two and inserts a new element 
	// populated with the content at substring (start, length) between them
	function injectElement( node, start, length ) {
		var text = node.textContent;
		var wordNode = document.createElement("span");
		var beforeText = document.createTextNode(text.substring(0, start));
		wordNode.textContent = text.substring(start, start + length);	
		wordNode.nthwrapped = true;
		node.parentNode.insertBefore(beforeText, node);
		node.textContent = text.substring(start + length);	
		node.parentNode.insertBefore(wordNode, node);
		return wordNode;
	}

	// Crawls the element (elm) and it's descendats matching words against
	// the formula (f). Matched words are wrapped in tags and returned in an
	// array.
	function getWordContent( elm, f ) {
		var endElm = elm.nextSibling, nodes = [], n = 1, match;
		while (elm !== endElm) {
			if (elm.nodeType === 3) {
				while (match = RE_WORD.exec(elm.textContent) ) {
					if ((n - f.b) % f.a === 0 && ((f.a > 0) ? n >= f.b : n <= f.b)) {
						if (!elm.parentNode.nthwrapped) {
							nodes.push(injectElement(elm, match.index, match[0].length));
							RE_WORD.lastIndex = 0;
						} else {
							nodes.push(elm.parentNode);
						}
						if (!f.repeat) {
							return nodes;
						}
					}
					n++;
				}
			}
	
			// non-recusive DOM walking
			if (elm.firstChild) {
				elm = elm.firstChild;
			} else {
				while (elm && !elm.nextSibling) {
					elm = elm.parentNode;
				}
				if (elm) {
					elm = elm.nextSibling;
				}
			}
		}
		return nodes;
	}
	
	// jQuery exposed function
	$.fn.nthWord = function( arg ) {
		var elms = [];	
		var formula = parseArgument( arg );
		this.each(function(e, elm) {
			elms = elms.concat(getWordContent(elm, formula));
		});
		return $(elms);
	};
	
}(jQuery));