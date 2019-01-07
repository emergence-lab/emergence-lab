const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');



const CSS = [
  // 'jquery-ui-dist/jquery-ui.min.css',
  // 'jquery-datetimepicker/jquery.datetimepicker.css'
];
const JS = [
  "bootstrap",
  "bootstrap-table",
  "django-formset",
  "dropzone",
  "font-awesome",
  "hallo",
  "jquery",
  "rangy",
  "select2",
  "select2-bootstrap-theme"
];

const Assets = [...JS, ...CSS];

module.exports = {
  entry: {
    app: "./src/app.js",
  },
  output: {
    path: __dirname + "/static/",
    filename: "[name].bundle.js"
  },
  plugins: [
    new CopyWebpackPlugin(
      Assets.map(asset => {
        return {
          from: path.resolve(__dirname, `./node_modules/${asset}`),
          to: path.resolve(__dirname, `./static/${asset}`)
        };
      })
    )
  ]
};
