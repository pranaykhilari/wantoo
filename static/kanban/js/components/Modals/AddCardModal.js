import React from 'react';
import ReactDOM from 'react-dom';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import striptags from 'striptags';

import * as cardActions from './../../actions/cardActions';
import * as listActions from './../../actions/listActions';
import validateCard from './../../utils/validateCard';


class AddCardForm extends React.Component {

	constructor() {
		super()
		this.setIdea = this.setIdea.bind(this)
	}
	componentDidMount() {

		//this didnt worki either
		// console.log('ComponentDidMount: AddCardForm', ReactDOM.findDOMNode(this.refs.focusInput));
		// ReactDOM.findDOMNode(this.refs.focusInput).focus();
	}

	setIdea(event) {
		this.props.updateState(event.target.value)
 	 }


	render() {
		const { fields: {title, description, category}, onClose, itemId, isUpdating, item, onChange, isFetching, statusTitle, handleSubmit } = this.props;
		return (
			<form onSubmit={handleSubmit}

				className="modal-form wantoo-form">
				<h2 className="modal-header">
				{
					isUpdating 
						? <p>Edit <b>Idea</b></p> 
						: <p>Add Idea: <b>{statusTitle}</b></p>
				}
				</h2>
				<div>
				{/*Added radio button option*/}
				{!isUpdating ?
					<div className="form-group">
						<div className="idea-selection">
							<div className="single-idea">
									<input className="format-radio" type="radio" name="add-idea"  onClick={this.setIdea} value={"single"} defaultChecked >Single idea</input>
							</div>
							<div className="multiple-idea">
									<input className="format-radio" type="radio" name="add-idea" onClick={this.setIdea} value={"multiple"} >Multiple ideas</input>
							</div>
						</div>
					</div>
					:
					<div></div>
                 }
						<div className="form-group">
							<label className="control-label">Titles <span className="idea-title">(70 characters max per title)</span></label>
							<textarea className="single-line-input form-control"
									  style={{height: '150px', paddingBottom: '27%'}}
                                      {...title}
									  type="text"
									  placeholder={isUpdating ? item.title : 'Idea titles must be one per line'}
									  ref="focusInput"/>

                            {title.error && title.touched && <div className="modal-error">{title.error}</div>}

						</div>

		 			{/*<div className="form-group">*/}
						{/*<label>Description</label>*/}
						{/*<textarea className="single-line-input form-control"*/}
							{/*{...description}*/}
							{/*type="text"*/}
							{/*rows="3"*/}
							{/*placeholder={isUpdating && item.description !== '' ? item.description : 'Description'}*/}
							{/*style={{resize: 'vertical', maxHeight: '300px'}}></textarea>*/}
		 			{/*</div>*/}

		 			<div className="form-group">
						<label>Category</label>
						<select className="cat-select form-control"
							{...category}>
				 			<option value={''}> ------- </option>
							{
								categories.length > 0
									? categories.map( cat => <option key={cat.id} value={cat.id}>{cat.title}</option>)
									: null
							}
						</select>
		 			</div>

					<button className="btn-fill-primary"
						type="submit"
						style={ {background: '#659701', float: 'left'} }>
						{isFetching ? 'Publishing...' : isUpdating ? 'Save' : 'Add'}
					</button>

					<button className="-btn-cancel btn-fill-transparent"
						type="button"
						onClick={onClose}
						style={{float: 'left'}}>
						Cancel
					</button>

					<div className="form-clearfix-footer"></div>
				</div>
			</form>
		);
	}
};


AddCardForm = reduxForm({
  form: 'add-card',
  fields: ['title', 'description', 'category'],
  touchOnBlur: true,
  validate: validateCard,
})(AddCardForm);

class AddCardModal extends React.Component {

	constructor() {
		super();
		this.updateState = this.updateState.bind(this);
		this.state = {
			checkedButton: 'single'
		}
	}

	handleSubmit(data) {
		console.log('FORM SUBMITTED: data=>', data);

		const {dispatch, isUpdating, item, onClose} = this.props;

		console.log('Submiting form from AddCardModal, item => ', item);
		data.description = striptags(data.description);
		data.title = striptags(data.title);

		if (this.state.checkedButton=="single"){
			var single="oneIdea";
			if (!isUpdating) {
				dispatch( cardActions.addCard(data.title, single,data.description, data.category, item.status_id, item.id) );
				dispatch( listActions.updateListCounts(item.id, null, 1, false, false) );
			} else {
				dispatch( cardActions.updateCard(data.title,single, data.description, data.category, item.id, item.idea_id) );
				mixpanel.track('Add Idea (' + data.title + ') from Kanban | Manage Feedback');
			}
		}
		else{
			var single="manyIdeas"
			if (!isUpdating) {
				dispatch( cardActions.addCard(data.title, single,data.description, data.category, item.status_id, item.id) );
				dispatch( listActions.updateListCounts(item.id, null, 1, false, false) );
			} else {
				dispatch( cardActions.updateCard(data.title,single, data.description, data.category, item.id, item.idea_id) );
				mixpanel.track('Add Idea (' + data.title + ') from Kanban | Manage Feedback');
			}

		}


	}

	updateState(checkedButton) {
		this.setState({checkedButton})
	}

	render() {
		const item = this.props.item;
		let initialFormValues = this.props.isUpdating
			? 	({ 
					initialValues: {
						title: item.title,
						description: item.description,
						category: item.category_id !== "None" ? item.category_id : "",
					}
				})
			: null;
		console.log('InitialValues for CardModal=>', initialFormValues);
		return (
			<div>
				<AddCardForm 
				onSubmit={(data) => this.handleSubmit(data)}
				checkedButton={this.state.checkedButton}
				updateState={this.updateState}
				{...initialFormValues}
				{...this.props} />
			</div> 
		);
	}
};



AddCardModal = connect()(AddCardModal);

export default AddCardModal;

