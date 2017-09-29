import uuid from 'uuid';
import Wantoo from './../utils/wantoo';

import * as modalActions from './modalActions';

/**
* Card actions
*/

// let nextCardID = 126000;
export const addCard = (title,single, description, categoryId, statusId, listId) => (dispatch) => {
	dispatch(requestCard());
	console.log('AddCard Async with Props => ', title, description, categoryId, statusId);

	return Wantoo.addIdea(title, single,description, categoryId, statusId).then( resolve => {
		console.log('\n\n\n\n RESOLVE DATA from => Wantoo.addIdea() => ', resolve, ' Calling receiveCard...');
		console.log('****** lenght of resolve',resolve.length);
		if(resolve.length == undefined)
		{
			dispatch( receiveCard(resolve, listId) );
		}
		for(var i=0;i<resolve.length;i++)
		{
			dispatch( receiveCard(resolve[i], listId) );

		}
		dispatch( modalActions.hideModal() );

	});

	// let new_id = uuid.v4();
	// return {
	// 	type: 'ADD_CARD',
	// 	id: new_id,
	// 	title: title,
	// 	description: description,
	// 	category_id: categoryId,
	// 	status: statusId,
	// 	list_id: listId
	// };
};

const requestCard = () => {
	console.log('requestCard called....');
	return { 
		type: 'REQUEST_DATA'
	};
};

//Gets card from backend to get actual card ID.
const receiveCard = (response, listId) => {
	console.log('receiveCard called....', response);
	
	return {
		type: 'RECEIVE_CARD',
		response,
		listId
	};

};

export const updateCard = (title,single, description, categoryId, cardId, idea_id) => (dispatch) => {
	dispatch(requestCard());
	console.log('updateCard Props => ', title, description, categoryId, cardId);

	Wantoo.updateIdea(title,single, description, categoryId, idea_id).then(resolve => {
		dispatch({
			type: 'UPDATE_CARD',
			title: title,
			description: description,
			category_id: categoryId,
			id: cardId,
			idea_id: idea_id,
			single:single,
		});
		dispatch( modalActions.hideModal() );
	});

	// return {
	// 	type: 'UPDATE_CARD',
	// 	title: title,
	// 	description: description,
	// 	category_id: categoryId,
	// 	id: cardId,
	// 	idea_id: idea_id,
	// };
};

export const moveCard = (sourceId, targetId, isDrop=false) => {
	return {
		type: 'MOVE_CARD',
		sourceId,
		targetId
	};
};

export const listAttach = (sourceId, targetId) => {
	return {
		type: 'LIST_ATTACH',
		sourceId,
		targetId
	};
};

export const deleteCard = (id, idea_id) => {
	Wantoo.deleteIdea(idea_id);
	return {
		type: 'DELETE_CARD',
		id
	};
};

export const updateCardListId = (id, targetId) => {
		return {
		type: 'UPDATE_OLD_LIST_ID',
		id,
		targetId,
	};
};