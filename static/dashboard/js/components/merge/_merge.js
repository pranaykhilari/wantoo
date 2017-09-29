'use strict';

/**

UI states:

- default (empty): its starting state
- searching: displaying results from search
- selected: after result idea selected

*/

import React from 'react';
import classNames from 'classnames';
import { algolia_search } from '../../API';
//import './_merge.styl'; 

export class Merge extends React.Component {

	constructor (props) {
		super(props);

		this.state = {
			currentState: 'default',
			searchResults: []
		};

		this.selectedIdeaID = '';
		this.selectedIdeaTitle = '';

		//function bindings
		this._handleChange = this._handleChange.bind(this);
		this._loadSearchResults = this._loadSearchResults.bind(this);
		this._selectIdea = this._selectIdea.bind(this);
		this._clearSelectedIdea = this._clearSelectedIdea.bind(this);
		this._showConfirmModal = this._showConfirmModal.bind(this);
	}

	_handleChange (event) {
		var self = this;

		if(event.target.value.length > 0) {
			algolia_search(event.target.value).then(function(results){
				self._loadSearchResults(results);
			});
		} else {
			this.setState({searchResults : []});
		}
	}

	_clearSelectedIdea () {
		this.selectedIdeaID = '';
		this.selectedIdeaTitle = '';
		this.setState({currentState : 'default'});
	}

	_selectIdea (event) {
		this.selectedIdeaID = $(event.target).data('id');
		this.selectedIdeaTitle = $(event.target).data('title');
		this.setState({currentState : 'selected'});
	}


	_showConfirmModal () {
		$('#_modal-mergeIdea').modal('show');
	}

	_loadSearchResults (results) {
		var searchResults = [];

		for(var i = 0; i < results.hits.length; i++) {

			//make sure the results don't show the selected merge idea as a merge option
			if(results.hits[i].objectID != window.mergeIdeaID) {
				var statusStyle = {
					background : results.hits[i].status_color ? '#' + results.hits[i].status_color : '#fff'
				}

				searchResults.push(
					<div className="comp-merge__result-item" key={ results.hits[i].objectID  }>
						<button className="comp-merge__result-item__btn-select" onClick={this._selectIdea} data-id={ results.hits[i].objectID } data-title={ results.hits[i].title }>Select</button>
						<div className="comp-merge__result-item__info">
							<h3 className="comp-merge__result-item__title">{ results.hits[i].title } <span style={ statusStyle } className="comp-merge__status">{ results.hits[i].status }</span></h3>
							<p className="comp-merge__result-item__meta"> { results.hits[i].vote_count } wants, { results.hits[i].comment_count } comments</p>
						</div>
					</div>
				);
			}
			
		}

		this.setState({searchResults : searchResults});
	}

	render () {

		var self = this;

		var mergeClasses = classNames({
			'comp-merge' : true,
			'is-default' : this.state.currentState == 'default' ? true : false,
			'is-selected' : this.state.currentState == 'selected' ? true : false
		});
		
    return (
			<div className={ mergeClasses }>
				<h2 className="comp-merge__main-title">Merge idea</h2>
				<p className="comp-merge__info">You are about to merge this idea, so voting and commenting will be closed.</p>
				<div className="comp-merge__selected-item">
					<h3 className="comp-merge__selected-item__title">{ window.mergeIdeaTitle }</h3>
				</div>
        <h2 className="comp-merge__sub-title">Merge with:</h2>
        <p className="comp-merge__info">Supporters and votes will be transferred to this idea. Comments will not be merged.</p>
        <div className="comp-merge__search-cont">
        	<input className="comp-merge__search" onChange={this._handleChange} type="text" placeholder="Search ideas to merge with..." />
	        <div className="comp-merge__search-results">
	        	{ this.state.searchResults }
	        </div>
        </div>
        <div className="comp-merge__selected-cont">
        	<div className="comp-merge__selected-item">
        		<h3 className="comp-merge__selected-item__title">{ this.selectedIdeaTitle }</h3>
        	</div>
        	<a href="#" className="comp-merge__btn-clear" onClick={ this._clearSelectedIdea }><img src="/static/dashboard/img/icons/icon_cross_merge.png" /></a>
        	<form id="mergeIdeaForm" className="comp-merge__controls" method="POST" action=".">
	        	<input type="hidden" name="merge_into_id" value={ this.selectedIdeaID } />
	        	<div dangerouslySetInnerHTML={{__html: window.token }}></div>
	        	<a href="#" className="btn-fill-primary" onClick={ this._showConfirmModal }>Merge</a>
	        	<a href="#" className="btn-fill-transparent" onClick={ this._clearSelectedIdea }>Cancel</a>
	        </form>
        </div>
    	</div>
    );
  }
}


