var page = require('webpage').create();
page.open('https://www.leboncoin.fr/vi/1997275853.htm#xtor=ES-3999-[MYSRCH]', function() {
    setTimeout(function() {
	var ua = page.evaluate(function() {
	  return document.title;
	});
	var content = page.evaluate(function(){
	    return document.body.innerText;
	});
	var html = page.evaluate(function(){
	    return document.body.innerHTML;
	});
	console.log(ua);
	console.log(content);
	console.log(html);
	console.log('exit');
	phantom.exit();
    }, 200);
});
