import { track } from './tracking';
import striptags from 'striptags';
// IIFE, local scoping
(function($, window, document, DataTable, userInfo) {

	var ideaInfo = {};

	if (!isMobile())
		$('[data-toggle="tooltip"]').tooltip()

	/* API Calls */

	/**
	* deleteComment
	* @ id (string): the id for the comment
	* Delete the target comment
	*/
	//Functions
	function deleteComment(commentID) {
		//post vote
		var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + window.userInfo.ideaID + '/comments/' + commentID + '/';

		$.ajax({
			method: "DELETE",
			url: endpoint
		}).done(function (results) {
			decrementCommentFeedCount();
		});
	}

	function stupidCounter(el) {
		var inputs = el.find('input, textarea');
		var stupidCounterArray = [];
		$.each(inputs, function(index, item){
			if($(item).attr('maxlength') !== undefined) {
				var cssClass = item.id + "_counter";
				var maxLength = $(item).attr('maxlength');
				var currentCount = maxLength - $(item).val().length;
				$('<p class="-stupid-counter '+cssClass+'">' + currentCount + '</p>').insertBefore(item);

				$(item).on('keyup', function(){
					currentCount = maxLength - $(this).val().length;
					$(this).prev().text(currentCount);
				});
			}
		});
	}

	$(".help-block").css("color", "#a7a7a7");
	/**
	* saveDescription
	* @ id (string): the id for the idea
	* @ description (string): The description text
	* AJAX call to our endpoint to save the new description
	*/
	//Functions
	function saveDescription(ideaID, description) {
		var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + ideaID + '/';

		$.ajax({
			method: "PUT",
			url: endpoint,
			data: {
		   	 description: description
		  	}
		}).done(function (results) {
			window.location.reload();
		});
	}

	/**
	* sendVote
	* @ id (string): the id for the idea
	* @ addVote (boolean): true to add vote, false to remove vote
	* AJAX call to our endpoint to store the vote
	*/
	//Functions
	function sendVote(id, addVote) {
		//post vote
		var endpoint;

		if(addVote) {
			endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + id + '/votes/';
			$.ajax({
				method: "POST",
				url: endpoint
			}).done(function (results) {

			});
		} else {
			endpoint = '/api/v1/' + window.userInfo.company + '/ideas/' + id + '/votes/';
			$.ajax({
				method: "DELETE",
				url: endpoint
			}).done(function (results) {

			});
		}
	}


	/**
	* clearNotifications
	* AJAX call to clearNotifications
	*/
	function clearNotifications() {
			var endpoint = '/' + window.userInfo.company + '/clear-notifications/';
		$.ajax({
			method: "GET",
			url: endpoint
		}).done(function (results) {

		});
	}

	/**
	* publishIdea
	* AJAX call to publish the idea
	*/
	function publishIdea(text, catID) {
		if (ideaInfo.text != "") {
			// var endpoint = '/' + window.userInfo.company + '/idea/add/';
			var endpoint = '/api/v1/' + window.userInfo.company + '/ideas/';

			console.log("PUBLISHING: {" + text + ", " + catID + "}");

			$.ajax({
				method: "POST",
				url: endpoint,
				data: {
					title: text,
					category: catID
				}
			}).done(function (results) {

				window.location = '/' + window.userInfo.company + '/ideas/?sort=new';

				//there shouldn't be any idea in localstorage, but just in case, remove it
				localStorage.removeItem('ideaInfo');
			});
		}
		else {
			window.location = '/' + window.userInfo.company;
		}
	}


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

	/**
	* decodeEntities
	* @ encodedString (string): the encoded string
	* Hack that returns decoded string
	*/
	function decodeEntities(encodedString) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = encodedString;
    return textArea.value;
	}

	function get_gravatar(email, size) {

    // MD5 (Message-Digest Algorithm) by WebToolkit
    //

    /* jshint ignore:start */
 		var MD5=function(s){function L(k,d){return(k<<d)|(k>>>(32-d))}function K(G,k){var I,d,F,H,x;F=(G&2147483648);H=(k&2147483648);I=(G&1073741824);d=(k&1073741824);x=(G&1073741823)+(k&1073741823);if(I&d){return(x^2147483648^F^H)}if(I|d){if(x&1073741824){return(x^3221225472^F^H)}else{return(x^1073741824^F^H)}}else{return(x^F^H)}}function r(d,F,k){return(d&F)|((~d)&k)}function q(d,F,k){return(d&k)|(F&(~k))}function p(d,F,k){return(d^F^k)}function n(d,F,k){return(F^(d|(~k)))}function u(G,F,aa,Z,k,H,I){G=K(G,K(K(r(F,aa,Z),k),I));return K(L(G,H),F)}function f(G,F,aa,Z,k,H,I){G=K(G,K(K(q(F,aa,Z),k),I));return K(L(G,H),F)}function D(G,F,aa,Z,k,H,I){G=K(G,K(K(p(F,aa,Z),k),I));return K(L(G,H),F)}function t(G,F,aa,Z,k,H,I){G=K(G,K(K(n(F,aa,Z),k),I));return K(L(G,H),F)}function e(G){var Z;var F=G.length;var x=F+8;var k=(x-(x%64))/64;var I=(k+1)*16;var aa=Array(I-1);var d=0;var H=0;while(H<F){Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=(aa[Z]|(G.charCodeAt(H)<<d));H++}Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=aa[Z]|(128<<d);aa[I-2]=F<<3;aa[I-1]=F>>>29;return aa}function B(x){var k="",F="",G,d;for(d=0;d<=3;d++){G=(x>>>(d*8))&255;F="0"+G.toString(16);k=k+F.substr(F.length-2,2)}return k}function J(k){k=k.replace(/rn/g,"n");var d="";for(var F=0;F<k.length;F++){var x=k.charCodeAt(F);if(x<128){d+=String.fromCharCode(x)}else{if((x>127)&&(x<2048)){d+=String.fromCharCode((x>>6)|192);d+=String.fromCharCode((x&63)|128)}else{d+=String.fromCharCode((x>>12)|224);d+=String.fromCharCode(((x>>6)&63)|128);d+=String.fromCharCode((x&63)|128)}}}return d}var C=Array();var P,h,E,v,g,Y,X,W,V;var S=7,Q=12,N=17,M=22;var A=5,z=9,y=14,w=20;var o=4,m=11,l=16,j=23;var U=6,T=10,R=15,O=21;s=J(s);C=e(s);Y=1732584193;X=4023233417;W=2562383102;V=271733878;for(P=0;P<C.length;P+=16){h=Y;E=X;v=W;g=V;Y=u(Y,X,W,V,C[P+0],S,3614090360);V=u(V,Y,X,W,C[P+1],Q,3905402710);W=u(W,V,Y,X,C[P+2],N,606105819);X=u(X,W,V,Y,C[P+3],M,3250441966);Y=u(Y,X,W,V,C[P+4],S,4118548399);V=u(V,Y,X,W,C[P+5],Q,1200080426);W=u(W,V,Y,X,C[P+6],N,2821735955);X=u(X,W,V,Y,C[P+7],M,4249261313);Y=u(Y,X,W,V,C[P+8],S,1770035416);V=u(V,Y,X,W,C[P+9],Q,2336552879);W=u(W,V,Y,X,C[P+10],N,4294925233);X=u(X,W,V,Y,C[P+11],M,2304563134);Y=u(Y,X,W,V,C[P+12],S,1804603682);V=u(V,Y,X,W,C[P+13],Q,4254626195);W=u(W,V,Y,X,C[P+14],N,2792965006);X=u(X,W,V,Y,C[P+15],M,1236535329);Y=f(Y,X,W,V,C[P+1],A,4129170786);V=f(V,Y,X,W,C[P+6],z,3225465664);W=f(W,V,Y,X,C[P+11],y,643717713);X=f(X,W,V,Y,C[P+0],w,3921069994);Y=f(Y,X,W,V,C[P+5],A,3593408605);V=f(V,Y,X,W,C[P+10],z,38016083);W=f(W,V,Y,X,C[P+15],y,3634488961);X=f(X,W,V,Y,C[P+4],w,3889429448);Y=f(Y,X,W,V,C[P+9],A,568446438);V=f(V,Y,X,W,C[P+14],z,3275163606);W=f(W,V,Y,X,C[P+3],y,4107603335);X=f(X,W,V,Y,C[P+8],w,1163531501);Y=f(Y,X,W,V,C[P+13],A,2850285829);V=f(V,Y,X,W,C[P+2],z,4243563512);W=f(W,V,Y,X,C[P+7],y,1735328473);X=f(X,W,V,Y,C[P+12],w,2368359562);Y=D(Y,X,W,V,C[P+5],o,4294588738);V=D(V,Y,X,W,C[P+8],m,2272392833);W=D(W,V,Y,X,C[P+11],l,1839030562);X=D(X,W,V,Y,C[P+14],j,4259657740);Y=D(Y,X,W,V,C[P+1],o,2763975236);V=D(V,Y,X,W,C[P+4],m,1272893353);W=D(W,V,Y,X,C[P+7],l,4139469664);X=D(X,W,V,Y,C[P+10],j,3200236656);Y=D(Y,X,W,V,C[P+13],o,681279174);V=D(V,Y,X,W,C[P+0],m,3936430074);W=D(W,V,Y,X,C[P+3],l,3572445317);X=D(X,W,V,Y,C[P+6],j,76029189);Y=D(Y,X,W,V,C[P+9],o,3654602809);V=D(V,Y,X,W,C[P+12],m,3873151461);W=D(W,V,Y,X,C[P+15],l,530742520);X=D(X,W,V,Y,C[P+2],j,3299628645);Y=t(Y,X,W,V,C[P+0],U,4096336452);V=t(V,Y,X,W,C[P+7],T,1126891415);W=t(W,V,Y,X,C[P+14],R,2878612391);X=t(X,W,V,Y,C[P+5],O,4237533241);Y=t(Y,X,W,V,C[P+12],U,1700485571);V=t(V,Y,X,W,C[P+3],T,2399980690);W=t(W,V,Y,X,C[P+10],R,4293915773);X=t(X,W,V,Y,C[P+1],O,2240044497);Y=t(Y,X,W,V,C[P+8],U,1873313359);V=t(V,Y,X,W,C[P+15],T,4264355552);W=t(W,V,Y,X,C[P+6],R,2734768916);X=t(X,W,V,Y,C[P+13],O,1309151649);Y=t(Y,X,W,V,C[P+4],U,4149444226);V=t(V,Y,X,W,C[P+11],T,3174756917);W=t(W,V,Y,X,C[P+2],R,718787259);X=t(X,W,V,Y,C[P+9],O,3951481745);Y=K(Y,h);X=K(X,E);W=K(W,v);V=K(V,g)}var i=B(Y)+B(X)+B(W)+B(V);return i.toLowerCase()};
 		/* jshint ignore:end */

    size = size || 80;

    return 'http://www.gravatar.com/avatar/' + MD5(email) + '.jpg?s=' + size + '&d=mm';
	}

	function get_gravatar_md5(md5, size) {

    size = size || 80;

    return 'http://www.gravatar.com/avatar/' + md5 + '.jpg?s=' + size + '&d=mm';
	}



	/**
	* checkIfAuthed
	* Checks if the current user has a django session
	*/
	function isUserAuthed() {
		var auth = $('#auth');
		if(auth.data('authed') === "True") {
			return true;
		} else {
			return false;
		}
	}

	/**
	* showModal
	* @ target (String): id of target modal
	* Show the target modal
	*/
	function showModal(target) {
		$('#' + target).modal('show');
	}


	/**
	* closeModal
	* @ target (String): id of target modal
	* Show the target modal
	*/
	function closeModal(target) {
		$('#' + target).modal('hide');
	}

	/**
	* showLoginModal
	* Show the login modal
	*/
	function showLoginModal() {
		Cookies.set('redirect_url', window.location.pathname);
		$('#_modal-login').modal('show');
	}

	/**
	* hideLoginModal
	* Show the login modal
	*/
	function closeLoginModal() {
		$('#_modal-login').modal('hide');
	}

	/**
	* showLoginModal
	* Show the login modal
	*/
	function showSignupModal() {
		Cookies.set('redirect_url', window.location.pathname);
		$('#_modal-newSignup').modal('show');
	}

	/**
	* hideLoginModal
	* Show the login modal
	*/
	function closeSignupModal() {
		$('#_modal-newSignup').modal('hide');
	}


	/**
	* animateVote
	* @ voteButton (element): the DOM object to manipulate
	* @ addVote (boolean): true to add vote, false to remove vote
	* Animate the adding or removing of a vote
	*/
	function animateVote(voteButton, addVote) {
		//get the vote count element so we can inject the updated score
		var voteCount = $(voteButton).parent().find('._vote-count');
		var count;

		//check the current state class
		if(addVote) {
			//update the state class
			$(voteButton).addClass('voted');
			$(voteButton).parent('.-cont-vote').addClass('voted');
			$(voteButton).removeClass('not_voted');
			//inject the updated vote count
			count = $(voteCount).text();
			$(voteCount).text(parseInt(count) + 1);

		} else {
			//update the state class
			$(voteButton).addClass('not_voted');
			$(voteButton).removeClass('voted');
			$(voteButton).parent('.-cont-vote').removeClass('voted');

			//inject the updated vote count
			count = $(voteCount).text();
			$(voteCount).text(parseInt(count) - 1);
		}
	}


 /**
 * getAllChecked
 * Get all the checked ideas id's
 */
 function getCheckedIdeas() {
 	var checkedIdeas = [];

 	$('._manageCheckBox:checked').each(function( index ){
 		checkedIdeas.push($(this).val());
 	});
	return checkedIdeas;
 }




 /**
 * saveIdea
 * Get all the checked ideas id's
 */
 function saveIdea() {
 	//save the idea
 	localStorage.setItem('ideaInfo', JSON.stringify(ideaInfo));
 }


 /**
 * isIdeaQueued
 * Check if an idea is saved in local storage and not published
 */
 function isIdeaQueued() {
 	if(localStorage.getItem('ideaInfo')) {
 		return true;
 	} else {
 		return false;
 	}
 }


 /**
	* createComment
	* @ comment (object): the comment object, contains required omment data
	* Create the new comment element and returns it;
	*/
 function createComment(comment) {
	/**
	Create html element with new comment to append to our comment feed
	*/
	var comment_html;

  var div = $(document.createElement("div"));



	if(comment.author_id !== window.userInfo.ID) {
		comment_html = '<div style="opacity:0" class="-comment -others _comment"><div class="-col-left"><a href="#" class="-profile-pic">';
		comment_html +=  '<img src="' + get_gravatar_md5(comment.email) + '"></a></div>';
		comment_html += '<div class="-col-right"><span class="-name">' + comment.author + '</span>';
	} else {
		comment_html = '<div style="opacity:0" class="-comment -myself _comment _commentNoDelete"><div class="-col-left"><a href="#" class="-profile-pic">';
		comment_html +=  '<img src="' + get_gravatar(window.userInfo.email, 80) + '"></a></div>';
		comment_html += '<div class="-col-right"><span class="-name">You&nbsp;&nbsp;&nbsp;&nbsp;Just now</span>';
	}

	//we need to split the string where there are new lines for formatting
	var splitted = comment.comment.split("\n");
	var commentStr = '';

	for(var i = 0; i < splitted.length; i++) {
		commentStr = commentStr + splitted[i];
		//dont add a break on the last item
		if(i !== splitted.length - 1) {
			commentStr = commentStr + '<br>';
		}
	}

	commentStr = linkifyStr(commentStr);
	//this is a bit of hack!
	//after using stringfy appending was plain text, not HTML. Need to revisit
	commentStr = decodeEntities(commentStr);

  comment_html += '<p class="-text">' + commentStr + '</p></div>';
  comment_html += '</div>';

  div.html(comment_html);

  return div;
 }

	/**
	* addCommentDelete
	* @ commentID (int): id of the comment
	* Once the comment has been created, add the delete button with the new comment ID
	*/
	function addCommentDelete(commentID) {
		$('._commentNoDelete .-name').append('<a href="#" class="-delete _deleteComment" data-comment-id="' + commentID + '"></a>');
		$('._commentNoDelete').removeClass('_commentNoDelete');
	}

	/**
	* updateCommentFeed
	* @ newCommentEl (element): id of the comment
	* Inject comment element into comment feed
	*/
	function updateCommentFeed(newCommentEl) {
		//inject our new comment
      $('._comp-comments ._inner-cont').append(newCommentEl);

      newComment = $('._comment:last-child');
      //only auto scroll down if the user is at the bottom of the page
	  	$('._comment:last-child').animate({
    		opacity: 1
    	}, 100);

	  	var $target = $('html,body');
    	$target.animate({scrollTop: $target.height()}, 1000);
	}

	function incrementCommentFeedCount() {
		var count = $('._commentCount').text();
		count++;
		$('._commentCount').text(count);
	}

	function decrementCommentFeedCount() {
		var count = $('._commentCount').text();
		count--;
		$('._commentCount').text(count);
	}

	function isMobile() {
	  var check = false;
	  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))check = true})(navigator.userAgent||navigator.vendor||window.opera); // jshint ignore:line
	  return check;
	}

	// jQuery and DOM ready
	$(function() {

		if(window.ideaListVisible) {
			$('._filterBar').show();
			$('.comp-ideaList-default').show();
			$('.pagination').show();
		} else {
			$('._showIdeaList').css('display', 'block');
		}

		$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		});

		if(localStorage.getItem('banner-' + window.userInfo.company) === null && !isUserAuthed()) {
			$('body').addClass('is-bannerVisible');
		}



		if(isMobile()) {
			$('body').addClass('no-touch');
		}

		//initialist DataTabl jQuery plugin
		$('#example').DataTable({
			"iDisplayLength": 20,
			"columnDefs": [
			  { targets: 'no-sort', orderable: false }
			],
			"order": [[ 5, "desc" ]]
		});

		$('#membersTable').DataTable({
			"iDisplayLength": 20,
			"columnDefs": [
			  { targets: 'no-sort', orderable: false }
			],
			"order": [[ 2, "desc" ]]
		});

		$('#categoriesTable').DataTable({
			"iDisplayLength": 20,
			"columnDefs": [
			  { targets: 'no-sort', orderable: false }
			],
			"order": [[ 0, "desc" ]]
		});

		$('#ideasTable').DataTable({
			"iDisplayLength": 20,
			"columnDefs": [
			  { targets: 'no-sort', orderable: false }
			],
			"order": [[ 4, "asc" ]]
		});

		//change style of DataTable search box
		$('.dataTables_filter input').attr('placeholder', 'Search');

		if(isIdeaQueued()) {
			var idea = JSON.parse(localStorage.getItem('ideaInfo'));
			publishIdea(idea.text, idea.category);
		}

		$('#comment_input').autogrow({vertical: true, horizontal: false});
		$('#idea_description').autogrow({vertical: true, horizontal: false});

		stupidCounter($('.form-wantoo'));


		var smallLogoVisible = false;
		var shadowVisible = false;
		//check if it starts fixed
		if($('._header').hasClass('l-header--isLogoSmall')) {
			smallLogoVisible = true;
			$(document).on('scroll', function(){
				if($(this).scrollTop() > 50 && !shadowVisible) {
					$('._header').addClass('l-header--isShowingShadow');
					shadowVisible = true;
				} else if($(this).scrollTop() < 50 && shadowVisible) {
					$('._header').removeClass('l-header--isShowingShadow');
					shadowVisible = false;
				}
			});
		} else {
			$(document).on('scroll', function(){
				if($(this).scrollTop() > 100 && !smallLogoVisible) {

					$('._header').addClass('l-header--isLogoSmall l-header--isShowingShadow');
					$('._headerBrand').addClass('isHidden');
					smallLogoVisible = true;
				} else if($(this).scrollTop() < 100 && smallLogoVisible) {
					$('._header').removeClass('l-header--isLogoSmall l-header--isShowingShadow');
					$('._headerBrand').removeClass('isHidden');
					smallLogoVisible = false;
				}
			});
		}

	});


	/**
	* Event listeners
	*/

	//listen for delegate vote events because of live search
	$('.comp-ideaList-search').on('click', '._vote', function(event){
		//prevent redirect to idea page
		event.preventDefault();

		var self = this;

		if(isUserAuthed()) {
			//get the idea id from HTML data
			var ideaID = $(self).data('id');
			var addVote = false;

			if($(self).hasClass('not_voted')) {
				addVote = true;
			} else if($(self).hasClass('voted')) {
				addVote = false;
			}

			//animate and send vote
			animateVote(self, addVote);
			sendVote(ideaID, addVote);
		} else {
			showLoginModal();
		}
	});

	// Button that votes for idea
	var voteButton = $("._vote");

	voteButton.on('click', function(event){
		//prevent redirect to idea page
		event.preventDefault();

		var self = this;

		if(isUserAuthed()) {
			//get the idea id from HTML data
			var ideaID = $(self).data('id');
			var addVote = false;

			if($(self).hasClass('not_voted')) {
				addVote = true;

				track('vote', {
					'source' : 'idea detail'
				})
			} else if($(self).hasClass('voted')) {
				addVote = false;

				track('unvote', {
					'source' : 'idea detail'
				})
			}

			//animate and send vote
			animateVote(self, addVote);
			sendVote(ideaID, addVote);
		} else {
			showLoginModal();
		}
	});


	// Form to add idea
 	var addIdeaFormInputs = $('#form-add-idea input, #form-add-idea textarea, #form-add-idea select');

	addIdeaFormInputs.focus(function(){
		if(!isUserAuthed()) {
			//show the login modal and don't submit form
			showLoginModal();
		}
	});


	//Bulk actions - delete
	var bulkActionDelete = $('._bulkActionDelete');

	bulkActionDelete.on('click', function(){
		//show bulk action delete modal
		$('#_modal-bulkActionsDelete').modal('show');

	});


	//Bulk actions - move
	var bulkActionMove = $('._bulkActionMove');

	bulkActionMove.on('click', function(){
		//show bulk action delete modal
		$('#_modal-bulkActionsMove').modal('show');
	});

	var bulkActionConfirmDelete = $('._bulkActionsConfirmDelete');

	bulkActionConfirmDelete.on('click', function(){

    //get the ideas to be deleted
		var checkedItems = getCheckedIdeas();

    //if the array is not empty, delete the ideas
    if(checkedItems.length >= 1) {
      $.ajax({
        method: "POST",
        url: '/' + userInfo.company + '/idea/delete/',
        data: JSON.stringify({
          ideas: checkedItems,
        })
      }).done(function (results) {
        //reload page so delete ideas are gone from table
        window.location.reload();
      });
    } else {
      alert('No ideas selected');
    }

	});


	var bulkActionConfirmMove = $('._bulkActionsConfirmMove');

	bulkActionConfirmMove.on('click', function(){

    //get the ideas to be deleted
		var checkedItems = getCheckedIdeas();
		var targetCat = $('#_targetCat').val();

    //if the array is not empty, delete the ideas
    if(checkedItems.length >= 1) {
      $.ajax({
        method: "POST",
        url: '/' + userInfo.company + '/idea/move/',
        data: JSON.stringify({
          ideas: checkedItems,
          category: targetCat
        })
      }).done(function (results) {
        //reload page so delete ideas are gone from table
        window.location.reload();
      });
    } else {
      alert('No ideas selected');
    }

	});

	var signUpFromModal = $('._signUpFromModal');

	signUpFromModal.on('click', function(){
		closeLoginModal();
		showSignupModal();
	});

	var loginFromModal = $('._loginFromModal');

	loginFromModal.on('click', function(){
		closeSignupModal();
		showLoginModal();
	});


	var yourIdea = $('._yourIdea');
	var ideaButtons = $('._addIdeaButtons');

	var firstFocus = true;
	var addButtonVisible = false;

	yourIdea.bind('paste', function(e){
		//stop people from pasting shit into our idea submission
		e.preventDefault();
		if(firstFocus) {
			track('add idea focused');

			$(this).html('');
			$(this).focus();
			firstFocus = false;
		}
		//max 70char limit, this is to make sure text stays formatted
		var content = striptags($(this).text() + e.originalEvent.clipboardData.getData('text')).slice(0, 70);
		$(this).empty().text(content);
	});


	yourIdea.on('click keypress', function(e){
		$('._showIdeaList').hide();
		if(firstFocus) {
			track('add idea focused');

			$(this).html('');
			$(this).focus();
			firstFocus = false;
		}

		if (isMobile) {
			//e.preventDefault();
			document.body.scrollTop = $('._yourIdea -highlight').offset.top;
		}

	});

	$('._yourIdea.-highlight').focus();

	yourIdea.on('focusout', function(){
		var self = this;

		//if the idea is empty on leaving focus, reset it
		if($(this).text().length <= 0) {
			if(window.ideaListVisible) {
				$('._filterBar').show();
				$('.comp-ideaList-default').show();
			} else {
				$('._showIdeaList').show();
			}

			//$(self).html('your idea');
			$(self).html('&nbspAdd your idea&nbsp');
			firstFocus = true;
		}

	});

	yourIdea.on('keydown', function(event){

		//prevent new lines, as it fucks everything up and allow delete
		//add length cap
		if(event.keyCode === 8 || event.keyCode === 46) {
			//do nothing
		}
		else if(event.keyCode === 13 || $(this).text().length >= 70) {
			event.preventDefault();
		}

	});

	yourIdea.on('keyup', function(){
		var self = this;
		//if over 5 characters show the buttons, if less hide them
		if($(this).text().trim().length >= 3 && !addButtonVisible) {
			//buttons are have hidden visibility to prevent click events, so make visible
			ideaButtons.css('visibility', 'visible');
			//animate opacity
			ideaButtons.css({opacity: 1});
			//update our flag
			addButtonVisible = true;
		} else if($(this).text().trim().length < 3 && addButtonVisible) {
			//animate opacity transition
			ideaButtons.css({opacity: 0});
			ideaButtons.css('visibility', 'hidden');
			//update our flag
			addButtonVisible = false;
		}
	});



	var addIdeaAddButton = $('._addIdeaAddButton');

	addIdeaAddButton.on('click', function(){
		var self = this;

		if($(self).hasClass('_step-1')) {

			ideaInfo.text = striptags($('._yourIdea').text());

			if(!window.userInfo.noCategories) {
				$(self).addClass('_step-2').removeClass('_step-1');
				$('._yourIdea-idea').fadeOut(function(){
					$('._yourIdea-category').fadeIn();
					$(self).text('Publish now');
				});
			} else {
				if(isUserAuthed()) {
					//publish idea
					publishIdea(ideaInfo.text, ideaInfo.category);
					$(self).attr('disabled', true);
					$(self).text('Publishing...');

				} else {
					saveIdea();
					showLoginModal();
				}
			}



		} else if($(self).hasClass('_step-2')) {
			if(isUserAuthed()) {
			//publish idea
			publishIdea(ideaInfo.text, ideaInfo.category);
			$(self).attr('disabled', true);
			$(self).text('Publishing...');

			} else {
				saveIdea();
				showLoginModal();
			}
		}
	});



	var categoryDropdownButton = $('._catDropdownButton');
	var categoryDropdownMenu = $('._catDropdownMenu');

	categoryDropdownButton.on('click', function(){
		var position = $(this).position();

		categoryDropdownMenu.css({
			left : position.left,
			top : position.top + 57
		});

		categoryDropdownMenu.show();
	});


	var categorySelect = $('._categorySelect');
	var currentSelected = $('._categorySelect:first');

	categorySelect.on('click', function(event){
		//stop anchor tag from auto scrolling to top
		event.preventDefault();

		currentSelected.removeClass('_active');
		$(this).addClass('_active');
		currentSelected = $(this);

		var clickedCat = $(this).data('cat');

		categoryDropdownMenu.hide();
		categoryDropdownButton.text(clickedCat);

		//store id for submission
		ideaInfo.category = $(this).data('id');

	});


	/**
	This is all of pile of shit. Scope of functionality grew.
	Needs refactoring.
	*/
	var addIdeaCancelButton = $('._addIdeaCancelButton');

	addIdeaCancelButton.on('click', function(){
		// window.location.reload();
		addIdeaAddButton.removeClass('_step-1 _step-2').addClass('_step-1');
		///yourIdea.html('your idea');
		yourIdea.html('&nbsp;Add your idea&nbsp');
		ideaButtons.css('visibility', 'hidden');
		addIdeaAddButton.text('Add idea');
		firstFocus = true;
		addButtonVisible = false;

		$.event.trigger({
      type: "liveSearchStarted",
      results: null,
      searchSource: 'ideaInput'
    });

		$('._allIdeasLink').show();
		$.event.trigger({
      type: "hideSoftLiveSearch"
    });

		$('._yourIdea-category').hide();
		$('._yourIdea-idea').show();

		currentSelected.removeClass('_active');
		$('._categorySelect:first').addClass('_active');
		ideaInfo.category = null;
		categoryDropdownButton.text('all ideas');

	});








	var ideaDescriptionInput = $('._ideaDescriptionInput');
	var saveButtonVisible = false;

	ideaDescriptionInput.on('keyup', function(){

		if($(this).val().length > 0 && !saveButtonVisible) {
			$('._descriptionButtons').fadeIn();
			saveButtonVisible = true;
		} else if($(this).val().length < 1 && saveButtonVisible) {
			$('._descriptionButtons').fadeOut();
			saveButtonVisible = false;
		}
	});


	var cancelMessage = $('._cancelMessage');

	cancelMessage.on('click', function(){
		$('._comment-text').val('');
		$('._comment-text').css('height', '40px');
		$('._commentButtons').fadeOut();
		sendButtonVisible = false;
	});


	var ideaDescriptionSave = $('._ideaDescriptionSave');

	ideaDescriptionSave.on('click', function(){
		var ideaID = $(this).data('idea-id');
		var text = striptags($('._ideaDescriptionInput').val());
		saveDescription(ideaID, text);
	});

	var cancelDescription = $('._cancelDescription');

	cancelDescription.on('click', function(){

		$('._ideaDescriptionInput').val('');
		$('._descriptionButtons').fadeOut();
		saveButtonVisible = false;
	});


	var sendMessage = $('._sendMessage');

	sendMessage.on('click', function(){
		$('._commentButtons').hide();
		$('._comment-text').css('height', '40px');
		sendButtonVisible = false;

		track('comment added');
	});


	var loginButtonNav = $('._loginButtonNav');

	loginButtonNav.on('click', function(){
		showLoginModal();
	});

	var signupButtonNav = $('._signupButtonNav');

	signupButtonNav.on('click', function(){
		showSignupModal();
	});


	var closeBannerButton = $('._closeBanner') ;

	closeBannerButton.on('click', function(){
		$('body').removeClass('is-bannerVisible');
		localStorage.setItem('banner-' + window.userInfo.company, true);
	});

	var joinCommunityButton = $('._joinCommunity');

	joinCommunityButton.on('click', function(){
		showSignupModal();
	});

	var selectAll = $('._selectAll');
	selectAll.on('click', function(){


		if($(this).prop('checked')) {
			$('._manageCheckBox').each(function(index, item){
				$(this).prop('checked', true);
			});
		} else {
			$('._manageCheckBox').each(function(index, item){
				$(this).prop('checked', false);
			});
		}


	});


	var checkBoxes = $('._checkIfChecked').on('click', function(){

		if(getCheckedIdeas().length > 0) {
			$('._bulkActionsBtn').prop('disabled', false);
		} else {
			$('._bulkActionsBtn').prop('disabled', true);
		}
	});

	$('._seeNotifications').on('click', function(){
		$(this).removeClass('is-unseen');
	});


	var targetComment;

	$('._comp-comments').on('click', '._deleteComment', function(){

		var commentID = $(this).data('comment-id');
		$('._confirmDelete').data('comment-id', commentID);
		showModal('_modal-deleteComment');

		targetComment = $(this).parents('.-comment');

		// deleteComment(commentID);
		// $(this).parents('.-comment').fadeOut(function(){
		// 	$(this).remove();
		// });

		return false;
	});


	var confirmDeleteButton = $('._confirmDelete');

	confirmDeleteButton.on('click', function(){
		closeModal('_modal-deleteComment');
		deleteComment($(this).data('comment-id'));
		targetComment.fadeOut(function(){
			$(this).remove();
		});
	});


	//prevent jQuery validate plugin from showing error messages
	//loop for multiple forms on page
	$('.form-validate').each(function(index, form){
		$(form).validate({ errorPlacement: function(error, element) {} });
	});

	$('.form-validate').on('keyup', function(){
		var self = this;


		//if valid, enalbed button. If not valid keep button disabled
		if($(this).valid()) {


			$(self).find('button[type="submit"]').prop('disabled', false);
		} else {
			if(!$(self).find('button[type="submit"]').prop('disabled')) {
				$(self).find('button[type="submit"]').prop('disabled', true);
			}
		}
	});

	$('.form-validate').on('change', function(){
		var self = this;


		//if valid, enalbed button. If not valid keep button disabled
		if($(this).valid()) {


			$(self).find('button[type="submit"]').prop('disabled', false);
		} else {
			if(!$(self).find('button[type="submit"]').prop('disabled')) {
				$(self).find('button[type="submit"]').prop('disabled', true);
			}
		}
	});

	$('#submit_model_login').click( function(e) {
		e.preventDefault();
		var check = $('#id_full_name').val().split(' ').length;
		if (check >= 2)
			$('#signup_form').submit();
		else {
			$('#msg-full-name').fadeIn(1000);
			setTimeout(function(){
				$('#msg-full-name').fadeOut(2000);
			},2000)
		}
	});


	/********************/
	/*    Commenting    */
	/********************/

	var commentText = $('._comment-text');
	var sendButtonVisible = false;

	commentText.on('keyup', function(){

		//when the comment is above a certain length show the send button
		if($(this).val().length > 0 && !sendButtonVisible) {
			$('._commentButtons').fadeIn();
			sendButtonVisible = true;
		} else if($(this).val().length < 1 && sendButtonVisible) {
			$('._commentButtons').fadeOut();
			sendButtonVisible = false;
		}
	});

	/**
	We use Pusher to handle live comments.
	Set up our instance here.
	*/
	var idea_id = window.userInfo.ideaID;
  var pusher = new Pusher('8d396c4a64f32d61c897', {
    encrypted: true
  });
  var newComment;
  var channel = pusher.subscribe('idea_'+ window.userInfo.ideaID);

  //listen for new comments
  channel.bind('new_comment', function(comment) {




  		if(comment.author_id === window.userInfo.ID) {
  			addCommentDelete(comment.id);
  		} else {
  			var div = createComment(comment);
  			incrementCommentFeedCount();
  			//inject our new comment
	      $('._comp-comments ._inner-cont').append(div);
	      updateCommentFeed(div);
  		}

  });


	$('._comment-text').focus(function(){
		//we don't want people to comment if not authed
		if(!isUserAuthed()) {
			showLoginModal();
		}
	});

	$('._sendMessage').on('click', function(){

		if(isUserAuthed()) {
			var csrftoken = getCookie('csrftoken');
    	var commentStr = striptags($('._comment-text').val());
    	$('._comment-text').val('');

    	var comment = {};
    	comment.comment = commentStr;
    	comment.author_id = window.userInfo.ID;
    	comment.email = window.userInfo.email;

    	var div = createComment(comment);
    	incrementCommentFeedCount();

    	updateCommentFeed(div);

    	//check if there is a message to send and check its not just spaces
    	if(commentStr.length > 0 && commentStr.replace(/\s/g, '').length) {
    		$.ajax({
					method: "POST",
					url: '/api/v1/' + window.userInfo.company + '/ideas/' + window.userInfo.ideaID + '/comments/',
					data: {
				    comment: commentStr,
				    csrftoken: csrftoken
					}
				}).done(function (results) {
					/**
					When we have the id of the newly created comment, update our
				 	delete button, so delete will actually work.
				 	*/
					var deleteButton = newComment.find('._deleteComment');
					$(deleteButton).attr('data-comment-id', results.id);
				});
    	}
		} else {
			showLoginModal();
		}
  });


	var mobileSearchBtn = $('._showMobileSearch');
	var notVisible = true;
	mobileSearchBtn.on('click', function(){

		if(notVisible) {
			$('._searchBar').fadeIn();
			notVisible = false;
		} else {
			$('._searchBar').fadeOut();
			notVisible = true;
		}

	});

	var showIdeaList = $('._showIdeaList');
	showIdeaList.on('click', function(){
		showIdeaList.fadeOut(function(){
			window.ideaListVisible = true;
			 $('._filterBar').show();
       $('.comp-ideaList-default').show();
       $('.pagination').show();
		});

		return false;
	});

	var notificationsMenuButton = $('._toggleNotificationPreview');
	notificationsMenuButton.on('click', function(){
		event.stopPropagation();
		$.event.trigger({
      type: "notificationsPreviewToggled"
    });

	});

	//when the singup with email option is clicked, signup email form
	var signupOrEmail = $('._signupOrEmail');
	signupOrEmail.on('click', function(){
		$('#_modal-newSignup').addClass('-showEmail');
	});

	//when the signup modal is closed, reset the state back
	$('#_modal-newSignup').on('hide.bs.modal', function(){
		$('#_modal-newSignup').removeClass('-showEmail');
	});

	var searchInput = $('._searchInput');

	var firstKeyUp = true;
	searchInput.on('keyup', function(){
		if(firstKeyUp) {
			track('search input focused');
			firstKeyUp = false;
		}
	});

	var filterOption = $('._filterOption');

	filterOption.on('click', function(){
		track('filter option clicked');
	});

	var shareOption = $('._shareOption');

	shareOption.on('click', function(){
		track('share option clicked', {
			'source' : 'idea detail'
		});
	});


	var loginDashboard = $('#login_dashboard');

	loginDashboard.on('click', function(){
		mixpanel.track('login clicked', {
			"source" : "dashboard"
		});
	});

	var signupDashboard = $('#signup_dashboard');

	signupDashboard.on('click', function(){
		mixpanel.track('signup clicked', {
			"source" : "dashboard"
		});
	});

	var chartToggle = $('._toggleCharts');

	chartToggle.on('click', function(){
		if(!$('._chartToggle').hasClass('is-voteChartVisible')) {
			$('._chartToggle').addClass('is-voteChartVisible');
			$('._toggle-buttons-cont').addClass('is-voteChartVisible');
		} else {
			$('._chartToggle').removeClass('is-voteChartVisible');
			$('._toggle-buttons-cont').removeClass('is-voteChartVisible');
		}

	});

	var confirmIdeaMerge = $('._confirmIdeaMerge');

	confirmIdeaMerge.on('click', function(){
		$('#mergeIdeaForm').submit();
	});


	var addIdeaNavBtn = $('._addIdeaNavBtn');

	addIdeaNavBtn.on('click', function(){
		var windowWidth = $(window).width();
		track('add idea in main nav clicked');
		window.location.pathname = `/${ window.userInfo.company }/`;
	});

	var searchNavBtn = $('._searchNavBtn');

	searchNavBtn.on('click', function(){
		$('._mobileSearch').fadeIn();
	});

	var closeMobileSearch = $('._closeMobileSearch');
	closeMobileSearch.on('click', function(){
		$('._mobileSearch').fadeOut();
	});

	//Clicking outside notification dropdown closes it
	$('body').bind("click", function(event){
		$.event.trigger({
      type: "notificationsClose",
    });
	});

	var singleDelete = $('._bulkActionsConfirmSingleDelete');
	singleDelete.on('click', function(event){

		var ideaID = $(event.target).data('ideaid')
		var endpoint = '/' + window.userInfo.company + '/delete-idea/';
		$.ajax({
			method: "POST",
			url: endpoint,
			data: {
		     idea_id: ideaID
			}
		}).done(function (results) {

			 window.location = '/' + window.userInfo.company  + '/ideas/';

		});
	});

	var deleteCategory = $('._bulkActionsConfirmDeleteCategory');
	deleteCategory.on('click', function(event){

		var catID = $(event.target).data('catid')
		var endpoint = '/' + window.userInfo.company + '/delete-category/';
		$.ajax({
			method: "POST",
			url: endpoint,
			data: {
		     category_id: catID
			}
		}).done(function (results) {

			 window.location = '/' + window.userInfo.company  + '/manage/categories/';

		});
	});

	/*#############################################*/

	$('#sendProEmail').on('click' ,function(){
		track('Pro Request Button clicked on modal');
		var endpoint = '/api/v1/' + window.userInfo.company + '/sendmail/';
		$.ajax({
			method: "POST",
			url: endpoint,
			data: {
		     company: window.userInfo.company,
		     email: window.userInfo.email
			}
		}).done(function (results) {

			 console.log(results);

		});
	});

	$('#user-home-page').attr('href', '/'+window.userInfo.companyName+'/');
	$('#user-invite-others').attr('href', "mailto:?subject="+window.userInfo.companyName+" wants your idea. &body="+window.userInfo.companyName+" has launched an Idea Board to hear from people like you.%0D%0A%0D%0AMake your voice heard, and add your ideas here: http://wantoo.io/"+window.userInfo.company);

	//focus on real input instead of imitation input
	$('.twitter-search__searchbar').on('click', function(e){
		if (this.isEqualNode(e.target)) {
			$('.twitter-search__text-enter').focus();
		}
	});

	$('.twitter-search__text-enter').on('keydown keyup focusout', function(e) {
		var size = $(this).val().length;
		$(this).attr('size', size > 0 ? size+5 : 27);
		if ( (e.type == 'focusout' || (e.type == 'keydown' && (e.keyCode == 13 || e.keyCode == 32))) && $(this).val().trim().length !== 0 ) {
			e.preventDefault();
			addKeyword($(this).val());
			$(this).val('');
			size = 0;
		}
	});

	$('.keyword__wrapper').on('click', '.key-close', function() {
		var parent = $(this).parents('.keyword');
		var re = new RegExp('\\s*' + parent.text().slice( 1 ));
		$('.twitter-search__input').val($('.twitter-search__input').val().replace(re, ''));
		parent.remove();
	});

	function addKeyword(word) {
		var keyword = '<span class="keyword"><span class="keyword-wrap">'
					 + '<span class="key-close">X</span>' + word.trim()
					 + '</span></span>';
		var val = $('.twitter-search__input').val() + ' ';
		if (val.trim().length === 0)
			val = '';
		$('.keyword__wrapper').append(keyword);
		var re = new RegExp('\\s*' + word);
		if (val.match(re) == null) {
			$('.twitter-search__input').val(val + word);
		}
	}

	function saveKeyword(word) {
		localStorage.setItem('wantoo_twitter_keywords', word);
	}

	//localStorage.setItem("lastname", "Smith");
	$('.twitter-search').submit(function(e) {
		e.preventDefault();

		// console.log('SET keywords: ');
		// console.log(localStorage.getItem('wantoo_twitter_keywords'));

		saveKeyword($('.twitter-search__input').val());

		this.submit();
	});

	if ($('.twitter-search__input').length) {

		// console.log('GET keywords: ');
		// console.log(localStorage.getItem('wantoo_twitter_keywords'));

		var inputs;
		if (localStorage.length > 0)
			inputs = localStorage.getItem('wantoo_twitter_keywords');
		else
			inputs = $('.twitter-search__input').val();
		inputs = inputs.split(' ');
		$('.twitter-search__input').val('');
		for (var i=0; i<inputs.length; i++)
			if (inputs[i].trim().length > 0)
				addKeyword(inputs[i].trim());
	}

}(window.jQuery, window, document, window.jQuery.fn.DataTable, window.userInfo));
// pass global objects