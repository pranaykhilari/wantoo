module.exports = {
	dashboard: {
		options: {
			compress: true,
			banner: '/*! <%= package.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
		},
	  files: {
	    'static/dist/css/styles-dash.min.css': 'static/dashboard/stylus/styles.styl'
	  }
	},
	landing: {
		options: {
			compress: true,
			banner: '/*! <%= package.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
		},
	  files: {
	    'static/dist/css/landing-page.min.css': 'static/landingpage/stylus/styles.styl'
	  }
	},
};