function showEventPopup(id) {
	$("body").css("overflow","hidden"); 
	// да, костыль, но работает же!

	$.get(resolveUrl("core:event_detail", id), function( response ) { 
		$('#event_popup #event_popup_frame').html(response);
	} );
    // event_popup.getElementsByTagName("iframe")[0].src = "{% url 'core:event_detail' pk=999 %}".replace(999, id);
    event_popup.style.display = "block";
    event_popup_frame.style.webkitAnimationName = 'event_popup_frame_showing';
    event_popup.style.webkitAnimationName = 'event_popup_showing';
}
function hideEventPopup() {
	$("body").css("overflow","auto"); 
	event_popup_frame.style.webkitAnimationName = 'event_popup_frame_hiding';
	event_popup.style.webkitAnimationName = 'event_popup_hiding';
	setTimeout(function() {
		event_popup.style.display='none';
	}, 400)
}


function setEventSubscribedState(elem, pk, state) {
	var action_url
	if(state)
		action_url = '/ajax/eventSubscribe/' + pk + '/'
	else
		action_url = '/ajax/eventUnsubscribe/' + pk + '/'
	$.ajax({
            type: 'GET',
            url: action_url,
            success: function(data) {
                    showNotification(data);
                    elem = $(elem)
                    if(state)
                    	elem.removeClass('subscribe-button').addClass('subscribed-button')
                    else
                    	elem.removeClass('subscribed-button').addClass('subscribe-button')
                    subscribers = parseInt(elem[0].getAttribute('subscribers'))
                    if(state)
                    	subscribers++
                    else
                    	subscribers--
                    elem[0].setAttribute('subscribers', subscribers)
                    if(state) {
	                    elem[0].textContent = "Отписаться (" + subscribers + ")"
	                    elem.unbind('click');
	                    elem[0].onclick = function() {
	                     	unsubscribeFromEvent(elem, pk)
	                    }
                	} else {
                		elem[0].textContent = "Подписаться (" + subscribers + ")"
	                    elem.unbind('click');
	                    elem[0].onclick = function() {
	                     	subscribeToEvent(elem, pk)
	                    }
                	}
            },
            error:  function(xhr, str){
                    alert('Возникла ошибка: ' + xhr.responseCode);
            }
	});
}
function subscribeToEvent(elem, pk) {
 	setEventSubscribedState(elem, pk, true)   
}
function unsubscribeFromEvent(elem, pk)
{
    setEventSubscribedState(elem, pk, false)
}