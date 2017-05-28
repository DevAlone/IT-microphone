// TODO: accounts:profile
function resolveUrl(url) {
	var arr = url.split(':');
	if(arr.length != 2)
		return "";
	var application = arr[0];
	var name = arr[1];
	switch(application) {
		case "core": {
			switch(name) {
				case "event_detail":
					if(arguments.length < 1)
						return ""
					return '/event/' + arguments[1] + '/'
				break;
			}
		}
		break;
		case "chat": {
			switch(name) {
				case "getMessages":
					if(arguments.length < 1)
						return "";
					return '/ajax/chat/' + arguments[1] + '/messages/';
				break;
				case "messageVote":
					if(arguments.length < 2)
						return "";
					return '/ajax/chat/message/' + arguments[1] + '/vote/' + arguments[2] + '/';
				break;
			}
		}
		break;
	}
	return ""
}