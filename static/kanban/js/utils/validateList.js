const validateList = (data, props) => {
	const errors = {};
	console.log('FROM validateList: data, props', data, props);

	if (!data.title || data.title.length <= 0) {
		errors.title = "Please enter a title";
	} else if (data.title.length > 20) {
		errors.title = "Please make your title less than 20 characters, it is currently " + data.title.length + " characters";
	}

	if (!data.color || data.color.length <= 0) {
		errors.color = "Please enter a color";
	} else if (data.color.replace('#','').trim().length > 6) {
		errors.color = "Please enter a valid hex color";
	}
	
	// if (Object.keys(errors).length <= 0) {
	// 	console.log('returning blank');
	// 	return {};
	// } else {
	// 	console.log('returning errors=>', errors);
	// 	return errors;
	// }
	return errors;
};

export default validateList;