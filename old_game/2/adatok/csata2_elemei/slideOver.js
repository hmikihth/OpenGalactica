$(document).ready(function ()
{
	var textMagnify = $("div[id='soTextMagnify']").text();
	var textClose = $("div[id='soTextClose']").text();
	var iconFull = $("div[id='soIconFull']").text();
	var iconClose = $("div[id='soIconClose']").text();

	var $bg = $('<div id="highslideBackground"></div>');
	var $fg = $('<div id="highslideClose"><img src="'+iconClose+'"></div>');
	$('body').append($bg);
	$('body').append($fg);

	$("a[rel='highslide']").each(function(i)
	{
		var $this = $(this).css("position", "relative");
		var $thumb = $this.find("img").eq(0);
		var position = $thumb.position();
		
		$this.attr('title', textMagnify);

		var $icon = $('<img src="'+iconFull+'" class="highslideFullScreenIcon" />');
		$this.append($icon);

		$this.click(function(e)
		{
			var $img = $(new Image());
			
			var timer = null;

			$img.load(function ()
			{
				$icon.css('opacity', '1');
				
				$img = $(this);
				
				var fnClose = function(e)
				{
					$bg.fadeOut(500);
					
					$img.animate(
					{
						width: $thumb.width(),
						height: $thumb.height(),
						top: $thumb.offset().top,
						left: $thumb.offset().left
					}, 500, 'easeOutExpo', function () {
						$img.remove();
					});
				}

				var cCoords = $.clientCoords();
				cCoords.width = $('body').width();
				
				var zoomFactor = Math.min(Math.min(
						(cCoords.height - 20) / this.height,
						(cCoords.width - 20) / this.width
				), 1);
				var zoomWidth = this.width * zoomFactor;
				var zoomHeight = this.height * zoomFactor;

				$img.attr('title', textClose).css(
				{
					position: "absolute",
					'z-index': 2,
					width: $thumb.width(),
					height: $thumb.height(),
					top: $thumb.offset().top,
					left: $thumb.offset().left,
					cursor: "hand",
					cursor: "pointer"
				})
				.click(fnClose)
				.mousemove(function()
				{
					if (timer == null) $('#highslideClose').fadeIn().click(fnClose);
					else clearTimeout(timer);
					timer = setTimeout(function()
					{
						$('#highslideClose').fadeOut();
						timer = null;
					},
					250);
				})
				.animate(
				{
					width: zoomWidth,
					height: zoomHeight,
					top: Math.max((cCoords.height - (this.height * zoomFactor)) / 2, 5),
					left: Math.max((cCoords.width - (this.width * zoomFactor)) / 2, 5)
				}, 500, 'easeOutExpo');
				$bg.css(
				{
					opacity: 0,
					left: '0px',
					top: '0px',
					width: cCoords.width,
					height: cCoords.height-4,
					display: 'block'
				}).fadeTo(500, 0.7);
				$('#highslideClose').css(
				{
					left: '0px',
					top: '0px',
					width: cCoords.width,
					height: cCoords.height-4
				}).before(this);
			})
			.error(function () {})
			.attr('src', $this.attr("href"));
	
			e.preventDefault();
		});
	});
});
