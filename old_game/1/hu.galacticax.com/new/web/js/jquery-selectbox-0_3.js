/*
 * jQuery selectbox plugin
 *
 * Copyright (c) 2007 Sadri Sahraoui (brainfault.com)
 * Licensed under the GPL license:
 *   http://www.gnu.org/licenses/gpl.html
 *
 * The code is inspired from Autocomplete plugin (http://www.dyve.net/jquery/?autocomplete)
 *
 * Revision: $Id$
 * Version: 0.3
 */
if(!navigator.userAgent.toLowerCase().match(/ip(od|hone)|iemobile|windows ce|netfront|midp|symbian|android|mobi/i)) 
{
	jQuery.fn.extend({
		selectbox: function(options) {
			return this.each(function() {
				new jQuery.SelectBox(this, options);
			});
		}
	});

	jQuery.SelectBox = function(selectobj, options) {
		
		var opt = options || {};
		opt.inputClass = opt.inputClass || "selectbox";
		opt.inputClass += ' ' + selectobj.className;
		opt.containerClass = opt.containerClass || "selectbox-wrapper";
		opt.hoverClass = opt.hoverClass || "selected";
		opt.debug = opt.debug || false;
		
		var elm_id = selectobj.id;
		var active = -1;
		var inFocus = false;
		var hasfocus = 0;
		//jquery object for select element
		var $select = $(selectobj);
		var onChangeFoo = selectobj.onchange;
		$select.onChange = (typeof selectobj.onchange == "function") ? selectobj.onchange : function(){};
		// jquery container object
		var $container = setupContainer(opt);
		//jquery input object 
		var $input = setupInput(opt);
		// hide select and append newly created elements
		$select.hide().before($input);

		var $icon = null;

		if ($select.hasClass('with-icons'))
		{
			$icon = $("<img class='selectbox-icon' />");
			$icon.attr("id", elm_id+"_icon");
			$input.before($icon);
		}

		$('body').append($container);

		init();

		$container
		.mouseover(function(event) {
			hasfocus = 1;
		})
		.mouseout(function(event) {
			hasfocus = -1;
		});

		if (!selectobj.disabled && !$select.attr('disabled')) $input
		.click(function()
		{
			if (!inFocus)
			{
			  $container.toggle();
			}
			else inFocus = false;
		})
		.focus(function()
		{
		   if ($container.not(':visible'))
		   {
			   inFocus = true;
			   $container.show();

				var offset = $input.offset();
				var clearanceTop = offset.top - $(document).scrollTop();
				var clearanceBottom = $(window).height() - (offset.top - $(document).scrollTop()) - $input.height();
				var clearanceDir = clearanceTop < clearanceBottom;
				var containerInnerHeight = $container.children("ul").height();
				var containerHeight = Math.min(containerInnerHeight,
					Math.max(clearanceTop, clearanceBottom)-10);
				offset.height = containerHeight;
				offset.width = $input.width();
				offset.top += clearanceDir * $input.height() - (!clearanceDir) * containerHeight;
				$container.css(offset);

				// second pass

				offset = $input.offset();
				clearanceTop = offset.top - $(document).scrollTop();
				clearanceBottom = $(window).height() - (offset.top - $(document).scrollTop()) - $input.height();
				clearanceDir = clearanceTop < clearanceBottom;
				containerInnerHeight = $container.children("ul").height();
				containerHeight = Math.min(containerInnerHeight,
					Math.max(clearanceTop, clearanceBottom)-10);
				offset.height = containerHeight;
				offset.width = $input.width();
				offset.top += clearanceDir * $input.height() - (!clearanceDir) * containerHeight;
				$container.css(offset);
		   }
		})
		.keydown(function(event) {  
			switch(event.keyCode) {
				case 38: // up
					event.preventDefault();
					moveSelect(-1);
					break;
				case 40: // down
					event.preventDefault();
					moveSelect(1);
					break;
				//case 9:  // tab 
				case 13: // return
					event.preventDefault(); // seems not working in mac !
					setCurrent();
					hideMe();
					$select.onChange();
					break;
			}
		})
		.blur(function() {
			if ($container.is(':visible') && hasfocus > 0 ) {
				if(opt.debug) console.log('container visible and has focus')
			} else {
				hideMe();	
			}
		});

		function hideMe() { 
			hasfocus = 0;
			$container.hide(); 
		}

		function init()
		{
			$container.append(getSelectOptions()).hide();
			var width = $input.width()
			$container.width(width);
		}

		function setupContainer(options)
		{
			var container = document.createElement("div");
			$container = $(container);
			$container.attr('id', elm_id+'_container');
			$container.addClass(options.containerClass);
			
			return $container;
		}
		
		function setupInput(options)
		{
			var input = document.createElement("input");
			var $input = $(input);
			$input.attr("id", elm_id+"_input");
			$input.attr("type", "text");
			$input.addClass(options.inputClass);
			$input.attr("autocomplete", "off");
			$input.attr("readonly", "readonly");
			$input.attr("tabIndex", $select.attr("tabindex")); // "I" capital is important for ie
			
			return $input;	
		}
		
		function moveSelect(step)
		{
			var lis = $("li", $container);
			if (!lis) return;

			active += step;

			if (active < 0) active = 0;
			else if (active >= lis.size()) active = lis.size() - 1;

			lis.removeClass(opt.hoverClass);

			$(lis[active]).addClass(opt.hoverClass);

			if ($container.not(':visible')) setCurrent();
		}
		
		function setCurrent(elm) {
			var li = (elm == null) ? $("li."+opt.hoverClass, $container).get(0) : elm;
			var el = li.id;
			$select.val(el);
			if ($icon != null) $icon.attr('src', $('option:selected', $select).attr('icon'));
			$input.val($(li).text().replace(/&nbsp;/gi, " "));
			return true;
		}
		
		// select value
		function getCurrentSelected() {
			return $select.val();
		}
		
		// input value
		function getCurrentValue() {
			return $input.val();
		}
		
		function getSelectOptions()
		{
			var select_options = new Array();
			var ul = document.createElement('ul');
			$select.children('option').each(function()
			{
				var li = document.createElement('li');
				li.setAttribute('id', $(this).val());
				li.innerHTML = $(this).html();

				if ($icon != null) $(li).prepend("<img class='option-icon' src='" + $(this).attr('icon') + "' />");

				if ($(this).is(':selected'))
				{
					$input.val($(this).text().replace(/&nbsp;/gi, " "));
					if ($icon != null) $icon.attr('src', $(this).attr('icon'));
					$(li).addClass(opt.hoverClass);
				}
				ul.appendChild(li);
				$(li)
				.mouseover(function(event)
				{
					if (opt.debug) console.log('out on : '+this.id);
					jQuery(event.target, $container).addClass(opt.hoverClass);
				})
				.mouseout(function(event)
				{
					if (opt.debug) console.log('out on : '+this.id);
					jQuery(event.target, $container).removeClass(opt.hoverClass);
				})
				.click(function(event)
				{
					if (opt.debug) console.log('click on :'+this.id);
					$(this).addClass(opt.hoverClass);
					setCurrent(this);
					hideMe();
					$select.onChange();
				});
			});
			return ul;
		}
		
	};
} else {
	jQuery.fn.extend({
		selectbox: function(options) {
			
		}
	});
}