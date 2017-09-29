import React from 'react';
import Modal from 'react-modal';

import { connect } from 'react-redux';

import AddCardModal from './Modals/AddCardModal';
import AddListModal from './Modals/AddListModal';
import DeleteModal from './Modals/DeleteModal';

// import { getIsFetching } from './../utils/general';

import * as modalActions from './../actions/modalActions';
import * as cardActions from './../actions/cardActions';
import Wantoo from './../utils/wantoo';


const modalMapper = {
	'ADD_CARD': AddCardModal,
	'ADD_LIST': AddListModal,
	'UPDATE_CARD': AddCardModal,
	'UPDATE_LIST': AddListModal,
	'DELETE_CARD': DeleteModal,
	'DELETE_LIST': DeleteModal
};

const ModalContainer = ({dispatch, modalType, isOpen, modalProps, onCloseModal, isFetching, onDeleteListClick, status}) => {	

	if (!modalType) {
		return (<span/>);
	}

	const ModalContent = modalMapper[modalType];
	const isList = (modalType == 'DELETE_LIST');

	const modalStyles = {
		overlay: {
			zIndex: 1001,
			background: 'none'
		}
	};

	return (
		<Modal
			isOpen={isOpen}
			onRequestClose={(e) => onCloseModal(e)}
			style={modalStyles} >

			<ModalContent 
				isFetching={isFetching} 
				isList={isList} 
				onClose={(e) => onCloseModal(e)}
				onDeleteListClick={(e) => onDeleteListClick(e, modalProps.item)}
				statusTitle={status ? status.title : null}
				{...modalProps} />

		</Modal>
	);
};

const mapStateToModalProps = (state, containerProps) => {
	return {
		modalType: state.modals.modalType,
		modalProps: state.modals.modalProps,
		isOpen: state.modals.isOpen,
		isFetching: state.isFetching,
		status: state.lists.find(l => l.id === state.modals.modalProps.itemId)
	};
};

const mapDispacheToModalProps = (dispatch) => {
	return {
		onCloseModal: (e) => {
			if (e)
				e.preventDefault();
			dispatch( modalActions.hideModal() );
		},
		onDeleteListClick: (e, list) =>  {
			window.Intercom("trackEvent", " Delete status");
			e.preventDefault();
			dispatch( modalActions.hideModal() );
			console.log('CALLING DELETE LIST ', list);
			dispatch( modalActions.showModal('DELETE_LIST', list.id, false, list) );
			mixpanel.track('Deleted Status (' + list.title + ') from Kanban | Manage Feedback');
		},
	};
};

const ActionModals = connect(mapStateToModalProps, mapDispacheToModalProps)(ModalContainer);

export default ActionModals;