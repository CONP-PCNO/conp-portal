import path from 'path';
import process from 'process';
import webpack from 'webpack';

const config: webpack.Configuration = {
  entry: [
    path.join(__dirname, 'src', 'index.ts')
  ],
  devtool: process.env.NODE_ENV === 'development' ? 'inline-source-map' : 'source-map',
  output: {
    clean: false,
    filename: 'experiments.bundle.js',
    path: path.join(__dirname, '..', '..', 'js'),
    library: {
      name: 'experiments',
      type: 'umd',
    },
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.ts?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
};

export default config;