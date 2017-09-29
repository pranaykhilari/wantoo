import React from 'react';
import { compose } from 'redux';
import { DragSource, DropTarget } from 'react-dnd';

import OrderedCards from './OrderedCards';

import Wantoo from './../utils/wantoo';

import ItemTypes from './../utils/ItemTypes';

class List extends React.Component {

	constructor() {
		super();
		this.state = {scrolled: false};
	}

	onScroll() {
		this.setState({scrolled: true})
	}

	falseScroll() {
		this.setState({scrolled: false})
	}
	render () {

		let hide = isDragging ? {visibility: 'hidden'} : {visibility: 'visible'};
		let showBlank = isDragging ? {background: 'grey'} : {background: '#e2e4e6'};
		const {id, list, onAddClick, onEditListClick, onMove, onAttachList, connectDragSource, connectDropTarget, isDragging, toggleOverlfow} = this.props;
		// return compose(connectDragSource, connectDropTarget)(
		return connectDropTarget(
			<div className="list-content" style={showBlank}>
				<div className="list-hide-wrap" style={hide}>
					<h1 className="list-header">
						<div className="list-header__color-band" style={ {background: list.color} }></div>
						<div className="list-header__text">{list.title}</div>
						{list.closed 
							? <span className="list-header__closed"></span>
							: null
						}
						<div style={{clear: 'both'}}></div>
						<div className="list-header__subtext">{list.count} Ideas • {list.vote_count} Supporters</div>
					</h1>
					<div className="idea-list" onScroll={() => this.onScroll()}>
						<OrderedCards toggleOverlfow={toggleOverlfow} checkScroll={this.state.scrolled} falseScroll={() => this.falseScroll()} isListDragging={isDragging} list={id} />
					</div>
					<div className="list-actions">
					
						<div className="add-card-button__wrapper">
							<button className="add-card" onClick={onAddClick}>
								<span className="add-icon">+</span> Add Idea
							</button>
						</div>

						{ list.id !== 0 
							? (<span className="actions-button" onClick={onEditListClick}></span>) 
							: null
						}

						<div style={{clear: 'both'}}></div>

					</div>
				</div>
			</div>
		);
	}

};

const listSource = {
	beginDrag(props) {
		return {
			id: props.id,
			vote_count: props.vote_count,
			count: props.count,
			isList: true
		};
	},
	isDragging: function (props, monitor) {
    	return monitor.getItem().id === props.id;
  	}
};

const listTarget = {
	hover(targetProps, monitor) {
		const targetId = targetProps.id;
	    const sourceId = monitor.getItem().id;
		if (monitor.getItem().isList) {
	    	if (sourceId !== targetId) {
	    		targetProps.onMove(sourceId, targetId);
	    	}
    	} else if (targetProps.list.count <= 0) {
    		targetProps.onAttachList(sourceId, targetId);
    	}
  	},
  	drop(targetProps, monitor) {
  		const targetId = targetProps.id;
	    const sourceId = monitor.getItem().id;
	    if (monitor.getItem().card.old_list_id !== targetProps.list.id) {
            targetProps.onUpdateListCounts(monitor.getItem().card.old_list_id, targetProps.list.id, monitor.getItem().card.vote_count, true);
            targetProps.onUpdateOldListId(monitor.getItem().id, targetProps.list.id)
	    }
	    Wantoo.updateCardOrder(monitor.getItem().card.idea_id, monitor.getItem().card.order, targetProps.list.status_id);
  	}
};

function connectList(connect, monitor) {
	return {
  		connectDragSource: connect.dragSource(),
  		isDragging: monitor.isDragging()
	}
}

List = compose(
	// DragSource(ItemTypes.LIST, listSource, connectList),
	DropTarget([ItemTypes.LIST, ItemTypes.CARD], listTarget, connect => ({
		connectDropTarget: connect.dropTarget()
	}))
)(List);

$( ".add-icon" ).click(function() {
  window.Intercom("trackEvent", " Add Idea");
});
export default List;