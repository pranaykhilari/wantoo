var path = require('path');
var webpack = require("webpack");
var ExtractTextPlugin = require('extract-text-webpack-plugin');

//Needed for django-webpack package
var BundleTracker = require('webpack-bundle-tracker');

var PATHS = {
  root: __dirname,
  dash: path.join(__dirname, 'static/dashboard'),
  build: path.join(__dirname, 'static/bundles'),
  vendor: path.join(__dirname, 'static/dashboard/js/vendor'),

  dashStyles: path.join(__dirname, 'static/dashboard/stylus/styles.styl'),
  landingStyles: path.join(__dirname, 'static/landingpage/stylus/styles.styl'),

  kanban: path.join(__dirname, 'static/kanban')
};


module.exports = {
  context: __dirname,
  entry: {
    app: [
      'webpack-dev-server/client?http://localhost:8080', 
      'webpack/hot/only-dev-server', 
      PATHS.dash + '/js/app.js'
    ],
    main: PATHS.dash + '/js/main.js',
    vendor: [ 
      PATHS.vendor + '/js.cookie.min.js',
      PATHS.vendor + '/jquery.validate.min.js',
      PATHS.vendor + '/algoliasearch.min.js',
      PATHS.vendor + '/dataTables.bootstrap.min.js',
      PATHS.vendor + '/toastr.min.js',
      PATHS.vendor + '/autogrow.js',
      PATHS.vendor + '/jscolor.min.js',
      PATHS.vendor + '/pusher.min.js',
      PATHS.vendor + '/linkify.min.js',
      PATHS.vendor + '/linkify-string.min.js'
    ],
    dashboard: PATHS.dashStyles,
    landing: PATHS.landingStyles,

    kanban: PATHS.kanban + '/js/app.js',
    kanbanStyles: PATHS.kanban + '/stylus/styles.styl',
  },
  output: {
    path: PATHS.build,
    filename: '[name].js',
    publicPath: 'http://localhost:8080/static/bundles/',
  },
  externals: {
    jquery: 'jQuery'
  },
  resolve: {
    root: path.resolve('static'),
    extensions: ['', '.js', '.jsx','.json', 'css', '.styl'],
    alias: {
        jquery: PATHS.vendor + '/jquery.min.js',
        datatables: PATHS.vendor + '/jquery.dataTables.min.js',
        algoliasearch: PATHS.vendor + '/algoliasearch.min.js',
        Cookies: PATHS.vendor + '/js.cookie.min.js',
    }
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: [/node_modules/, /vendor/],
        loaders: ['react-hot', 'babel'],
      },
      { 
        test: /\.styl$/, 
        exclude: /vendor/,
        loader: ExtractTextPlugin.extract('style', 'css!stylus'),
        include: [PATHS.dashStyles, PATHS.landingStyles, PATHS.kanban + '/stylus/styles.styl']
      }
    ]
  },
  plugins: [ 
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
      algoliasearch: 'algoliasearch',
      Cookies: 'Cookies'
    }),
    new ExtractTextPlugin('[name].css'),
  ],
  devServer: {
    publicPath: 'http://localhost:8080/static/bundles/',
    hot: true,
    inline: true,
    historyApiFallback: true,
    stats: 'errors-only'
  },
};

