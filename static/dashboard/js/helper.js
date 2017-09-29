export function isUserAuthed() {
	var auth = $('#auth');
	if(auth.data('authed') === "True") {
		return true;
	} else {
		return false;
	}
}

export function showModal(target) {
	$('#' + target).modal('show');
}

export function createMarkup(encodedHtml) { 
	return {
		__html: encodedHtml
	};
};

export function getUrlParameter(paramName) {
	var query = window.location.search.substring(1);
	var vars = query.split("&");
		for (var i=0;i<vars.length;i++) {
			var pair = vars[i].split("=");
			if(pair[0] == paramName){return pair[1];}
		}	
	return(false);
}

export function checkUrlParameterExists(paramName) {
	var query = window.location.search.substring(1);
	var vars = query.split("&");
		for (var i=0;i<vars.length;i++) {
			var pair = vars[i].split("=");
			if(pair[0] == paramName){
				return true;
			}
		}	
	return(false);
}
