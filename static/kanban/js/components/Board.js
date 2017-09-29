import React, { Component } from 'react';
import { connect } from 'react-redux';

import List from './List';

import * as modalActions from './../actions/modalActions';
import * as listActions from './../actions/listActions';
import * as cardActions from './../actions/cardActions';


const ListGroup = ({lists, onAddListClick, onAddClick, onEditListClick, onMoveList, onAttachList, onUpdateOldListId, onUpdateListCounts, toggleOverlfow}) => (
	<ul className="lists-wrapper">
		{lists.map(list => {
			return (
				<li className="list-wrapper" key={list.id}>
					<List
						toggleOverlfow={toggleOverlfow}
						id={list.id}
						list={list}
						onAddClick={() => onAddClick(list)}
						onEditListClick={() => onEditListClick(list)}
						onMove={(sourceId, targetId) => onMoveList(sourceId, targetId)}
						onAttachList={(sourceId, targetId) => onAttachList(sourceId, targetId)}
						onUpdateListCounts={(listID, idea_count, want_count, isMove, isDelete) => onUpdateListCounts(listID, idea_count, want_count, isMove, isDelete)}
						onUpdateOldListId={(id, old_list_id) => onUpdateOldListId(id, old_list_id)}
					/>
				</li>
			);
		})}
		<li className="list-wrapper">

			{/* <AddListButton /> */}
			<div className="add-list-button__wrapper list-content">
				<button className="add-list"
					onClick={() => onAddListClick()}>
					Add a status...
				</button>
			</div>

		</li>

	</ul>
);

const getListOrder = (lists, filter) => {

	switch (filter) {
		case 'DISPLAY_WANTOO':
			return lists;
			break;
		case 'DISPLAY_TRELLO':
			return lists;
			break;
		default:
			return lists;
			break;
	}

};

const mapStateToListGroupProps = (state) => {
	return {
		lists: getListOrder(state.lists, state.displayFilter)
	};
};

const mapDispacheToListGroupProps = (dispatch) => {
	return {
		onAddListClick: () => {
			window.Intercom("trackEvent", " Add status");
			dispatch( modalActions.showModal('ADD_LIST') );
		},
		onAddClick: (list) => {
			window.Intercom("trackEvent", " Add idea");
			dispatch( modalActions.showModal('ADD_CARD', list.id, false, list) );
		},
		onEditListClick: (list) =>  {
			window.Intercom("trackEvent", " Edit status");
			dispatch( modalActions.showModal('UPDATE_LIST', list.id, true, list) )
		},
		// onDeleteClick: (listId) =>  {
		// 	dispatch( modalActions.showModal('DELETE_LIST', listId) )
		// },
		onMoveList: (sourceId, targetId) => {
			dispatch( listActions.moveList(sourceId, targetId) );
		},
		onAttachList: (sourceId, targetId) => {
			dispatch( cardActions.listAttach(sourceId, targetId) );
		},
		onUpdateListCounts: (listID, idea_count, want_count, isMove, isDelete) => {
			dispatch( listActions.updateListCounts(listID, idea_count, want_count, isMove, isDelete) )
		},
		onUpdateOldListId: (id, targetId) => {
			dispatch( cardActions.updateCardListId(id, targetId) );
		}
	};
};

//class for adding lifecycle hooks
class Board extends React.Component {

	render() {
		return (<ListGroup {...this.props} />);
	}

}

Board = connect(mapStateToListGroupProps, mapDispacheToListGroupProps)(ListGroup);

export default Board;