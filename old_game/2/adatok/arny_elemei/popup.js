function gal6TimePopupFunction()
{
	var m = /\.page\.html/g.exec(window.location);
	var l =  (m != null) ? "reference.page.html?chapter=GENERAL,213#current-chapter" :
		"/popup/reference/general/213.html#current-chapter";
	var win = window.open(l, 'help', 'width=1000,height=500,directories=0,location=0,menubar=0,resizable=1,scrollbars=1,status=0,toolbar=0');
	win.focus();
}

$(document).ready(function()
{
	var popupszoveg;
	var COOKIE_NAME = 'reference_window_size';
	var STRATMAP_COOKIE_NAME = 'stratmap_window_size';

	$("span.g6t").each(
		function (i) {
			var content = this.innerHTML.match(/([0-9]{2}:)?[0-9]{4}:[0-9]{2}/g)
			if (content == null || $('#gal6time') == null) return
			content = content[0]
			var ido=content.split(':')
			var tick = $('#gal6time').attr("alt").split(':')
			var idolen = ido.length
			ido=60*(60*ido[idolen-2]+parseInt(ido[idolen-1]))
			tick=60*(60*tick[1]+parseInt(tick[2]))
			var most=new Date()
			var akkor=new Date(most.getTime()-1000*(tick-ido+most.getSeconds()))
			this.alt=akkor.toLocaleString()
			this.title=akkor.toLocaleString()
		}
	)
	$("div.g6t").each(
		function (i) {
			var content = this.innerHTML.match(/([0-9]{2}:)?[0-9]{4}:[0-9]{2}/g)
			if (content == null || $('#gal6time') == null) return
			content = content[0]
			var ido=content.split(':')
			var tick = $('#gal6time').attr("alt").split(':')
			var idolen = ido.length
			ido=60*(60*ido[idolen-2]+parseInt(ido[idolen-1]))
			tick=60*(60*tick[1]+parseInt(tick[2]))
			var most=new Date()
			var akkor=new Date(most.getTime()-1000*(tick-ido+most.getSeconds()))
			this.alt=akkor.toLocaleString()
			this.title=akkor.toLocaleString()
		}
	)

	if (/(\/reference\/|reference\.page\.html)/i.test(window.location))
		$(window).bind("unload", function()
	{
		var cCoords = $.clientCoords();
		$.cookie(COOKIE_NAME + '_width', cCoords.width, {path: '/', expires: null});
		$.cookie(COOKIE_NAME + '_height', cCoords.height, {path: '/', expires: null});
	});

	if (/(\/stategicalmap\/|fleet_locator\.page\.html)/i.test(window.location))
		$(window).bind("unload", function()
	{
		var cCoords = $.clientCoords();
		$.cookie(STRATMAP_COOKIE_NAME + '_width', cCoords.width, {path: '/', expires: null});
		$.cookie(STRATMAP_COOKIE_NAME + '_height', cCoords.height, {path: '/', expires: null});
	});

	var bodyClass = $('body').get(0).className;
	if (bodyClass.indexOf("popup") === 0)
	{
		m1 = /http:\/\/([a-z0-9\-_]+\.)?([a-z0-9\-_]+\.[a-z0-9\-_]+)\//gi.exec(document.referrer);
		m2 = /http:\/\/([a-z0-9\-_]+\.)?([a-z0-9\-_]+\.[a-z0-9\-_]+)\//gi.exec(window.location);

		if (m1 != null && m2 != null && m1[2] == m2[2]) setTimeout(function()
		{
			var h, w;
			if ($('#reference_content').get(0))
			{
				var coordsW = $.cookie(COOKIE_NAME + '_width');
				var coordsH = $.cookie(COOKIE_NAME + '_height');
				if (coordsW > 0 && coordsH > 0)
				{
					w = coordsW;
					h = coordsH;
				}
				else
				{
					w = 1000;
					h = 500;
				}
			}
			else if ($('#locator_content').get(0))
			{
				var coordsW = $.cookie(STRATMAP_COOKIE_NAME + '_width');
				var coordsH = $.cookie(STRATMAP_COOKIE_NAME + '_height');
				if (coordsW > 0 && coordsH > 0)
				{
					w = coordsW;
					h = coordsH;
				}
				else
				{
					w = 1000;
					h = 680;
				}
			}
			else
			{
//				alert('nincs #reference_content');
				h = $("#container").height();
				if (h > 780) h = 620;
	
				w = 790;
				switch (bodyClass)
				{
					case 'popup-extrawide': w = 1260; break;
					case 'popup-wide': w = 1000; break;
					case 'popup-tiny': w = 440; break;
				}
			}
			// setClientSize(w, h);
			var cCoords = $.clientCoords();
			cCoords.width = $('body').width();
			window.resizeBy(w - cCoords.width, h - cCoords.height + 4);
		}, 200);
/*
		$("a[rel!=popup]").bind("click", function(e) {
			var $this = $(this);
			var href = $this.attr("href");
			href += (href.indexOf("?") == -1 ? "?" : "&") + "popupSessionId="+popupSessionId;
			$this.attr("href", href); 
		});
*/
	}
	var helpUrlBase = "";

	var m = /\.page\.html/g.exec(window.location);

	if (m != null)
	{
		m = /\/([a-z0-9\-_]+)\.page\.html/gi.exec(window.location);
		if (m != null) helpUrlBase = "reference.page.html?chapter=" + m[1].toUpperCase() + ',';
		else helpUrlBase = "reference.page.html?chapter=UNKNOWN,";
	}
	else
	{
		var m = /(\/(universe|popup|registration))?\/([a-z\-_]+)(\/|\.html)/g.exec(window.location);
		helpUrlBase = "/popup/reference/" + m[3] + '/';
		// helpUrlBase = "http://drupal.gal6.com/reference/" + m[2] + '/';
	}

	if (helpUrlBase != "") $('a[rel=help]').each(function()
	{
		var m = /\.page\.html/g.exec(window.location);

		$(this).bind('click', doPopUp);
		this.tabIndex = -1;
//		this.title = this.title + " [Opens in pop-up window]";

		var panelId = $(this).parents('.panel').attr('id');

		if (panelId == "")
		{
			panelId = $('#contents div.panel').not('.panel_facebox').attr('id');
		}
		
		this.href = helpUrlBase + panelId + (m == null ? ".html" : "") + '#current-chapter';
	});

	var featureHelpUrlBase = /\.page\.html/g.test(window.location) ?
		'credit_extra_help_popup.page.html' : '/popup/creditextrahelp.html';

	$("img.feature_help_icon:visible").each(function()
	{
		var $this = $(this);
		var rel = $this.attr('rel');
		if (rel && rel.substring(0, 8) == "feature#")
		{
			$host = $this.parents().find('.feature-disabled, .col-feature-disabled');
			$host.get(0).href = featureHelpUrlBase+$this.attr('rel').substring(7);
			$host
			.css({cursor: 'help'})
			.bind('click', doPopUp)
			.attr('title', '[Click to open features help]');
		}
	});
	$('a[rel=popup]').each(function()
	{
		$(this).bind('click', doPopUp);
		this.tabIndex = -1;
	//	this.title = this.title + " [Opens in pop-up window]";
	//	this.title = this.title + popupszoveg?popupszoveg:"[Opens in pop-up window]";	
	});
});

function doPopUp(e)
{
	var l = this.href;
	var w = 790;
	var h = 150;
	var t = "";
	
//	if (!l) alert($(this).data('href'));

	if (/(\/reference\/|reference\.page\.html)/i.test(l))
	{
		h = 500;
		w = 1000;
		t = 'help';
		var win = window.open(l, t, 'width=' + w + ',height=' + h + ',directories=0,location=0,menubar=0,resizable=1,scrollbars=1,status=0,toolbar=0');
		win.focus();
	}
	else if (/(\/stategicalmap\/|fleet_locator\.page\.html)/i.test(l))
	{
		h = 500;
		w = 1000;
		t = 'stratmap';
		var win = window.open(l, t, 'width=' + w + ',height=' + h + ',directories=0,location=0,menubar=0,resizable=1,scrollbars=1,status=0,toolbar=0');
		win.moveTo(100, 100);
		win.focus();
	}
	else if ($("body").is("[class^='popup ']"))
	{
		window.location = l;
	}
	else
	{
		if (this.target != "") t = this.target;
		window.open(l, t, 'width=' + w + ',height=' + h + ',directories=0,location=0,menubar=0,resizable=1,scrollbars=1,status=0,toolbar=0').focus();
	}
	//cancel the default link action if pop-up activated
	e.preventDefault();
	e.stopPropagation();
}

$.clientCoords = function() {
     var dimensions = {width: 0, height: 0};
     if (document.documentElement) {
         dimensions.width = document.documentElement.offsetWidth;
         dimensions.height = document.documentElement.offsetHeight;
     } else if (window.innerWidth && window.innerHeight) {
         dimensions.width = window.innerWidth;
         dimensions.height = window.innerHeight;
     }
     return dimensions;
}
