/**
* Display Filter Reducers
* For toggling Trello/Wantoo ordering.
*/

const displayFilters = (state = 'DISPLAY_WANTOO', action) => {

	switch(action.type) {
		case 'SET_DISPLAY_FILTER':
			return action.filter;
			break;
		default:
			return state;
	}

};

export default displayFilters;