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

import React from 'react';
import classNames from 'classnames';
import { IdeaItem } from '../_ideaItem';
import { getUrlParameter } from '../../helper';
import { checkUrlParameterExists } from '../../helper';
//import './_ideaList.styl';


export class IdeaList extends React.Component {

	constructor (props) {
		super(props);

		this.newArray = [];
		this.searchSource = '';
		this.searchTerm = '';
		this.searchResults = false;
		
		this.state = {
			initialIdeas: app.ideas,
			currentIdeas: [],
		}
	}

	liveSearchResultsUpdate (results, searchSource, searchTerm) {

		this.newArray = [];
		var idea = [];
		this.searchResults = true;

		//check if the search is coming from the search input of the idea submission
		this.searchSource = searchSource;
		this.searchTerm = searchTerm;

		//if we have hits, hide shit and show results
		if(results && results.hits.length > 0) {

			for(var i = 0; i < results.hits.length; i++) {
				idea[i] = {};
				//jQuery hack to replace HTML special characters
				idea[i].title = $("<div />").html(results.hits[i].title).text();
				idea[i].idea_id = results.hits[i].objectID;
				idea[i].vote_count = results.hits[i].vote_count;
				idea[i].comment_count = results.hits[i].comment_count;
					
				//if no category, set fallback to 'None' - if not 'All ideas' wont be rendered
				if(results.hits[i].category) {
					idea[i].category = results.hits[i].category;	
				} else {
					idea[i].category = 'None';
				}
				
				idea[i].category_id = results.hits[i].category_id;
				idea[i].status = {};
				idea[i].status.id = results.hits[i].status_id;
				idea[i].status.title = results.hits[i].status;
				idea[i].status.color = results.hits[i].status_color;
				idea[i].voted = 'not_voted';

				// console.log('search, idea votes='+results.hits[i].idea_votes);
				// console.log('search, idea votes='+results.hits[i].idea_votes);

				idea[i].created_by = {};
				idea[i].created_by.id = results.hits[i].created_by_id;
				idea[i].created_by.gravatar_url = results.hits[i].created_by_avatar;

				idea[i].last_activity = {};
				idea[i].last_activity.action = results.hits[i].last_activity_action;
				idea[i].last_activity.user = {};
				idea[i].last_activity.user.id = results.hits[i].last_activity_user_id;
				idea[i].last_activity.user.first_name = results.hits[i].last_activity_user;
				idea[i].last_activity.user.gravatar_url = results.hits[i].last_activity_avatar;

				for(var y = 0; y < window.voted_ideas.length; y++) {
					if(idea[i].idea_id == window.voted_ideas[y]) {
						idea[i].voted = 'voted';
					}
				}

				this.newArray.push(<IdeaItem key={ i } idea={ idea[i] } isSearchResult={true} />);
			}


			//trigger for render
			//clear the array completely first
			//we want to recreate it so the contructor class is called on our new idea item component
			this.setState({currentIdeas: []});
			this.setState({currentIdeas: this.newArray});
		} else {

			if(searchSource == 'searchInput') {
				if(searchTerm.length <= 0) {
					this.searchResults = false;
					this._loadIdeas();
				} else {
					//trigger for render
					//clear the array completely first
					//we want to recreate it so the contructor class is called on our new idea item component
					this.setState({currentIdeas: []});
					this.setState({currentIdeas: this.newArray});		
				}
			} else {
				//trigger for render
				//clear the array completely first
				//we want to recreate it so the contructor class is called on our new idea item component
				this.setState({currentIdeas: []});
				this.setState({currentIdeas: this.newArray});
			}
			
		}
	}

	componentWillMount () {
		var self = this;
		
		this._loadIdeas();
	}

	componentDidMount () {
		var self = this;

		$(document).on("liveSearchStarted", function(event){
			self.liveSearchResultsUpdate(event.results, event.searchSource, event.searchTerm);
		});

		$(document).on("liveSearchEnded", function(event){
			self._loadIdeas();
		});
	}

	_hideUIElements () {
		
		if(this.searchSource === 'searchInput') {

			if(this.props.isHomePage) {
				$('._hideOnLiveSearch').hide();
			}
			
			$('.pagination.pagination-centered, ._idea-count').hide();
			$('._filterBar').hide();
		}
	}

	_showUIElements() {
		if(this.searchSource === 'searchInput') {

			if(this.props.isHomePage) {
				$('._hideOnLiveSearch').show();
			}	
			
			$('._header').removeClass('l-header--isLogoSmall');
			$('.pagination.pagination-centered, ._idea-count').show();
			$('._filterBar').show();	
		}
	}

	_loadIdeas () {
		//copy array
		this.newArray = [];

		//load all the initial ideas from Django into our current ideas to display
		for(var i = 0; i < this.state.initialIdeas.length; i++) {
			this.newArray.push(<IdeaItem key={i} idea={this.state.initialIdeas[i]} isSearchResult={false} />);
		}

		//trigger for render
		//clear the array completely first
		//we want to recreate it so the contructor class is called on our new idea item component
		this.setState({currentIdeas: []});
		this.setState({currentIdeas: this.newArray});
	}

	render () {
		var self = this;


		var liveSearchLayout, ideaLiveSearchLayout, showNoResultsMsg = false;
		var isHidden;
		var resultsMsg = 'No ideas found. Check the spelling or try different keywords.';

		if(this.props.isHomePage) {
			isHidden = true;
		} else {
			isHidden = false;
		}

		//check if the results are search results
		if(this.searchResults) {
				
			//by default the list component is hidden on the home page, so unhide it	
			if(this.props.isHomePage) {
				// isHidden = false;
			}

			//check the source of the live search and display the right layout
			if(this.searchSource === 'searchInput') {
				liveSearchLayout = true;
				isHidden = false;
			} else if (this.searchSource === 'ideaInput') {
				ideaLiveSearchLayout = true;
			}

			//if we have no results and are on the live search, show the no results message
			if((this.state.currentIdeas.length <= 0) && liveSearchLayout) {
				if(this.searchTerm.length <= 0) {
					//end search
					liveSearchLayout = false;
				} else {
					showNoResultsMsg = true;
				}
			}

			if(this.state.currentIdeas.length > 0 && ideaLiveSearchLayout) {
				isHidden = false;
			}

		} else {
			console.log(this.state.currentIdeas.length);
			if(!this.props.isHomePage) {
				if(this.state.currentIdeas.length <= 0) {

					if(this.props.isIdeaList) {
						resultsMsg = "No Ideas have been added yet!";
						isHidden = false;
						showNoResultsMsg = true;
						if ( window.userInfo.company )
							$('#_modal-Summary').modal('show');
					}

					//all filter strings have status in the URL
					// if(checkUrlParameterExists('status')) {
					// 	isHidden = false;
					// 	showNoResultsMsg = true;
					// }
					
					//if status param has a value then show the message below
					if(getUrlParameter('status')) {
						resultsMsg = "No ideas found with this status. Choose a different status.";
					}
				}

			}
			
		}

		var ideaListClasses = classNames({
			'comp-ideaList' : true,
			'isHidden': isHidden,
			'comp-ideaList--ideaInputLiveSearch': ideaLiveSearchLayout,
			'comp-ideaList--liveSearch': liveSearchLayout,
			'is-empty': showNoResultsMsg
		});
		
    return (
      <div className={ ideaListClasses }>
      	<h2 className="comp-ideaList__searchInfo">{ this.state.currentIdeas.length } ideas match <span className="comp-ideaList__searchTerm">&quot;{ this.searchTerm }&quot;</span></h2>
      	<p className="comp-ideaList__blurb">Check out these similar ideas</p>
      	<p className="comp-ideaList__noResults">{ resultsMsg } {this.props.isIdeaList ? <a className="noResults__link" href={ '/'+window.userInfo.company }>Add your idea.</a> : false}</p>
      	{ this.state.currentIdeas }
      </div>
    );
  }
}
