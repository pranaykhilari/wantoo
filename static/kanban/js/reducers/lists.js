/**
* List/Status Reducers
*/

const list = (state, action) => {

	switch(action.type) {
		case 'ADD_LIST':
			return {
				id: action.id,
				title: action.title,
				color: action.color,
				count: 0,
				vote_count: 0
			};
			break;
		default: 
			return state;
	}

};

const lists = (state = [], action) => {

	switch(action.type) {
		case 'RECEIVE_LIST':
			console.log('RecieveCall called -lists- reducer');

			const listFromServer = action.response;
			listFromServer['status_id'] = listFromServer['id'];
			listFromServer['id'];

			listFromServer['color'] = listFromServer['color'].indexOf('#') === -1 ? '#' + listFromServer['color'] : listFromServer['color'];

			listFromServer['count'] = 0;
			listFromServer['vote_count'] = 0;

			return [
				...state,
				// list(undefined, action)
				listFromServer
			];
			break;
		case 'MOVE_LIST':

			//TOTALLY UNEFFICIENT AND NEEDS ALOT OF OPTIMIZATION

			let sourceList = state.find( l => l.id === action.sourceId);

			console.log('sourceLIST => ', sourceList);

			const sourceListIndex = state.findIndex( l => l.id === action.sourceId);
			const tagretListIndex = state.findIndex( l => l.id === action.targetId);

			let newState = [
				...state.slice(0, sourceListIndex),
				...state.slice(sourceListIndex+1)
			];
			newState = [
				...newState.slice(0, tagretListIndex),
				sourceList,
				...newState.slice(tagretListIndex)
			];

			return newState;
			break;
		case 'UPDATE_LIST':
			return state.map(list => {
				if (list.id === action.id) {
					console.log('update list object from reducer');
					let newColor = action.color.indexOf('#') === -1 ? '#' + action.color : action.color;
					return Object.assign({}, list, {
						title: action.title,
						color: newColor,
						closed: action.closed,
					});
				}
				return list;
			});
			break;
		case 'DELETE_LIST':
			return state.filter(list => {
				return list.id !== action.id
			});
			break;
		case 'UPDATE_COUNTS':

			let targetList, newSourceList;

			if (action.sourceId) {
				newSourceList = state.find(l => l.id === action.sourceId);
			} else {
				console.log('using INDEX LIST for newSourceList');
				newSourceList = state.find(l => l.id === 0);
			}

			if (action.isMove) {
				console.log('UPDATE_COUNTS REDUCER: action.isMove is true');
				if (action.targetId) {
					targetList = state.find(l => l.id === action.targetId);
				} else {
					console.log('using INDEX LIST for targetList');
					targetList = state.find(l => l.id === 0);
				}

				console.log('targetList => ', targetList);
				console.log('newSourceList => ', newSourceList);

				++targetList.count;
				targetList.vote_count += action.want_count;

				--newSourceList.count;
				newSourceList.vote_count -= action.want_count;
			} else {
				console.log('UPDATE_COUNTS REDUCER: action.isMove is false');

				console.log('newSourceList => ', newSourceList);

				if(action.isDelete) {
					newSourceList.vote_count -= action.want_count;
					--newSourceList.count;
				} else {
					newSourceList.vote_count += action.want_count;
					++newSourceList.count;
				}
			}


			return state.map(list => {
				if (list.id === action.sourceId) {
					return newSourceList;
				}
				if (action.isMove && list.id === action.targetId) {
					return targetList;
				}
				return list;
			});
			break;
		default: 
			return state;
	}

}

export default lists;