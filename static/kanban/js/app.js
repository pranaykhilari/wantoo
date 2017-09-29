
import React from 'react';
import ReactDOM from 'react-dom';

import configStore from './configStore';
import AppRoot from './components/AppRoot';


const store = configStore();

ReactDOM.render(
	<AppRoot store={store} />,
  document.getElementById('kanban-root')
);


