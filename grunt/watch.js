module.exports = {
	dashboard: {
		files: ['static/dashboard/stylus/**/*.styl'],
		tasks: ['stylus:dashboard'],
		options: {
			spawn: false,
		}
	},
	landing: {
		files: ['static/landingpage/stylus/**/*.styl'],
		tasks: ['stylus:landing'],
		options: {
			spawn: false,
		}
	},
}; 