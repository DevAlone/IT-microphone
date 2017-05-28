function updateChat(elem, id, offset, count) {
	if(typeof offset === 'undefined')
		offset = 0;
	if(typeof count === 'undefined')
		count = 50;

	$.ajax({
        type: 'GET',
        url: resolveUrl('chat:getMessages', id) + '?offset=' + offset + '&count=' + count,
        success: function(data) {
            comments_count = data['count_messages'];
            messagesDom = []
            var len = data['messages'].length;
            for (var i = 0; i < len; i++) {
            	message = data['messages'][i];
            	author = message.author;

            	messageDom = {
					class: 'message',
					content: [
						{
							class: 'top',
							content: [
								{
									class: 'author',
									content: [
										{
											tag: 'a',
											class: '',
											href: resolveUrl('accounts:profile', 'admin'),
											content: author.first_name.length > 0 ? author.first_name : author.username,
										},
									],
								}, 
								{
									class: 'pub_date',
									content: message['pub_date'],
								},
							]
						},
						{
							class: 'text',
							content: message['text'],
						}, 
						{
							class: 'rating',	
							content: [
								{
									tag: 'a',
									class: 'plus',
									href: '#',
									onclick: "rateMessage(this, " + message.pk + ", 1)",
									content: '+',
								},
								{
									tag: 'span',
									class: 'value',
									content: message.likes_count - message.dislikes_count,
									alt: "+" + message.likes_count + " -" + message.dislikes_count,
								},
								{
									tag: 'a',
									class: 'minus',
									onclick: "rateMessage(this, " + message.pk + ", 0)",
									href: '#',
									content: '-',
								}
							]
							// content: [
							// 	{
							// 		class: 'likes_count',
							// 		content: message['likes_count'],
							// 	}, 
							// 	{
							// 		class: 'dislikes_count',
							// 		content: message['dislikes_count'],
							// 	}, 
							// ]
						}
					], //['text'],
				}; 
				
            	messagesDom.push(messageDom)
            };
            pagesDom = []
            // TODO: вынести 50 в settings
            	for(var i = 0; i < comments_count; i+= 50) {
            		pagesDom.push({
            			tag: 'a',
            			class: 'button',
            			href: '#',
            			onclick: 'updateChat(' + elem.id + ',' + id + ',' + (i) + ', ' + count + ')',
            			content: (i / 50),
            		})
            }
			chatDom = [
				{
					class: 'comments_count',
					content: 'Количество комментариев - ' + comments_count,
				},
				{
					class: 'messages',
					content: messagesDom,
				},
				{
					class: 'pagination',
					content: pagesDom,
				},
			]
			elem.innerHTML = ''
			generateDOM(chatDom, elem);
        },
        error:  function(xhr, str){
            alert('Возникла ошибка: ' + xhr.responseCode);
        }
	});	
}

function rateMessage(element, pk, action) {
	$.ajax({
		type: 'POST', 
		url: resolveUrl('chat:messageVote', pk, action),
		success: function(data) {
			var ratingElem = $(element).parent().children('.value');

			if(!data.state) {
				showNotification(data.text);
				return;
			}
			var rating = parseInt(data.likes_count) - parseInt(data.dislikes_count);
			ratingElem.text(rating);
		},
		error:  function(xhr, str){
			alert('Возникла ошибка: ' + xhr.responseCode);
        }
	});
}