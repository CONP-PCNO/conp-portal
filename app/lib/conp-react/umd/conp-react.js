/*!
 * conp-react v1.0.0
 * MIT Licensed
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["CONPReact"] = factory(require("react"));
	else
		root["CONPReact"] = factory(root["React"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE__0__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 6);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE__0__;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

/**
 * Copyright (c) 2013-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

if (false) { var throwOnDirectAccess, ReactIs; } else {
  // By explicitly using `prop-types` you are opting into new production behavior.
  // http://fb.me/prop-types-in-prod
  module.exports = __webpack_require__(7)();
}


/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "run_on_cbrain_green.31f6d0cb.png";

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "run_on_cbrain_gray.37dd4e0c.png";

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "download_green.3d072364.png";

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "download_gray.057ee6dd.png";

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(9);


/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/**
 * Copyright (c) 2013-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */



var ReactPropTypesSecret = __webpack_require__(8);

function emptyFunction() {}
function emptyFunctionWithReset() {}
emptyFunctionWithReset.resetWarningCache = emptyFunction;

module.exports = function() {
  function shim(props, propName, componentName, location, propFullName, secret) {
    if (secret === ReactPropTypesSecret) {
      // It is still safe when called from React.
      return;
    }
    var err = new Error(
      'Calling PropTypes validators directly is not supported by the `prop-types` package. ' +
      'Use PropTypes.checkPropTypes() to call them. ' +
      'Read more at http://fb.me/use-check-prop-types'
    );
    err.name = 'Invariant Violation';
    throw err;
  };
  shim.isRequired = shim;
  function getShim() {
    return shim;
  };
  // Important!
  // Keep this list in sync with production version in `./factoryWithTypeCheckers.js`.
  var ReactPropTypes = {
    array: shim,
    bool: shim,
    func: shim,
    number: shim,
    object: shim,
    string: shim,
    symbol: shim,

    any: shim,
    arrayOf: getShim,
    element: shim,
    elementType: shim,
    instanceOf: getShim,
    node: shim,
    objectOf: getShim,
    oneOf: getShim,
    oneOfType: getShim,
    shape: getShim,
    exact: getShim,

    checkPropTypes: emptyFunctionWithReset,
    resetWarningCache: emptyFunction
  };

  ReactPropTypes.PropTypes = ReactPropTypes;

  return ReactPropTypes;
};


/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/**
 * Copyright (c) 2013-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */



var ReactPropTypesSecret = 'SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED';

module.exports = ReactPropTypesSecret;


/***/ }),
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: external {"root":"React","commonjs2":"react","commonjs":"react","amd":"react"}
var external_root_React_commonjs2_react_commonjs_react_amd_react_ = __webpack_require__(0);
var external_root_React_commonjs2_react_commonjs_react_amd_react_default = /*#__PURE__*/__webpack_require__.n(external_root_React_commonjs2_react_commonjs_react_amd_react_);

// EXTERNAL MODULE: ./node_modules/prop-types/index.js
var prop_types = __webpack_require__(1);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);

// EXTERNAL MODULE: ./src/data-table/img/run_on_cbrain_green.png
var run_on_cbrain_green = __webpack_require__(2);
var run_on_cbrain_green_default = /*#__PURE__*/__webpack_require__.n(run_on_cbrain_green);

// EXTERNAL MODULE: ./src/data-table/img/run_on_cbrain_gray.png
var run_on_cbrain_gray = __webpack_require__(3);
var run_on_cbrain_gray_default = /*#__PURE__*/__webpack_require__.n(run_on_cbrain_gray);

// EXTERNAL MODULE: ./src/data-table/img/download_green.png
var download_green = __webpack_require__(4);
var download_green_default = /*#__PURE__*/__webpack_require__.n(download_green);

// EXTERNAL MODULE: ./src/data-table/img/download_gray.png
var download_gray = __webpack_require__(5);
var download_gray_default = /*#__PURE__*/__webpack_require__.n(download_gray);

// CONCATENATED MODULE: ./src/data-table/index.js








var data_table_DataTable = function DataTable(_ref) {
  var authorized = _ref.authorized,
      elements = _ref.elements,
      query = _ref.query,
      setQuery = _ref.setQuery,
      onDownload = _ref.onDownload,
      onRunWithCBRAIN = _ref.onRunWithCBRAIN;

  var innerQuery = query;
  var innerSetQuery = setQuery;

  if (!innerSetQuery) {
    var _React$useState = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useState(null);

    innerQuery = _React$useState[0];
    innerSetQuery = _React$useState[1];
  }

  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
    "table",
    { className: "data-table row-border", cellSpacing: 0 },
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("thead", null),
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "tbody",
      null,
      elements.map(function (element) {
        return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "tr",
          null,
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "td",
            null,
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "table",
              null,
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "tr",
                null,
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "th",
                  { colspan: "3" },
                  external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
                    alt: "dataset format",
                    className: "dataset-thumbnail",
                    src: element.thumbnailURL
                  })
                )
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "tr",
                null,
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-download" })
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-eye" })
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-heart" })
                )
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "tr",
                null,
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.downloads
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.views
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.likes
                )
              )
            )
          ),
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "td",
            null,
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "table",
              null,
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "tr",
                null,
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "th",
                  { colspan: "8" },
                  external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                    "h3",
                    null,
                    element.title
                  )
                )
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "tr",
                null,
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Date Added"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Date Updated"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Size"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Files"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Subjects"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Format"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Modalities"
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  "Sources"
                )
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "tr",
                null,
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.dateAdded
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.dateUpdated
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.size
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.files
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.subjects
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.format
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.modalities
                ),
                external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                  "td",
                  null,
                  element.sources
                )
              )
            )
          ),
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "td",
            null,
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
              alt: "Run On Cbrain",
              className: "run-on-cbrain-button",
              src: element.public || authorized ? run_on_cbrain_green_default.a : run_on_cbrain_gray_default.a,
              onClick: function onClick(event) {
                event.preventDefault();
                if (!(element.public || authorized)) {
                  return;
                }
                onRunWithCBRAIN instanceof Function && onRunWithCBRAIN(event);
              }
            })
          ),
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "td",
            null,
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
              alt: "Run On Cbrain",
              className: "download-button",
              src: element.public || authorized ? download_green_default.a : download_gray_default.a,
              onClick: function onClick(event) {
                event.preventDefault();
                if (!(element.public || authorized)) {
                  return;
                }
                onDownload instanceof Function && onDownload(event);
              }
            })
          )
        );
      })
    ),
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("tfoot", null)
  );
};

data_table_DataTable.propTypes = {
  authorized: prop_types_default.a.bool,
  elements: prop_types_default.a.arrayOf(prop_types_default.a.shape({
    public: prop_types_default.a.bool,
    thumbnailURL: prop_types_default.a.string,
    downloads: prop_types_default.a.number,
    views: prop_types_default.a.number,
    likes: prop_types_default.a.number,
    dateAdded: prop_types_default.a.string,
    dateUpdated: prop_types_default.a.string,
    size: prop_types_default.a.string,
    files: prop_types_default.a.number,
    subjects: prop_types_default.a.number,
    format: prop_types_default.a.string,
    modalities: prop_types_default.a.string,
    sources: prop_types_default.a.number
  })),
  query: prop_types_default.a.shape({
    sort: prop_types_default.a.shape({
      key: prop_types_default.a.string,
      comparitor: prop_types_default.a.string
    }),
    page: prop_types_default.a.number,
    search: prop_types_default.a.string
  }),
  setQuery: prop_types_default.a.func,
  onDownload: prop_types_default.a.func,
  onRunWithCBRAIN: prop_types_default.a.func
};

data_table_DataTable.defaultProps = {};

/* harmony default export */ var data_table = (data_table_DataTable);
// CONCATENATED MODULE: ./src/index.js
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "DataTable", function() { return data_table; });


/***/ })
/******/ ])["default"];
});