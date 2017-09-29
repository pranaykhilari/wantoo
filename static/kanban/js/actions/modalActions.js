/**
* Modal Actions
* modalType: maps the modal ui to another action
* such as deleteList, addList, addCard, deleteCard, etc.
*/

export const showModal = (modalType, itemId, isUpdating=false, item) => {
	return {
		type: 'SHOW_MODAL',
		modalType,
		modalProps: {
			itemId,
			isUpdating,
			item,
		}
	};
};

export const hideModal = () => {
	return {
		type: 'HIDE_MODAL'
	};
};