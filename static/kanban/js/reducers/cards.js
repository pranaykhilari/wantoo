/**
* Card/Idea Reducers
*/

const card = (state, action) => {

	switch(action.type) {
		case 'ADD_CARD':
			return {
				id: action.id,
				title: action.title,
				list: action.list_id,
				comment_count: 0,
				vote_count: 0,
				voted_users: {
					gravatar_url: []
				},
				category_id: null
			};
			break;
		case 'LIST_ATTACH':
			return Object.assign({}, state, {
				list: action.targetId
			});
			break;
		default: 
			return state;
	}

};

const cards = (state = [], action) => {

	switch(action.type) {
		case 'RECEIVE_CARD':


			console.log('RecieveCall called -cards- reducer');

			console.log('request.response: ', action.response);

			const cardFromServer = action.response;
			console.log('***********************');
			console.log(cardFromServer);
			cardFromServer.list = action.listId;
			cardFromServer.old_list_id = action.listId;
			cardFromServer['idea_id'] = cardFromServer['id'];
			cardFromServer['id'];

			//weird structure, should change this...
			cardFromServer['voted_users'] = {};
			cardFromServer.voted_users['gravatar_url'] = [userInfo.gravatar_url];
			cardFromServer.voted_users['id'] = [userInfo.ID];
			cardFromServer['old_order'] = 0;
			cardFromServer['order'] = app.ideas.length + 1;

			if (!cardFromServer['status']) {
				cardFromServer['status'] = {};
				cardFromServer['status'].id = cardFromServer['status'].title = cardFromServer['status'].color = "";
				console.log('RECEIVED NULL CARD => ', cardFromServer);
			} else {
				let newStatId = cardFromServer['status'];
				cardFromServer['status'] = {};
				cardFromServer['status'].id = newStatId;
				cardFromServer['status'].title = cardFromServer['status'].color = "";
				console.log("inside cards.js")
				console.log('RECEIVED VALUE CARD FROM SERVER => ', cardFromServer);
			}

			console.log('cardFromServer = ', cardFromServer);

			return [
				...state,
				// card(undefined, action)
				cardFromServer
			];
			break;
		case 'UPDATE_CARD':
			return state.map(card => {
				if (card.id === action.id) {
					console.log('update card object from reducer');
					return Object.assign({}, card, {
						title: action.title,
						description: action.description,
						category_id: action.category_id,
						id: action.id,
						idea_id: action.idea_id,
					});
				}
				return card
			});
			break;
		case 'MOVE_CARD':

			//We collect needed information
			const sourceCard = state.find( c => c.id === action.sourceId);
			const targetCard = state.find( c => c.id === action.targetId);

			console.log('sourceCARD => ', sourceCard);
			console.log('sourceCARD => ', targetCard);

			let sourceLaneCards = state.filter( c => {
				return c.list === sourceCard.list;
			});
			let targetLaneCards = state.filter( c => {
				return c.list === targetCard.list;
			});

			const sourceCardIndex = sourceLaneCards.findIndex(c => c.id == action.sourceId);
			const tagretCardIndex = targetLaneCards.findIndex(c => c.id == action.targetId);

			const sourceCardOrder = sourceCard.order;
			const targetCardOrder = targetCard.order;

			// Logic to reorder the cards
			if(sourceCardOrder > targetCardOrder) {
				state.forEach(item => {
					if(item.order == sourceCardOrder){
						item.order = targetCardOrder;
					} else if (item.order >= targetCardOrder && item.order < sourceCardOrder) {
						item.order = item.order + 1;
					}
				});
			} else {
				state.forEach(item => {
					if(item.order == sourceCardOrder){
						item.order = targetCardOrder - 1;
					} else if (item.order < targetCardOrder && item.order > sourceCardOrder) {
						item.order = item.order - 1;
					}
				});
			}

			//In this block, we actually change the order.
			if (sourceCard.list === targetCard.list) {


				//TOTALLY UNEFFICIENT AND NEEDS ALOT OF OPTIMIZATION
				sourceLaneCards = [
					...sourceLaneCards.slice(0, sourceCardIndex),
					...sourceLaneCards.slice(sourceCardIndex+1)
				];
				sourceLaneCards = [
					...sourceLaneCards.slice(0, tagretCardIndex),
					sourceCard,
					...sourceLaneCards.slice(tagretCardIndex)
				];
				sourceLaneCards = [
					...sourceLaneCards,
					...state.filter( c => c.list !== sourceCard.list)
				];

				return sourceLaneCards;
			} else {

				let filter = state.filter( c => {return (c.list !== sourceCard.list && c.list !== targetCard.list); });

				//TOTALLY UNEFFICIENT AND NEEDS ALOT OF OPTIMIZATION
				sourceLaneCards = [
					...sourceLaneCards.slice(0, sourceCardIndex),
					...sourceLaneCards.slice(sourceCardIndex+1)
				];

				targetLaneCards = [
					...targetLaneCards.slice(0, tagretCardIndex),
					sourceCard,
					...targetLaneCards.slice(tagretCardIndex)
				];
				sourceCard.list = targetCard.list;

				console.log('TARGET CARD ', targetCard);

				console.log('NEW LANE FROM REDUCER => ', sourceCard.status.id, ', ', targetCard.status.id);
				sourceCard.status.id = targetCard.status.id;

				return [
					...targetLaneCards,
					...sourceLaneCards,
					...filter
				];

			}


			return state;
			break;
		case 'LIST_ATTACH':
			return state.map(c => {
				if (c.id === action.sourceId) {
					return card(c, action);
				}
				// if (c.id === action.targetId)
				// 	return card(c, )
				return c;
			});
			break;
		case 'DELETE_CARD':
			let deletedCard = state.find( c => c.id === action.id);
			state.forEach(item => {
				if(item.order > deletedCard.order){
					item.order = item.order - 1;
				}
			});

			return state.filter(card => {
				return card.id !== action.id
			});
			break;
		case 'DELETE_LIST':
			return state.map(card => {
				if (card.list === action.id) {
					return Object.assign({}, card, {
						list: 0
					});
				}
				return card;
			});
			break;
		case 'UPDATE_OLD_LIST_ID':
			return state.map(card => {
				if (card.id === action.id) {
					return Object.assign({}, card, {
						old_list_id: action.targetId,
					});
				}
				return card
			});
			break;
		default:
			return state;
	}

};

export default cards;