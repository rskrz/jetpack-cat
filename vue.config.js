const path = require('path')
const glob = require('glob-all')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const PurgecssPlugin = require('purgecss-webpack-plugin')

module.exports = {
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.pug$/,
          loader: "pug-plain-loader"
        }
      ]
    },
    plugins: [
      new PurgecssPlugin({
        paths: glob.sync([
          path.join(__dirname, "src/*.ts"),
          path.join(__dirname, "src/**/*.vue")
        ]),
        minimize: true,
        purifyOptions: {
          whitelist: []
        }
      })
    ]
  },
  pluginOptions: {
    "style-resources-loader": {
      preProcessor: "scss",
      patterns: [path.resolve(__dirname, "./src/styles/_global.scss")]
    }
  },
  devServer: {
    host: "0.0.0.0",
    disableHostCheck: true
  }
};
