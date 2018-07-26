const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = (env = {}) => {
  return {
    context: __dirname,

    entry: {
  	  vendor: [path.resolve('./starlight/static/js/vendor')],
  	},

    output: {
      path: path.resolve('./starlight/static/build'),
      filename: '[name]-[chunkhash].js',
      library: 'vendor_lib',
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
          use: {
            loader: 'file-loader',
            options: {
              name: 'fonts/[name].[ext]'
            }
          },
        },
      ],
    },

    plugins: [
      new webpack.optimize.CommonsChunkPlugin({
        name: 'vendor'
      }),
      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'window.jQuery': 'jquery',
        'window.$': 'jquery',
      }),
      new webpack.DllPlugin({
        name: 'vendor_lib',
        path: './starlight/static/vendor-manifest.json',
      }),
      new ExtractTextPlugin({filename: 'css/[name]-[chunkhash].css', disable: false}),
      new BundleTracker({filename: './starlight/static/webpack-stats-vendor.json'}),
      new webpack.LoaderOptionsPlugin({minimize: true}),
      new webpack.optimize.UglifyJsPlugin({compress: {warnings: false}}),
    ],
  };
};
