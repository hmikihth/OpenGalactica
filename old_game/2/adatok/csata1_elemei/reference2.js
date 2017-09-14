function referenceResizeHandler()
{
	var height = $('body').height();
	var width = $('body').width();
	var fHeight = ($("#foot").length > 0) ? 24 : 0;
	$('#pane1holder').css(
	{
		height: (height - 138 - fHeight) +'px'
	});
	$('#pane1holder .jScrollPaneContainer').css(
	{
		height: (height - 138 - fHeight) +'px'
	});
	$('#pane1').jScrollPane();

	$('#pane2holder').css(
	{
		height: (height - 43 - fHeight) +'px',
		width: (width - 264) +'px'
	});
	$('#pane2holder .jScrollPaneContainer').css(
	{
		height: (height - 43 - fHeight) +'px',
		'width': (width - 264) +'px'
	});
	$('#pane2').jScrollPane();
}

$(document).ready(function() {
	var isResizing;
	var $menuPane = $("#pane1");

	var setContainerHeight = function()
	{
		$menuPane.jScrollPane();
	}

	var $input = $("#search_term");
	$input.val('');

	var $entries = $("ul#references_menu li");
	$entries.bind('click', setContainerHeight);

	$input.bind('keyup', function (e)
	{
		var search_string = String($(this).val());
		if (search_string.length > 0)
		{
			x = search_string.toLowerCase().replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$1');
			$entries.each(function (i) {
				if ($(this).text().toLowerCase().search(x) == -1) $(this).addClass('search-hide');
			});
		}
		else
		{
			$entries.removeClass('search-hide'); 
		}
		$('#pane1').jScrollPane();
	});

	var patchLink = function(e)
	{
		var $this = $(e.target);
		var href = $this.attr("href");
		var page = /^[^?]+/.exec(href);
		var args = /\?[^#]+/.exec(href);
		var hash = /#.*$/.exec(href);

		href = (page == null) ? "" : page;
		href += ((args == null) ? "?" : args + "&") + "menuScrollTop=" + (-parseInt($("#pane1").css("top")));
		href += (hash == null) ? "" : hash;
		
		$this.attr("href", href);
	}

	var $chapterLink = $('li[class="active"]', $('#pane1')).eq(0);

	ddtreemenu.createTree("references_menu", true);

	setTimeout(function()
	{
		$('#pane1').jScrollPane();
		$('#pane2').jScrollPane({reinitialiseOnImageLoad: true});
	
		referenceResizeHandler();
	
	    var $pane1 = $('#pane1');
		
		var menuScrollTop = /(\?|&)menuScrollTop=([0-9]+)([#&].*)?$/.exec(location.href);
	
		var resizeTimer = null;
		$(window).bind('resize', function()
		{
			if (resizeTimer) clearTimeout(resizeTimer);
			resizeTimer = setTimeout(referenceResizeHandler, 100);
		});

		if (menuScrollTop != null) 
			$('#pane1')[0].scrollTo(parseInt(menuScrollTop[2]), false);
		else if ($chapterLink !== null) $('#pane1')[0].scrollTo($chapterLink.position().top -10, false);
	},
	250);

	$("#references_menu a").bind("mousedown", patchLink);
	$('.ddtree_operate').bind('mouseup', function()
	{
		setTimeout(setContainerHeight, 100)
	});
});

