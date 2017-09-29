import React from 'react';
import { compose } from 'redux';
import { DragSource, DropTarget } from 'react-dnd';

import Wantoo from './../utils/wantoo';

import ItemTypes from './../utils/ItemTypes';


class Card extends React.Component {

	constructor() {
		super();
		this.state = {isOpen: false, top: 0, left: 0};
	}

	toggleDropdown(e, close) {

		let top = e.nativeEvent.target.getBoundingClientRect().top,
		left = e.nativeEvent.target.getBoundingClientRect().left + e.nativeEvent.target.offsetWidth + 168;

		this.props.toggleOverlfow();
		this.props.falseScroll();
		this.setState({isOpen: !this.state.isOpen, top: top, left: left,})
	}

	shouldComponentUpdate(newProps, newState) {

		if (this.state.isOpen && newProps.checkScroll) {
			this.setState({isOpen: !this.state.isOpen, top: this.state.top, left: this.state.left,});
			this.props.falseScroll();
			return true;
		}
		//  else if (this.state.isOpen && newProps.checkScroll) {
		// 	this.props.falseScroll();
		// 	return false;
		// }
		return true
	}

	render() {

		const {id, card, onDeleteClick, onEditClick, onMove, connectDragSource, connectDropTarget, isDragging, isListDragging, onUpdateListCounts, toggleOverlfow} = this.props;
		let hide = isDragging || isListDragging ? {visibility: 'hidden'} : {visibility: 'visible'};
		let showBlank = isDragging ? {background: 'grey'} : {background: 'white'};

		const dropdownStyles = {};
		dropdownStyles.style = {
			display: this.state.isOpen ? 'block' : 'none',
			top: this.state.top,
			left: this.state.left,
		};

		return compose(connectDragSource, connectDropTarget)(
			<li className="list-card" style={showBlank}>
				<div className="card-hide-wrap" style={hide}>

					<div className="card-wants">
						<div className="wants-num">{card.vote_count}</div>
						<span className="wants-img"></span>
					</div>

					<div className="card-data">
						<h4 className="card-header">{card.title}</h4>
						<div className="card-supporters">
						{
							card.voted_users.gravatar_url.map(user_image => {
								return (
									<a key={user_image} className="-profile-link" href="#">
										<img className="-profile-pic -profile-left" 
										src= { user_image } />
									</a>
								);
							})
						}
						</div>
					</div>

					<div className="dropdown -btn-edit" data-id={'dropdownButton-' + id}
						onClick={this.toggleDropdown.bind(this)}
						ref="dropdownButton" >
						<button className="kanban-card-drop" 
							type="button" >
							<img className="kanban-card-drop__image" src="/static/dashboard/img/icons/idea_detail_menu.svg" />
						</button>
					</div>

					{	this.state.isOpen
						?	(<div onClick={this.toggleDropdown.bind(this)} className="kanban-card-menu" id={'dropdownMenu-' + id} ref="dropdownMenu" {...dropdownStyles}>
								<ul className="dropdown-menu kanban-dropdown-menu">
									<li><a id="Edit" href="#" onClick={onEditClick}>Edit</a></li>
									{ userInfo.mergeIdeasEnabled
										?	<li><a href={ '/' + userInfo.company + '/idea/' + card.idea_id + '/merge/' }>Merge</a></li>
										:	<li><a href="/accounts/preferences/subscription/">Merge<span className="mainNav__proFeature"></span></a></li>
									}
									<li><a href="#" onClick={onDeleteClick}>Delete</a></li>
									<li><a href={ '/' +card.idea_id + '/' }>View idea</a></li>
								</ul>
							</div>)
						: null
					}

					<div style={{display: this.state.isOpen ? 'block' : 'none'}} onClick={this.toggleDropdown.bind(this)} className="floating-dropdown"></div>

				</div>
			</li>
		);

	};

};

const cardSource = {
	beginDrag(props) {
		return {
			id: props.id,
			card: props.card,
			isList: false
		};
	},
	isDragging: function (props, monitor) {
    	return monitor.getItem().id === props.id;
  	},
};

const cardTarget = {
	hover(targetProps, monitor) {
    	const targetId = targetProps.id;
    	const sourceId = monitor.getItem().id;

    	console.log('HOVERING OVER CARD');

    	if (sourceId !== targetId) {
			targetProps.onMove(sourceId, targetId, false);
    	}
  	},

  	drop(targetProps, monitor) {

  	}
};

const connectCard = (connect, monitor) => {
	return {
  		connectDragSource: connect.dragSource(),
  		isDragging: monitor.isDragging(),
	};
}

Card = compose(
	DragSource(ItemTypes.CARD, cardSource, connectCard),
	DropTarget(ItemTypes.CARD, cardTarget, connect => ({
		connectDropTarget: connect.dropTarget()
	}))
)(Card);

$( "#Edit" ).click(function() {
  window.Intercom("trackEvent", "Edit Idea");
});

export default Card;