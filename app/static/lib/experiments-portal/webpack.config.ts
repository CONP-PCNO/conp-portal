import path from 'path';
import process from 'process';
import webpack from 'webpack';

const config: webpack.Configuration = {
  entry: [
    path.join(__dirname, 'src', 'index.ts')
  ],
  devtool: process.env.NODE_ENV === 'development' ? 'inline-source-map' : 'source-map',
  output: {
    clean: true,
    filename: '[name].bundle.js',
    path: path.join(__dirname, 'dist'),
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
        test: /\.ts?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
};

export default config;