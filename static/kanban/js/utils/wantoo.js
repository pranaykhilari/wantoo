require('jquery');


/* ############### BELOW WAS COPIED FROM MAIN.JS ################ */

/**
* getCookie
* @ name (string): name of the cookie
* Returns cookie
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/* ########################################################## */


const Wantoo = {

	/**
	* Idea Actions
	*/

	addIdea(text,single, description, catID=null, statID=null) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/';

		console.log("PUBLISHING IDEA: { text: " + text + ", single:"+ single+",description: " + description + ", catID: " + catID +  ", statID: " + statID + "}");
		return new Promise( resolve => {
			$.ajax({
				method: "POST",
				url: endpoint,
				data: {
			     title: text,
			     description: description,
			     category: catID,
			     status: statID,
				 check:single,
				}
			}).done(function (results) {
				console.log('here in wantoo.js');
				console.log('Publish Idea Results => ', results);
				resolve(results);
			});
		}).then(resolve => {
			return resolve;
		});
	},

	updateIdea(title,single, description, category, ideaID) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + ideaID + '/';

		console.log("PUBLISHING IDEA EDIT: { title:" + title + ",single:"+ single+", description: " + description + ", category: " + category + ", ideaID: " + ideaID + "}");

		return new Promise( resolve => {
			$.ajax({
				method: "PUT",
				url: endpoint,
				data: {
					title: title,
			   		description: description,
			   		category: category,
			   		status: 307,
					check:single,
			  	}
			}).done(function (results) {
				console.log('Publish Idea EDIT Results => ', results);
				resolve(results);
			});
		}).then(resolve => {
			return resolve;
		});
	},

	deleteIdea(ideaID) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + ideaID + '/';

		console.log("PUBLISHING IDEA DELETE: { ideaID: " + ideaID + "}");

		$.ajax({
			method: "DELETE",
			url: endpoint
		}).done(function (results) {
			console.log('Publish Idea DELETE Results => ', results);
		});

	},

	updateCardOrder(ideaID, newOrder, statusID) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + ideaID + '/order/';
		var changedIdeas = [];
		app.ideas.forEach(item => {
			if(item.idea_id == ideaID) {
				item.status.id = statusID;
			}else if(item.old_order != item.order) {
				var changeIdea = {};
				changeIdea.ideaId = item.idea_id;
				changeIdea.order = item.order;
				changedIdeas.push(changeIdea);
				item.old_order = item.order;
			}
		});
		console.log("PUBLISHING NEW IDEA ORDER: { ideaID: " + ideaID + ", order: " + newOrder + ", status: " + statusID + "}");

		if (!statusID) {
			console.log('STATUS ID IS NULL');
			statusID = null;
		}

		$.ajax({
			method: "PUT",
			url: endpoint,
			data: {
				order: newOrder,
				status: statusID,
				changedIdeas: JSON.stringify(changedIdeas)
		  	},
		}).done(function (results) {
			console.log('Publish Idea ORDER Results => ', results);
		});

	},


	/**
	* Status Actions
	*/

	addStatus(title, color, closed) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/statuses/';

		console.log("PUBLISHING STATUS: { title: " + title + ", color: " + color + ", closed: " + closed + "}");

		return new Promise( resolve => {
			$.ajax({
				method: "POST",
				url: endpoint,
				data: {
			     title: title,
			     color: color,
			     closed: closed,
				}
			}).done(function (results) {
				// console.log('Publish Idea Results => ', results);
				resolve(results);
			});
		}).then(resolve => {
			return resolve;
		});

	},

	updateStatus(title, color, closed, statusID) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/statuses/' + statusID + '/';

		console.log("PUBLISHING STATUS EDIT: { title: " + title + ", color: " + color + ", closed: " + closed + ", statusID: " + statusID + "}");

		return new Promise( resolve => {
			$.ajax({
				method: "PUT",
				url: endpoint,
				data: {
					title: title,
			   		color: color,
			   		closed: closed,		
			  	}
			}).done(function (results) {
				console.log('Publish Status EDIT Results => ', results);
				resolve(results);
			});
		}).then(resolve => {
			return resolve;
		});

	},

	deleteStatus(statusID) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/statuses/' + statusID + '/';

		console.log("PUBLISHING STATUS DELETE: { statusID: " + statusID + "}");

		$.ajax({
			method: "DELETE",
			url: endpoint
		}).done(function (results) {
			console.log('Publish Status DELETE Results => ', results);
		});

	},

	updateListOrder(statusID, newOrder) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/statuses/' + statusID + '/order/';

		console.log("PUBLISHING STATUS DELETE: { ideaID: " + ideaID + ", newOrder:" + newOrder + "}");

	},


	/**
	* General Events
	*/

	reIndexCards() {
		

	},

	reIndexLists() {



	}




};

export default Wantoo;