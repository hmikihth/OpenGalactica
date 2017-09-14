function initSearch(xpEntries, xpInput, xpResults, xpFloatingPanel)
{
	var $results = $(xpResults);
	var $entries = $(xpEntries);
	var $input = $(xpInput);
	var $panel = $(xpFloatingPanel);
	var lastInitial = "";
	
	if (location.hash)
	{
		$entry = $('a[name=' + location.hash.substring(1) + ']').parent();

		if ($entry)
		{
			setTimeout(function ()
			{
				$('html,body').attr('scrollTop', $entry.offset().top - 228);

				$entry.animate({backgroundColor: '#313131'}, 250)
					.animate({backgroundColor: '#101010'}, 500);
		
				$entry.find('h5').animate({color: '#ffffff'}, 250)
					.animate({color: '#ffe3a5;'}, 1500);
			}, 500);
		}
	}
	else
	{
		$('html,body').attr('scrollTop', 0);		
	}
	$entries.each(function (i)
	{
		var $this = $(this);
		var title = $this.find("h5").html();
		var initial = title.substring(0, 1).toUpperCase();

		if (initial != lastInitial)
		{
			var $h4 = $(document.createElement("H4"));
			$h4.append(initial + ' ');

			$this.before($h4);
			var a = document.createElement("A");
			$h4.append(a);

			a.href = '#';
			a.className = 'encyclopedia-link';
			a.innerHTML = "[Ugrás a lap tetejére]";
			
			lastInitial = initial;
		}
		$this.attr('id', 'search-subject-' + i);

		$this.before('<a name="search-subject-'+i+'"></a>');

		var $li = $(document.createElement("LI"));
		$results.append($li);

		var a = document.createElement("A");
		$li.append(a);

		a.href = '#search-subject-' + i;
		a.innerHTML = title;

		$(a).bind('click', function (e)
		{
			e.preventDefault();
			// e.stopPropagation();

			$('html,body').attr('scrollTop', $this.offset().top - 228);

			$this.animate({backgroundColor: '#313131'}, 250)
				.animate({backgroundColor: '#101010'}, 500);

			$this.find('h5').animate({color: '#ffffff'}, 250)
				.animate({color: '#ffe3a5;'}, 1500);
		});

		this.searchLink = $li;
	});
	$input.val('');
	$input.bind('keyup', function (e)
	{
		var search_string = String($(this).val());

		if (search_string.length > 0)
		{
			x = RegExp.escape(search_string.toLowerCase());
			$entries.each(function (i) {
				if ($(this).find('h5').text().toLowerCase().search(x) != -1) this.searchLink.show();
				else this.searchLink.hide();
			});
			$panel.css("position", "fixed");
		}
		else // if (search_string.length == 0)
		{
			$('html,body').animate({scrollTop: 0}, 1000, null, function () {
				$panel.css("position", "relative");
				$entries.each(function (i) {
					this.searchLink.show();
				});
			}); 
		}
		// else $panel.css("position", "fixed");

	});	
}
RegExp.escape = function(str) {
  return String(str).replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$1');
};
