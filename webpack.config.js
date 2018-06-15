var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: [
	 'webpack-dev-server/client?http://localhost:8081',
	 'webpack/hot/only-dev-server',
	 path.resolve('./starlight/static/js/App'),
	 ],

  output: {
      path: path.resolve('./starlight/static/build'),
      filename: "[name].js",
  },

  plugins: [
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
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  }

};
