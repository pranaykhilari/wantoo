var companyName = window.userInfo.company;
var companyId = window.userInfo.companyId;
var ALGOLIA_APP_ID = window.ALGOLIA_APP_ID;
var ALGOLIA_SEARCH_KEY = window.ALGOLIA_SEARCH_KEY;

try {
  var client = algoliasearch(ALGOLIA_APP_ID, ALGOLIA_SEARCH_KEY);
  var index = client.initIndex('idea_index');
} catch(error) {
  console.log(error);
}

export function getNotifications () {
	var deferred = $.Deferred();

	var endpoint = '/api/v1/' + companyName + '/notifications/';
	
	$.ajax({
		method: "GET",
		url: endpoint
	}).done(function (results) {
		deferred.resolve(results);
	});

	return deferred.promise();
}

export function clearNotifications() {	

	var endpoint = '/' + companyName + '/clear-notifications/';

	$.ajax({
		method: "GET",
		url: endpoint
	}).done(function (results) {
		//done
	});
}

export function publishIdea(text, catID) {	
	// var endpoint = '/' + window.userInfo.company + '/idea/add/';
	var endpoint = '/api/v1/' + companyName + '/ideas/';

	$.ajax({
		method: "POST",
		url: endpoint,
		data: {
	     title: text,
	     category: catID
		}
	}).done(function (results) {
		
		 window.location = '/' + results.id + '/';

		//there shouldn't be any idea in localstorage, but just in case, remove it
		localStorage.removeItem('ideaInfo');
	});
}

export function api_vote(id, alreadyVoted) {
	console.log("vote!");
	console.log(id);
	console.log(alreadyVoted);

	//post vote
	var endpoint;

	if(!alreadyVoted) {
		endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + id + '/votes/';
		$.ajax({
			method: "POST",
			url: endpoint
		}).done(function (results) {
			console.log(results);
		});
	} else {
		endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + id + '/votes/';
		$.ajax({
			method: "DELETE",
			url: endpoint
		}).done(function (results) {
			console.log(results);
		});
	}
}


export function algolia_search(searchString = null) {
	return new Promise(function(resolve, reject){
		index.search(searchString, {
	    numericFilters: `company_id=${companyId}`,
	    hitsPerPage: 30,
	    facets: '*'
	  }, function fireCallback(err, content){
	  	if(err) {
	  		reject(err);
	  	} else {
	  		resolve(content);
	  	}
	  });
	});
}	

