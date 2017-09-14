
function slide(direction)
{
	var elapsed = new Date().getTime() - this.animationStartTime;
	var thisobj = this;
	var pos = 0.5 - Math.cos(elapsed / this.animationTimeLength * Math.PI) / 2;
	if (elapsed < this.animationTimeLength) { //if time run is less than specified length
		var distancepercent = (direction) ? pos : 1 - pos;
		this.style.height = (distancepercent * (this.scrollHeight-19) + 19) +"px";
		this.runtimer = setTimeout(function() { thisobj.slide(direction) }, 20);
	}
	else { //if animation finished
		this.style.height = (direction) ? this.scrollHeight + "px" : "19px";
		this.isExpanded = direction; //remember whether content is expanded or not
		this.runtimer = null;
		setCookie(uniquepageid+"-" + this.id, this.isExpanded ? "" : "collapsed");
	}
}

var uniquepageid = window.location.href.replace("http://"+window.location.hostname, "").replace(/^\/|[^a-z_-]+/g, "");
var panels_initialized = false;

function panels_init()
{
	if (panels_initialized) return;

	var panels = getElementsByClassName("panel", "*");
	
	for (var i = 0; i < panels.length; i++)
	{
		panels[i].isExpanded = getCookie(uniquepageid + "-" + panels[i].id) != "collapsed";
		if (!panels[i].isExpanded) panels[i].style.height = "19px";
		panels[i].slide = slide;
	}
	panels_initialized = true;
}

function getElementsByClassName(className, tag, elm){
	var testClass = new RegExp("(^|\\\\s)" + className + "(\\\\s|$)");
	var tag = tag || "*";
	var elm = elm || document;
	var elements = (tag == "*" && elm.all) ? elm.all : elm.getElementsByTagName(tag);
	var returnElements = [];
	var current;
	var length = elements.length;
	for(var i=0; i<length; i++){
		current = elements[i];
		if(testClass.test(current.className)){
			returnElements.push(current);
		}
	}
	return returnElements;
}

function togglePanel(e)
{
	panels_init();

	e = (e) ? e : ((window.event) ? window.event : "");
	var elem = (e.target) ? e.target : e.srcElement;
	if (e && elem.tagName != "A")
	{
		var div = elem.parentNode;
		var state = div.isExpanded;
		// alert('helo: '+div.clientHeight);
		// div.style.height = (state ? div.scrollHeight : 17) +'px';
		div.animationStartTime = new Date().getTime();
		div.animationTimeLength = 300;
		div.slide(!state);
	}
}

function getCookie(name) {
   var arg = name + "=";
   var alen = arg.length;
   var clen = document.cookie.length;
   var i = 0;
   while (i < clen) {
     var j = i + alen;
     if (document.cookie.substring(i, j) == arg)
       return getCookieVal(j);
     i = document.cookie.indexOf(" ", i) + 1;
     if (i == 0) break;
   }
  return null;
}

function getCookieVal(offset) {
     var endstr = document.cookie.indexOf (";", offset);
     if (endstr == -1)
         endstr = document.cookie.length;
     return unescape(document.cookie.substring(offset, endstr));
}

function setCookie(name, value, expires, path, domain, secure) {
    document.cookie = name + "=" + escape (value) +
         ((expires) ? "; expires=" + expires.toGMTString() : "") +
         ((path) ? "; path=" + path : "") +
         ((domain) ? "; domain=" + domain : "") +
         ((secure) ? "; secure" : "");
}
