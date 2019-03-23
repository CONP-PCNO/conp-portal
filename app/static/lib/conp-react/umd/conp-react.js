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
/******/ 	return __webpack_require__(__webpack_require__.s = 2);
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
  module.exports = __webpack_require__(3)();
}


/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(5);


/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/**
 * Copyright (c) 2013-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */



var ReactPropTypesSecret = __webpack_require__(4);

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
/* 4 */
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
/* 5 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: external {"root":"React","commonjs2":"react","commonjs":"react","amd":"react"}
var external_root_React_commonjs2_react_commonjs_react_amd_react_ = __webpack_require__(0);
var external_root_React_commonjs2_react_commonjs_react_amd_react_default = /*#__PURE__*/__webpack_require__.n(external_root_React_commonjs2_react_commonjs_react_amd_react_);

// EXTERNAL MODULE: ./node_modules/prop-types/index.js
var prop_types = __webpack_require__(1);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);

// CONCATENATED MODULE: ./src/data-table/DataTable.js



var DataTable_DataTable = function DataTable(_ref) {
  var authorized = _ref.authorized,
      elements = _ref.elements,
      query = _ref.query,
      setQuery = _ref.setQuery,
      onDownload = _ref.onDownload,
      onRunWithCBRAIN = _ref.onRunWithCBRAIN,
      imgPath = _ref.imgPath;

  var runOnCbrainEnabled = imgPath + "/run_on_cbrain_green.png";
  var runOnCbrainDisabled = imgPath + "/run_on_cbrain_gray.png";
  var downloadEnabled = imgPath + "/download_green.png";
  var downloadDisabled = imgPath + "/download_gray.png";

  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
    "div",
    { className: "search-dataset-table", cellSpacing: 0 },
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "search-dataset-toolbar" },
      "SEARCH TOOLBAR"
    ),
    elements.map(function (element) {
      return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
        "div",
        { className: "search-dataset" },
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "div",
          { className: "dataset-social" },
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
            alt: "dataset format",
            className: "dataset-social-img",
            src: element.thumbnailURL
          }),
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "div",
            { className: "dataset-social-icons" },
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-social-icon" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-download social-fa" }),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                null,
                element.downloads
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-social-icon" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-eye social-fa" }),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                null,
                element.views
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-social-icon" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-heart social-fa" }),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                null,
                element.likes
              )
            )
          )
        ),
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "div",
          { className: "dataset-details" },
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "div",
            { className: "dataset-details-stats" },
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-title" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                null,
                element.title
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Date Added"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.dateAdded
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Date Updated"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.dateUpdated
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Size"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.size
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Files"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.files
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Subjects"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.subjects
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Format"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.format
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Modalities"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.modalities
              )
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-stat" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-text" },
                "Sources"
              ),
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
                "div",
                { className: "dataset-stat-num" },
                element.sources
              )
            )
          ),
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "div",
            { className: "dataset-options" },
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              { className: "dataset-option" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
                alt: "Run On Cbrain",
                className: "run-on-cbrain-button option-icon",
                src: element.public || authorized ? runOnCbrainEnabled : runOnCbrainDisabled,
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
              "div",
              { className: "dataset-option" },
              external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
                alt: "Run On Cbrain",
                className: "download-button  option-icon",
                src: element.public || authorized ? downloadEnabled : downloadDisabled,
                onClick: function onClick(event) {
                  event.preventDefault();
                  if (!(element.public || authorized)) {
                    return;
                  }
                  onDownload instanceof Function && onDownload(event);
                }
              })
            )
          )
        )
      );
    })
  );
};

DataTable_DataTable.propTypes = {
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

DataTable_DataTable.defaultProps = {
  imgPath: ""
};

/* harmony default export */ var data_table_DataTable = (DataTable_DataTable);

// import React from "react";
// import PropTypes from "prop-types";

// const DataTable = ({
//   authorized,
//   elements,
//   query,
//   setQuery,
//   onDownload,
//   onRunWithCBRAIN,
//   imgPath
// }) => {
//   const runOnCbrainEnabled = `${imgPath}/run_on_cbrain_green.png`;
//   const runOnCbrainDisabled = `${imgPath}/run_on_cbrain_gray.png`;
//   const downloadEnabled = `${imgPath}/download_green.png`;
//   const downloadDisabled = `${imgPath}/download_gray.png`;

//   return (
//     <table className="table data-table row-border" cellSpacing={0}>
//       <thead />
//       <tbody>
//         {elements.map(element => {
//           return (
//             <tr>
//               <td>
//                 <table className="table">
//                   <tbody>
//                     <tr>
//                       <th colSpan={3}>
//                         <img
//                           alt="dataset format"
//                           className="dataset-thumbnail"
//                           src={element.thumbnailURL}
//                         />
//                       </th>
//                     </tr>
//                     <tr>
//                       <td>
//                         <i className="fa fa-download" />
//                       </td>
//                       <td>
//                         <i className="fa fa-eye" />
//                       </td>
//                       <td>
//                         <i className="fa fa-heart" />
//                       </td>
//                     </tr>
//                     <tr>
//                       <td>{element.downloads}</td>
//                       <td>{element.views}</td>
//                       <td>{element.likes}</td>
//                     </tr>
//                   </tbody>
//                 </table>
//               </td>
//               <td>
//                 <table className="table">
//                   <tbody>
//                     <tr>
//                       <th colSpan={8}>
//                         <h3>{element.title}</h3>
//                       </th>
//                     </tr>
//                     <tr>
//                       <td>Date Added</td>
//                       <td>Date Updated</td>
//                       <td>Size</td>
//                       <td>Files</td>
//                       <td>Subjects</td>
//                       <td>Format</td>
//                       <td>Modalities</td>
//                       <td>Sources</td>
//                     </tr>
//                     <tr>
//                       <td>{element.dateAdded}</td>
//                       <td>{element.dateUpdated}</td>
//                       <td>{element.size}</td>
//                       <td>{element.files}</td>
//                       <td>{element.subjects}</td>
//                       <td>{element.format}</td>
//                       <td>{element.modalities}</td>
//                       <td>{element.sources}</td>
//                     </tr>
//                   </tbody>
//                 </table>
//               </td>
//               <td>
//                 <img
//                   alt="Run On Cbrain"
//                   className="run-on-cbrain-button"
//                   src={
//                     element.public || authorized
//                       ? runOnCbrainEnabled
//                       : runOnCbrainDisabled
//                   }
//                   onClick={event => {
//                     event.preventDefault();
//                     if (!(element.public || authorized)) {
//                       return;
//                     }
//                     onRunWithCBRAIN instanceof Function &&
//                       onRunWithCBRAIN(event);
//                   }}
//                 />
//               </td>
//               <td>
//                 <img
//                   alt="Run On Cbrain"
//                   className="download-button"
//                   src={
//                     element.public || authorized
//                       ? downloadEnabled
//                       : downloadDisabled
//                   }
//                   onClick={event => {
//                     event.preventDefault();
//                     if (!(element.public || authorized)) {
//                       return;
//                     }
//                     onDownload instanceof Function && onDownload(event);
//                   }}
//                 />
//               </td>
//             </tr>
//           );
//         })}
//       </tbody>
//       <tfoot />
//     </table>
//   );
// };

// DataTable.propTypes = {
//   authorized: PropTypes.bool,
//   elements: PropTypes.arrayOf(
//     PropTypes.shape({
//       public: PropTypes.bool,
//       thumbnailURL: PropTypes.string,
//       downloads: PropTypes.number,
//       views: PropTypes.number,
//       likes: PropTypes.number,
//       dateAdded: PropTypes.string,
//       dateUpdated: PropTypes.string,
//       size: PropTypes.string,
//       files: PropTypes.number,
//       subjects: PropTypes.number,
//       format: PropTypes.string,
//       modalities: PropTypes.string,
//       sources: PropTypes.number
//     })
//   ),
//   query: PropTypes.shape({
//     sort: PropTypes.shape({
//       key: PropTypes.string,
//       comparitor: PropTypes.string
//     }),
//     page: PropTypes.number,
//     search: PropTypes.string
//   }),
//   setQuery: PropTypes.func,
//   onDownload: PropTypes.func,
//   onRunWithCBRAIN: PropTypes.func
// };

// DataTable.defaultProps = {
//   imgPath: ""
// };

// export default DataTable;
// CONCATENATED MODULE: ./src/data-table/DataTableAJAX.js
function _objectWithoutProperties(obj, keys) { var target = {}; for (var i in obj) { if (keys.indexOf(i) >= 0) continue; if (!Object.prototype.hasOwnProperty.call(obj, i)) continue; target[i] = obj[i]; } return target; }






var DataTableAJAX_DataTableAJAX = function DataTableAJAX(_ref) {
  var baseURL = _ref.baseURL,
      props = _objectWithoutProperties(_ref, ["baseURL"]);

  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(data_table_DataTable, props);
};

DataTableAJAX_DataTableAJAX.propTypes = {
  baseURL: prop_types_default.a.string
};

data_table_DataTable.defaultProps = {};

/* harmony default export */ var data_table_DataTableAJAX = (DataTableAJAX_DataTableAJAX);
// CONCATENATED MODULE: ./src/data-table/index.js


// CONCATENATED MODULE: ./src/index.js
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "DataTable", function() { return data_table_DataTable; });
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "DataTableAJAX", function() { return data_table_DataTableAJAX; });



/* harmony default export */ var src = __webpack_exports__["default"] = ({ DataTable: data_table_DataTable, DataTableAJAX: data_table_DataTableAJAX });

/***/ })
/******/ ])["default"];
});