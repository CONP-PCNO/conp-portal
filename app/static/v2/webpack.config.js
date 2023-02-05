const path = require('path');
const process = require('process');

/** @type {import('webpack').Configuration} */
module.exports = {
  entry: [path.join(__dirname, 'src', 'index.ts')],
  devtool: process.env.NODE_ENV === 'development' ? 'inline-source-map' : 'source-map',
  output: {
    clean: true,
    filename: 'conp-portal.bundle.js',
    path: path.resolve(__dirname, 'dist'),
    library: {
      name: 'CONP',
      type: 'umd'
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    },
    extensions: ['.tsx', '.ts', '.js']
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.s[ac]ss$/i,
        use: ['style-loader', 'css-loader', 'sass-loader']
      },
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource'
      }
    ]
  }
};
