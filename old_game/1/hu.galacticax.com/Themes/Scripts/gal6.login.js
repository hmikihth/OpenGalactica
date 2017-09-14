$(document).ready(function()
{
	var loginUsername = $.cookie("loginUsername");

	if (loginUsername !== null && $('#login_remember').get(0) != null)
	{
		$('#login_remember').get(0).click();
		$('#login_username').val(loginUsername);
		$('#login_password').show().val($.cookie('loginPassword'));
		$('#login_password_fake').hide();

		if ($('#newscomment_login_section').get(0) != null)
		{
			$('#newscomment_login_remember').get(0).click();
			$('#newscomment_login_username').val(loginUsername);
			$('#newscomment_login_password').show().val($.cookie('loginPassword'));
			$('#newscomment_login_password_fake').hide();
		}
	}
	else $('#login_password').val('').hide();

	$('#login_section input').keydown(function(e) { if (e.keyCode == 13) { $(this).parents('form').submit(); return false; } });
	$("#login_username").blur(function() { if (this.value=='') this.value = this.title;	})
		.focus(function() { if (this.value==this.title) this.value = ''; });
	$('#login_password_fake').focus(function() { $(this).hide(); $('#login_password').show().focus().val(''); });
	$('#login_password').blur(function() { if (this.value == '') { $(this).hide(); $('#login_password_fake').show(); } });
	$('#login_retry').click(function() { $('#login_section').removeClass('failure'); });
	$('#login_submit').click(function()
	{
		var cookieArgs = { expires: 365, path: '/', domain: '.galacticax.com' };

		if ($('#login_remember').get(0) != null && $('#login_remember').get(0).checked &&
			$('#login_username').val() != $('#login_username').attr('title') &&
			$('#login_password').val() != "")
		{
			$.cookie("loginUsername", $('#login_username').val(), cookieArgs);
			$.cookie("loginPassword", $('#login_password').val(), cookieArgs);
		}
		else
		{
			$.cookie("loginUsername", null, cookieArgs);
			$.cookie("loginPassword", null, cookieArgs);
		}
		$('form#loginbox').submit();
	});
	if ($('#newscomment_login_section') != null) {
//		$('#newscomment_login_section input').keydown( = $('#login_section input').
//		$('#newscomment_login_section input'). = $('#login_section input').

		$('#newscomment_login_section input').keydown(function(e) { if (e.keyCode == 13) { $(this).parents('form').submit(); return false; } });
		$("#newscomment_login_username").blur(function() { if (this.value=='') this.value = this.title;	})
			.focus(function() { if (this.value==this.title) this.value = ''; });
		$('#newscomment_login_password_fake').focus(function() { $(this).hide(); $('#newscomment_login_password').show().focus().val(''); });
		$('#newscomment_login_password').blur(function() { if (this.value == '') { $(this).hide(); $('#newscomment_login_password_fake').show(); } });
		$('#newscomment_login_retry').click(function() { $('#newscomment_login_section').removeClass('failure'); });
		$('#newscomment_login_submit').click(function()
		{
			var cookieArgs = { expires: 365, path: '/', domain: '.galacticax.com' };

			if ($('#newscomment_login_remember').get(0) != null && $('#newscomment_login_remember').get(0).checked &&
				$('#newscomment_login_username').val() != $('#newscomment_login_username').attr('title') &&
				$('#newscomment_login_password').val() != "")
			{
				$.cookie("loginUsername", $('#newscomment_login_username').val(), cookieArgs);
				$.cookie("loginPassword", $('#newscomment_login_password').val(), cookieArgs);
			}
			else
			{
				$.cookie("loginUsername", null, cookieArgs);
				$.cookie("loginPassword", null, cookieArgs);
			}
			$('form#newscomment_loginbox').submit();
		});


	}

});
function loginFailed() { document.getElementById('login_section').className = 'failure'; }