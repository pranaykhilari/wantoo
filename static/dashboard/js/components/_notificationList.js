'use strict';

/*

States:
- addCategory
	-- show category selection
- showButtons
	-- ready to submit

Minimal (but complete) UI representation
- new idea text
- category array

*/

/*

UI States

- Empty
	if no notifications after fetch

- Fetching
	getting notifications

- Full
	showing notifications

- Visible
	wheter should be hidden or not (dependent on external click)

Behaviour

- onclick
		if no notifications
			if first call
				make call
				update based on results
			
			else
				make call
				update if necessary

		if notifications
			make call
			update if necessary	

*/

import React from 'react';
import classNames from 'classnames';
import { createMarkup } from '../helper';
import { getNotifications } from '../API';
import { clearNotifications } from '../API';
import { track } from '../tracking';

export class NotificationList extends React.Component {

	constructor (props) {
		super(props);

		this.notifications = [];
		this.isVisible = false;

		this.state = {
			display: 'empty',
			isVisible: false
		};
	}


	_toggleNotifications () {
		if(this.state.isVisible) {
			this.setState({ isVisible : false });
		} else {
			track('notifications preview opened');
			this.setState({ isVisible : true });
			this._checkNotifications();

			/** 
			Clear the notifications on open, but wait a second before making the request, because a
			a request is already made straigh away to get the new notifications.
			Just prevents to requests being made at the same time
			*/
			setTimeout(function(){ 
				clearNotifications();
			}, 1000);
		}
	}

	_checkNotifications () {
		var self = this;	
	
		getNotifications().done(function(results){
			self.notifications = Object.keys(results).map(key => results[key])

			if(self.notifications.length <= 0) {
				self.setState({ display : 'empty'});
			} else {
				self.setState({ display : 'full'});
			}
			
		});
	}

	componentDidMount () {
		var self = this;
		$(document).on("notificationsPreviewToggled", function(event){
			self._toggleNotifications();
		});

		$(document).on("notificationsClose", function(event){
			if(self.state.isVisible) {
				self.setState({isVisible : false});
			}
		});
	}

	render () {
		
		var seeAllUrl = '/' + window.userInfo.company + '/notifications/';

		var classes = classNames({
			'dropdown-menu' : true,
			'mainNav__dropdown' : true,
			'comp-notificationsPreview' : true,
			'isVisible' : this.state.isVisible,
			'isEmpty': this.state.display === 'empty' ? true : false
		});

    return (
			<div className={ classes } aria-labelledby="dropdownMenu1">
				<ul className="-inner-scrollable">
					{this.notifications.map(function(notification, key){
						
						var notificationClasses = classNames({
							'-notification-item' : true,
							'-is-unseen' : !notification.seen
						});

						var url = '/' + notification.idea_id + '/';

						var action;

						switch(notification.action) {
							case 'comment_added':
								if(notification.own_idea) {
									action = 'commented on your idea "<span class="comp-notificationsPreview__idea-title">' + notification.idea_title + '</span>"';
								} else {
								 action = 'commented on the idea "<span class="comp-notificationsPreview__idea-title">' + notification.idea_title + '</span>"';
								}
								break;
						  	
							case 'status_changed':
						    action = 'updated status to ' + notification.status_title + ' for the idea \"' + notification.idea_title + '\"';
						    break;

						  case 'idea_submitted':
						    action = 'added an idea "<span class="comp-notificationsPreview__idea-title">' + notification.idea_title + '</span>"';
						    break;  

						  case 'idea_wanted':
						    action = 'wants your idea "<span class="comp-notificationsPreview__idea-title">' + notification.idea_title + '</span>"';
						    break;  
						    
						 	default:
						 		action = '';
						}

						var notificationText = '<span class="comp-notificationsPreview__name">' + notification.user_full_name + '</span> ' + action + '<br /><span className="-time">' + notification.timesince + '</span></p>'; 

						return (
							<li key={ key } className={ notificationClasses }>
								<a href={ url }>
									<img className="-user-pic" src={ notification.avatar } alt="Avatar" />
										<p className="-description" dangerouslySetInnerHTML={ createMarkup(notificationText) }></p>
								</a>
							</li>	
						)
					})}

					<p className="-empty-message">No notifications yet.</p>								
				</ul>
				<a href={ seeAllUrl } className="-btn-all-notifications">See all notifications</a>
		  </div>
    );
  }
}


