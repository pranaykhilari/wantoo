
const isFetching = (state=false, action) => {

	switch(action.type) {
		case 'REQUEST_DATA':
			return true;
		case 'RECEIVE_CARD':
			return false;
		case 'UPDATE_CARD':
			return false;
		case 'UPDATE_LIST':
			return false;
		case 'RECEIVE_LIST':
			return false;
		default:
			return state;
	}

};

export default isFetching;