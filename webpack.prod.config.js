var path = require('path');
var webpack = require("webpack");
var CleanWebpackPlugin = require('clean-webpack-plugin');
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
    app: PATHS.dash + '/js/app.js', 
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
    filename: '[name]-[hash].js',
    publicPath: '/static/bundles/', 
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
        loader: 'uglify!babel?presets[]=react,presets[]=es2015',
      },
      //note the specific loader syntax. Stylus loader must be sent through to css loader
      //Make sure that stylus loader v > 2.0.0, or it won't work with uglify
      { 
        test: /\.styl$/, 
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader!stylus-loader'),
        include: [PATHS.dashStyles, PATHS.landingStyles, PATHS.kanban + '/stylus/styles.styl']
      }
    ]
  },
  plugins: [ 
    new CleanWebpackPlugin([PATHS.build], {
      root: process.cwd()
    }),
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
      algoliasearch: 'algoliasearch',
      Cookies: 'Cookies'
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
        drop_console: true
      },
      mangle: {
        except: ['$', 'webpackJsonp']
      }
    }),
    new ExtractTextPlugin('[name]-[hash].css'),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    }),
  ]
};

