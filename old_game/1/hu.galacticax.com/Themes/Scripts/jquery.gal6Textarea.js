// 	<script language="javascript" src="js/jquery.js" type="text/javascript"></script>

$(document).ready(function()
{
	$('textarea.characterCountdown').each(function()
	{
		var ta = $(this);

		var template = ta.attr("title");
		ta.attr("title", "");
		if (template == null) template = '%d karakter van hátra';

		var maxAllowed = ta.attr("size");
		if (maxAllowed == null) maxAllowed = 512;

		var ind = ta.after('<div class="characterCountdownIndicator" />').next();
		ind.text(template.replace(/%d/, maxAllowed));

		ta.keyup(function()
		{
			ind.text(template.replace(/%d/, maxAllowed - ta.val().length));
                        
                        var textvalue = ta.val().substr(0, maxAllowed);
                        if (ta.val().length > maxAllowed){
                            $('textarea.characterCountdown').val(textvalue);
                            ind.text(template.replace(/%d/, maxAllowed - ta.val().length));
                        }
		});
	});
});