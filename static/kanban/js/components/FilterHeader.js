import React from 'react';
import { connect } from 'react-redux';

import * as filterActions from './../actions/filterActions';

const MainButton = ({active, children, onClick}) => {
	if (active)
		return (<b>{ children }</b>);
	return (
		<a href="#"
			onClick={e => {
				e.preventDefault();
				onClick();
			}}
		>
			{ children }
		</a>
	);
};
const mapStateToMainButtonProps = (state, containerProps) => {
	return {
		active: containerProps.filter === state.displayFilter
	};
};
const mapDispatchToMainButtonProps = (dispatch, containerProps) => {
	return {
		onClick: filter => {
			dispatch( filterActions.setDisplayFilter(containerProps.filter) )
		}
	};
};
const FilterButton = connect(mapStateToMainButtonProps, mapDispatchToMainButtonProps)(MainButton);

const FilterHeader = () => (
	<p>
		Display: 
		{' '}
		<FilterButton filter='DISPLAY_WANTOO'>Wantoo</FilterButton>
		<span> / </span>
		<FilterButton filter='DISPLAY_TRELLO'>Trello</FilterButton>
	</p>
);

export default FilterHeader;