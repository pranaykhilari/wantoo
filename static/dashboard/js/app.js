'use strict';


/**
* Pro tip:
*
* React is different than jQuery. With jQuery, you write lots of code explaining how to transform the user 
* interface of your application from one complicated state (that you might never have anticipated happening) 
* to another complicated state. 
*
* When using React.js you don't write code about how your application's visible state changes -- 
* instead you write code to answer the question: "given this state, what should the application look like".
*/

import React from 'react';
import ReactDOM from 'react-dom';
import { IdeaList } from './components/ideaList/_ideaList';
import { NotificationList } from './components/_notificationList';
import { Merge } from './components/merge/_merge';

//suppress target DOM error - temp fix
try {

	var isHomePage =  false, isIdeaList = false;
	if(window.location.pathname == ('/' + window.userInfo.company + '/')) {
		isHomePage = true;
	}
	if(window.location.pathname == ('/' + window.userInfo.company + '/manage/feedback/')) {
		isHomePage = true;
	}
	if (window.location.pathname == '/' + window.userInfo.company + '/ideas/') {
 		isIdeaList = true;
 	}

	ReactDOM.render(
		<IdeaList isHomePage={ isHomePage } isIdeaList={ isIdeaList } />,
		document.getElementById('ideaList')
	);
} catch(error) {
	console.log(error);
}	

try {
	ReactDOM.render(
		<NotificationList />,
		document.getElementById('notificationList')
	);
}
catch (error) {
	console.log(error);
}

try {
	ReactDOM.render(
		<Merge />,
		document.getElementById('merge')
	);
}
catch (error) {
	console.log(error);
}

