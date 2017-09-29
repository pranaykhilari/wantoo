import striptags from 'striptags';
const validateCard = (data, props) => {
	const errors = {};
	console.log('FROM validateCard: data, props', data, props);

	if (!data.title || data.title.length <= 0) {
		errors.title = "Please enter a title";
	} else if(striptags(data.title).length <= 0){
		errors.title = "Please remove html tags";
	}
	// if (!data.description || data.description.length <= 0) {
	// 	errors.color = "Please enter a description";
	// }

	console.log('errors => ', errors);
	
	return errors;
};

export default validateCard;