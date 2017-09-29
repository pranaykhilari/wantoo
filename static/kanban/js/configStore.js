import { createStore, applyMiddleware } from 'redux';

// import promiseMiddleware from 'redux-promise';
import thunk from 'redux-thunk';
// import createLogger from 'redux-logger';

import kanbanApp from './reducers/kanbanApp'
// import storage from './utils/storage';



const configStore = () => {

	// const APP_STORAGE = 'redux_kanban';

	let vote_count = app.ideas.length > 0 ? app.ideas.reduce((prev, curr, i) => {
		if (i === 1 || i === 0) {
			if (!prev.status.id) {
				prev = prev.vote_count
			} else {
				prev = 0;
			}
		}

		if (!curr.status.id) {
			return prev + curr.vote_count;
		} else {
			return prev;
		}
		
	}): 0;

	if (typeof vote_count === 'object') {
		if (!vote_count.status.id)
			vote_count = vote_count.vote_count;
		else 
			vote_count = 0;
	}

	console.log('vote_count,',vote_count);

	const appData = {
		lists: [
			{
				id: 0,
				title: 'Inbox',
				color: '#E2E4E6',
				count: app.ideas.filter(c => c.status.id === null).length,
				vote_count: vote_count,
			},
			...statuses
		],
		cards: app.ideas,
	};

	return createStore(
		kanbanApp, 
		appData,
		// applyMiddleware(promiseMiddleware, createLogger())
		applyMiddleware(thunk)
	);

	// store.subscribe(() => {
	// 	storage.set(APP_STORAGE, store.getState());
	// });
	// localStorage.clear();

	// return store;

};

export default configStore;