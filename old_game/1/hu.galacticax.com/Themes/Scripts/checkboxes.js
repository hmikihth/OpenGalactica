//global variables that can be used by ALL the function son this page.

$(document).ready(function()
{
	$('input[type=radio], input[type=checkbox]').each(function(i)
	{
		var $this = $(this);
		var input = this;

		var display = document.createElement('span');
			
		display.inputNode = input;
		display.onclick = changeState;

		$this.before(display);
		$this.hide();

		input.displayNode = display;
		var savedOnclick = input.onclick;
		input.onclick = updateState;
		input.onclick();			
		input.savedOnclick = savedOnclick;
	});
});

function updateState()
{
	var display = this.displayNode;
	display.className = this.className + (this.type == 'radio' ? " radio" : " checkbox") + (this.checked ? "_on" : "_off");
	if (typeof(this.savedOnclick) == "function") this.savedOnclick();
}

function changeState()
{
	var input = this.inputNode;
	var form = input.form;
	if (input.getAttribute('type') == 'radio')
	{
		for (var i = 0, node; node = form.elements[i]; i++) 
		
		if (node != input && node.name == input.name)
		{
			node.checked = false;
			node.onclick();
		}
	}
	input.click();
}

function checkBoxToolkitToggleAll(that)
{
	var form = that.form;
	var val = that.checked;
	var els = form.elements;
	var el = null;

	for (var i=0; i < els.length; i++)
	{ 
		el = els[i];
		if (el.type == "checkbox" && el !== that)
		{
			el.checked = val;
			el.onclick();
		}
	}	
}

/*
$(document).ready(function ()
{
	$('input[type=radio], input[type=checkbox]').each(function (i)
	{
		var $this = $(this);
		var type = $this.attr('type');
		var $form = $this.parents('form').eq(0);

		var $display = $('<span></span>');
		$display.attr('class', $this.attr("class"));
		
		if ($this.attr('checked') == false) $display.addClass(type + '_off');

		var updateState = function()
		{
			$display.toggleClass(type + '_off');
		};

		$display.click(function (e)
		{
			if (type == 'radio')
			{
				$form.find('input[name='+$this.attr('name')+']')
				.attr('checked', false)
				.trigger('updateState');
				$this.trigger('updateState');			
			}
			$this.trigger('click');			
		});
		$this.bind('updateState', updateState);
		$this.bind('click', updateState);

		$this.hide().before($display);
		
		$this.get(0).checkAll = function ()
		{
			$form.find('[type=checkbox]').each(function (i)
			{
				this.checked = !$this.attr('checked');
				$(this).trigger('updateState');
			});
			alert($this.attr('checked'));
			$this.trigger('updateState');
		};
	});
});
*/