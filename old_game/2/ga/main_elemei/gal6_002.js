/**
 * @author hoesh
 */

$(document).ready(function()
{
	setTimeout(function()
	{
		var _fixedPanel = $('.panel-imagebar-right-content');
		var fixPosY = _fixedPanel.offset().top;
		var fixHeight = _fixedPanel.height();
		var footerClearance = 90;
		var screenHeight = $(window).height();
		// alert((fixPosY + fixHeight) + ' : ' + (screenHeight - footerClearance));
	
		if (fixPosY + fixHeight > screenHeight - footerClearance)
		{
			_fixedPanel.css({position: 'relative'});
			var _content =	_fixedPanel.parents('.panel')
			if (_content.height() < fixHeight+100) _content.height(fixHeight+100);
		}
	}, 200);
});
