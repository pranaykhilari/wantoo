import React from 'react';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import { ChromePicker } from 'react-color';

import * as listActions from './../../actions/listActions';
import validateList from './../../utils/validateList';


let AddListForm = ({fields: {title, color, closed}, onClose, isUpdating, isFetching, onDeleteListClick, item, handleSubmit, handleColorClick, handleColorClose, displayColorPicker, handleColorChange, defaultColor, checkClosed, toggleClosed}) => {
	return (
		<form onSubmit={handleSubmit}
			className="modal-form wantoo-form" 
			style={{padding: '0 60px'}}>
			<h2 className="modal-header">
			{
				isUpdating 
					? <p>Status settings: <b>{item.title}</b></p> 
					: <p>Add New <b>Status</b></p>
			}
			</h2>
			<div>

				<div className="form-group">
					<label className="control-label">Status title</label>
					
					<input className="single-line-input form-control"
						{...title}
						type="text"
						placeholder={isUpdating ? item.title : 'Title'} />
					{title.error && title.touched && <div className="modal-error">{title.error}</div>}
	 			</div>

	 			<div className="form-group">
					<label>Status color</label>
					<input className="single-line-input form-control jscolor"
						{...color}
						onClick={handleColorClick}
						value={defaultColor}
						type="text"
						placeholder={isUpdating ? item.color : 'Hex Color'}
						style={{background: defaultColor, color: 'white'}}/>
					{color.error && color.touched && <div className="modal-error">{color.error}</div>}
					{ displayColorPicker 
						? (
							<span>
								<div style={{position: 'fixed', top: '0', right: '0', bottom: '0', left: '0'}} onClick={handleColorClose}/>
								<div style={{position: 'absolute', zIndex: '2'}}>
									<ChromePicker color={defaultColor} onChange={handleColorChange}/>
								</div>
							</span>
							)
						: null
					}

	 			</div>

	 			<div className="form-group">
					<label style={ {display: 'block'} }>Status options</label>

					<input className="modal-checkbox"
						{...closed}
						onChange={e => {
							console.log('Checkbox cliked:  e.target.checked =>', e.target.checked);
							console.log('closed.value=>', closed.value);
							closed.value = !closed.value;
							toggleClosed(!closed.value);
						}}
						type="checkbox"
						checked={checkClosed}
						style={ {float: 'left', display: 'inline-block', position: 'absolute'} } />

					<div style={ {float: 'left', display: 'inline-block', 'margin': '0 5px 0 22px'} } >
						<b style={{marginLeft: '5px'}}>Hide ideas</b><span className="eye-form"></span>
						<p style={ {float: 'left', display: 'block', 'margin': '0 0 40px 0', 'color': 'grey', fontSize: '12px'} }>
							Ideas are excluded from list and activity views but can still be found via search
						</p>
					</div>

	 			</div>
				<button className="btn-fill-primary"
					type="submit"
					style={ {background: '#659701', float: 'left'} }
				>{isFetching ? 'Publishing...' : isUpdating ? 'Save' : 'Add'}</button>

				<button onClick={onClose}
					type="button"
					className="-btn-cancel btn-fill-transparent"
					style={ {float: 'left'} } >
					Cancel
				</button>
				<button onClick={onClose}
					type="button"
					id="Delete_status"
					className="-btn-delete btn-fill-transparent-red"
					style={{float: 'left'}}
					onClick={onDeleteListClick} style={{position: 'relative', float: 'right', right: '-30px'}}>
					Delete
				</button>

				<div className="form-clearfix-footer"></div>
			</div>
		</form>
	);
};

AddListForm = reduxForm({
  form: 'add-list',
  fields: ['title', 'color', 'closed'],
  validate: validateList,
})(AddListForm);

class AddListModal extends React.Component {

	constructor(props) {
		super(props);
		console.log('ADDLIST CONSTRUCTOR: ', props);
		this.state = {
			displayColorPicker: false,
			color: props.item ? props.item.color : '#70777B',
			checkClosed: props.item ? (props.item.closed ? true: false) : false,
		};

  	}

  	handleColorClick() {
  		console.log('handleColorCLICKED CALLED');
  		this.setState({ displayColorPicker: !this.state.displayColorPicker })
  	}

  	handleColorClose() {
  		console.log('handleColorClose CALLED');
  		this.setState({ displayColorPicker: false })
  	}

  	handleColorChange(color) {
  		console.log('handleColorChange CALLED with color => ', color.hex);
  		this.setState({ color: color.hex })
  	}

	handleSubmit(data) {
		console.log('FORM SUBMITTED: data=>', data);

		const {dispatch, item, isUpdating} = this.props;

		console.log('Submit clicked from addListModal, item => ', item);

		if (!isUpdating) {
			dispatch( listActions.addList(data.title, data.color, data.closed) );
			mixpanel.track('Add Status (' + data.title + ') from Kanban | Manage Feedback');
		} else {
			dispatch( listActions.updateList(data.title, data.color, data.closed, item.status_id, item.id) );
		}
		this.handleColorClose();
	}

	toggleClosed(val) {
		let newState = this.state;
		newState.checkClosed = !val;
		this.setState(newState);
	}

	render() {
		const item = this.props.item;
		let initialFormValues = {
			initialValues: {
				color: this.state.color,
			}
		};
		if (this.props.isUpdating) {
			initialFormValues.initialValues['title'] = item.title;
			initialFormValues.initialValues['closed'] = item.closed ? true : false;
		}
		console.log('InitialValues for CardModal=>', initialFormValues);
		console.log('this.state.checkClosed=>', this.state.checkClosed);
		return (
			<div>
				<AddListForm
				onSubmit={(data) => this.handleSubmit(data)}
				handleColorClose={() => this.handleColorClose()}
				handleColorClick={() => this.handleColorClick()}
				displayColorPicker={this.state.displayColorPicker}
				defaultColor={this.state.color}
				handleColorChange={(color) => this.handleColorChange(color)}
				checkClosed={this.state.checkClosed}
				toggleClosed={(val) => this.toggleClosed(val)}
				{...initialFormValues}
				{...this.props} />
			</div>
		);
	}
};

AddListModal = connect()(AddListModal);
$( "#Delete_status" ).click(function() {
  window.Intercom("trackEvent", " Delete Status");
});

export default AddListModal;