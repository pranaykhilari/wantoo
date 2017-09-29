/**
* track
* @description - String
* @properties (optional) - Object 
* Sends mixpanel event
*/
export function track(description, properties) {

	if(properties) {
		mixpanel.track(description, properties);
	} else {
		mixpanel.track(description);	
	}
	
}

$(document).ready(function(){
	mixpanel.track_links('#activity_link', 'activity link clicked', {
		'source' : 'nav'
	});

	mixpanel.track_links('#see_all_ideas', 'see all ideas clicked');
	
});