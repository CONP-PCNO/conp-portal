const path = require("path");

module.exports = {
  parser: "babel-eslint",
  extends: ["react-app"],
  settings: {
    "import/resolver": {
      "babel-module": {
        alias: {
          src: path.resolve("src")
        }
      }
    }
  }
};
