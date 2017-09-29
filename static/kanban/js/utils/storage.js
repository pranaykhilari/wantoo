const storage = {

	get(k) {
		try {
			const serializedData = localStorage.getItem(k);
			if (serializedData !== null) {
				return JSON.parse(serializedData);
			}
			return undefined;
		} catch(error) {
			return undefined;
		}
	},

	set(k, v) {
		try {
			const serializedData = JSON.stringify(v);
			localStorage.setItem(k, serializedData);
		} catch(error) {
			console.log('Something went wrong when saving data to localStorage...');
		}
	}

};

export default storage;