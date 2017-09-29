import React from 'react';
import { connect } from 'react-redux';

import * as listActions from './../../actions/listActions';
import * as cardActions from './../../actions/cardActions';


let DeleteModal = ({ dispatch, onClose, item, itemId, isList}) => (
	<div className="modal-form wantoo-form no-padding">
		<h2 className="modal-header">Delete { isList ? 'status' : 'idea'}</h2>
		<div>
			<div className="form-group">
				<div> 
				{ isList 
					? ('This status will be deleted, and all ideas in this status will be moved to the Inbox lists.' +
						' Deleted statuses are gone forever but simple to re-create! Are you sure?')

					: ('This idea will be deleted, including all data and activity.' + 
						' Deleted ideas are gone forever. Are you sure?')
				}
				</div>
 			</div>
 			<button onClick={onClose}
				className="-btn-cancel btn-fill-transparent"
				style={{float: 'right'}}
			>Cancel</button>
			<button onClick={(e) => {
					console.log('ITEM INSIDE DELETE MODAL', item);
					if (isList) {
						dispatch( listActions.deleteList(itemId, item.status_id) );
					} else {
						dispatch( cardActions.deleteCard(itemId, item.idea_id) );
						dispatch( listActions.updateListCounts(item.list, null, item.vote_count, false, true) );
					}
					if (e)
						e.preventDefault();
					onClose(e);
				}}
				className="btn-fill-primary"
				style={ {background: '#659701', float: 'right'} }
			>Yes, Delete</button>
			<div className="form-clearfix-footer"></div>
		</div>
	</div>
);

DeleteModal = connect()(DeleteModal);

export default DeleteModal;