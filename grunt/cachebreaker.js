module.exports = {
	dashboard: {
		options: {
			match: ['styles-dash.min.css', 'webpack-bundle.js', 'init.js', 'app.js', 'main.js'],
		},
		files: {
			src: ['templates/base.html']
		}
	},
	landingpage: {
		options: {
			match: ['landing-page.min.css'],
		},
		files: {
			src: ['templates/landing/base.html']
		}
	},
};