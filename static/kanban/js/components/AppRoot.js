import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import HTML5Backend from 'react-dnd-html5-backend';
import { DragDropContext } from 'react-dnd';

import Board from './Board';
import ActionModals from './ActionModals';


class AppWrap extends React.Component {

	constructor() {
		super();
		this.state = {overflow: true};
	}

	toggleOverlfow() {
		console.log('TOGGLE OVERLFOW CALLED EXECUTED');
		this.setState({overflow: !this.state.overflow});
	}

	render() {
		return (
			<div style={{overflowX: this.state.overflow ? 'auto' : 'hidden'}} className="board-wrapper">
				{/* <FilterHeader /> */}
				<Board toggleOverlfow={() => this.toggleOverlfow()} />
				<ActionModals />
			</div>
		);
	}
}
AppWrap  = DragDropContext(HTML5Backend)(AppWrap);

const AppRoot = ({store}) => (
	<Provider store={store} >
 		<AppWrap />
  	</Provider>
);

export default AppRoot;