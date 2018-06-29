const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: [
	  'webpack-dev-server/client?http://localhost:8081',
	  'webpack/hot/only-dev-server',
	  path.resolve('./starlight/static/js/App'),
	],

  output: {
    path: path.resolve('./starlight/static/build'),
    filename: '[name].js',
    publicPath: 'http://localhost:8081/assets/build/',
  },

  module: {
    rules: [
      {test: /\.jsx?$/, exclude: /node_modules/, use: 'babel-loader'},
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          use: ['css-loader', 'sass-loader'],
          fallback: 'style-loader',
          publicPath: '../',
        }),
      },
      {test: /\.txt$/, use: 'raw-loader'},
      {
        test: /\.(png|jpg|jpeg|gif)([?]?.*)$/,
        use: 'file-loader?name=img/[name].[ext]',
      },
      {
        test: /\.(svg|woff|woff2|eot|ttf|wav|mp3|otf)([?]?.*)$/,
        use: 'file-loader?name=[name].[ext]',
      },
    ],
  },

  plugins: [
    new ExtractTextPlugin({filename: 'css/[name].css', disable: false}),
    new BundleTracker({filename: './starlight/static/webpack-stats.json'}),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.LoaderOptionsPlugin({minimize: true}),
    new webpack.optimize.UglifyJsPlugin({compress: {warnings: false}}),
  ],

  devServer: {
    host: '0.0.0.0',
    port: 8081
  },
};
