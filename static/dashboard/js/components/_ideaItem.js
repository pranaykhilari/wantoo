'use strict';

/**
The properties passed into this React component come from 2 sources.
1. Django when the page first loads (if there are ideas on the page)
2. When live searching, Algolia search results are passed into this component
and it re-renders based on those results
Because the data return by Algolia differs from the data returned from Django, this
component has to be able to handle both cases.
The object passed into this object is created in base.html (app.ideas) and in ideaList.js
when Algolia search results are returned. Both objects have the following data structure:
//Django
idea. ->
	.idea_id
	.title
	.category
	.category_id
	.vote_count
	.comment_count
	.status
	.status.id
	.status.title
	.status.color
	.last_activity
	.last_activity.action
	.last_activity.user
	.last_activity.user.id
	.last_activity.user.gravatar_url
	.last_activity.user.first_name
	.last_activity.created_at
//Algolia search results
idea. ->
	.idea_id
	.title
	.category
	.category_id 
	.vote_count
	.comment_count
	.status
	.status.id
	.status.title
	.status.color
	.last_activity
	.last_activity.action
	.last_activity.user
	.last_activity.user.id
	.last_activity.user.gravatar_url
	.last_activity.user.first_name
	.last_activity.created_at
//In Django but not Algolia search results
.voted
*/

import React from 'react';
import classNames from 'classnames';
import { track } from '../tracking';
import { isUserAuthed } from '../helper';
import { showModal } from '../helper';
import { api_vote } from '../API';

export class IdeaItem extends React.Component {

	constructor (props) {
		super(props);
		this.state = {
			voted: this.props.idea.voted == 'not_voted' ? false : true,
			vote_count: this.props.idea.vote_count
		};
	}

	/**
	* vote
	* Update state, vote count and send vote
	*/
	_vote () {
		if(isUserAuthed()) {
			//update our state to show the different button state
			this.setState({voted: !this.state.voted});

			var newVoteCount = this.state.vote_count;
			//increment/decrement vote count
			if(this.state.voted) {
				newVoteCount = newVoteCount - 1;
				this.setState({vote_count: newVoteCount});
				track('unvote clicked', {
					'source': 'idea list'
				});	
			} else {
				newVoteCount = newVoteCount + 1;
				this.setState({vote_count: newVoteCount});
				track('vote clicked', {
					'source': 'idea list'
				});		
			}
			
			//send our vote
			api_vote(this.props.idea.idea_id, this.state.voted); 
		} else {
			showModal('_modal-login');
		}
	}


	/**
	* createUrls
	* Create all the required urls and return object
	*/
	_createUrls () {
		var urls = {};

		//set up all the urls required
		urls.idea = '/' + this.props.idea.idea_id + '/';
		urls.category = '/';
		urls.status = '/' + window.userInfo.company + '/ideas/?status=' + this.props.idea.status.id;

		console.log("props...");
		console.log(this.props.idea);

		//member details are not returned from live search results
		urls.member = '/' + window.userInfo.company + '/member/' + this.props.idea.last_activity.user.id + '/'; 
		urls.created_by = '/' + window.userInfo.company + '/member/' + this.props.idea.created_by.id + '/';	
		
		//fall back for no category
		if( this.props.idea.category_id != null ) {
			urls.category = '/' + window.userInfo.company + '/category/' + this.props.idea.category_id + '/';
		} else {
			urls.category = '/';
		}

		return urls;
	}

	render () {

		var self = this;

		var urls = this._createUrls();

		//custom label colors
		var statusStyle = {
		  backgroundColor: '#' + this.props.idea.status.color
		};

		var voteButtonClasses = classNames({
			'-cont-vote': true,
			'voted': this.state.voted,
			'not_voted': !this.state.voted
		});

		var supporters = [];
		if (this.props.idea.voted_users) {
			var len = this.props.idea.voted_users.id.length;
			for (var i=0; i < len; i++) {
				urls.voted_by = '/'+ window.userInfo.company + '/member/' + this.props.idea.voted_users.id[i] + '/';
				console.log(urls.voted_by);
				if (urls.voted_by !== urls.created_by)
					supporters.push(<a href={ urls.voted_by } key={ this.props.idea.voted_users.id[i] } onClick={ track.bind(this, 'member clicked', {'source':'idea list'}) } className="-profile-link"><img className="-profile-pic -profile-left" src= { this.props.idea.voted_users.gravatar_url[i] } /></a>);
			}
		}
		
    return (
			<div className="-idea">
        <div className="-col-vote">
            <div className={ voteButtonClasses }>
                <h3 className="-score _vote-count">{ this.state.vote_count }</h3>
                <button onClick={this._vote.bind(this)}  className="-btn-vote" data-id={ this.props.idea.idea_id }>want</button>
            </div>
        </div>
        <div className="-col-info">
            <div className="-cont-info">
                <a href={ urls.idea } onClick={ track.bind(this, 'idea title clicked', {'source':'idea list'}) } className="-title">{ this.props.idea.title }</a>
                <div className="-activity">
                    <span className="-recent">
									    <span>
									    <a href={ urls.created_by } onClick={ track.bind(this, 'member clicked', {'source':'idea list'}) }  className="-profile-link">
									    	<img className="-profile-pic" src={ this.props.idea.created_by.gravatar_url } alt="" />
									    	{ /*this.props.idea.last_activity.user.first_name*/ }
									    </a>

									    { supporters }

									    {/*(() => {
								        switch (this.props.idea.last_activity.action) {
								          case 'idea_submitted':   return ' added the idea ';
								          case 'idea_wanted':   return ' wants the idea ';
								          case 'comment_added': return ' commented on the idea ';
								          case 'status_changed':  return this.props.idea.status.title == 'None' ? ' updated the status ' : ' updated status to ' + this.props.idea.status.title + ' ';
								          default:      return ' wants the ideas ';
								        }
								      	})()*/} 
									    </span>
                    </span>
                    <a href={ urls.idea } onClick={ track.bind(this, 'comments clicked', {'source':'idea list'}) } ><span className="-comments">+ { this.props.idea.comment_count } comments</span></a>
                    {/* <a href={ urls.category } onClick={ track.bind(this, 'category clicked', {'source':'idea list'}) } className="-category">{ this.props.idea.category == "None" ? 'All ideas' : this.props.idea.category }</a> */}
					<a href={ urls.status } style={ statusStyle } className="-status-badge">{ this.props.idea.status.title }</a>
                </div>
            </div>
        </div>
        <div className="-col-vote-small">
            <div className={ voteButtonClasses }>
                <h3 className="-score _vote-count">{ this.state.vote_count } votes</h3>
                <button onClick={this._vote.bind(this)} className="-btn-vote" data-id={ this.props.idea.idea_id }>want</button>
            </div>
        </div>
    	</div>
    );
  }
}