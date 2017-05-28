function make_sidebar_menu() {
	$('.sidebar .item .hide_show_button').click(function() {
		$(this).parent().children('.submenu').slideToggle(250);
		$(this).text(function(i, text){
		  return text === ">" ? "<" : ">";
		});
	});
}	

function showNotification(text) {
	// TODO: добавить типы уведомлений(ошибка, предупреждение и т.д.)
	ajaxResult.textContent = text;
    $('#ajaxResult').css('background-color', '#ccf')
    $('#ajaxResult').fadeIn(500).delay(1000).fadeOut(500)
}