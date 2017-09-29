import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';

import lists from './lists';
import cards from './cards';
import modals from './modals';
import displayFilters from './displayFilters';
import isFetching from './isFetching';

// Creates signle state tree

const KanbanApp = combineReducers({
	isFetching,
	lists,
	cards,
	modals,
	displayFilters,
	form: formReducer,
});

export default KanbanApp;