import uuid from 'uuid';

import * as modalActions from './modalActions';
import Wantoo from './../utils/wantoo';

/**
* List actions
*/

// let nextListID = 9000;
export const addList = (title, color, closed) => (dispatch) => {
	dispatch(requestList());

	console.log('AddList Async with Props => ', title, color, closed);

	closed = closed ? 1 : 0;
	color = color.replace('#', '').trim();

	return Wantoo.addStatus(title, color, closed).then( resolve => {
		console.log('\n\n\n\n RESOLVE DATA from => Wantoo.addStatus() => ', resolve, ' Calling receiveList...');
		dispatch( receiveList(resolve) );
		dispatch( modalActions.hideModal() ); //same as add card modal
	});

	// let new_id = uuid.v4();
	// return {
	// 	type: 'ADD_LIST',
	// 	// id: (nextCardID+=3000),
	// 	id: new_id,
	// 	title,
	// 	color: color
	// };
};

const requestList = () => {
	console.log('requestList called....');
	return { 
		type: 'REQUEST_DATA'
	};
};

//Gets card from backend to get actual card ID.
const receiveList = (response, listId=null) => {
	console.log('receiveList called....');
	
	return {
		type: 'RECEIVE_LIST',
		response
	};

};


// // let nextCardID = 126000;
// export const addCard = (title, description, categoryId, statusId, listId) => (dispatch) => {
// 	dispatch(requestCard());

// 	console.log('AddCard Async with Props => ', title, description, categoryId, statusId);

// 	return Wantoo.addIdea(title, description, categoryId, statusId).then( resolve => {
// 		console.log('\n\n\n\n RESOLVE DATA from => Wantoo.addIdea() => ', resolve, ' Calling receiveCard...');
// 		dispatch( receiveCard(resolve, listId) );
// 		dispatch( modalActions.hideModal() );
// 	});

// 	// let new_id = uuid.v4();
// 	// return {
// 	// 	type: 'ADD_CARD',
// 	// 	id: new_id,
// 	// 	title: title,
// 	// 	description: description,
// 	// 	category_id: categoryId,
// 	// 	status: statusId,
// 	// 	list_id: listId
// 	// };
// };

// const requestCard = () => {
// 	console.log('requestCard called....');
// 	return { 
// 		type: 'REQUEST_DATA'
// 	};
// };

// //Gets card from backend to get actual card ID.
// const receiveCard = (response, listId) => {
// 	console.log('receiveCard called....');
	
// 	return {
// 		type: 'RECEIVE_DATA',
// 		response,
// 		listId
// 	};

// };



export const updateList = (title, color, closed, statusID, listID) => (dispatch) =>{
	dispatch(requestList());

	console.log('updateList Props => ', title, color, closed, statusID, listID);

	closed = closed ? 1 : 0;
	color = color.replace('#', '').trim();

	Wantoo.updateStatus(title, color, closed, statusID).then( resolve => {
		dispatch({
			type: 'UPDATE_LIST',
			id: listID,
			title: title,
			color: color,
			closed: closed,
		});
		dispatch( modalActions.hideModal() );
	});

	// return {
	// 	type: 'UPDATE_LIST',
	// 	id: listID,
	// 	title: title,
	// 	color: color,
	// 	closed: closed,
	// };
};

export const moveList = (sourceId, targetId) => {
	return {
		type: 'MOVE_LIST',
		sourceId,
		targetId
	};
};

export const deleteList = (id, statusID) => {
	console.log('DELETE LIST CATION WITH PROPS ', id, statusID );
	Wantoo.deleteStatus(statusID);
	return {
		type: 'DELETE_LIST',
		id
	};
};

export const updateListCounts = (sourceId, targetId, want_count, isMove, isDelete) => {
	console.log('Updating List counts -- Action creator fired...');

	console.log('Action Creator { sourceId=' + sourceId + ', targetId=' + targetId + ', want_count=' +want_count +', isMove='+isMove+', isDelete='+isDelete+'}');

	return {
		type: 'UPDATE_COUNTS',
		sourceId,
		targetId,
		want_count,
		isMove,
		isDelete,
	};
}