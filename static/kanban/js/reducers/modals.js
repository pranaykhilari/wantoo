/**
* Modal Reducers
*/

const modals = (state = { modalType: null, modalProps: {}, isOpen: false }, action) => {

	switch(action.type) {
		case 'SHOW_MODAL':
			return {
				modalType: action.modalType,
				modalProps: action.modalProps,
				isOpen: true
			};
			break;
		case 'HIDE_MODAL':
			return {
				modalType: null,
				modalProps: {},
				isOpen: false
			}
			break;
		default: 
			return state;
			break;
	}

};

export default modals;