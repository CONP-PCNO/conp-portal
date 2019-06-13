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
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 	};
/******/
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		0: 0
/******/ 	};
/******/
/******/
/******/
/******/ 	// script path function
/******/ 	function jsonpScriptSrc(chunkId) {
/******/ 		return __webpack_require__.p + "" + chunkId + ".conp-react.js"
/******/ 	}
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
/******/ 	// This file contains only the entry chunk.
/******/ 	// The chunk loading function for additional chunks
/******/ 	__webpack_require__.e = function requireEnsure(chunkId) {
/******/ 		var promises = [];
/******/
/******/
/******/ 		// JSONP chunk loading for javascript
/******/
/******/ 		var installedChunkData = installedChunks[chunkId];
/******/ 		if(installedChunkData !== 0) { // 0 means "already installed".
/******/
/******/ 			// a Promise means "currently loading".
/******/ 			if(installedChunkData) {
/******/ 				promises.push(installedChunkData[2]);
/******/ 			} else {
/******/ 				// setup Promise in chunk cache
/******/ 				var promise = new Promise(function(resolve, reject) {
/******/ 					installedChunkData = installedChunks[chunkId] = [resolve, reject];
/******/ 				});
/******/ 				promises.push(installedChunkData[2] = promise);
/******/
/******/ 				// start chunk loading
/******/ 				var head = document.getElementsByTagName('head')[0];
/******/ 				var script = document.createElement('script');
/******/ 				var onScriptComplete;
/******/
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.src = jsonpScriptSrc(chunkId);
/******/
/******/ 				onScriptComplete = function (event) {
/******/ 					// avoid mem leaks in IE.
/******/ 					script.onerror = script.onload = null;
/******/ 					clearTimeout(timeout);
/******/ 					var chunk = installedChunks[chunkId];
/******/ 					if(chunk !== 0) {
/******/ 						if(chunk) {
/******/ 							var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 							var realSrc = event && event.target && event.target.src;
/******/ 							var error = new Error('Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')');
/******/ 							error.type = errorType;
/******/ 							error.request = realSrc;
/******/ 							chunk[1](error);
/******/ 						}
/******/ 						installedChunks[chunkId] = undefined;
/******/ 					}
/******/ 				};
/******/ 				var timeout = setTimeout(function(){
/******/ 					onScriptComplete({ type: 'timeout', target: script });
/******/ 				}, 120000);
/******/ 				script.onerror = script.onload = onScriptComplete;
/******/ 				head.appendChild(script);
/******/ 			}
/******/ 		}
/******/ 		return Promise.all(promises);
/******/ 	};
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
/******/ 	// on error function for async loading
/******/ 	__webpack_require__.oe = function(err) { console.error(err); throw err; };
/******/
/******/ 	var jsonpArray = window["webpackJsonpCONPReact"] = window["webpackJsonpCONPReact"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 14);
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
  module.exports = __webpack_require__(15)();
}


/***/ }),
/* 2 */
/***/ (function(module, exports) {

/*!
* screenfull
* v4.2.0 - 2019-04-01
* (c) Sindre Sorhus; MIT License
*/
(function () {
	'use strict';

	var document = typeof window !== 'undefined' && typeof window.document !== 'undefined' ? window.document : {};
	var isCommonjs = typeof module !== 'undefined' && module.exports;
	var keyboardAllowed = typeof Element !== 'undefined' && 'ALLOW_KEYBOARD_INPUT' in Element;

	var fn = (function () {
		var val;

		var fnMap = [
			[
				'requestFullscreen',
				'exitFullscreen',
				'fullscreenElement',
				'fullscreenEnabled',
				'fullscreenchange',
				'fullscreenerror'
			],
			// New WebKit
			[
				'webkitRequestFullscreen',
				'webkitExitFullscreen',
				'webkitFullscreenElement',
				'webkitFullscreenEnabled',
				'webkitfullscreenchange',
				'webkitfullscreenerror'

			],
			// Old WebKit (Safari 5.1)
			[
				'webkitRequestFullScreen',
				'webkitCancelFullScreen',
				'webkitCurrentFullScreenElement',
				'webkitCancelFullScreen',
				'webkitfullscreenchange',
				'webkitfullscreenerror'

			],
			[
				'mozRequestFullScreen',
				'mozCancelFullScreen',
				'mozFullScreenElement',
				'mozFullScreenEnabled',
				'mozfullscreenchange',
				'mozfullscreenerror'
			],
			[
				'msRequestFullscreen',
				'msExitFullscreen',
				'msFullscreenElement',
				'msFullscreenEnabled',
				'MSFullscreenChange',
				'MSFullscreenError'
			]
		];

		var i = 0;
		var l = fnMap.length;
		var ret = {};

		for (; i < l; i++) {
			val = fnMap[i];
			if (val && val[1] in document) {
				for (i = 0; i < val.length; i++) {
					ret[fnMap[0][i]] = val[i];
				}
				return ret;
			}
		}

		return false;
	})();

	var eventNameMap = {
		change: fn.fullscreenchange,
		error: fn.fullscreenerror
	};

	var screenfull = {
		request: function (elem) {
			return new Promise(function (resolve) {
				var request = fn.requestFullscreen;

				var onFullScreenEntered = function () {
					this.off('change', onFullScreenEntered);
					resolve();
				}.bind(this);

				elem = elem || document.documentElement;

				// Work around Safari 5.1 bug: reports support for
				// keyboard in fullscreen even though it doesn't.
				// Browser sniffing, since the alternative with
				// setTimeout is even worse.
				if (/ Version\/5\.1(?:\.\d+)? Safari\//.test(navigator.userAgent)) {
					elem[request]();
				} else {
					elem[request](keyboardAllowed ? Element.ALLOW_KEYBOARD_INPUT : {});
				}

				this.on('change', onFullScreenEntered);
			}.bind(this));
		},
		exit: function () {
			return new Promise(function (resolve) {
				if (!this.isFullscreen) {
					resolve();
					return;
				}

				var onFullScreenExit = function () {
					this.off('change', onFullScreenExit);
					resolve();
				}.bind(this);

				document[fn.exitFullscreen]();

				this.on('change', onFullScreenExit);
			}.bind(this));
		},
		toggle: function (elem) {
			return this.isFullscreen ? this.exit() : this.request(elem);
		},
		onchange: function (callback) {
			this.on('change', callback);
		},
		onerror: function (callback) {
			this.on('error', callback);
		},
		on: function (event, callback) {
			var eventName = eventNameMap[event];
			if (eventName) {
				document.addEventListener(eventName, callback, false);
			}
		},
		off: function (event, callback) {
			var eventName = eventNameMap[event];
			if (eventName) {
				document.removeEventListener(eventName, callback, false);
			}
		},
		raw: fn
	};

	if (!fn) {
		if (isCommonjs) {
			module.exports = false;
		} else {
			window.screenfull = false;
		}

		return;
	}

	Object.defineProperties(screenfull, {
		isFullscreen: {
			get: function () {
				return Boolean(document[fn.fullscreenElement]);
			}
		},
		element: {
			enumerable: true,
			get: function () {
				return document[fn.fullscreenElement];
			}
		},
		enabled: {
			enumerable: true,
			get: function () {
				// Coerce to boolean in case of old WebKit
				return Boolean(document[fn.fullscreenEnabled]);
			}
		}
	});

	if (isCommonjs) {
		module.exports = screenfull;
		// TODO: remove this in the next major version
		module.exports.default = screenfull;
	} else {
		window.screenfull = screenfull;
	}
})();


/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(17);


/***/ }),
/* 4 */
/***/ (function(module, exports) {

var g;

// This works in non-strict mode
g = (function() {
	return this;
})();

try {
	// This works if eval is allowed (see CSP)
	g = g || Function("return this")() || (1, eval)("this");
} catch (e) {
	// This works if the window reference is available
	if (typeof window === "object") g = window;
}

// g can still be undefined, but nothing to do about it...
// We return undefined, instead of nothing here, so it's
// easier to handle this case. if(!global) { ...}

module.exports = g;


/***/ }),
/* 5 */
/***/ (function(module, exports) {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };


/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var KEBAB_REGEX = /[A-Z]/g;

var hash = function (str) {
    var hash = 5381, i = str.length;

    while (i) hash = (hash * 33) ^ str.charCodeAt(--i);

    return '_' + (hash >>> 0).toString(36);
};

exports.create = function (config) {
    config = config || {};
    var assign = config.assign || Object.assign;
    var client = typeof window === 'object';

    // Check if we are really in browser environment.
    if (false) {}

    var renderer = assign({
        raw: '',
        pfx: '_',
        client: client,
        assign: assign,
        stringify: JSON.stringify,
        kebab: function (prop) {
            return prop.replace(KEBAB_REGEX, '-$&').toLowerCase();
        },
        decl: function (key, value) {
            key = renderer.kebab(key);
            return key + ':' + value + ';';
        },
        hash: function (obj) {
            return hash(renderer.stringify(obj));
        },
        selector: function (parent, selector) {
            return parent + (selector[0] === ':' ? ''  : ' ') + selector;
        },
        putRaw: function (rawCssRule) {
            renderer.raw += rawCssRule;
        },
    }, config);

    if (renderer.client) {
        if (!renderer.sh)
            document.head.appendChild(renderer.sh = document.createElement('style'));

        if (false) {}

        renderer.putRaw = function (rawCssRule) {
            // .insertRule() is faster than .appendChild(), that's why we use it in PROD.
            // But CSS injected using .insertRule() is not displayed in Chrome Devtools,
            // that's why we use .appendChild in DEV.
            if (true) {
                var sheet = renderer.sh.sheet;

                // Unknown pseudo-selectors will throw, this try/catch swallows all errors.
                try {
                    sheet.insertRule(rawCssRule, sheet.cssRules.length);
                // eslint-disable-next-line no-empty
                } catch (error) {}
            } else {}
        };
    }

    renderer.put = function (selector, decls, atrule) {
        var str = '';
        var prop, value;
        var postponed = [];

        for (prop in decls) {
            value = decls[prop];

            if ((value instanceof Object) && !(value instanceof Array)) {
                postponed.push(prop);
            } else {
                if (false) {} else {
                    str += renderer.decl(prop, value, selector, atrule);
                }
            }
        }

        if (str) {
            if (false) {} else {
                str = selector + '{' + str + '}';
            }
            renderer.putRaw(atrule ? atrule + '{' + str + '}' : str);
        }

        for (var i = 0; i < postponed.length; i++) {
            prop = postponed[i];

            if (prop[0] === "@" && prop !== "@font-face") {
                renderer.putAt(selector, decls[prop], prop);
            } else {
                renderer.put(renderer.selector(selector, prop), decls[prop], atrule);
            }
        }
    };

    renderer.putAt = renderer.put;

    return renderer;
};


/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


exports.addon = function (renderer) {
    // CSSOM support only browser environment.
    if (!renderer.client) return;

    if (false) {}

    // Style sheet for media queries.
    document.head.appendChild(renderer.msh = document.createElement('style'));

    renderer.createRule = function (selector, prelude) {
        var rawCss = selector + '{}';
        if (prelude) rawCss = prelude + '{' + rawCss + '}';
        var sheet = prelude ? renderer.msh.sheet : renderer.sh.sheet;
        var index = sheet.insertRule(rawCss, sheet.cssRules.length);
        var rule = (sheet.cssRules || sheet.rules)[index];

        // Keep track of `index` where rule was inserted in the sheet. This is
        // needed for rule deletion.
        rule.index = index;

        if (prelude) {
            // If rule has media query (it has prelude), move style (CSSStyleDeclaration)
            // object to the "top" to normalize it with a rule without the media
            // query, so that both rules have `.style` property available.
            var selectorRule = (rule.cssRules || rule.rules)[0];
            rule.style = selectorRule.style;
            rule.styleMap = selectorRule.styleMap;
        }

        return rule;
    };
};


/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var removeRule = __webpack_require__(21).removeRule;

exports.addon = function (renderer) {
    // VCSSOM support only browser environment.
    if (!renderer.client) return;

    if (false) {}

    var kebab = renderer.kebab;

    function VRule (selector, prelude) {
        this.rule = renderer.createRule(selector, prelude);
        this.decl = {};
    }
    VRule.prototype.diff = function (newDecl) {
        var oldDecl = this.decl;
        var style = this.rule.style;
        var property;
        for (property in oldDecl)
            if (newDecl[property] === undefined)
                style.removeProperty(property);
        for (property in newDecl)
            if (newDecl[property] !== oldDecl[property])
                style.setProperty(kebab(property), newDecl[property]);
        this.decl = newDecl;
    };
    VRule.prototype.del = function () {
        removeRule(this.rule);
    };

    function VSheet () {
        /**
         * {
         *   '<at-rule-prelude>': {
         *     '<selector>': {
         *       color: 'red
         *     }
         *   }
         * }
         */
        this.tree = {};
    }
    VSheet.prototype.diff = function (newTree) {
        var oldTree = this.tree;

        // Remove media queries not present in new tree.
        for (var prelude in oldTree) {
            if (newTree[prelude] === undefined) {
                var rules = oldTree[prelude];
                for (var selector in rules)
                    rules[selector].del();
            }
        }

        for (var prelude in newTree) {
            if (oldTree[prelude] === undefined) {
                // Whole media query is new.
                for (var selector in newTree[prelude]) {
                    var rule = new VRule(selector, prelude);
                    rule.diff(newTree[prelude][selector]);
                    newTree[prelude][selector] = rule;
                }
            } else {
                // Old tree already has rules with this media query.
                var oldRules = oldTree[prelude];
                var newRules = newTree[prelude];

                // Remove rules not present in new tree.
                for (var selector in oldRules)
                    if (!newRules[selector])
                        oldRules[selector].del();

                // Apply new rules.
                for (var selector in newRules) {
                    var rule = oldRules[selector];
                    if (rule) {
                        rule.diff(newRules[selector]);
                        newRules[selector] = rule;
                    } else {
                        rule = new VRule(selector, prelude);
                        rule.diff(newRules[selector]);
                        newRules[selector] = rule;
                    }
                }
            }
        }

        this.tree = newTree;
    };

    renderer.VRule = VRule;
    renderer.VSheet = VSheet;
};


/***/ }),
/* 9 */
/***/ (function(module, exports) {

function cssToTree (tree, css, selector, prelude) {
    var declarations = {};
    var hasDeclarations = false;
    var key, value;

    for (key in css) {
        value = css[key];
        if (typeof value !== 'object') {
            hasDeclarations = true;
            declarations[key] = value;
        }
    }

    if (hasDeclarations) {
        if (!tree[prelude]) tree[prelude] = {};
        tree[prelude][selector] = declarations;
    }

    for (key in css) {
        value = css[key];
        if (typeof value === 'object') {
            if (key[0] === '@') {
                cssToTree(tree, value, selector, key);
            } else {
                var hasCurrentSymbol = key.indexOf('&') > -1;
                var selectorParts = selector.split(',');
                if (hasCurrentSymbol) {
                    for (var i = 0; i < selectorParts.length; i++) {
                        selectorParts[i] = key.replace(/&/g, selectorParts[i]);
                    }
                } else {
                    for (var i = 0; i < selectorParts.length; i++) {
                        selectorParts[i] = selectorParts[i] + ' ' + key;
                    }
                }
                cssToTree(tree, value, selectorParts.join(','), prelude);
            }
        }
    }
};

exports.cssToTree = cssToTree;


/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var isArray = Array.isArray;
var keyList = Object.keys;
var hasProp = Object.prototype.hasOwnProperty;
var hasElementType = typeof Element !== 'undefined';

function equal(a, b) {
  // fast-deep-equal index.js 2.0.1
  if (a === b) return true;

  if (a && b && typeof a == 'object' && typeof b == 'object') {
    var arrA = isArray(a)
      , arrB = isArray(b)
      , i
      , length
      , key;

    if (arrA && arrB) {
      length = a.length;
      if (length != b.length) return false;
      for (i = length; i-- !== 0;)
        if (!equal(a[i], b[i])) return false;
      return true;
    }

    if (arrA != arrB) return false;

    var dateA = a instanceof Date
      , dateB = b instanceof Date;
    if (dateA != dateB) return false;
    if (dateA && dateB) return a.getTime() == b.getTime();

    var regexpA = a instanceof RegExp
      , regexpB = b instanceof RegExp;
    if (regexpA != regexpB) return false;
    if (regexpA && regexpB) return a.toString() == b.toString();

    var keys = keyList(a);
    length = keys.length;

    if (length !== keyList(b).length)
      return false;

    for (i = length; i-- !== 0;)
      if (!hasProp.call(b, keys[i])) return false;
    // end fast-deep-equal

    // start react-fast-compare
    // custom handling for DOM elements
    if (hasElementType && a instanceof Element && b instanceof Element)
      return a === b;

    // custom handling for React
    for (i = length; i-- !== 0;) {
      key = keys[i];
      if (key === '_owner' && a.$$typeof) {
        // React-specific: avoid traversing React elements' _owner.
        //  _owner contains circular references
        // and is not needed when comparing the actual elements (and not their owners)
        // .$$typeof and ._store on just reasonable markers of a react element
        continue;
      } else {
        // all other properties should be traversed as usual
        if (!equal(a[key], b[key])) return false;
      }
    }
    // end react-fast-compare

    // fast-deep-equal index.js 2.0.1
    return true;
  }

  return a !== a && b !== b;
}
// end fast-deep-equal

module.exports = function exportedEqual(a, b) {
  try {
    return equal(a, b);
  } catch (error) {
    if ((error.message && error.message.match(/stack|recursion/i)) || (error.number === -2146828260)) {
      // warn on circular references, don't crash
      // browsers give this different errors name and messages:
      // chrome/safari: "RangeError", "Maximum call stack size exceeded"
      // firefox: "InternalError", too much recursion"
      // edge: "Error", "Out of stack space"
      console.warn('Warning: react-fast-compare does not handle circular references.', error.name, error.message);
      return false;
    }
    // some other error. we should definitely know about these
    throw error;
  }
};


/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(process, setImmediate) {/**
 *  Copyright (c) 2013, Facebook, Inc.
 *  All rights reserved.
 *
 *  This source code is licensed under the BSD-style license found in the
 *  LICENSE file in the root directory of this source tree. An additional grant
 *  of patent rights can be found in the PATENTS file in the same directory.
 */
(function (global, factory) {
	 true ? module.exports = factory() :
	undefined;
}(this, (function () { 'use strict';

var _onFrame = void 0;
if (typeof window !== 'undefined') {
  _onFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame || window.oRequestAnimationFrame;
}

if (!_onFrame && typeof process !== 'undefined' && process.title === 'node') {
  _onFrame = setImmediate;
}

_onFrame = _onFrame || function (callback) {
  window.setTimeout(callback, 1000 / 60);
};

var _onFrame$1 = _onFrame;

/* eslint-disable flowtype/no-weak-types */

var concat = Array.prototype.concat;
var slice = Array.prototype.slice;

// Bind a function to a context object.
function bind(func, context) {
  for (var _len = arguments.length, outerArgs = Array(_len > 2 ? _len - 2 : 0), _key = 2; _key < _len; _key++) {
    outerArgs[_key - 2] = arguments[_key];
  }

  return function () {
    for (var _len2 = arguments.length, innerArgs = Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
      innerArgs[_key2] = arguments[_key2];
    }

    func.apply(context, concat.call(outerArgs, slice.call(innerArgs)));
  };
}

// Add all the properties in the source to the target.
function extend(target, source) {
  for (var key in source) {
    if (source.hasOwnProperty(key)) {
      target[key] = source[key];
    }
  }
}

// Cross browser/node timer functions.
function onFrame(func) {
  return _onFrame$1(func);
}

// Lop off the first occurence of the reference in the Array.
function removeFirst(array, item) {
  var idx = array.indexOf(item);
  idx !== -1 && array.splice(idx, 1);
}

var colorCache = {};
/**
 * Converts a hex-formatted color string to its rgb-formatted equivalent. Handy
 * when performing color tweening animations
 * @public
 * @param colorString A hex-formatted color string
 * @return An rgb-formatted color string
 */
function hexToRGB(colorString) {
  if (colorCache[colorString]) {
    return colorCache[colorString];
  }
  var normalizedColor = colorString.replace('#', '');
  if (normalizedColor.length === 3) {
    normalizedColor = normalizedColor[0] + normalizedColor[0] + normalizedColor[1] + normalizedColor[1] + normalizedColor[2] + normalizedColor[2];
  }
  var parts = normalizedColor.match(/.{2}/g);
  if (!parts || parts.length < 3) {
    throw new Error('Expected a color string of format #rrggbb');
  }

  var ret = {
    r: parseInt(parts[0], 16),
    g: parseInt(parts[1], 16),
    b: parseInt(parts[2], 16)
  };

  colorCache[colorString] = ret;
  return ret;
}

/**
 * Converts a rgb-formatted color string to its hex-formatted equivalent. Handy
 * when performing color tweening animations
 * @public
 * @param colorString An rgb-formatted color string
 * @return A hex-formatted color string
 */
function rgbToHex(rNum, gNum, bNum) {
  var r = rNum.toString(16);
  var g = gNum.toString(16);
  var b = bNum.toString(16);
  r = r.length < 2 ? '0' + r : r;
  g = g.length < 2 ? '0' + g : g;
  b = b.length < 2 ? '0' + b : b;
  return '#' + r + g + b;
}

var util = Object.freeze({
	bind: bind,
	extend: extend,
	onFrame: onFrame,
	removeFirst: removeFirst,
	hexToRGB: hexToRGB,
	rgbToHex: rgbToHex
});

/**
 * This helper function does a linear interpolation of a value from
 * one range to another. This can be very useful for converting the
 * motion of a Spring to a range of UI property values. For example a
 * spring moving from position 0 to 1 could be interpolated to move a
 * view from pixel 300 to 350 and scale it from 0.5 to 1. The current
 * position of the `Spring` just needs to be run through this method
 * taking its input range in the _from_ parameters with the property
 * animation range in the _to_ parameters.
 * @public
 */
function mapValueInRange(value, fromLow, fromHigh, toLow, toHigh) {
  var fromRangeSize = fromHigh - fromLow;
  var toRangeSize = toHigh - toLow;
  var valueScale = (value - fromLow) / fromRangeSize;
  return toLow + valueScale * toRangeSize;
}

/**
 * Interpolate two hex colors in a 0 - 1 range or optionally provide a
 * custom range with fromLow,fromHight. The output will be in hex by default
 * unless asRGB is true in which case it will be returned as an rgb string.
 *
 * @public
 * @param asRGB Whether to return an rgb-style string
 * @return A string in hex color format unless asRGB is true, in which case a string in rgb format
 */
function interpolateColor(val, startColorStr, endColorStr) {
  var fromLow = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : 0;
  var fromHigh = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : 1;
  var asRGB = arguments[5];

  var startColor = hexToRGB(startColorStr);
  var endColor = hexToRGB(endColorStr);
  var r = Math.floor(mapValueInRange(val, fromLow, fromHigh, startColor.r, endColor.r));
  var g = Math.floor(mapValueInRange(val, fromLow, fromHigh, startColor.g, endColor.g));
  var b = Math.floor(mapValueInRange(val, fromLow, fromHigh, startColor.b, endColor.b));
  if (asRGB) {
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  } else {
    return rgbToHex(r, g, b);
  }
}

function degreesToRadians(deg) {
  return deg * Math.PI / 180;
}

function radiansToDegrees(rad) {
  return rad * 180 / Math.PI;
}

var MathUtil = Object.freeze({
	mapValueInRange: mapValueInRange,
	interpolateColor: interpolateColor,
	degreesToRadians: degreesToRadians,
	radiansToDegrees: radiansToDegrees
});

// Math for converting from
// [Origami](http://facebook.github.io/origami/) to
// [Rebound](http://facebook.github.io/rebound).
// You mostly don't need to worry about this, just use
// SpringConfig.fromOrigamiTensionAndFriction(v, v);

function tensionFromOrigamiValue(oValue) {
  return (oValue - 30.0) * 3.62 + 194.0;
}

function origamiValueFromTension(tension) {
  return (tension - 194.0) / 3.62 + 30.0;
}

function frictionFromOrigamiValue(oValue) {
  return (oValue - 8.0) * 3.0 + 25.0;
}

function origamiFromFriction(friction) {
  return (friction - 25.0) / 3.0 + 8.0;
}

var OrigamiValueConverter = Object.freeze({
	tensionFromOrigamiValue: tensionFromOrigamiValue,
	origamiValueFromTension: origamiValueFromTension,
	frictionFromOrigamiValue: frictionFromOrigamiValue,
	origamiFromFriction: origamiFromFriction
});

var classCallCheck = function (instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
};









var _extends = Object.assign || function (target) {
  for (var i = 1; i < arguments.length; i++) {
    var source = arguments[i];

    for (var key in source) {
      if (Object.prototype.hasOwnProperty.call(source, key)) {
        target[key] = source[key];
      }
    }
  }

  return target;
};

/**
 * Plays each frame of the SpringSystem on animation
 * timing loop. This is the default type of looper for a new spring system
 * as it is the most common when developing UI.
 * @public
 */
/**
 *  Copyright (c) 2013, Facebook, Inc.
 *  All rights reserved.
 *
 *  This source code is licensed under the BSD-style license found in the
 *  LICENSE file in the root directory of this source tree. An additional grant
 *  of patent rights can be found in the PATENTS file in the same directory.
 *
 * 
 */

var AnimationLooper = function () {
  function AnimationLooper() {
    classCallCheck(this, AnimationLooper);
    this.springSystem = null;
  }

  AnimationLooper.prototype.run = function run() {
    var springSystem = getSpringSystem.call(this);

    onFrame(function () {
      springSystem.loop(Date.now());
    });
  };

  return AnimationLooper;
}();

/**
 * Resolves the SpringSystem to a resting state in a
 * tight and blocking loop. This is useful for synchronously generating
 * pre-recorded animations that can then be played on a timing loop later.
 * Sometimes this lead to better performance to pre-record a single spring
 * curve and use it to drive many animations; however, it can make dynamic
 * response to user input a bit trickier to implement.
 * @public
 */
var SimulationLooper = function () {
  function SimulationLooper(timestep) {
    classCallCheck(this, SimulationLooper);
    this.springSystem = null;
    this.time = 0;
    this.running = false;

    this.timestep = timestep || 16.667;
  }

  SimulationLooper.prototype.run = function run() {
    var springSystem = getSpringSystem.call(this);

    if (this.running) {
      return;
    }
    this.running = true;
    while (!springSystem.getIsIdle()) {
      springSystem.loop(this.time += this.timestep);
    }
    this.running = false;
  };

  return SimulationLooper;
}();

/**
 * Resolves the SpringSystem one step at a
 * time controlled by an outside loop. This is useful for testing and
 * verifying the behavior of a SpringSystem or if you want to control your own
 * timing loop for some reason e.g. slowing down or speeding up the
 * simulation.
 * @public
 */
var SteppingSimulationLooper = function () {
  function SteppingSimulationLooper() {
    classCallCheck(this, SteppingSimulationLooper);
    this.springSystem = null;
    this.time = 0;
    this.running = false;
  }

  SteppingSimulationLooper.prototype.run = function run() {}
  // this.run is NOOP'd here to allow control from the outside using
  // this.step.


  // Perform one step toward resolving the SpringSystem.
  ;

  SteppingSimulationLooper.prototype.step = function step(timestep) {
    var springSystem = getSpringSystem.call(this);
    springSystem.loop(this.time += timestep);
  };

  return SteppingSimulationLooper;
}();

function getSpringSystem() {
  if (this.springSystem == null) {
    throw new Error('cannot run looper without a springSystem');
  }
  return this.springSystem;
}



var Loopers = Object.freeze({
	AnimationLooper: AnimationLooper,
	SimulationLooper: SimulationLooper,
	SteppingSimulationLooper: SteppingSimulationLooper
});

/**
 * Provides math for converting from Origami PopAnimation
 * config values to regular Origami tension and friction values. If you are
 * trying to replicate prototypes made with PopAnimation patches in Origami,
 * then you should create your springs with
 * SpringSystem.createSpringWithBouncinessAndSpeed, which uses this Math
 * internally to create a spring to match the provided PopAnimation
 * configuration from Origami.
 */
var BouncyConversion = function () {
  function BouncyConversion(bounciness, speed) {
    classCallCheck(this, BouncyConversion);

    this.bounciness = bounciness;
    this.speed = speed;

    var b = this.normalize(bounciness / 1.7, 0, 20.0);
    b = this.projectNormal(b, 0.0, 0.8);
    var s = this.normalize(speed / 1.7, 0, 20.0);

    this.bouncyTension = this.projectNormal(s, 0.5, 200);
    this.bouncyFriction = this.quadraticOutInterpolation(b, this.b3Nobounce(this.bouncyTension), 0.01);
  }

  BouncyConversion.prototype.normalize = function normalize(value, startValue, endValue) {
    return (value - startValue) / (endValue - startValue);
  };

  BouncyConversion.prototype.projectNormal = function projectNormal(n, start, end) {
    return start + n * (end - start);
  };

  BouncyConversion.prototype.linearInterpolation = function linearInterpolation(t, start, end) {
    return t * end + (1.0 - t) * start;
  };

  BouncyConversion.prototype.quadraticOutInterpolation = function quadraticOutInterpolation(t, start, end) {
    return this.linearInterpolation(2 * t - t * t, start, end);
  };

  BouncyConversion.prototype.b3Friction1 = function b3Friction1(x) {
    return 0.0007 * Math.pow(x, 3) - 0.031 * Math.pow(x, 2) + 0.64 * x + 1.28;
  };

  BouncyConversion.prototype.b3Friction2 = function b3Friction2(x) {
    return 0.000044 * Math.pow(x, 3) - 0.006 * Math.pow(x, 2) + 0.36 * x + 2;
  };

  BouncyConversion.prototype.b3Friction3 = function b3Friction3(x) {
    return 0.00000045 * Math.pow(x, 3) - 0.000332 * Math.pow(x, 2) + 0.1078 * x + 5.84;
  };

  BouncyConversion.prototype.b3Nobounce = function b3Nobounce(tension) {
    var friction = 0;
    if (tension <= 18) {
      friction = this.b3Friction1(tension);
    } else if (tension > 18 && tension <= 44) {
      friction = this.b3Friction2(tension);
    } else {
      friction = this.b3Friction3(tension);
    }
    return friction;
  };

  return BouncyConversion;
}();

/**
 * Maintains a set of tension and friction constants
 * for a Spring. You can use fromOrigamiTensionAndFriction to convert
 * values from the [Origami](http://facebook.github.io/origami/)
 * design tool directly to Rebound spring constants.
 * @public
 */

var SpringConfig = function () {

  /**
   * Convert an origami Spring tension and friction to Rebound spring
   * constants. If you are prototyping a design with Origami, this
   * makes it easy to make your springs behave exactly the same in
   * Rebound.
   * @public
   */
  SpringConfig.fromOrigamiTensionAndFriction = function fromOrigamiTensionAndFriction(tension, friction) {
    return new SpringConfig(tensionFromOrigamiValue(tension), frictionFromOrigamiValue(friction));
  };

  /**
   * Convert an origami PopAnimation Spring bounciness and speed to Rebound
   * spring constants. If you are using PopAnimation patches in Origami, this
   * utility will provide springs that match your prototype.
   * @public
   */


  SpringConfig.fromBouncinessAndSpeed = function fromBouncinessAndSpeed(bounciness, speed) {
    var bouncyConversion = new BouncyConversion(bounciness, speed);
    return SpringConfig.fromOrigamiTensionAndFriction(bouncyConversion.bouncyTension, bouncyConversion.bouncyFriction);
  };

  /**
   * Create a SpringConfig with no tension or a coasting spring with some
   * amount of Friction so that it does not coast infininitely.
   * @public
   */


  SpringConfig.coastingConfigWithOrigamiFriction = function coastingConfigWithOrigamiFriction(friction) {
    return new SpringConfig(0, frictionFromOrigamiValue(friction));
  };

  function SpringConfig(tension, friction) {
    classCallCheck(this, SpringConfig);

    this.tension = tension;
    this.friction = friction;
  }

  return SpringConfig;
}();

SpringConfig.DEFAULT_ORIGAMI_SPRING_CONFIG = SpringConfig.fromOrigamiTensionAndFriction(40, 7);

/**
 * Consists of a position and velocity. A Spring uses
 * this internally to keep track of its current and prior position and
 * velocity values.
 */
var PhysicsState = function PhysicsState() {
  classCallCheck(this, PhysicsState);
  this.position = 0;
  this.velocity = 0;
};

/**
 * Provides a model of a classical spring acting to
 * resolve a body to equilibrium. Springs have configurable
 * tension which is a force multipler on the displacement of the
 * spring from its rest point or `endValue` as defined by [Hooke's
 * law](http://en.wikipedia.org/wiki/Hooke's_law). Springs also have
 * configurable friction, which ensures that they do not oscillate
 * infinitely. When a Spring is displaced by updating it's resting
 * or `currentValue`, the SpringSystems that contain that Spring
 * will automatically start looping to solve for equilibrium. As each
 * timestep passes, `SpringListener` objects attached to the Spring
 * will be notified of the updates providing a way to drive an
 * animation off of the spring's resolution curve.
 * @public
 */

var Spring = function () {
  function Spring(springSystem) {
    classCallCheck(this, Spring);
    this.listeners = [];
    this._startValue = 0;
    this._currentState = new PhysicsState();
    this._displacementFromRestThreshold = 0.001;
    this._endValue = 0;
    this._overshootClampingEnabled = false;
    this._previousState = new PhysicsState();
    this._restSpeedThreshold = 0.001;
    this._tempState = new PhysicsState();
    this._timeAccumulator = 0;
    this._wasAtRest = true;

    this._id = 's' + Spring._ID++;
    this._springSystem = springSystem;
  }

  /**
   * Remove a Spring from simulation and clear its listeners.
   * @public
   */


  Spring.prototype.destroy = function destroy() {
    this.listeners = [];
    this._springSystem.deregisterSpring(this);
  };

  /**
   * Get the id of the spring, which can be used to retrieve it from
   * the SpringSystems it participates in later.
   * @public
   */


  Spring.prototype.getId = function getId() {
    return this._id;
  };

  /**
   * Set the configuration values for this Spring. A SpringConfig
   * contains the tension and friction values used to solve for the
   * equilibrium of the Spring in the physics loop.
   * @public
   */


  Spring.prototype.setSpringConfig = function setSpringConfig(springConfig) {
    this._springConfig = springConfig;
    return this;
  };

  /**
   * Retrieve the SpringConfig used by this Spring.
   * @public
   */


  Spring.prototype.getSpringConfig = function getSpringConfig() {
    return this._springConfig;
  };

  /**
   * Set the current position of this Spring. Listeners will be updated
   * with this value immediately. If the rest or `endValue` is not
   * updated to match this value, then the spring will be dispalced and
   * the SpringSystem will start to loop to restore the spring to the
   * `endValue`.
   *
   * A common pattern is to move a Spring around without animation by
   * calling.
   *
   * ```
   * spring.setCurrentValue(n).setAtRest();
   * ```
   *
   * This moves the Spring to a new position `n`, sets the endValue
   * to `n`, and removes any velocity from the `Spring`. By doing
   * this you can allow the `SpringListener` to manage the position
   * of UI elements attached to the spring even when moving without
   * animation. For example, when dragging an element you can
   * update the position of an attached view through a spring
   * by calling `spring.setCurrentValue(x)`. When
   * the gesture ends you can update the Springs
   * velocity and endValue
   * `spring.setVelocity(gestureEndVelocity).setEndValue(flingTarget)`
   * to cause it to naturally animate the UI element to the resting
   * position taking into account existing velocity. The codepaths for
   * synchronous movement and spring driven animation can
   * be unified using this technique.
   * @public
   */


  Spring.prototype.setCurrentValue = function setCurrentValue(currentValue, skipSetAtRest) {
    this._startValue = currentValue;
    this._currentState.position = currentValue;
    if (!skipSetAtRest) {
      this.setAtRest();
    }
    this.notifyPositionUpdated(false, false);
    return this;
  };

  /**
   * Get the position that the most recent animation started at. This
   * can be useful for determining the number off oscillations that
   * have occurred.
   * @public
   */


  Spring.prototype.getStartValue = function getStartValue() {
    return this._startValue;
  };

  /**
   * Retrieve the current value of the Spring.
   * @public
   */


  Spring.prototype.getCurrentValue = function getCurrentValue() {
    return this._currentState.position;
  };

  /**
   * Get the absolute distance of the Spring from its resting endValue
   * position.
   * @public
   */


  Spring.prototype.getCurrentDisplacementDistance = function getCurrentDisplacementDistance() {
    return this.getDisplacementDistanceForState(this._currentState);
  };

  /**
   * Get the absolute distance of the Spring from a given state value
   */


  Spring.prototype.getDisplacementDistanceForState = function getDisplacementDistanceForState(state) {
    return Math.abs(this._endValue - state.position);
  };

  /**
   * Set the endValue or resting position of the spring. If this
   * value is different than the current value, the SpringSystem will
   * be notified and will begin running its solver loop to resolve
   * the Spring to equilibrium. Any listeners that are registered
   * for onSpringEndStateChange will also be notified of this update
   * immediately.
   * @public
   */


  Spring.prototype.setEndValue = function setEndValue(endValue) {
    if (this._endValue === endValue && this.isAtRest()) {
      return this;
    }
    this._startValue = this.getCurrentValue();
    this._endValue = endValue;
    this._springSystem.activateSpring(this.getId());
    for (var i = 0, len = this.listeners.length; i < len; i++) {
      var listener = this.listeners[i];
      var onChange = listener.onSpringEndStateChange;
      onChange && onChange(this);
    }
    return this;
  };

  /**
   * Retrieve the endValue or resting position of this spring.
   * @public
   */


  Spring.prototype.getEndValue = function getEndValue() {
    return this._endValue;
  };

  /**
   * Set the current velocity of the Spring, in pixels per second. As
   * previously mentioned, this can be useful when you are performing
   * a direct manipulation gesture. When a UI element is released you
   * may call setVelocity on its animation Spring so that the Spring
   * continues with the same velocity as the gesture ended with. The
   * friction, tension, and displacement of the Spring will then
   * govern its motion to return to rest on a natural feeling curve.
   * @public
   */


  Spring.prototype.setVelocity = function setVelocity(velocity) {
    if (velocity === this._currentState.velocity) {
      return this;
    }
    this._currentState.velocity = velocity;
    this._springSystem.activateSpring(this.getId());
    return this;
  };

  /**
   * Get the current velocity of the Spring, in pixels per second.
   * @public
   */


  Spring.prototype.getVelocity = function getVelocity() {
    return this._currentState.velocity;
  };

  /**
   * Set a threshold value for the movement speed of the Spring below
   * which it will be considered to be not moving or resting.
   * @public
   */


  Spring.prototype.setRestSpeedThreshold = function setRestSpeedThreshold(restSpeedThreshold) {
    this._restSpeedThreshold = restSpeedThreshold;
    return this;
  };

  /**
   * Retrieve the rest speed threshold for this Spring.
   * @public
   */


  Spring.prototype.getRestSpeedThreshold = function getRestSpeedThreshold() {
    return this._restSpeedThreshold;
  };

  /**
   * Set a threshold value for displacement below which the Spring
   * will be considered to be not displaced i.e. at its resting
   * `endValue`.
   * @public
   */


  Spring.prototype.setRestDisplacementThreshold = function setRestDisplacementThreshold(displacementFromRestThreshold) {
    this._displacementFromRestThreshold = displacementFromRestThreshold;
  };

  /**
   * Retrieve the rest displacement threshold for this spring.
   * @public
   */


  Spring.prototype.getRestDisplacementThreshold = function getRestDisplacementThreshold() {
    return this._displacementFromRestThreshold;
  };

  /**
   * Enable overshoot clamping. This means that the Spring will stop
   * immediately when it reaches its resting position regardless of
   * any existing momentum it may have. This can be useful for certain
   * types of animations that should not oscillate such as a scale
   * down to 0 or alpha fade.
   * @public
   */


  Spring.prototype.setOvershootClampingEnabled = function setOvershootClampingEnabled(enabled) {
    this._overshootClampingEnabled = enabled;
    return this;
  };

  /**
   * Check if overshoot clamping is enabled for this spring.
   * @public
   */


  Spring.prototype.isOvershootClampingEnabled = function isOvershootClampingEnabled() {
    return this._overshootClampingEnabled;
  };

  /**
   * Check if the Spring has gone past its end point by comparing
   * the direction it was moving in when it started to the current
   * position and end value.
   * @public
   */


  Spring.prototype.isOvershooting = function isOvershooting() {
    var start = this._startValue;
    var end = this._endValue;
    return this._springConfig.tension > 0 && (start < end && this.getCurrentValue() > end || start > end && this.getCurrentValue() < end);
  };

  /**
   * The main solver method for the Spring. It takes
   * the current time and delta since the last time step and performs
   * an RK4 integration to get the new position and velocity state
   * for the Spring based on the tension, friction, velocity, and
   * displacement of the Spring.
   * @public
   */


  Spring.prototype.advance = function advance(time, realDeltaTime) {
    var isAtRest = this.isAtRest();

    if (isAtRest && this._wasAtRest) {
      return;
    }

    var adjustedDeltaTime = realDeltaTime;
    if (realDeltaTime > Spring.MAX_DELTA_TIME_SEC) {
      adjustedDeltaTime = Spring.MAX_DELTA_TIME_SEC;
    }

    this._timeAccumulator += adjustedDeltaTime;

    var tension = this._springConfig.tension;
    var friction = this._springConfig.friction;
    var position = this._currentState.position;
    var velocity = this._currentState.velocity;
    var tempPosition = this._tempState.position;
    var tempVelocity = this._tempState.velocity;
    var aVelocity = void 0;
    var aAcceleration = void 0;
    var bVelocity = void 0;
    var bAcceleration = void 0;
    var cVelocity = void 0;
    var cAcceleration = void 0;
    var dVelocity = void 0;
    var dAcceleration = void 0;
    var dxdt = void 0;
    var dvdt = void 0;

    while (this._timeAccumulator >= Spring.SOLVER_TIMESTEP_SEC) {
      this._timeAccumulator -= Spring.SOLVER_TIMESTEP_SEC;

      if (this._timeAccumulator < Spring.SOLVER_TIMESTEP_SEC) {
        this._previousState.position = position;
        this._previousState.velocity = velocity;
      }

      aVelocity = velocity;
      aAcceleration = tension * (this._endValue - tempPosition) - friction * velocity;

      tempPosition = position + aVelocity * Spring.SOLVER_TIMESTEP_SEC * 0.5;
      tempVelocity = velocity + aAcceleration * Spring.SOLVER_TIMESTEP_SEC * 0.5;
      bVelocity = tempVelocity;
      bAcceleration = tension * (this._endValue - tempPosition) - friction * tempVelocity;

      tempPosition = position + bVelocity * Spring.SOLVER_TIMESTEP_SEC * 0.5;
      tempVelocity = velocity + bAcceleration * Spring.SOLVER_TIMESTEP_SEC * 0.5;
      cVelocity = tempVelocity;
      cAcceleration = tension * (this._endValue - tempPosition) - friction * tempVelocity;

      tempPosition = position + cVelocity * Spring.SOLVER_TIMESTEP_SEC;
      tempVelocity = velocity + cAcceleration * Spring.SOLVER_TIMESTEP_SEC;
      dVelocity = tempVelocity;
      dAcceleration = tension * (this._endValue - tempPosition) - friction * tempVelocity;

      dxdt = 1.0 / 6.0 * (aVelocity + 2.0 * (bVelocity + cVelocity) + dVelocity);
      dvdt = 1.0 / 6.0 * (aAcceleration + 2.0 * (bAcceleration + cAcceleration) + dAcceleration);

      position += dxdt * Spring.SOLVER_TIMESTEP_SEC;
      velocity += dvdt * Spring.SOLVER_TIMESTEP_SEC;
    }

    this._tempState.position = tempPosition;
    this._tempState.velocity = tempVelocity;

    this._currentState.position = position;
    this._currentState.velocity = velocity;

    if (this._timeAccumulator > 0) {
      this._interpolate(this._timeAccumulator / Spring.SOLVER_TIMESTEP_SEC);
    }

    if (this.isAtRest() || this._overshootClampingEnabled && this.isOvershooting()) {
      if (this._springConfig.tension > 0) {
        this._startValue = this._endValue;
        this._currentState.position = this._endValue;
      } else {
        this._endValue = this._currentState.position;
        this._startValue = this._endValue;
      }
      this.setVelocity(0);
      isAtRest = true;
    }

    var notifyActivate = false;
    if (this._wasAtRest) {
      this._wasAtRest = false;
      notifyActivate = true;
    }

    var notifyAtRest = false;
    if (isAtRest) {
      this._wasAtRest = true;
      notifyAtRest = true;
    }

    this.notifyPositionUpdated(notifyActivate, notifyAtRest);
  };

  Spring.prototype.notifyPositionUpdated = function notifyPositionUpdated(notifyActivate, notifyAtRest) {
    for (var i = 0, len = this.listeners.length; i < len; i++) {
      var listener = this.listeners[i];
      if (notifyActivate && listener.onSpringActivate) {
        listener.onSpringActivate(this);
      }

      if (listener.onSpringUpdate) {
        listener.onSpringUpdate(this);
      }

      if (notifyAtRest && listener.onSpringAtRest) {
        listener.onSpringAtRest(this);
      }
    }
  };

  /**
   * Check if the SpringSystem should advance. Springs are advanced
   * a final frame after they reach equilibrium to ensure that the
   * currentValue is exactly the requested endValue regardless of the
   * displacement threshold.
   * @public
   */


  Spring.prototype.systemShouldAdvance = function systemShouldAdvance() {
    return !this.isAtRest() || !this.wasAtRest();
  };

  Spring.prototype.wasAtRest = function wasAtRest() {
    return this._wasAtRest;
  };

  /**
   * Check if the Spring is atRest meaning that it's currentValue and
   * endValue are the same and that it has no velocity. The previously
   * described thresholds for speed and displacement define the bounds
   * of this equivalence check. If the Spring has 0 tension, then it will
   * be considered at rest whenever its absolute velocity drops below the
   * restSpeedThreshold.
   * @public
   */


  Spring.prototype.isAtRest = function isAtRest() {
    return Math.abs(this._currentState.velocity) < this._restSpeedThreshold && (this.getDisplacementDistanceForState(this._currentState) <= this._displacementFromRestThreshold || this._springConfig.tension === 0);
  };

  /**
   * Force the spring to be at rest at its current position. As
   * described in the documentation for setCurrentValue, this method
   * makes it easy to do synchronous non-animated updates to ui
   * elements that are attached to springs via SpringListeners.
   * @public
   */


  Spring.prototype.setAtRest = function setAtRest() {
    this._endValue = this._currentState.position;
    this._tempState.position = this._currentState.position;
    this._currentState.velocity = 0;
    return this;
  };

  Spring.prototype._interpolate = function _interpolate(alpha) {
    this._currentState.position = this._currentState.position * alpha + this._previousState.position * (1 - alpha);
    this._currentState.velocity = this._currentState.velocity * alpha + this._previousState.velocity * (1 - alpha);
  };

  Spring.prototype.getListeners = function getListeners() {
    return this.listeners;
  };

  Spring.prototype.addListener = function addListener(newListener) {
    this.listeners.push(newListener);
    return this;
  };

  Spring.prototype.removeListener = function removeListener(listenerToRemove) {
    removeFirst(this.listeners, listenerToRemove);
    return this;
  };

  Spring.prototype.removeAllListeners = function removeAllListeners() {
    this.listeners = [];
    return this;
  };

  Spring.prototype.currentValueIsApproximately = function currentValueIsApproximately(value) {
    return Math.abs(this.getCurrentValue() - value) <= this.getRestDisplacementThreshold();
  };

  return Spring;
}();

Spring._ID = 0;
Spring.MAX_DELTA_TIME_SEC = 0.064;
Spring.SOLVER_TIMESTEP_SEC = 0.001;

/**
 * A set of Springs that all run on the same physics
 * timing loop. To get started with a Rebound animation, first
 * create a new SpringSystem and then add springs to it.
 * @public
 */

var SpringSystem = function () {
  function SpringSystem(looper) {
    classCallCheck(this, SpringSystem);
    this.listeners = [];
    this._activeSprings = [];
    this._idleSpringIndices = [];
    this._isIdle = true;
    this._lastTimeMillis = -1;
    this._springRegistry = {};

    this.looper = looper || new AnimationLooper();
    this.looper.springSystem = this;
  }

  /**
   * A SpringSystem is iterated by a looper. The looper is responsible
   * for executing each frame as the SpringSystem is resolved to idle.
   * There are three types of Loopers described below AnimationLooper,
   * SimulationLooper, and SteppingSimulationLooper. AnimationLooper is
   * the default as it is the most useful for common UI animations.
   * @public
   */


  SpringSystem.prototype.setLooper = function setLooper(looper) {
    this.looper = looper;
    looper.springSystem = this;
  };

  /**
   * Add a new spring to this SpringSystem. This Spring will now be solved for
   * during the physics iteration loop. By default the spring will use the
   * default Origami spring config with 40 tension and 7 friction, but you can
   * also provide your own values here.
   * @public
   */


  SpringSystem.prototype.createSpring = function createSpring(tension, friction) {
    var springConfig = void 0;
    if (tension === undefined || friction === undefined) {
      springConfig = SpringConfig.DEFAULT_ORIGAMI_SPRING_CONFIG;
    } else {
      springConfig = SpringConfig.fromOrigamiTensionAndFriction(tension, friction);
    }
    return this.createSpringWithConfig(springConfig);
  };

  /**
   * Add a spring with a specified bounciness and speed. To replicate Origami
   * compositions based on PopAnimation patches, use this factory method to
   * create matching springs.
   * @public
   */


  SpringSystem.prototype.createSpringWithBouncinessAndSpeed = function createSpringWithBouncinessAndSpeed(bounciness, speed) {
    var springConfig = void 0;
    if (bounciness === undefined || speed === undefined) {
      springConfig = SpringConfig.DEFAULT_ORIGAMI_SPRING_CONFIG;
    } else {
      springConfig = SpringConfig.fromBouncinessAndSpeed(bounciness, speed);
    }
    return this.createSpringWithConfig(springConfig);
  };

  /**
   * Add a spring with the provided SpringConfig.
   * @public
   */


  SpringSystem.prototype.createSpringWithConfig = function createSpringWithConfig(springConfig) {
    var spring = new Spring(this);
    this.registerSpring(spring);
    spring.setSpringConfig(springConfig);
    return spring;
  };

  /**
   * Check if a SpringSystem is idle or active. If all of the Springs in the
   * SpringSystem are at rest, i.e. the physics forces have reached equilibrium,
   * then this method will return true.
   * @public
   */


  SpringSystem.prototype.getIsIdle = function getIsIdle() {
    return this._isIdle;
  };

  /**
   * Retrieve a specific Spring from the SpringSystem by id. This
   * can be useful for inspecting the state of a spring before
   * or after an integration loop in the SpringSystem executes.
   * @public
   */


  SpringSystem.prototype.getSpringById = function getSpringById(id) {
    return this._springRegistry[id];
  };

  /**
   * Get a listing of all the springs registered with this
   * SpringSystem.
   * @public
   */


  SpringSystem.prototype.getAllSprings = function getAllSprings() {
    var vals = [];
    for (var _id in this._springRegistry) {
      if (this._springRegistry.hasOwnProperty(_id)) {
        vals.push(this._springRegistry[_id]);
      }
    }
    return vals;
  };

  /**
   * Manually add a spring to this system. This is called automatically
   * if a Spring is created with SpringSystem#createSpring.
   *
   * This method sets the spring up in the registry so that it can be solved
   * in the solver loop.
   * @public
   */


  SpringSystem.prototype.registerSpring = function registerSpring(spring) {
    this._springRegistry[spring.getId()] = spring;
  };

  /**
   * Deregister a spring with this SpringSystem. The SpringSystem will
   * no longer consider this Spring during its integration loop once
   * this is called. This is normally done automatically for you when
   * you call Spring#destroy.
   * @public
   */


  SpringSystem.prototype.deregisterSpring = function deregisterSpring(spring) {
    removeFirst(this._activeSprings, spring);
    delete this._springRegistry[spring.getId()];
  };

  SpringSystem.prototype.advance = function advance(time, deltaTime) {
    while (this._idleSpringIndices.length > 0) {
      this._idleSpringIndices.pop();
    }
    for (var i = 0, len = this._activeSprings.length; i < len; i++) {
      var spring = this._activeSprings[i];
      if (spring.systemShouldAdvance()) {
        spring.advance(time / 1000.0, deltaTime / 1000.0);
      } else {
        this._idleSpringIndices.push(this._activeSprings.indexOf(spring));
      }
    }
    while (this._idleSpringIndices.length > 0) {
      var idx = this._idleSpringIndices.pop();
      idx >= 0 && this._activeSprings.splice(idx, 1);
    }
  };

  /**
   * This is the main solver loop called to move the simulation
   * forward through time. Before each pass in the solver loop
   * onBeforeIntegrate is called on an any listeners that have
   * registered themeselves with the SpringSystem. This gives you
   * an opportunity to apply any constraints or adjustments to
   * the springs that should be enforced before each iteration
   * loop. Next the advance method is called to move each Spring in
   * the systemShouldAdvance forward to the current time. After the
   * integration step runs in advance, onAfterIntegrate is called
   * on any listeners that have registered themselves with the
   * SpringSystem. This gives you an opportunity to run any post
   * integration constraints or adjustments on the Springs in the
   * SpringSystem.
   * @public
   */


  SpringSystem.prototype.loop = function loop(currentTimeMillis) {
    var listener = void 0;
    if (this._lastTimeMillis === -1) {
      this._lastTimeMillis = currentTimeMillis - 1;
    }
    var ellapsedMillis = currentTimeMillis - this._lastTimeMillis;
    this._lastTimeMillis = currentTimeMillis;

    var i = 0;
    var len = this.listeners.length;
    for (i = 0; i < len; i++) {
      listener = this.listeners[i];
      listener.onBeforeIntegrate && listener.onBeforeIntegrate(this);
    }

    this.advance(currentTimeMillis, ellapsedMillis);
    if (this._activeSprings.length === 0) {
      this._isIdle = true;
      this._lastTimeMillis = -1;
    }

    for (i = 0; i < len; i++) {
      listener = this.listeners[i];
      listener.onAfterIntegrate && listener.onAfterIntegrate(this);
    }

    if (!this._isIdle) {
      this.looper.run();
    }
  };

  /**
   * Used to notify the SpringSystem that a Spring has become displaced.
   * The system responds by starting its solver loop up if it is currently idle.
   */


  SpringSystem.prototype.activateSpring = function activateSpring(springId) {
    var spring = this._springRegistry[springId];
    if (this._activeSprings.indexOf(spring) === -1) {
      this._activeSprings.push(spring);
    }
    if (this.getIsIdle()) {
      this._isIdle = false;
      this.looper.run();
    }
  };

  /**
   * Add a listener to the SpringSystem to receive before/after integration
   * notifications allowing Springs to be constrained or adjusted.
   * @public
   */


  SpringSystem.prototype.addListener = function addListener(listener) {
    this.listeners.push(listener);
  };

  /**
   * Remove a previously added listener on the SpringSystem.
   * @public
   */


  SpringSystem.prototype.removeListener = function removeListener(listener) {
    removeFirst(this.listeners, listener);
  };

  /**
   * Remove all previously added listeners on the SpringSystem.
   * @public
   */


  SpringSystem.prototype.removeAllListeners = function removeAllListeners() {
    this.listeners = [];
  };

  return SpringSystem;
}();

var index = _extends({}, Loopers, {
  OrigamiValueConverter: OrigamiValueConverter,
  MathUtil: MathUtil,
  Spring: Spring,
  SpringConfig: SpringConfig,
  SpringSystem: SpringSystem,
  util: _extends({}, util, MathUtil)
});

return index;

})));

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(5), __webpack_require__(22).setImmediate))

/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
exports.easing = {
    // No easing, no acceleration
    linear: function (t) { return t; },
    // Accelerates fast, then slows quickly towards end.
    quadratic: function (t) { return t * (-(t * t) * t + 4 * t * t - 6 * t + 4); },
    // Overshoots over 1 and then returns to 1 towards end.
    cubic: function (t) { return t * (4 * t * t - 9 * t + 6); },
    // Overshoots over 1 multiple times - wiggles around 1.
    elastic: function (t) { return t * (33 * t * t * t * t - 106 * t * t * t + 126 * t * t - 67 * t + 15); },
    // Accelerating from zero velocity
    inQuad: function (t) { return t * t; },
    // Decelerating to zero velocity
    outQuad: function (t) { return t * (2 - t); },
    // Acceleration until halfway, then deceleration
    inOutQuad: function (t) { return t < .5 ? 2 * t * t : -1 + (4 - 2 * t) * t; },
    // Accelerating from zero velocity
    inCubic: function (t) { return t * t * t; },
    // Decelerating to zero velocity
    outCubic: function (t) { return (--t) * t * t + 1; },
    // Acceleration until halfway, then deceleration
    inOutCubic: function (t) { return t < .5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1; },
    // Accelerating from zero velocity
    inQuart: function (t) { return t * t * t * t; },
    // Decelerating to zero velocity
    outQuart: function (t) { return 1 - (--t) * t * t * t; },
    // Acceleration until halfway, then deceleration
    inOutQuart: function (t) { return t < .5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t; },
    // Accelerating from zero velocity
    inQuint: function (t) { return t * t * t * t * t; },
    // Decelerating to zero velocity
    outQuint: function (t) { return 1 + (--t) * t * t * t * t; },
    // Acceleration until halfway, then deceleration
    inOutQuint: function (t) { return t < .5 ? 16 * t * t * t * t * t : 1 + 16 * (--t) * t * t * t * t; },
    // Accelerating from zero velocity
    inSine: function (t) { return -Math.cos(t * (Math.PI / 2)) + 1; },
    // Decelerating to zero velocity
    outSine: function (t) { return Math.sin(t * (Math.PI / 2)); },
    // Accelerating until halfway, then decelerating
    inOutSine: function (t) { return -(Math.cos(Math.PI * t) - 1) / 2; },
    // Exponential accelerating from zero velocity
    inExpo: function (t) { return Math.pow(2, 10 * (t - 1)); },
    // Exponential decelerating to zero velocity
    outExpo: function (t) { return -Math.pow(2, -10 * t) + 1; },
    // Exponential accelerating until halfway, then decelerating
    inOutExpo: function (t) {
        t /= .5;
        if (t < 1)
            return Math.pow(2, 10 * (t - 1)) / 2;
        t--;
        return (-Math.pow(2, -10 * t) + 2) / 2;
    },
    // Circular accelerating from zero velocity
    inCirc: function (t) { return -Math.sqrt(1 - t * t) + 1; },
    // Circular decelerating to zero velocity Moves VERY fast at the beginning and
    // then quickly slows down in the middle. This tween can actually be used
    // in continuous transitions where target value changes all the time,
    // because of the very quick start, it hides the jitter between target value changes.
    outCirc: function (t) { return Math.sqrt(1 - (t = t - 1) * t); },
    // Circular acceleration until halfway, then deceleration
    inOutCirc: function (t) {
        t /= .5;
        if (t < 1)
            return -(Math.sqrt(1 - t * t) - 1) / 2;
        t -= 2;
        return (Math.sqrt(1 - t * t) + 1) / 2;
    }
};


/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

const strictUriEncode = __webpack_require__(24);
const decodeComponent = __webpack_require__(25);
const splitOnFirst = __webpack_require__(26);

function encoderForArrayFormat(options) {
	switch (options.arrayFormat) {
		case 'index':
			return key => (result, value) => {
				const index = result.length;
				if (value === undefined) {
					return result;
				}

				if (value === null) {
					return [...result, [encode(key, options), '[', index, ']'].join('')];
				}

				return [
					...result,
					[encode(key, options), '[', encode(index, options), ']=', encode(value, options)].join('')
				];
			};

		case 'bracket':
			return key => (result, value) => {
				if (value === undefined) {
					return result;
				}

				if (value === null) {
					return [...result, [encode(key, options), '[]'].join('')];
				}

				return [...result, [encode(key, options), '[]=', encode(value, options)].join('')];
			};

		case 'comma':
			return key => (result, value, index) => {
				if (value === null || value === undefined || value.length === 0) {
					return result;
				}

				if (index === 0) {
					return [[encode(key, options), '=', encode(value, options)].join('')];
				}

				return [[result, encode(value, options)].join(',')];
			};

		default:
			return key => (result, value) => {
				if (value === undefined) {
					return result;
				}

				if (value === null) {
					return [...result, encode(key, options)];
				}

				return [...result, [encode(key, options), '=', encode(value, options)].join('')];
			};
	}
}

function parserForArrayFormat(options) {
	let result;

	switch (options.arrayFormat) {
		case 'index':
			return (key, value, accumulator) => {
				result = /\[(\d*)\]$/.exec(key);

				key = key.replace(/\[\d*\]$/, '');

				if (!result) {
					accumulator[key] = value;
					return;
				}

				if (accumulator[key] === undefined) {
					accumulator[key] = {};
				}

				accumulator[key][result[1]] = value;
			};

		case 'bracket':
			return (key, value, accumulator) => {
				result = /(\[\])$/.exec(key);
				key = key.replace(/\[\]$/, '');

				if (!result) {
					accumulator[key] = value;
					return;
				}

				if (accumulator[key] === undefined) {
					accumulator[key] = [value];
					return;
				}

				accumulator[key] = [].concat(accumulator[key], value);
			};

		case 'comma':
			return (key, value, accumulator) => {
				const isArray = typeof value === 'string' && value.split('').indexOf(',') > -1;
				const newValue = isArray ? value.split(',') : value;
				accumulator[key] = newValue;
			};

		default:
			return (key, value, accumulator) => {
				if (accumulator[key] === undefined) {
					accumulator[key] = value;
					return;
				}

				accumulator[key] = [].concat(accumulator[key], value);
			};
	}
}

function encode(value, options) {
	if (options.encode) {
		return options.strict ? strictUriEncode(value) : encodeURIComponent(value);
	}

	return value;
}

function decode(value, options) {
	if (options.decode) {
		return decodeComponent(value);
	}

	return value;
}

function keysSorter(input) {
	if (Array.isArray(input)) {
		return input.sort();
	}

	if (typeof input === 'object') {
		return keysSorter(Object.keys(input))
			.sort((a, b) => Number(a) - Number(b))
			.map(key => input[key]);
	}

	return input;
}

function removeHash(input) {
	const hashStart = input.indexOf('#');
	if (hashStart !== -1) {
		input = input.slice(0, hashStart);
	}

	return input;
}

function extract(input) {
	input = removeHash(input);
	const queryStart = input.indexOf('?');
	if (queryStart === -1) {
		return '';
	}

	return input.slice(queryStart + 1);
}

function parse(input, options) {
	options = Object.assign({
		decode: true,
		sort: true,
		arrayFormat: 'none',
		parseNumbers: false
	}, options);

	const formatter = parserForArrayFormat(options);

	// Create an object with no prototype
	const ret = Object.create(null);

	if (typeof input !== 'string') {
		return ret;
	}

	input = input.trim().replace(/^[?#&]/, '');

	if (!input) {
		return ret;
	}

	for (const param of input.split('&')) {
		let [key, value] = splitOnFirst(param.replace(/\+/g, ' '), '=');

		// Missing `=` should be `null`:
		// http://w3.org/TR/2012/WD-url-20120524/#collect-url-parameters
		value = value === undefined ? null : decode(value, options);

		if (options.parseNumbers && !Number.isNaN(Number(value))) {
			value = Number(value);
		}

		formatter(decode(key, options), value, ret);
	}

	if (options.sort === false) {
		return ret;
	}

	return (options.sort === true ? Object.keys(ret).sort() : Object.keys(ret).sort(options.sort)).reduce((result, key) => {
		const value = ret[key];
		if (Boolean(value) && typeof value === 'object' && !Array.isArray(value)) {
			// Sort object keys, not values
			result[key] = keysSorter(value);
		} else {
			result[key] = value;
		}

		return result;
	}, Object.create(null));
}

exports.extract = extract;
exports.parse = parse;

exports.stringify = (object, options) => {
	if (!object) {
		return '';
	}

	options = Object.assign({
		encode: true,
		strict: true,
		arrayFormat: 'none'
	}, options);

	const formatter = encoderForArrayFormat(options);
	const keys = Object.keys(object);

	if (options.sort !== false) {
		keys.sort(options.sort);
	}

	return keys.map(key => {
		const value = object[key];

		if (value === undefined) {
			return '';
		}

		if (value === null) {
			return encode(key, options);
		}

		if (Array.isArray(value)) {
			return value
				.reduce(formatter(key), [])
				.join('&');
		}

		return encode(key, options) + '=' + encode(value, options);
	}).filter(x => x.length > 0).join('&');
};

exports.parseUrl = (input, options) => {
	return {
		url: removeHash(input).split('?')[0] || '',
		query: parse(extract(input), options)
	};
};


/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(27);


/***/ }),
/* 15 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/**
 * Copyright (c) 2013-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */



var ReactPropTypesSecret = __webpack_require__(16);

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
/* 16 */
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
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

/**
 * Copyright (c) 2014-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// This method of obtaining a reference to the global object needs to be
// kept identical to the way it is obtained in runtime.js
var g = (function() { return this })() || Function("return this")();

// Use `getOwnPropertyNames` because not all browsers support calling
// `hasOwnProperty` on the global `self` object in a worker. See #183.
var hadRuntime = g.regeneratorRuntime &&
  Object.getOwnPropertyNames(g).indexOf("regeneratorRuntime") >= 0;

// Save the old regeneratorRuntime in case it needs to be restored later.
var oldRuntime = hadRuntime && g.regeneratorRuntime;

// Force reevalutation of runtime.js.
g.regeneratorRuntime = undefined;

module.exports = __webpack_require__(18);

if (hadRuntime) {
  // Restore the original runtime.
  g.regeneratorRuntime = oldRuntime;
} else {
  // Remove the global property added by runtime.js.
  try {
    delete g.regeneratorRuntime;
  } catch(e) {
    g.regeneratorRuntime = undefined;
  }
}


/***/ }),
/* 18 */
/***/ (function(module, exports) {

/**
 * Copyright (c) 2014-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

!(function(global) {
  "use strict";

  var Op = Object.prototype;
  var hasOwn = Op.hasOwnProperty;
  var undefined; // More compressible than void 0.
  var $Symbol = typeof Symbol === "function" ? Symbol : {};
  var iteratorSymbol = $Symbol.iterator || "@@iterator";
  var asyncIteratorSymbol = $Symbol.asyncIterator || "@@asyncIterator";
  var toStringTagSymbol = $Symbol.toStringTag || "@@toStringTag";

  var inModule = typeof module === "object";
  var runtime = global.regeneratorRuntime;
  if (runtime) {
    if (inModule) {
      // If regeneratorRuntime is defined globally and we're in a module,
      // make the exports object identical to regeneratorRuntime.
      module.exports = runtime;
    }
    // Don't bother evaluating the rest of this file if the runtime was
    // already defined globally.
    return;
  }

  // Define the runtime globally (as expected by generated code) as either
  // module.exports (if we're in a module) or a new, empty object.
  runtime = global.regeneratorRuntime = inModule ? module.exports : {};

  function wrap(innerFn, outerFn, self, tryLocsList) {
    // If outerFn provided and outerFn.prototype is a Generator, then outerFn.prototype instanceof Generator.
    var protoGenerator = outerFn && outerFn.prototype instanceof Generator ? outerFn : Generator;
    var generator = Object.create(protoGenerator.prototype);
    var context = new Context(tryLocsList || []);

    // The ._invoke method unifies the implementations of the .next,
    // .throw, and .return methods.
    generator._invoke = makeInvokeMethod(innerFn, self, context);

    return generator;
  }
  runtime.wrap = wrap;

  // Try/catch helper to minimize deoptimizations. Returns a completion
  // record like context.tryEntries[i].completion. This interface could
  // have been (and was previously) designed to take a closure to be
  // invoked without arguments, but in all the cases we care about we
  // already have an existing method we want to call, so there's no need
  // to create a new function object. We can even get away with assuming
  // the method takes exactly one argument, since that happens to be true
  // in every case, so we don't have to touch the arguments object. The
  // only additional allocation required is the completion record, which
  // has a stable shape and so hopefully should be cheap to allocate.
  function tryCatch(fn, obj, arg) {
    try {
      return { type: "normal", arg: fn.call(obj, arg) };
    } catch (err) {
      return { type: "throw", arg: err };
    }
  }

  var GenStateSuspendedStart = "suspendedStart";
  var GenStateSuspendedYield = "suspendedYield";
  var GenStateExecuting = "executing";
  var GenStateCompleted = "completed";

  // Returning this object from the innerFn has the same effect as
  // breaking out of the dispatch switch statement.
  var ContinueSentinel = {};

  // Dummy constructor functions that we use as the .constructor and
  // .constructor.prototype properties for functions that return Generator
  // objects. For full spec compliance, you may wish to configure your
  // minifier not to mangle the names of these two functions.
  function Generator() {}
  function GeneratorFunction() {}
  function GeneratorFunctionPrototype() {}

  // This is a polyfill for %IteratorPrototype% for environments that
  // don't natively support it.
  var IteratorPrototype = {};
  IteratorPrototype[iteratorSymbol] = function () {
    return this;
  };

  var getProto = Object.getPrototypeOf;
  var NativeIteratorPrototype = getProto && getProto(getProto(values([])));
  if (NativeIteratorPrototype &&
      NativeIteratorPrototype !== Op &&
      hasOwn.call(NativeIteratorPrototype, iteratorSymbol)) {
    // This environment has a native %IteratorPrototype%; use it instead
    // of the polyfill.
    IteratorPrototype = NativeIteratorPrototype;
  }

  var Gp = GeneratorFunctionPrototype.prototype =
    Generator.prototype = Object.create(IteratorPrototype);
  GeneratorFunction.prototype = Gp.constructor = GeneratorFunctionPrototype;
  GeneratorFunctionPrototype.constructor = GeneratorFunction;
  GeneratorFunctionPrototype[toStringTagSymbol] =
    GeneratorFunction.displayName = "GeneratorFunction";

  // Helper for defining the .next, .throw, and .return methods of the
  // Iterator interface in terms of a single ._invoke method.
  function defineIteratorMethods(prototype) {
    ["next", "throw", "return"].forEach(function(method) {
      prototype[method] = function(arg) {
        return this._invoke(method, arg);
      };
    });
  }

  runtime.isGeneratorFunction = function(genFun) {
    var ctor = typeof genFun === "function" && genFun.constructor;
    return ctor
      ? ctor === GeneratorFunction ||
        // For the native GeneratorFunction constructor, the best we can
        // do is to check its .name property.
        (ctor.displayName || ctor.name) === "GeneratorFunction"
      : false;
  };

  runtime.mark = function(genFun) {
    if (Object.setPrototypeOf) {
      Object.setPrototypeOf(genFun, GeneratorFunctionPrototype);
    } else {
      genFun.__proto__ = GeneratorFunctionPrototype;
      if (!(toStringTagSymbol in genFun)) {
        genFun[toStringTagSymbol] = "GeneratorFunction";
      }
    }
    genFun.prototype = Object.create(Gp);
    return genFun;
  };

  // Within the body of any async function, `await x` is transformed to
  // `yield regeneratorRuntime.awrap(x)`, so that the runtime can test
  // `hasOwn.call(value, "__await")` to determine if the yielded value is
  // meant to be awaited.
  runtime.awrap = function(arg) {
    return { __await: arg };
  };

  function AsyncIterator(generator) {
    function invoke(method, arg, resolve, reject) {
      var record = tryCatch(generator[method], generator, arg);
      if (record.type === "throw") {
        reject(record.arg);
      } else {
        var result = record.arg;
        var value = result.value;
        if (value &&
            typeof value === "object" &&
            hasOwn.call(value, "__await")) {
          return Promise.resolve(value.__await).then(function(value) {
            invoke("next", value, resolve, reject);
          }, function(err) {
            invoke("throw", err, resolve, reject);
          });
        }

        return Promise.resolve(value).then(function(unwrapped) {
          // When a yielded Promise is resolved, its final value becomes
          // the .value of the Promise<{value,done}> result for the
          // current iteration. If the Promise is rejected, however, the
          // result for this iteration will be rejected with the same
          // reason. Note that rejections of yielded Promises are not
          // thrown back into the generator function, as is the case
          // when an awaited Promise is rejected. This difference in
          // behavior between yield and await is important, because it
          // allows the consumer to decide what to do with the yielded
          // rejection (swallow it and continue, manually .throw it back
          // into the generator, abandon iteration, whatever). With
          // await, by contrast, there is no opportunity to examine the
          // rejection reason outside the generator function, so the
          // only option is to throw it from the await expression, and
          // let the generator function handle the exception.
          result.value = unwrapped;
          resolve(result);
        }, reject);
      }
    }

    var previousPromise;

    function enqueue(method, arg) {
      function callInvokeWithMethodAndArg() {
        return new Promise(function(resolve, reject) {
          invoke(method, arg, resolve, reject);
        });
      }

      return previousPromise =
        // If enqueue has been called before, then we want to wait until
        // all previous Promises have been resolved before calling invoke,
        // so that results are always delivered in the correct order. If
        // enqueue has not been called before, then it is important to
        // call invoke immediately, without waiting on a callback to fire,
        // so that the async generator function has the opportunity to do
        // any necessary setup in a predictable way. This predictability
        // is why the Promise constructor synchronously invokes its
        // executor callback, and why async functions synchronously
        // execute code before the first await. Since we implement simple
        // async functions in terms of async generators, it is especially
        // important to get this right, even though it requires care.
        previousPromise ? previousPromise.then(
          callInvokeWithMethodAndArg,
          // Avoid propagating failures to Promises returned by later
          // invocations of the iterator.
          callInvokeWithMethodAndArg
        ) : callInvokeWithMethodAndArg();
    }

    // Define the unified helper method that is used to implement .next,
    // .throw, and .return (see defineIteratorMethods).
    this._invoke = enqueue;
  }

  defineIteratorMethods(AsyncIterator.prototype);
  AsyncIterator.prototype[asyncIteratorSymbol] = function () {
    return this;
  };
  runtime.AsyncIterator = AsyncIterator;

  // Note that simple async functions are implemented on top of
  // AsyncIterator objects; they just return a Promise for the value of
  // the final result produced by the iterator.
  runtime.async = function(innerFn, outerFn, self, tryLocsList) {
    var iter = new AsyncIterator(
      wrap(innerFn, outerFn, self, tryLocsList)
    );

    return runtime.isGeneratorFunction(outerFn)
      ? iter // If outerFn is a generator, return the full iterator.
      : iter.next().then(function(result) {
          return result.done ? result.value : iter.next();
        });
  };

  function makeInvokeMethod(innerFn, self, context) {
    var state = GenStateSuspendedStart;

    return function invoke(method, arg) {
      if (state === GenStateExecuting) {
        throw new Error("Generator is already running");
      }

      if (state === GenStateCompleted) {
        if (method === "throw") {
          throw arg;
        }

        // Be forgiving, per 25.3.3.3.3 of the spec:
        // https://people.mozilla.org/~jorendorff/es6-draft.html#sec-generatorresume
        return doneResult();
      }

      context.method = method;
      context.arg = arg;

      while (true) {
        var delegate = context.delegate;
        if (delegate) {
          var delegateResult = maybeInvokeDelegate(delegate, context);
          if (delegateResult) {
            if (delegateResult === ContinueSentinel) continue;
            return delegateResult;
          }
        }

        if (context.method === "next") {
          // Setting context._sent for legacy support of Babel's
          // function.sent implementation.
          context.sent = context._sent = context.arg;

        } else if (context.method === "throw") {
          if (state === GenStateSuspendedStart) {
            state = GenStateCompleted;
            throw context.arg;
          }

          context.dispatchException(context.arg);

        } else if (context.method === "return") {
          context.abrupt("return", context.arg);
        }

        state = GenStateExecuting;

        var record = tryCatch(innerFn, self, context);
        if (record.type === "normal") {
          // If an exception is thrown from innerFn, we leave state ===
          // GenStateExecuting and loop back for another invocation.
          state = context.done
            ? GenStateCompleted
            : GenStateSuspendedYield;

          if (record.arg === ContinueSentinel) {
            continue;
          }

          return {
            value: record.arg,
            done: context.done
          };

        } else if (record.type === "throw") {
          state = GenStateCompleted;
          // Dispatch the exception by looping back around to the
          // context.dispatchException(context.arg) call above.
          context.method = "throw";
          context.arg = record.arg;
        }
      }
    };
  }

  // Call delegate.iterator[context.method](context.arg) and handle the
  // result, either by returning a { value, done } result from the
  // delegate iterator, or by modifying context.method and context.arg,
  // setting context.delegate to null, and returning the ContinueSentinel.
  function maybeInvokeDelegate(delegate, context) {
    var method = delegate.iterator[context.method];
    if (method === undefined) {
      // A .throw or .return when the delegate iterator has no .throw
      // method always terminates the yield* loop.
      context.delegate = null;

      if (context.method === "throw") {
        if (delegate.iterator.return) {
          // If the delegate iterator has a return method, give it a
          // chance to clean up.
          context.method = "return";
          context.arg = undefined;
          maybeInvokeDelegate(delegate, context);

          if (context.method === "throw") {
            // If maybeInvokeDelegate(context) changed context.method from
            // "return" to "throw", let that override the TypeError below.
            return ContinueSentinel;
          }
        }

        context.method = "throw";
        context.arg = new TypeError(
          "The iterator does not provide a 'throw' method");
      }

      return ContinueSentinel;
    }

    var record = tryCatch(method, delegate.iterator, context.arg);

    if (record.type === "throw") {
      context.method = "throw";
      context.arg = record.arg;
      context.delegate = null;
      return ContinueSentinel;
    }

    var info = record.arg;

    if (! info) {
      context.method = "throw";
      context.arg = new TypeError("iterator result is not an object");
      context.delegate = null;
      return ContinueSentinel;
    }

    if (info.done) {
      // Assign the result of the finished delegate to the temporary
      // variable specified by delegate.resultName (see delegateYield).
      context[delegate.resultName] = info.value;

      // Resume execution at the desired location (see delegateYield).
      context.next = delegate.nextLoc;

      // If context.method was "throw" but the delegate handled the
      // exception, let the outer generator proceed normally. If
      // context.method was "next", forget context.arg since it has been
      // "consumed" by the delegate iterator. If context.method was
      // "return", allow the original .return call to continue in the
      // outer generator.
      if (context.method !== "return") {
        context.method = "next";
        context.arg = undefined;
      }

    } else {
      // Re-yield the result returned by the delegate method.
      return info;
    }

    // The delegate iterator is finished, so forget it and continue with
    // the outer generator.
    context.delegate = null;
    return ContinueSentinel;
  }

  // Define Generator.prototype.{next,throw,return} in terms of the
  // unified ._invoke helper method.
  defineIteratorMethods(Gp);

  Gp[toStringTagSymbol] = "Generator";

  // A Generator should always return itself as the iterator object when the
  // @@iterator function is called on it. Some browsers' implementations of the
  // iterator prototype chain incorrectly implement this, causing the Generator
  // object to not be returned from this call. This ensures that doesn't happen.
  // See https://github.com/facebook/regenerator/issues/274 for more details.
  Gp[iteratorSymbol] = function() {
    return this;
  };

  Gp.toString = function() {
    return "[object Generator]";
  };

  function pushTryEntry(locs) {
    var entry = { tryLoc: locs[0] };

    if (1 in locs) {
      entry.catchLoc = locs[1];
    }

    if (2 in locs) {
      entry.finallyLoc = locs[2];
      entry.afterLoc = locs[3];
    }

    this.tryEntries.push(entry);
  }

  function resetTryEntry(entry) {
    var record = entry.completion || {};
    record.type = "normal";
    delete record.arg;
    entry.completion = record;
  }

  function Context(tryLocsList) {
    // The root entry object (effectively a try statement without a catch
    // or a finally block) gives us a place to store values thrown from
    // locations where there is no enclosing try statement.
    this.tryEntries = [{ tryLoc: "root" }];
    tryLocsList.forEach(pushTryEntry, this);
    this.reset(true);
  }

  runtime.keys = function(object) {
    var keys = [];
    for (var key in object) {
      keys.push(key);
    }
    keys.reverse();

    // Rather than returning an object with a next method, we keep
    // things simple and return the next function itself.
    return function next() {
      while (keys.length) {
        var key = keys.pop();
        if (key in object) {
          next.value = key;
          next.done = false;
          return next;
        }
      }

      // To avoid creating an additional object, we just hang the .value
      // and .done properties off the next function object itself. This
      // also ensures that the minifier will not anonymize the function.
      next.done = true;
      return next;
    };
  };

  function values(iterable) {
    if (iterable) {
      var iteratorMethod = iterable[iteratorSymbol];
      if (iteratorMethod) {
        return iteratorMethod.call(iterable);
      }

      if (typeof iterable.next === "function") {
        return iterable;
      }

      if (!isNaN(iterable.length)) {
        var i = -1, next = function next() {
          while (++i < iterable.length) {
            if (hasOwn.call(iterable, i)) {
              next.value = iterable[i];
              next.done = false;
              return next;
            }
          }

          next.value = undefined;
          next.done = true;

          return next;
        };

        return next.next = next;
      }
    }

    // Return an iterator with no values.
    return { next: doneResult };
  }
  runtime.values = values;

  function doneResult() {
    return { value: undefined, done: true };
  }

  Context.prototype = {
    constructor: Context,

    reset: function(skipTempReset) {
      this.prev = 0;
      this.next = 0;
      // Resetting context._sent for legacy support of Babel's
      // function.sent implementation.
      this.sent = this._sent = undefined;
      this.done = false;
      this.delegate = null;

      this.method = "next";
      this.arg = undefined;

      this.tryEntries.forEach(resetTryEntry);

      if (!skipTempReset) {
        for (var name in this) {
          // Not sure about the optimal order of these conditions:
          if (name.charAt(0) === "t" &&
              hasOwn.call(this, name) &&
              !isNaN(+name.slice(1))) {
            this[name] = undefined;
          }
        }
      }
    },

    stop: function() {
      this.done = true;

      var rootEntry = this.tryEntries[0];
      var rootRecord = rootEntry.completion;
      if (rootRecord.type === "throw") {
        throw rootRecord.arg;
      }

      return this.rval;
    },

    dispatchException: function(exception) {
      if (this.done) {
        throw exception;
      }

      var context = this;
      function handle(loc, caught) {
        record.type = "throw";
        record.arg = exception;
        context.next = loc;

        if (caught) {
          // If the dispatched exception was caught by a catch block,
          // then let that catch block handle the exception normally.
          context.method = "next";
          context.arg = undefined;
        }

        return !! caught;
      }

      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        var record = entry.completion;

        if (entry.tryLoc === "root") {
          // Exception thrown outside of any try block that could handle
          // it, so set the completion value of the entire function to
          // throw the exception.
          return handle("end");
        }

        if (entry.tryLoc <= this.prev) {
          var hasCatch = hasOwn.call(entry, "catchLoc");
          var hasFinally = hasOwn.call(entry, "finallyLoc");

          if (hasCatch && hasFinally) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            } else if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else if (hasCatch) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            }

          } else if (hasFinally) {
            if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else {
            throw new Error("try statement without catch or finally");
          }
        }
      }
    },

    abrupt: function(type, arg) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc <= this.prev &&
            hasOwn.call(entry, "finallyLoc") &&
            this.prev < entry.finallyLoc) {
          var finallyEntry = entry;
          break;
        }
      }

      if (finallyEntry &&
          (type === "break" ||
           type === "continue") &&
          finallyEntry.tryLoc <= arg &&
          arg <= finallyEntry.finallyLoc) {
        // Ignore the finally entry if control is not jumping to a
        // location outside the try/catch block.
        finallyEntry = null;
      }

      var record = finallyEntry ? finallyEntry.completion : {};
      record.type = type;
      record.arg = arg;

      if (finallyEntry) {
        this.method = "next";
        this.next = finallyEntry.finallyLoc;
        return ContinueSentinel;
      }

      return this.complete(record);
    },

    complete: function(record, afterLoc) {
      if (record.type === "throw") {
        throw record.arg;
      }

      if (record.type === "break" ||
          record.type === "continue") {
        this.next = record.arg;
      } else if (record.type === "return") {
        this.rval = this.arg = record.arg;
        this.method = "return";
        this.next = "end";
      } else if (record.type === "normal" && afterLoc) {
        this.next = afterLoc;
      }

      return ContinueSentinel;
    },

    finish: function(finallyLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.finallyLoc === finallyLoc) {
          this.complete(entry.completion, entry.afterLoc);
          resetTryEntry(entry);
          return ContinueSentinel;
        }
      }
    },

    "catch": function(tryLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc === tryLoc) {
          var record = entry.completion;
          if (record.type === "throw") {
            var thrown = record.arg;
            resetTryEntry(entry);
          }
          return thrown;
        }
      }

      // The context.catch method must only be called with a location
      // argument that corresponds to a known catch block.
      throw new Error("illegal catch attempt");
    },

    delegateYield: function(iterable, resultName, nextLoc) {
      this.delegate = {
        iterator: values(iterable),
        resultName: resultName,
        nextLoc: nextLoc
      };

      if (this.method === "next") {
        // Deliberately forget the last sent value so that we don't
        // accidentally pass it on to the delegate.
        this.arg = undefined;
      }

      return ContinueSentinel;
    }
  };
})(
  // In sloppy mode, unbound `this` refers to the global object, fallback to
  // Function constructor if we're in global strict mode. That is sadly a form
  // of indirect eval which violates Content Security Policy.
  (function() { return this })() || Function("return this")()
);


/***/ }),
/* 19 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var deselectCurrent = __webpack_require__(20);

var defaultMessage = "Copy to clipboard: #{key}, Enter";

function format(message) {
  var copyKey = (/mac os x/i.test(navigator.userAgent) ? "⌘" : "Ctrl") + "+C";
  return message.replace(/#{\s*key\s*}/g, copyKey);
}

function copy(text, options) {
  var debug,
    message,
    reselectPrevious,
    range,
    selection,
    mark,
    success = false;
  if (!options) {
    options = {};
  }
  debug = options.debug || false;
  try {
    reselectPrevious = deselectCurrent();

    range = document.createRange();
    selection = document.getSelection();

    mark = document.createElement("span");
    mark.textContent = text;
    // reset user styles for span element
    mark.style.all = "unset";
    // prevents scrolling to the end of the page
    mark.style.position = "fixed";
    mark.style.top = 0;
    mark.style.clip = "rect(0, 0, 0, 0)";
    // used to preserve spaces and line breaks
    mark.style.whiteSpace = "pre";
    // do not inherit user-select (it may be `none`)
    mark.style.webkitUserSelect = "text";
    mark.style.MozUserSelect = "text";
    mark.style.msUserSelect = "text";
    mark.style.userSelect = "text";
    mark.addEventListener("copy", function(e) {
      e.stopPropagation();
      if (options.format) {
        e.preventDefault();
        e.clipboardData.clearData();
        e.clipboardData.setData(options.format, text);
      }
    });

    document.body.appendChild(mark);

    range.selectNodeContents(mark);
    selection.addRange(range);

    var successful = document.execCommand("copy");
    if (!successful) {
      throw new Error("copy command was unsuccessful");
    }
    success = true;
  } catch (err) {
    debug && console.error("unable to copy using execCommand: ", err);
    debug && console.warn("trying IE specific stuff");
    try {
      window.clipboardData.setData(options.format || "text", text);
      success = true;
    } catch (err) {
      debug && console.error("unable to copy using clipboardData: ", err);
      debug && console.error("falling back to prompt");
      message = format("message" in options ? options.message : defaultMessage);
      window.prompt(message, text);
    }
  } finally {
    if (selection) {
      if (typeof selection.removeRange == "function") {
        selection.removeRange(range);
      } else {
        selection.removeAllRanges();
      }
    }

    if (mark) {
      document.body.removeChild(mark);
    }
    reselectPrevious();
  }

  return success;
}

module.exports = copy;


/***/ }),
/* 20 */
/***/ (function(module, exports) {


module.exports = function () {
  var selection = document.getSelection();
  if (!selection.rangeCount) {
    return function () {};
  }
  var active = document.activeElement;

  var ranges = [];
  for (var i = 0; i < selection.rangeCount; i++) {
    ranges.push(selection.getRangeAt(i));
  }

  switch (active.tagName.toUpperCase()) { // .toUpperCase handles XHTML
    case 'INPUT':
    case 'TEXTAREA':
      active.blur();
      break;

    default:
      active = null;
      break;
  }

  selection.removeAllRanges();
  return function () {
    selection.type === 'Caret' &&
    selection.removeAllRanges();

    if (!selection.rangeCount) {
      ranges.forEach(function(range) {
        selection.addRange(range);
      });
    }

    active &&
    active.focus();
  };
};


/***/ }),
/* 21 */
/***/ (function(module, exports) {

function removeRule (rule) {
    var maxIndex = rule.index;
    var sh = rule.parentStyleSheet;
    var rules = sh.cssRules || sh.rules;
    maxIndex = Math.max(maxIndex, rules.length - 1);
    while (maxIndex >= 0) {
        if (rules[maxIndex] === rule) {
            sh.deleteRule(maxIndex);
            break;
        }
        maxIndex--;
    }
}

exports.removeRule = removeRule;


/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {var scope = (typeof global !== "undefined" && global) ||
            (typeof self !== "undefined" && self) ||
            window;
var apply = Function.prototype.apply;

// DOM APIs, for completeness

exports.setTimeout = function() {
  return new Timeout(apply.call(setTimeout, scope, arguments), clearTimeout);
};
exports.setInterval = function() {
  return new Timeout(apply.call(setInterval, scope, arguments), clearInterval);
};
exports.clearTimeout =
exports.clearInterval = function(timeout) {
  if (timeout) {
    timeout.close();
  }
};

function Timeout(id, clearFn) {
  this._id = id;
  this._clearFn = clearFn;
}
Timeout.prototype.unref = Timeout.prototype.ref = function() {};
Timeout.prototype.close = function() {
  this._clearFn.call(scope, this._id);
};

// Does not start the time, just sets up the members needed.
exports.enroll = function(item, msecs) {
  clearTimeout(item._idleTimeoutId);
  item._idleTimeout = msecs;
};

exports.unenroll = function(item) {
  clearTimeout(item._idleTimeoutId);
  item._idleTimeout = -1;
};

exports._unrefActive = exports.active = function(item) {
  clearTimeout(item._idleTimeoutId);

  var msecs = item._idleTimeout;
  if (msecs >= 0) {
    item._idleTimeoutId = setTimeout(function onTimeout() {
      if (item._onTimeout)
        item._onTimeout();
    }, msecs);
  }
};

// setimmediate attaches itself to the global object
__webpack_require__(23);
// On some exotic environments, it's not clear which object `setimmediate` was
// able to install onto.  Search each possibility in the same order as the
// `setimmediate` library.
exports.setImmediate = (typeof self !== "undefined" && self.setImmediate) ||
                       (typeof global !== "undefined" && global.setImmediate) ||
                       (this && this.setImmediate);
exports.clearImmediate = (typeof self !== "undefined" && self.clearImmediate) ||
                         (typeof global !== "undefined" && global.clearImmediate) ||
                         (this && this.clearImmediate);

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(4)))

/***/ }),
/* 23 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global, process) {(function (global, undefined) {
    "use strict";

    if (global.setImmediate) {
        return;
    }

    var nextHandle = 1; // Spec says greater than zero
    var tasksByHandle = {};
    var currentlyRunningATask = false;
    var doc = global.document;
    var registerImmediate;

    function setImmediate(callback) {
      // Callback can either be a function or a string
      if (typeof callback !== "function") {
        callback = new Function("" + callback);
      }
      // Copy function arguments
      var args = new Array(arguments.length - 1);
      for (var i = 0; i < args.length; i++) {
          args[i] = arguments[i + 1];
      }
      // Store and register the task
      var task = { callback: callback, args: args };
      tasksByHandle[nextHandle] = task;
      registerImmediate(nextHandle);
      return nextHandle++;
    }

    function clearImmediate(handle) {
        delete tasksByHandle[handle];
    }

    function run(task) {
        var callback = task.callback;
        var args = task.args;
        switch (args.length) {
        case 0:
            callback();
            break;
        case 1:
            callback(args[0]);
            break;
        case 2:
            callback(args[0], args[1]);
            break;
        case 3:
            callback(args[0], args[1], args[2]);
            break;
        default:
            callback.apply(undefined, args);
            break;
        }
    }

    function runIfPresent(handle) {
        // From the spec: "Wait until any invocations of this algorithm started before this one have completed."
        // So if we're currently running a task, we'll need to delay this invocation.
        if (currentlyRunningATask) {
            // Delay by doing a setTimeout. setImmediate was tried instead, but in Firefox 7 it generated a
            // "too much recursion" error.
            setTimeout(runIfPresent, 0, handle);
        } else {
            var task = tasksByHandle[handle];
            if (task) {
                currentlyRunningATask = true;
                try {
                    run(task);
                } finally {
                    clearImmediate(handle);
                    currentlyRunningATask = false;
                }
            }
        }
    }

    function installNextTickImplementation() {
        registerImmediate = function(handle) {
            process.nextTick(function () { runIfPresent(handle); });
        };
    }

    function canUsePostMessage() {
        // The test against `importScripts` prevents this implementation from being installed inside a web worker,
        // where `global.postMessage` means something completely different and can't be used for this purpose.
        if (global.postMessage && !global.importScripts) {
            var postMessageIsAsynchronous = true;
            var oldOnMessage = global.onmessage;
            global.onmessage = function() {
                postMessageIsAsynchronous = false;
            };
            global.postMessage("", "*");
            global.onmessage = oldOnMessage;
            return postMessageIsAsynchronous;
        }
    }

    function installPostMessageImplementation() {
        // Installs an event handler on `global` for the `message` event: see
        // * https://developer.mozilla.org/en/DOM/window.postMessage
        // * http://www.whatwg.org/specs/web-apps/current-work/multipage/comms.html#crossDocumentMessages

        var messagePrefix = "setImmediate$" + Math.random() + "$";
        var onGlobalMessage = function(event) {
            if (event.source === global &&
                typeof event.data === "string" &&
                event.data.indexOf(messagePrefix) === 0) {
                runIfPresent(+event.data.slice(messagePrefix.length));
            }
        };

        if (global.addEventListener) {
            global.addEventListener("message", onGlobalMessage, false);
        } else {
            global.attachEvent("onmessage", onGlobalMessage);
        }

        registerImmediate = function(handle) {
            global.postMessage(messagePrefix + handle, "*");
        };
    }

    function installMessageChannelImplementation() {
        var channel = new MessageChannel();
        channel.port1.onmessage = function(event) {
            var handle = event.data;
            runIfPresent(handle);
        };

        registerImmediate = function(handle) {
            channel.port2.postMessage(handle);
        };
    }

    function installReadyStateChangeImplementation() {
        var html = doc.documentElement;
        registerImmediate = function(handle) {
            // Create a <script> element; its readystatechange event will be fired asynchronously once it is inserted
            // into the document. Do so, thus queuing up the task. Remember to clean up once it's been called.
            var script = doc.createElement("script");
            script.onreadystatechange = function () {
                runIfPresent(handle);
                script.onreadystatechange = null;
                html.removeChild(script);
                script = null;
            };
            html.appendChild(script);
        };
    }

    function installSetTimeoutImplementation() {
        registerImmediate = function(handle) {
            setTimeout(runIfPresent, 0, handle);
        };
    }

    // If supported, we should attach to the prototype of global, since that is where setTimeout et al. live.
    var attachTo = Object.getPrototypeOf && Object.getPrototypeOf(global);
    attachTo = attachTo && attachTo.setTimeout ? attachTo : global;

    // Don't get fooled by e.g. browserify environments.
    if ({}.toString.call(global.process) === "[object process]") {
        // For Node.js before 0.9
        installNextTickImplementation();

    } else if (canUsePostMessage()) {
        // For non-IE10 modern browsers
        installPostMessageImplementation();

    } else if (global.MessageChannel) {
        // For web workers, where supported
        installMessageChannelImplementation();

    } else if (doc && "onreadystatechange" in doc.createElement("script")) {
        // For IE 6–8
        installReadyStateChangeImplementation();

    } else {
        // For older browsers
        installSetTimeoutImplementation();
    }

    attachTo.setImmediate = setImmediate;
    attachTo.clearImmediate = clearImmediate;
}(typeof self === "undefined" ? typeof global === "undefined" ? this : global : self));

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(4), __webpack_require__(5)))

/***/ }),
/* 24 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

module.exports = str => encodeURIComponent(str).replace(/[!'()*]/g, x => `%${x.charCodeAt(0).toString(16).toUpperCase()}`);


/***/ }),
/* 25 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var token = '%[a-f0-9]{2}';
var singleMatcher = new RegExp(token, 'gi');
var multiMatcher = new RegExp('(' + token + ')+', 'gi');

function decodeComponents(components, split) {
	try {
		// Try to decode the entire string first
		return decodeURIComponent(components.join(''));
	} catch (err) {
		// Do nothing
	}

	if (components.length === 1) {
		return components;
	}

	split = split || 1;

	// Split the array in 2 parts
	var left = components.slice(0, split);
	var right = components.slice(split);

	return Array.prototype.concat.call([], decodeComponents(left), decodeComponents(right));
}

function decode(input) {
	try {
		return decodeURIComponent(input);
	} catch (err) {
		var tokens = input.match(singleMatcher);

		for (var i = 1; i < tokens.length; i++) {
			input = decodeComponents(tokens, i).join('');

			tokens = input.match(singleMatcher);
		}

		return input;
	}
}

function customDecodeURIComponent(input) {
	// Keep track of all the replacements and prefill the map with the `BOM`
	var replaceMap = {
		'%FE%FF': '\uFFFD\uFFFD',
		'%FF%FE': '\uFFFD\uFFFD'
	};

	var match = multiMatcher.exec(input);
	while (match) {
		try {
			// Decode as big chunks as possible
			replaceMap[match[0]] = decodeURIComponent(match[0]);
		} catch (err) {
			var result = decode(match[0]);

			if (result !== match[0]) {
				replaceMap[match[0]] = result;
			}
		}

		match = multiMatcher.exec(input);
	}

	// Add `%C2` at the end of the map to make sure it does not replace the combinator before everything else
	replaceMap['%C2'] = '\uFFFD';

	var entries = Object.keys(replaceMap);

	for (var i = 0; i < entries.length; i++) {
		// Replace all decoded components
		var key = entries[i];
		input = input.replace(new RegExp(key, 'g'), replaceMap[key]);
	}

	return input;
}

module.exports = function (encodedURI) {
	if (typeof encodedURI !== 'string') {
		throw new TypeError('Expected `encodedURI` to be of type `string`, got `' + typeof encodedURI + '`');
	}

	try {
		encodedURI = encodedURI.replace(/\+/g, ' ');

		// Try the built in decoder first
		return decodeURIComponent(encodedURI);
	} catch (err) {
		// Fallback to a more advanced decoder
		return customDecodeURIComponent(encodedURI);
	}
};


/***/ }),
/* 26 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = (string, separator) => {
	if (!(typeof string === 'string' && typeof separator === 'string')) {
		throw new TypeError('Expected the arguments to be of type `string`');
	}

	if (separator === '') {
		return [string];
	}

	const separatorIndex = string.indexOf(separator);

	if (separatorIndex === -1) {
		return [string];
	}

	return [
		string.slice(0, separatorIndex),
		string.slice(separatorIndex + separator.length)
	];
};


/***/ }),
/* 27 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);

// CONCATENATED MODULE: ./node_modules/ramda/es/internal/_isPlaceholder.js
function _isPlaceholder(a) {
       return a != null && typeof a === 'object' && a['@@functional/placeholder'] === true;
}
// CONCATENATED MODULE: ./node_modules/ramda/es/internal/_curry1.js


/**
 * Optimized internal one-arity curry function.
 *
 * @private
 * @category Function
 * @param {Function} fn The function to curry.
 * @return {Function} The curried function.
 */
function _curry1(fn) {
  return function f1(a) {
    if (arguments.length === 0 || _isPlaceholder(a)) {
      return f1;
    } else {
      return fn.apply(this, arguments);
    }
  };
}
// CONCATENATED MODULE: ./node_modules/ramda/es/internal/_curry2.js



/**
 * Optimized internal two-arity curry function.
 *
 * @private
 * @category Function
 * @param {Function} fn The function to curry.
 * @return {Function} The curried function.
 */
function _curry2(fn) {
  return function f2(a, b) {
    switch (arguments.length) {
      case 0:
        return f2;
      case 1:
        return _isPlaceholder(a) ? f2 : _curry1(function (_b) {
          return fn(a, _b);
        });
      default:
        return _isPlaceholder(a) && _isPlaceholder(b) ? f2 : _isPlaceholder(a) ? _curry1(function (_a) {
          return fn(_a, b);
        }) : _isPlaceholder(b) ? _curry1(function (_b) {
          return fn(a, _b);
        }) : fn(a, b);
    }
  };
}
// CONCATENATED MODULE: ./node_modules/ramda/es/internal/_isNumber.js
function _isNumber(x) {
  return Object.prototype.toString.call(x) === '[object Number]';
}
// CONCATENATED MODULE: ./node_modules/ramda/es/range.js



/**
 * Returns a list of numbers from `from` (inclusive) to `to` (exclusive).
 *
 * @func
 * @memberOf R
 * @since v0.1.0
 * @category List
 * @sig Number -> Number -> [Number]
 * @param {Number} from The first number in the list.
 * @param {Number} to One more than the last number in the list.
 * @return {Array} The list of numbers in the set `[a, b)`.
 * @example
 *
 *      R.range(1, 5);    //=> [1, 2, 3, 4]
 *      R.range(50, 53);  //=> [50, 51, 52]
 */
var range_range = /*#__PURE__*/_curry2(function range(from, to) {
  if (!(_isNumber(from) && _isNumber(to))) {
    throw new TypeError('Both arguments to range must be numbers');
  }
  var result = [];
  var n = from;
  while (n < to) {
    result.push(n);
    n += 1;
  }
  return result;
});
/* harmony default export */ var es_range = (range_range);
// EXTERNAL MODULE: external {"root":"React","commonjs2":"react","commonjs":"react","amd":"react"}
var external_root_React_commonjs2_react_commonjs_react_amd_react_ = __webpack_require__(0);
var external_root_React_commonjs2_react_commonjs_react_amd_react_default = /*#__PURE__*/__webpack_require__.n(external_root_React_commonjs2_react_commonjs_react_amd_react_);

// EXTERNAL MODULE: ./node_modules/prop-types/index.js
var prop_types = __webpack_require__(1);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);

// CONCATENATED MODULE: ./src/DataTable/DataTable.js
var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };





var DataTable_DataTable = function DataTable(_ref) {
  var authorized = _ref.authorized,
      sortKeys = _ref.sortKeys,
      elements = _ref.elements,
      total = _ref.total,
      renderElement = _ref.renderElement,
      query = _ref.query,
      setQuery = _ref.setQuery;

  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
    "div",
    { className: "search-dataset-table", cellSpacing: 0 },
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "search-dataset-toolbar" },
      external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
        "div",
        { className: "input-group" },
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "label",
          { className: "input-group-addon" },
          "Sort By:"
        ),
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "select",
          {
            className: "form-control",
            value: query.sortKey,
            onChange: function onChange(e) {
              return setQuery(_extends({}, query, { sortKey: e.currentTarget.value }));
            }
          },
          sortKeys.map(function (_ref2, i) {
            var sortKey = _ref2.key,
                label = _ref2.label;
            return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "option",
              { key: i, value: sortKey },
              label
            );
          })
        )
      ),
      external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
        "div",
        { className: "input-group" },
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("input", {
          className: "form-control",
          style: { width: "350px" },
          value: query.search,
          onChange: function onChange(e) {
            return setQuery(_extends({}, query, { search: e.currentTarget.value }));
          }
        }),
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "span",
          { className: "input-group-addon" },
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("i", { className: "fa fa-search" })
        )
      )
    ),
    elements.map(function (element, i) {
      return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
        "div",
        {
          key: element.id,
          style: {
            borderBottom: "solid",
            borderBottomWidth: i === elements.length - 1 ? "0px" : "1px"
          }
        },
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(renderElement, _extends({}, element, { authorized: authorized }))
      );
    }),
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "search-dataset-footer" },
      external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
        "ul",
        { className: "pagination" },
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "li",
          {
            onClick: function onClick() {
              return setQuery(_extends({}, query, {
                cursor: Math.max(query.cursor - query.limit, 0)
              }));
            }
          },
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "a",
            { href: "#" },
            "\xAB"
          )
        ),
        es_range(1, Math.max(Math.floor(total / query.limit) + 1, 2)).map(function (page, i) {
          return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "li",
            {
              key: i,
              onClick: function onClick() {
                return setQuery(_extends({}, query, { cursor: (page - 1) * query.limit }));
              },
              className: page === Math.floor(query.cursor / query.limit) + 1 ? "active" : ""
            },
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "a",
              { href: "#" },
              page
            )
          );
        }),
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "li",
          {
            onClick: function onClick() {
              return setQuery(_extends({}, query, {
                cursor: Math.max(Math.min(query.cursor + query.limit, total - query.limit), 0)
              }));
            }
          },
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "a",
            { href: "#" },
            "\xBB"
          )
        )
      )
    )
  );
};

DataTable_DataTable.propTypes = {
  authorized: prop_types_default.a.bool,
  sortKeys: prop_types_default.a.arrayOf(prop_types_default.a.shape({ key: prop_types_default.a.string, label: prop_types_default.a.string })),
  elements: prop_types_default.a.arrayOf(prop_types_default.a.object),
  total: prop_types_default.a.number,
  renderElement: prop_types_default.a.func,
  query: prop_types_default.a.shape({
    search: prop_types_default.a.string,
    sortKey: prop_types_default.a.string,
    sortComparitor: prop_types_default.a.string,
    cursor: prop_types_default.a.number,
    limit: prop_types_default.a.number
  }),
  setQuery: prop_types_default.a.func
};

DataTable_DataTable.defaultProps = {
  sortKeys: [],
  elements: [],
  total: 0
};

/* harmony default export */ var src_DataTable_DataTable = (DataTable_DataTable);
// EXTERNAL MODULE: ./node_modules/babel-runtime/regenerator/index.js
var regenerator = __webpack_require__(3);
var regenerator_default = /*#__PURE__*/__webpack_require__.n(regenerator);

// CONCATENATED MODULE: ./node_modules/react-use/esm/createMemo.js

var createMemo = function (fn) { return function () {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
    }
    return Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"])(function () { return fn.apply(void 0, args); }, args);
}; };
/* harmony default export */ var esm_createMemo = (createMemo);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useAsync.js

var useAsync = function (fn, deps) {
    if (deps === void 0) { deps = []; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({
        loading: true
    }), state = _a[0], set = _a[1];
    var memoized = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(fn, deps);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var mounted = true;
        set({
            loading: true
        });
        var promise = memoized();
        promise.then(function (value) {
            if (mounted) {
                set({
                    loading: false,
                    value: value
                });
            }
        }, function (error) {
            if (mounted) {
                set({
                    loading: false,
                    error: error
                });
            }
        });
        return function () {
            mounted = false;
        };
    }, [memoized]);
    return state;
};
/* harmony default export */ var esm_useAsync = (useAsync);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useAsyncRetry.js
var __assign = (undefined && undefined.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};


var useAsyncRetry = function (fn, deps) {
    if (deps === void 0) { deps = []; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(0), attempt = _a[0], setAttempt = _a[1];
    var state = esm_useAsync(fn, deps.concat([attempt]));
    var stateLoading = state.loading;
    var retry = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function () {
        if (stateLoading) {
            if (false) {}
            return;
        }
        setAttempt(function (attempt) { return attempt + 1; });
    }, deps.concat([stateLoading, attempt]));
    return __assign({}, state, { retry: retry });
};
/* harmony default export */ var esm_useAsyncRetry = (useAsyncRetry);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useSetState.js

var useSetState = function (initialState) {
    if (initialState === void 0) { initialState = {}; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialState), state = _a[0], set = _a[1];
    var setState = function (patch) {
        set(function (prevState) { return Object.assign({}, prevState, patch instanceof Function ? patch(prevState) : patch); });
    };
    return [state, setState];
};
/* harmony default export */ var esm_useSetState = (useSetState);

// CONCATENATED MODULE: ./node_modules/react-use/esm/util/parseTimeRanges.js
var parseTimeRanges = function (ranges) {
    var result = [];
    for (var i = 0; i < ranges.length; i++) {
        result.push({
            start: ranges.start(i),
            end: ranges.end(i)
        });
    }
    return result;
};
/* harmony default export */ var util_parseTimeRanges = (parseTimeRanges);

// CONCATENATED MODULE: ./node_modules/react-use/esm/util/createHTMLMediaHook.js
var createHTMLMediaHook_assign = (undefined && undefined.__assign) || function () {
    createHTMLMediaHook_assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return createHTMLMediaHook_assign.apply(this, arguments);
};




var createHTMLMediaHook = function (tag) {
    var hook = function (elOrProps) {
        var element;
        var props;
        if (external_root_React_commonjs2_react_commonjs_react_amd_react_["isValidElement"](elOrProps)) {
            element = elOrProps;
            props = element.props;
        }
        else {
            props = elOrProps;
        }
        var _a = esm_useSetState({
            buffered: [],
            time: 0,
            duration: 0,
            isPlaying: false,
            muted: false,
            volume: 1,
        }), state = _a[0], setState = _a[1];
        var ref = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(null);
        var wrapEvent = function (userEvent, proxyEvent) {
            return function (event) {
                try {
                    proxyEvent && proxyEvent(event);
                }
                finally {
                    userEvent && userEvent(event);
                }
            };
        };
        var onPlay = function () { return setState({ isPlaying: true }); };
        var onPause = function () { return setState({ isPlaying: false }); };
        var onVolumeChange = function () {
            var el = ref.current;
            if (!el)
                return;
            setState({
                muted: el.muted,
                volume: el.volume,
            });
        };
        var onDurationChange = function () {
            var el = ref.current;
            if (!el)
                return;
            var duration = el.duration, buffered = el.buffered;
            setState({
                duration: duration,
                buffered: util_parseTimeRanges(buffered),
            });
        };
        var onTimeUpdate = function () {
            var el = ref.current;
            if (!el)
                return;
            setState({ time: el.currentTime });
        };
        var onProgress = function () {
            var el = ref.current;
            if (!el)
                return;
            setState({ buffered: util_parseTimeRanges(el.buffered) });
        };
        if (element) {
            element = external_root_React_commonjs2_react_commonjs_react_amd_react_["cloneElement"](element, createHTMLMediaHook_assign({ controls: false }, props, { ref: ref, onPlay: wrapEvent(props.onPlay, onPlay), onPause: wrapEvent(props.onPause, onPause), onVolumeChange: wrapEvent(props.onVolumeChange, onVolumeChange), onDurationChange: wrapEvent(props.onDurationChange, onDurationChange), onTimeUpdate: wrapEvent(props.onTimeUpdate, onTimeUpdate), onProgress: wrapEvent(props.onProgress, onProgress) }));
        }
        else {
            element = external_root_React_commonjs2_react_commonjs_react_amd_react_["createElement"](tag, createHTMLMediaHook_assign({ controls: false }, props, { ref: ref, onPlay: wrapEvent(props.onPlay, onPlay), onPause: wrapEvent(props.onPause, onPause), onVolumeChange: wrapEvent(props.onVolumeChange, onVolumeChange), onDurationChange: wrapEvent(props.onDurationChange, onDurationChange), onTimeUpdate: wrapEvent(props.onTimeUpdate, onTimeUpdate), onProgress: wrapEvent(props.onProgress, onProgress) })); // TODO: fix this typing.
        }
        // Some browsers return `Promise` on `.play()` and may throw errors
        // if one tries to execute another `.play()` or `.pause()` while that
        // promise is resolving. So we prevent that with this lock.
        // See: https://bugs.chromium.org/p/chromium/issues/detail?id=593273
        var lockPlay = false;
        var controls = {
            play: function () {
                var el = ref.current;
                if (!el)
                    return undefined;
                if (!lockPlay) {
                    var promise = el.play();
                    var isPromise = typeof promise === 'object';
                    if (isPromise) {
                        lockPlay = true;
                        var resetLock = function () {
                            lockPlay = false;
                        };
                        promise.then(resetLock, resetLock);
                    }
                    return promise;
                }
                return undefined;
            },
            pause: function () {
                var el = ref.current;
                if (el && !lockPlay) {
                    return el.pause();
                }
            },
            seek: function (time) {
                var el = ref.current;
                if (!el || (state.duration === undefined))
                    return;
                time = Math.min(state.duration, Math.max(0, time));
                el.currentTime = time;
            },
            volume: function (volume) {
                var el = ref.current;
                if (!el)
                    return;
                volume = Math.min(1, Math.max(0, volume));
                el.volume = volume;
                setState({ volume: volume });
            },
            mute: function () {
                var el = ref.current;
                if (!el)
                    return;
                el.muted = true;
            },
            unmute: function () {
                var el = ref.current;
                if (!el)
                    return;
                el.muted = false;
            },
        };
        Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
            var el = ref.current;
            if (!el) {
                if (false) {}
                return;
            }
            // Start media, if autoPlay requested.
            if (props.autoPlay && el.paused) {
                controls.play();
            }
            setState({
                volume: el.volume,
                muted: el.muted,
            });
        }, [props.src]);
        return [element, state, controls, ref];
    };
    return hook;
};
/* harmony default export */ var util_createHTMLMediaHook = (createHTMLMediaHook);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useAudio.js

var useAudio = util_createHTMLMediaHook('audio');
/* harmony default export */ var esm_useAudio = (useAudio);

// CONCATENATED MODULE: ./node_modules/react-use/esm/util.js
var isClient = typeof window === 'object';
var util_on = function (obj) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    return obj.addEventListener.apply(obj, args);
};
var off = function (obj) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    return obj.removeEventListener.apply(obj, args);
};

// CONCATENATED MODULE: ./node_modules/react-use/esm/useBattery.js


var useBattery = function () {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({}), state = _a[0], setState = _a[1];
    var mounted = true;
    var battery = null;
    var onChange = function () {
        var charging = battery.charging, level = battery.level, chargingTime = battery.chargingTime, dischargingTime = battery.dischargingTime;
        setState({
            charging: charging,
            level: level,
            chargingTime: chargingTime,
            dischargingTime: dischargingTime
        });
    };
    var onBattery = function () {
        onChange();
        util_on(battery, 'chargingchange', onChange);
        util_on(battery, 'levelchange', onChange);
        util_on(battery, 'chargingtimechange', onChange);
        util_on(battery, 'dischargingtimechange', onChange);
    };
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        navigator.getBattery().then(function (bat) {
            if (mounted) {
                battery = bat;
                onBattery();
            }
        });
        return function () {
            mounted = false;
            if (battery) {
                off(battery, 'chargingchange', onChange);
                off(battery, 'levelchange', onChange);
                off(battery, 'chargingtimechange', onChange);
                off(battery, 'dischargingtimechange', onChange);
            }
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useBattery = (useBattery);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useToggle.js

var useToggle = function (state) {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(state), value = _a[0], setValue = _a[1];
    var toggle = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (nextValue) {
        if (typeof nextValue !== 'undefined') {
            setValue(!!nextValue);
            return;
        }
        setValue(function (value) { return !value; });
    }, [setValue]);
    return [value, toggle];
};
/* harmony default export */ var esm_useToggle = (useToggle);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useBoolean.js

/* harmony default export */ var useBoolean = (esm_useToggle);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useUpdateEffect.js

var useUpdateEffect = function (effect, deps) {
    var isInitialMount = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(true);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(isInitialMount.current
        ? function () {
            isInitialMount.current = false;
        }
        : effect, deps);
};
/* harmony default export */ var esm_useUpdateEffect = (useUpdateEffect);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useRefMounted.js

var useRefMounted = function () {
    var refMounted = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(false);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        refMounted.current = true;
        return function () {
            refMounted.current = false;
        };
    });
    return refMounted;
};
/* harmony default export */ var esm_useRefMounted = (useRefMounted);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useCopyToClipboard.js
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (undefined && undefined.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var _this = undefined;



var writeTextDefault = __webpack_require__(19);
var useCopyToClipboard = function (text, options) {
    if (text === void 0) { text = ''; }
    var _a = (options || {}), _b = _a.writeText, writeText = _b === void 0 ? writeTextDefault : _b, onCopy = _a.onCopy, onError = _a.onError;
    if (false) {}
    var mounted = esm_useRefMounted();
    var latestText = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(text);
    var _c = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(false), copied = _c[0], setCopied = _c[1];
    var copyToClipboard = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function () { return __awaiter(_this, void 0, void 0, function () {
        var error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (latestText.current !== text) {
                        if (false) {}
                        return [2 /*return*/];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, writeText(text)];
                case 2:
                    _a.sent();
                    if (!mounted.current)
                        return [2 /*return*/];
                    setCopied(true);
                    onCopy && onCopy(text);
                    return [3 /*break*/, 4];
                case 3:
                    error_1 = _a.sent();
                    if (!mounted.current)
                        return [2 /*return*/];
                    console.error(error_1);
                    setCopied(false);
                    onError && onError(error_1, text);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    }); }, [text]);
    esm_useUpdateEffect(function () {
        setCopied(false);
        latestText.current = text;
    }, [text]);
    return [copied, copyToClipboard];
};
/* harmony default export */ var esm_useCopyToClipboard = (useCopyToClipboard);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useDrop.js


var useState = external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"], useMemo = external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"], useCallback = external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"], useEffect = external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"];
var noop = function () { };
var useDrop_defaultState = {
    over: false,
};
var createProcess = function (options, mounted) { return function (dataTransfer, event) {
    var uri = dataTransfer.getData('text/uri-list');
    if (uri) {
        (options.onUri || noop)(uri, event);
        return;
    }
    if (dataTransfer.files && dataTransfer.files.length) {
        (options.onFiles || noop)(Array.from(dataTransfer.files), event);
        return;
    }
    if (dataTransfer.items && dataTransfer.items.length) {
        dataTransfer.items[0].getAsString(function (text) {
            if (mounted.current) {
                (options.onText || noop)(text, event);
            }
        });
    }
}; };
var useDrop = function (options, args) {
    if (options === void 0) { options = {}; }
    if (args === void 0) { args = []; }
    var onFiles = options.onFiles, onText = options.onText, onUri = options.onUri;
    var mounted = esm_useRefMounted();
    var _a = useState(false), over = _a[0], setOverRaw = _a[1];
    var setOver = useCallback(setOverRaw, []);
    var process = useMemo(function () { return createProcess(options, mounted); }, [onFiles, onText, onUri]);
    useEffect(function () {
        var onDragOver = function (event) {
            event.preventDefault();
            setOver(true);
        };
        var onDragEnter = function (event) {
            event.preventDefault();
            setOver(true);
        };
        var onDragLeave = function () {
            setOver(false);
        };
        var onDragExit = function () {
            setOver(false);
        };
        var onDrop = function (event) {
            event.preventDefault();
            setOver(false);
            process(event.dataTransfer, event);
        };
        var onPaste = function (event) {
            process(event.clipboardData, event);
        };
        document.addEventListener('dragover', onDragOver);
        document.addEventListener('dragenter', onDragEnter);
        document.addEventListener('dragleave', onDragLeave);
        document.addEventListener('dragexit', onDragExit);
        document.addEventListener('drop', onDrop);
        if (onText)
            document.addEventListener('paste', onPaste);
        return function () {
            document.removeEventListener('dragover', onDragOver);
            document.removeEventListener('dragenter', onDragEnter);
            document.removeEventListener('dragleave', onDragLeave);
            document.removeEventListener('dragexit', onDragExit);
            document.removeEventListener('drop', onDrop);
            document.removeEventListener('paste', onPaste);
        };
    }, [process].concat(args));
    return { over: over };
};
/* harmony default export */ var esm_useDrop = (useDrop);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useDropArea.js


var useDropArea_noop = function () { };
var useDropArea_defaultState = {
    over: false,
};
var useDropArea_createProcess = function (options, mounted) { return function (dataTransfer, event) {
    var uri = dataTransfer.getData('text/uri-list');
    if (uri) {
        (options.onUri || useDropArea_noop)(uri, event);
        return;
    }
    if (dataTransfer.files && dataTransfer.files.length) {
        (options.onFiles || useDropArea_noop)(Array.from(dataTransfer.files), event);
        return;
    }
    if (dataTransfer.items && dataTransfer.items.length) {
        dataTransfer.items[0].getAsString(function (text) {
            if (mounted.current) {
                (options.onText || useDropArea_noop)(text, event);
            }
        });
    }
}; };
var createBond = function (process, setOver) { return ({
    onDragOver: function (event) {
        event.preventDefault();
    },
    onDragEnter: function (event) {
        event.preventDefault();
        setOver(true);
    },
    onDragLeave: function () {
        setOver(false);
    },
    onDrop: function (event) {
        event.preventDefault();
        event.persist();
        setOver(false);
        process(event.dataTransfer, event);
    },
    onPaste: function (event) {
        event.persist();
        process(event.clipboardData, event);
    },
}); };
var useDropArea = function (options) {
    if (options === void 0) { options = {}; }
    var onFiles = options.onFiles, onText = options.onText, onUri = options.onUri;
    var mounted = esm_useRefMounted();
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(false), over = _a[0], setOver = _a[1];
    var process = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"])(function () { return useDropArea_createProcess(options, mounted); }, [onFiles, onText, onUri]);
    var bond = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"])(function () { return createBond(process, setOver); }, [process, setOver]);
    return [bond, { over: over }];
};
/* harmony default export */ var esm_useDropArea = (useDropArea);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useUpdate.js

var useUpdate = function () {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(0), setState = _a[1];
    return function () { return setState(function (cnt) { return cnt + 1; }); };
};
/* harmony default export */ var esm_useUpdate = (useUpdate);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useGetSet.js


var useGetSet = function (initialValue) {
    var state = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(initialValue);
    var update = esm_useUpdate();
    var get = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function () { return state.current; }, []);
    var set = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (value) {
        state.current = value;
        update();
    }, []);
    return [get, set];
};
/* harmony default export */ var esm_useGetSet = (useGetSet);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useCounter.js


var useCounter = function (initialValue) {
    if (initialValue === void 0) { initialValue = 0; }
    var _a = esm_useGetSet(initialValue), get = _a[0], set = _a[1];
    var inc = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (delta) {
        if (delta === void 0) { delta = 1; }
        return set(get() + delta);
    }, []);
    var dec = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (delta) {
        if (delta === void 0) { delta = 1; }
        return inc(-delta);
    }, []);
    var reset = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (value) {
        if (value === void 0) { value = initialValue; }
        initialValue = value;
        set(value);
    }, []);
    var actions = {
        inc: inc,
        dec: dec,
        get: get,
        set: set,
        reset: reset,
    };
    return [get(), actions];
};
/* harmony default export */ var esm_useCounter = (useCounter);

// EXTERNAL MODULE: ./node_modules/nano-css/index.js
var nano_css = __webpack_require__(6);

// EXTERNAL MODULE: ./node_modules/nano-css/addon/cssom.js
var cssom = __webpack_require__(7);

// EXTERNAL MODULE: ./node_modules/nano-css/addon/vcssom.js
var vcssom = __webpack_require__(8);

// EXTERNAL MODULE: ./node_modules/nano-css/addon/vcssom/cssToTree.js
var cssToTree = __webpack_require__(9);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useCss.js





var nano = Object(nano_css["create"])();
Object(cssom["addon"])(nano);
Object(vcssom["addon"])(nano);
var counter = 0;
var useCss = function (css) {
    var className = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"])(function () { return 'react-use-css-' + (counter++).toString(36); }, []);
    var sheet = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"])(function () { return new nano.VSheet(); }, []);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useLayoutEffect"])(function () {
        var tree = {};
        Object(cssToTree["cssToTree"])(tree, css, '.' + className, '');
        sheet.diff(tree);
        return function () {
            sheet.diff({});
        };
    });
    return className;
};
/* harmony default export */ var esm_useCss = (useCss);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useDebounce.js

var useDebounce = function (fn, ms, args) {
    if (ms === void 0) { ms = 0; }
    if (args === void 0) { args = []; }
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var handle = setTimeout(fn.bind(null, args), ms);
        return function () {
            // if args change then clear timeout
            clearTimeout(handle);
        };
    }, args);
};
/* harmony default export */ var esm_useDebounce = (useDebounce);

// EXTERNAL MODULE: ./node_modules/react-fast-compare/index.js
var react_fast_compare = __webpack_require__(10);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useDeepCompareEffect.js


var isPrimitive = function (val) { return val !== Object(val); };
var useDeepCompareEffect = function (effect, deps) {
    if (false) {}
    var ref = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(undefined);
    if (!react_fast_compare(deps, ref.current)) {
        ref.current = deps;
    }
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(effect, ref.current);
};
/* harmony default export */ var esm_useDeepCompareEffect = (useDeepCompareEffect);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useEffectOnce.js

var useEffectOnce = function (effect) {
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(effect, []);
};
/* harmony default export */ var esm_useEffectOnce = (useEffectOnce);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useEvent.js


var defaultTarget = isClient ? window : null;
var useEvent = function (name, handler, target, options) {
    if (target === void 0) { target = defaultTarget; }
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (!handler)
            return;
        if (!target)
            return;
        var fn = (target.addEventListener || target.on);
        fn.call(target, name, handler, options);
        return function () {
            var fn = (target.removeEventListener || target.off);
            fn.call(target, name, handler, options);
        };
    }, [name, handler, target, JSON.stringify(options)]);
};
/* harmony default export */ var esm_useEvent = (useEvent);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useFavicon.js

var useFavicon = function (href) {
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = href;
        document.getElementsByTagName('head')[0].appendChild(link);
    }, [href]);
};
/* harmony default export */ var esm_useFavicon = (useFavicon);

// EXTERNAL MODULE: ./node_modules/screenfull/dist/screenfull.js
var screenfull = __webpack_require__(2);
var screenfull_default = /*#__PURE__*/__webpack_require__.n(screenfull);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useFullscreen.js


var useFullscreen_noop = function () { };
var useFullscreen = function (ref, on, options) {
    if (options === void 0) { options = {}; }
    var video = options.video, _a = options.onClose, onClose = _a === void 0 ? useFullscreen_noop : _a;
    var _b = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(on), isFullscreen = _b[0], setIsFullscreen = _b[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useLayoutEffect"])(function () {
        if (!on)
            return;
        if (!ref.current)
            return;
        var onWebkitEndFullscreen = function () {
            video.current.removeEventListener('webkitendfullscreen', onWebkitEndFullscreen);
            onClose();
        };
        var onChange = function () {
            if (screenfull_default.a) {
                var isFullscreen_1 = screenfull_default.a.isFullscreen;
                setIsFullscreen(isFullscreen_1);
                if (!isFullscreen_1) {
                    onClose();
                }
            }
        };
        if (screenfull_default.a && screenfull_default.a.enabled) {
            try {
                screenfull_default.a.request(ref.current);
                setIsFullscreen(true);
            }
            catch (error) {
                onClose(error);
                setIsFullscreen(false);
            }
            screenfull_default.a.on('change', onChange);
        }
        else if (video && video.current && video.current.webkitEnterFullscreen) {
            video.current.webkitEnterFullscreen();
            video.current.addEventListener('webkitendfullscreen', onWebkitEndFullscreen);
            setIsFullscreen(true);
        }
        else {
            onClose();
            setIsFullscreen(false);
        }
        return function () {
            setIsFullscreen(false);
            if (screenfull_default.a && screenfull_default.a.enabled) {
                try {
                    screenfull_default.a.off('change', onChange);
                    screenfull_default.a.exit();
                }
                catch (_a) { }
            }
            else if (video && video.current && video.current.webkitExitFullscreen) {
                video.current.removeEventListener('webkitendfullscreen', onWebkitEndFullscreen);
                video.current.webkitExitFullscreen();
            }
        };
    }, [ref.current, video, on]);
    return isFullscreen;
};
/* harmony default export */ var esm_useFullscreen = (useFullscreen);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useGeolocation.js
var useGeolocation_assign = (undefined && undefined.__assign) || function () {
    useGeolocation_assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return useGeolocation_assign.apply(this, arguments);
};

var useGeolocation = function () {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({
        loading: true,
        accuracy: null,
        altitude: null,
        altitudeAccuracy: null,
        heading: null,
        latitude: null,
        longitude: null,
        speed: null,
        timestamp: Date.now(),
    }), state = _a[0], setState = _a[1];
    var mounted = true;
    var watchId;
    var onEvent = function (event) {
        if (mounted) {
            setState({
                loading: false,
                accuracy: event.coords.accuracy,
                altitude: event.coords.altitude,
                altitudeAccuracy: event.coords.altitudeAccuracy,
                heading: event.coords.heading,
                latitude: event.coords.latitude,
                longitude: event.coords.longitude,
                speed: event.coords.speed,
                timestamp: event.timestamp,
            });
        }
    };
    var onEventError = function (error) {
        return mounted && setState(function (oldState) { return (useGeolocation_assign({}, oldState, { loading: false, error: error })); });
    };
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        navigator.geolocation.getCurrentPosition(onEvent, onEventError);
        watchId = navigator.geolocation.watchPosition(onEvent, onEventError);
        return function () {
            mounted = false;
            navigator.geolocation.clearWatch(watchId);
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useGeolocation = (useGeolocation);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useGetSetState.js
var useGetSetState_assign = (undefined && undefined.__assign) || function () {
    useGetSetState_assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return useGetSetState_assign.apply(this, arguments);
};


var useGetSetState = function (initialState) {
    if (initialState === void 0) { initialState = {}; }
    if (false) {}
    var update = esm_useUpdate();
    var state = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(useGetSetState_assign({}, initialState));
    var get = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function () { return state.current; }, []);
    var set = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (patch) {
        if (!patch)
            return;
        if (false) {}
        Object.assign(state.current, patch);
        update();
    }, []);
    return [get, set];
};
/* harmony default export */ var esm_useGetSetState = (useGetSetState);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useHover.js

var useHover_useState = external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"];
var useHover_noop = function () { };
var useHover = function (element) {
    var _a = useHover_useState(false), state = _a[0], setState = _a[1];
    var onMouseEnter = function (originalOnMouseEnter) { return function (event) {
        (originalOnMouseEnter || useHover_noop)(event);
        setState(true);
    }; };
    var onMouseLeave = function (originalOnMouseLeave) { return function (event) {
        (originalOnMouseLeave || useHover_noop)(event);
        setState(false);
    }; };
    if (typeof element === 'function') {
        element = element(state);
    }
    var el = external_root_React_commonjs2_react_commonjs_react_amd_react_["cloneElement"](element, {
        onMouseEnter: onMouseEnter(element.props.onMouseEnter),
        onMouseLeave: onMouseLeave(element.props.onMouseLeave)
    });
    return [el, state];
};
/* harmony default export */ var esm_useHover = (useHover);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useHoverDirty.js

// kudos: https://usehooks.com/
var useHoverDirty = function (ref, enabled) {
    if (enabled === void 0) { enabled = true; }
    if (false) {}
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(false), value = _a[0], setValue = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var onMouseOver = function () { return setValue(true); };
        var onMouseOut = function () { return setValue(false); };
        if (enabled && ref && ref.current) {
            ref.current.addEventListener('mouseover', onMouseOver);
            ref.current.addEventListener('mouseout', onMouseOut);
        }
        return function () {
            if (enabled && ref && ref.current) {
                ref.current.removeEventListener('mouseover', onMouseOver);
                ref.current.removeEventListener('mouseout', onMouseOut);
            }
        };
    }, [enabled, ref]);
    return value;
};
/* harmony default export */ var esm_useHoverDirty = (useHoverDirty);

// CONCATENATED MODULE: ./node_modules/throttle-debounce/dist/index.esm.js
/* eslint-disable no-undefined,no-param-reassign,no-shadow */

/**
 * Throttle execution of a function. Especially useful for rate limiting
 * execution of handlers on events like resize and scroll.
 *
 * @param  {Number}    delay          A zero-or-greater delay in milliseconds. For event callbacks, values around 100 or 250 (or even higher) are most useful.
 * @param  {Boolean}   [noTrailing]   Optional, defaults to false. If noTrailing is true, callback will only execute every `delay` milliseconds while the
 *                                    throttled-function is being called. If noTrailing is false or unspecified, callback will be executed one final time
 *                                    after the last throttled-function call. (After the throttled-function has not been called for `delay` milliseconds,
 *                                    the internal counter is reset)
 * @param  {Function}  callback       A function to be executed after delay milliseconds. The `this` context and all arguments are passed through, as-is,
 *                                    to `callback` when the throttled-function is executed.
 * @param  {Boolean}   [debounceMode] If `debounceMode` is true (at begin), schedule `clear` to execute after `delay` ms. If `debounceMode` is false (at end),
 *                                    schedule `callback` to execute after `delay` ms.
 *
 * @return {Function}  A new, throttled, function.
 */
function throttle (delay, noTrailing, callback, debounceMode) {
  /*
   * After wrapper has stopped being called, this timeout ensures that
   * `callback` is executed at the proper times in `throttle` and `end`
   * debounce modes.
   */
  var timeoutID;
  var cancelled = false; // Keep track of the last time `callback` was executed.

  var lastExec = 0; // Function to clear existing timeout

  function clearExistingTimeout() {
    if (timeoutID) {
      clearTimeout(timeoutID);
    }
  } // Function to cancel next exec


  function cancel() {
    clearExistingTimeout();
    cancelled = true;
  } // `noTrailing` defaults to falsy.


  if (typeof noTrailing !== 'boolean') {
    debounceMode = callback;
    callback = noTrailing;
    noTrailing = undefined;
  }
  /*
   * The `wrapper` function encapsulates all of the throttling / debouncing
   * functionality and when executed will limit the rate at which `callback`
   * is executed.
   */


  function wrapper() {
    var self = this;
    var elapsed = Date.now() - lastExec;
    var args = arguments;

    if (cancelled) {
      return;
    } // Execute `callback` and update the `lastExec` timestamp.


    function exec() {
      lastExec = Date.now();
      callback.apply(self, args);
    }
    /*
     * If `debounceMode` is true (at begin) this is used to clear the flag
     * to allow future `callback` executions.
     */


    function clear() {
      timeoutID = undefined;
    }

    if (debounceMode && !timeoutID) {
      /*
       * Since `wrapper` is being called for the first time and
       * `debounceMode` is true (at begin), execute `callback`.
       */
      exec();
    }

    clearExistingTimeout();

    if (debounceMode === undefined && elapsed > delay) {
      /*
       * In throttle mode, if `delay` time has been exceeded, execute
       * `callback`.
       */
      exec();
    } else if (noTrailing !== true) {
      /*
       * In trailing throttle mode, since `delay` time has not been
       * exceeded, schedule `callback` to execute `delay` ms after most
       * recent execution.
       *
       * If `debounceMode` is true (at begin), schedule `clear` to execute
       * after `delay` ms.
       *
       * If `debounceMode` is false (at end), schedule `callback` to
       * execute after `delay` ms.
       */
      timeoutID = setTimeout(debounceMode ? clear : exec, debounceMode === undefined ? delay - elapsed : delay);
    }
  }

  wrapper.cancel = cancel; // Return the wrapper function.

  return wrapper;
}

/* eslint-disable no-undefined */
/**
 * Debounce execution of a function. Debouncing, unlike throttling,
 * guarantees that a function is only executed a single time, either at the
 * very beginning of a series of calls, or at the very end.
 *
 * @param  {Number}   delay         A zero-or-greater delay in milliseconds. For event callbacks, values around 100 or 250 (or even higher) are most useful.
 * @param  {Boolean}  [atBegin]     Optional, defaults to false. If atBegin is false or unspecified, callback will only be executed `delay` milliseconds
 *                                  after the last debounced-function call. If atBegin is true, callback will be executed only at the first debounced-function call.
 *                                  (After the throttled-function has not been called for `delay` milliseconds, the internal counter is reset).
 * @param  {Function} callback      A function to be executed after delay milliseconds. The `this` context and all arguments are passed through, as-is,
 *                                  to `callback` when the debounced-function is executed.
 *
 * @return {Function} A new, debounced function.
 */

function debounce (delay, atBegin, callback) {
  return callback === undefined ? throttle(delay, atBegin, false) : throttle(delay, callback, atBegin !== false);
}



// CONCATENATED MODULE: ./node_modules/react-use/esm/useIdle.js



var defaultEvents = ['mousemove', 'mousedown', 'resize', 'keydown', 'touchstart', 'wheel'];
var oneMinute = 60e3;
var useIdle = function (ms, initialState, events) {
    if (ms === void 0) { ms = oneMinute; }
    if (initialState === void 0) { initialState = false; }
    if (events === void 0) { events = defaultEvents; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialState), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var mounted = true;
        var timeout;
        var localState = state;
        var set = function (newState) {
            if (mounted) {
                localState = newState;
                setState(newState);
            }
        };
        var onEvent = throttle(50, function () {
            if (localState) {
                set(false);
            }
            clearTimeout(timeout);
            timeout = setTimeout(function () { return set(true); }, ms);
        });
        var onVisibility = function () {
            if (!document.hidden)
                onEvent();
        };
        for (var i = 0; i < events.length; i++) {
            util_on(window, events[i], onEvent);
        }
        util_on(document, 'visibilitychange', onVisibility);
        timeout = setTimeout(function () { return set(true); }, ms);
        return function () {
            mounted = false;
            for (var i = 0; i < events.length; i++) {
                off(window, events[i], onEvent);
            }
            off(document, 'visibilitychange', onVisibility);
        };
    }, events);
    return state;
};
/* harmony default export */ var esm_useIdle = (useIdle);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useKey.js


var useKey_noop = function () { };
var createKeyPredicate = function (keyFilter) {
    return typeof keyFilter === 'function'
        ? keyFilter
        : typeof keyFilter === 'string'
            ? function (event) { return event.key === keyFilter; }
            : keyFilter
                ? function () { return true; }
                : function () { return false; };
};
var useKey = function (key, fn, opts, deps) {
    if (fn === void 0) { fn = useKey_noop; }
    if (opts === void 0) { opts = {}; }
    if (deps === void 0) { deps = [key]; }
    var _a = opts.event, event = _a === void 0 ? 'keydown' : _a, target = opts.target, options = opts.options;
    var handler = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useMemo"])(function () {
        var predicate = createKeyPredicate(key);
        var handler = function (event) {
            if (predicate(event))
                return fn(event);
        };
        return handler;
    }, deps);
    esm_useEvent(event, handler, target, options);
};
/* harmony default export */ var esm_useKey = (useKey);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useKeyPress.js


var useKeyPress_useKeyPress = function (keyFilter) {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])([false, null]), state = _a[0], set = _a[1];
    esm_useKey(keyFilter, function (event) { return set([true, event]); }, { event: 'keydown' }, [state]);
    esm_useKey(keyFilter, function (event) { return set([false, event]); }, { event: 'keyup' }, [state]);
    return state;
};
/* harmony default export */ var esm_useKeyPress = (useKeyPress_useKeyPress);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useKeyPressEvent.js


var useKeyPressEvent = function (key, keydown, keyup, useKeyPress) {
    if (useKeyPress === void 0) { useKeyPress = esm_useKeyPress; }
    var _a = useKeyPress(key), pressed = _a[0], event = _a[1];
    esm_useUpdateEffect(function () {
        if (!pressed && keyup)
            keyup(event);
        else if (pressed && keydown)
            keydown(event);
    }, [pressed]);
};
/* harmony default export */ var esm_useKeyPressEvent = (useKeyPressEvent);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMount.js

var useMount = function (fn) {
    esm_useEffectOnce(function () {
        fn();
    });
};
/* harmony default export */ var esm_useMount = (useMount);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useKeyboardJs.js


var useKeyboardJs = function (combination) {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])([false, null]), state = _a[0], set = _a[1];
    var _b = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(null), keyboardJs = _b[0], setKeyboardJs = _b[1];
    esm_useMount(function () {
        __webpack_require__.e(/* import() */ 1).then(__webpack_require__.t.bind(null, 33, 7)).then(setKeyboardJs);
    });
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (!keyboardJs)
            return;
        var down = function (event) { return set([true, event]); };
        var up = function (event) { return set([false, event]); };
        keyboardJs.bind(combination, down, up);
        return function () {
            keyboardJs.unbind(combination, down, up);
        };
    }, [combination, keyboardJs]);
    return state;
};
/* harmony default export */ var esm_useKeyboardJs = (useKeyboardJs);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useLifecycles.js

var useLifecycles = function (mount, unmount) {
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (mount)
            mount();
        return function () {
            if (unmount)
                unmount();
        };
    }, []);
};
/* harmony default export */ var esm_useLifecycles = (useLifecycles);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useList.js

var useList = function (initialList) {
    if (initialList === void 0) { initialList = []; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialList), list = _a[0], set = _a[1];
    return [list, {
            set: set,
            clear: function () { return set([]); },
            updateAt: function (index, entry) { return set(function (list) { return list.slice(0, index).concat([
                entry
            ], list.slice(index + 1)); }); },
            remove: function (index) { return set(function (list) { return list.slice(0, index).concat(list.slice(index + 1)); }); },
            push: function (entry) { return set(function (list) { return list.concat([entry]); }); },
            filter: function (fn) { return set(function (list) { return list.filter(fn); }); },
            sort: function (fn) { return set(function (list) { return list.slice().sort(fn); }); },
        }];
};
/* harmony default export */ var esm_useList = (useList);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useLocalStorage.js


var useLocalStorage = function (key, initialValue, raw) {
    if (!isClient) {
        return [initialValue, function () { }];
    }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(function () {
        try {
            var localStorageValue = localStorage.getItem(key);
            if (typeof localStorageValue !== 'string') {
                localStorage.setItem(key, raw ? String(initialValue) : JSON.stringify(initialValue));
                return initialValue;
            }
            else {
                return raw ? localStorageValue : JSON.parse(localStorageValue || 'null');
            }
        }
        catch (_a) {
            // If user is in private mode or has storage restriction
            // localStorage can throw. JSON.parse and JSON.stringify
            // can throw, too.
            return initialValue;
        }
    }), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        try {
            var serializedState = raw ? String(state) : JSON.stringify(state);
            localStorage.setItem(key, serializedState);
        }
        catch (_a) {
            // If user is in private mode or has storage restriction
            // localStorage can throw. Also JSON.stringify can throw.
        }
    });
    return [state, setState];
};
/* harmony default export */ var esm_useLocalStorage = (useLocalStorage);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useLocation.js


var patchHistoryMethod = function (method) {
    var original = history[method];
    history[method] = function (state) {
        var result = original.apply(this, arguments);
        var event = new Event(method.toLowerCase());
        event.state = state;
        window.dispatchEvent(event);
        return result;
    };
};
if (isClient) {
    patchHistoryMethod('pushState');
    patchHistoryMethod('replaceState');
}
var useLocation = function () {
    var buildState = function (trigger) {
        var state = history.state, length = history.length;
        var hash = location.hash, host = location.host, hostname = location.hostname, href = location.href, origin = location.origin, pathname = location.pathname, port = location.port, protocol = location.protocol, search = location.search;
        return {
            trigger: trigger,
            state: state,
            length: length,
            hash: hash,
            host: host,
            hostname: hostname,
            href: href,
            origin: origin,
            pathname: pathname,
            port: port,
            protocol: protocol,
            search: search
        };
    };
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(isClient
        ? buildState('load')
        : {
            trigger: 'load',
            length: 1
        }), state = _a[0], setState = _a[1];
    var onChange = function (trigger) {
        return setState(buildState(trigger));
    };
    var onPopstate = function () { return onChange('popstate'); };
    var onPushstate = function () { return onChange('pushstate'); };
    var onReplacestate = function () { return onChange('replacestate'); };
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        util_on(window, 'popstate', onPopstate);
        util_on(window, 'pushstate', onPushstate);
        util_on(window, 'replacestate', onReplacestate);
        return function () {
            off(window, 'popstate', onPopstate);
            off(window, 'pushstate', onPushstate);
            off(window, 'replacestate', onReplacestate);
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useLocation = (useLocation);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useLockBodyScroll.js

var useLockBodyScroll_counter = 0;
var originalOverflow = null;
var lock = function () {
    originalOverflow = window.getComputedStyle(document.body).overflow;
    document.body.style.overflow = 'hidden';
};
var unlock = function () {
    document.body.style.overflow = originalOverflow;
    originalOverflow = null;
};
var increment = function () {
    useLockBodyScroll_counter++;
    if (useLockBodyScroll_counter === 1)
        lock();
};
var decrement = function () {
    useLockBodyScroll_counter--;
    if (useLockBodyScroll_counter === 0)
        unlock();
};
var useLockBodyScroll = function (enabled) {
    if (enabled === void 0) { enabled = true; }
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () { return enabled ? (increment(), decrement) : undefined; }, [enabled]);
};
/* harmony default export */ var esm_useLockBodyScroll = (useLockBodyScroll);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useLogger.js


var useLogger = function (componentName) {
    var rest = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        rest[_i - 1] = arguments[_i];
    }
    esm_useEffectOnce(function () {
        console.log.apply(console, [componentName + " mounted"].concat(rest));
        return function () { return console.log(componentName + " unmounted"); };
    });
    esm_useUpdateEffect(function () {
        console.log.apply(console, [componentName + " updated"].concat(rest));
    });
};
/* harmony default export */ var esm_useLogger = (useLogger);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMap.js
var useMap_assign = (undefined && undefined.__assign) || function () {
    useMap_assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return useMap_assign.apply(this, arguments);
};
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) if (e.indexOf(p[i]) < 0)
            t[p[i]] = s[p[i]];
    return t;
};

var useMap = function (initialMap) {
    if (initialMap === void 0) { initialMap = {}; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialMap), map = _a[0], set = _a[1];
    return [map, {
            get: function (key) { return map[key]; },
            set: function (key, entry) {
                var _a;
                return set(useMap_assign({}, map, (_a = {}, _a[key] = entry, _a)));
            },
            remove: function (key) {
                var _a = map, _b = key, omit = _a[_b], rest = __rest(_a, [typeof _b === "symbol" ? _b : _b + ""]);
                set(rest);
            },
            reset: function () { return set(initialMap); },
        }];
};
/* harmony default export */ var esm_useMap = (useMap);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMedia.js

var useMedia = function (query, defaultState) {
    if (defaultState === void 0) { defaultState = false; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(defaultState), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var mounted = true;
        var mql = window.matchMedia(query);
        var onChange = function () {
            if (!mounted)
                return;
            setState(!!mql.matches);
        };
        mql.addListener(onChange);
        setState(mql.matches);
        return function () {
            mounted = false;
            mql.removeListener(onChange);
        };
    }, [query]);
    return state;
};
/* harmony default export */ var esm_useMedia = (useMedia);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMediaDevices.js


var useMediaDevices_noop = function () { };
var useMediaDevices = function () {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({}), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var mounted = true;
        var onChange = function () {
            navigator.mediaDevices.enumerateDevices()
                .then(function (devices) {
                if (mounted) {
                    setState({
                        devices: devices.map(function (_a) {
                            var deviceId = _a.deviceId, groupId = _a.groupId, kind = _a.kind, label = _a.label;
                            return ({ deviceId: deviceId, groupId: groupId, kind: kind, label: label });
                        })
                    });
                }
            })
                .catch(useMediaDevices_noop);
        };
        util_on(navigator.mediaDevices, 'devicechange', onChange);
        onChange();
        return function () {
            mounted = false;
            off(navigator.mediaDevices, 'devicechange', onChange);
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useMediaDevices = (useMediaDevices);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMotion.js


var useMotion_defaultState = {
    acceleration: {
        x: null,
        y: null,
        z: null,
    },
    accelerationIncludingGravity: {
        x: null,
        y: null,
        z: null,
    },
    rotationRate: {
        alpha: null,
        beta: null,
        gamma: null,
    },
    interval: 16,
};
var useMotion = function (initialState) {
    if (initialState === void 0) { initialState = useMotion_defaultState; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialState), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var handler = function (event) {
            var acceleration = event.acceleration, accelerationIncludingGravity = event.accelerationIncludingGravity, rotationRate = event.rotationRate, interval = event.interval;
            setState({
                acceleration: {
                    x: acceleration.x,
                    y: acceleration.y,
                    z: acceleration.z
                },
                accelerationIncludingGravity: {
                    x: accelerationIncludingGravity.x,
                    y: accelerationIncludingGravity.y,
                    z: accelerationIncludingGravity.z
                },
                rotationRate: {
                    alpha: rotationRate.alpha,
                    beta: rotationRate.beta,
                    gamma: rotationRate.gamma,
                },
                interval: interval
            });
        };
        util_on(window, 'devicemotion', handler);
        return function () {
            off(window, 'devicemotion', handler);
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useMotion = (useMotion);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMouse.js

var useMouse = function (ref) {
    if (false) {}
    var frame = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(0);
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({
        docX: 0,
        docY: 0,
        posX: 0,
        posY: 0,
        elX: 0,
        elY: 0,
        elH: 0,
        elW: 0,
    }), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var moveHandler = function (event) {
            cancelAnimationFrame(frame.current);
            frame.current = requestAnimationFrame(function () {
                if (ref && ref.current) {
                    var _a = ref.current.getBoundingClientRect(), left = _a.left, top_1 = _a.top, elW = _a.width, elH = _a.height;
                    var posX = left + window.scrollX;
                    var posY = top_1 + window.scrollY;
                    var elX = event.pageX - posX;
                    var elY = event.pageY - posY;
                    setState({
                        docX: event.pageX,
                        docY: event.pageY,
                        posX: posX,
                        posY: posY,
                        elX: elX,
                        elY: elY,
                        elH: elH,
                        elW: elW,
                    });
                }
            });
        };
        document.addEventListener('mousemove', moveHandler);
        return function () {
            cancelAnimationFrame(frame.current);
            document.removeEventListener('mousemove', moveHandler);
        };
    }, [ref.current]);
    return state;
};
/* harmony default export */ var esm_useMouse = (useMouse);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useMouseHovered.js


var nullRef = { current: null };
var useMouseHovered = function (ref, options) {
    if (options === void 0) { options = {}; }
    var whenHovered = !!options.whenHovered;
    var bound = !!options.bound;
    var isHovered = esm_useHoverDirty(ref, whenHovered);
    var state = esm_useMouse(whenHovered && !isHovered ? nullRef : ref);
    if (bound) {
        state.elX = Math.max(0, Math.min(state.elX, state.elW));
        state.elY = Math.max(0, Math.min(state.elY, state.elH));
    }
    return state;
};
/* harmony default export */ var esm_useMouseHovered = (useMouseHovered);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useNetwork.js
var useNetwork_assign = (undefined && undefined.__assign) || function () {
    useNetwork_assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return useNetwork_assign.apply(this, arguments);
};


var getConnection = function () {
    if (typeof navigator !== 'object') {
        return null;
    }
    var nav = navigator;
    return nav.connection || nav.mozConnection || nav.webkitConnection;
};
var getConnectionState = function () {
    var connection = getConnection();
    if (!connection) {
        return {};
    }
    var downlink = connection.downlink, downlinkMax = connection.downlinkMax, effectiveType = connection.effectiveType, type = connection.type, rtt = connection.rtt;
    return {
        downlink: downlink,
        downlinkMax: downlinkMax,
        effectiveType: effectiveType,
        type: type,
        rtt: rtt
    };
};
var useNetwork = function (initialState) {
    if (initialState === void 0) { initialState = {}; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialState), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var localState = state;
        var localSetState = function (patch) {
            localState = useNetwork_assign({}, localState, patch);
            setState(localState);
        };
        var connection = getConnection();
        var onOnline = function () {
            localSetState({
                online: true,
                since: new Date()
            });
        };
        var onOffline = function () {
            localSetState({
                online: false,
                since: new Date()
            });
        };
        var onConnectionChange = function () {
            localSetState(getConnectionState());
        };
        util_on(window, 'online', onOnline);
        util_on(window, 'offline', onOffline);
        if (connection) {
            util_on(connection, 'change', onConnectionChange);
            localSetState(useNetwork_assign({}, state, { online: navigator.onLine, since: undefined }, getConnectionState()));
        }
        return function () {
            off(window, 'online', onOnline);
            off(window, 'offline', onOffline);
            if (connection) {
                off(connection, 'change', onConnectionChange);
            }
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useNetwork = (useNetwork);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useNumber.js

/* harmony default export */ var useNumber = (esm_useCounter);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useObservable.js

var useObservable = function (observable$, initialValue) {
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialValue), value = _a[0], update = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var s = observable$.subscribe(update);
        return function () { return s.unsubscribe(); };
    }, [observable$]);
    return value;
};
/* harmony default export */ var esm_useObservable = (useObservable);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useOrientation.js


var useOrientation_defaultState = {
    angle: 0,
    type: 'landscape-primary'
};
var useOrientation = function (initialState) {
    if (initialState === void 0) { initialState = useOrientation_defaultState; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(initialState), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var mounted = true;
        var onChange = function () {
            if (mounted) {
                var orientation_1 = screen.orientation;
                if (orientation_1) {
                    var angle = orientation_1.angle, type = orientation_1.type;
                    setState({ angle: angle, type: type });
                }
                else if (window.orientation) {
                    setState({
                        angle: typeof window.orientation === 'number' ? window.orientation : 0,
                        type: ''
                    });
                }
                else {
                    setState(initialState);
                }
            }
        };
        util_on(window, 'orientationchange', onChange);
        onChange();
        return function () {
            mounted = false;
            off(window, 'orientationchange', onChange);
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useOrientation = (useOrientation);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useClickAway.js


var useClickAway = function (ref, onClickAway) {
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var handler = function (event) {
            var el = ref.current;
            el && !el.contains(event.target) && onClickAway(event);
        };
        util_on(document, 'click', handler);
        return function () {
            off(document, 'click', handler);
        };
    });
};
/* harmony default export */ var esm_useClickAway = (useClickAway);

// CONCATENATED MODULE: ./node_modules/react-use/esm/usePageLeave.js

var usePageLeave = function (onPageLeave, args) {
    if (args === void 0) { args = []; }
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (!onPageLeave)
            return;
        var handler = function (event) {
            event = event ? event : window.event;
            var from = event.relatedTarget || event.toElement;
            if (!from || from.nodeName === 'HTML')
                onPageLeave();
        };
        document.addEventListener('mouseout', handler);
        return function () {
            document.removeEventListener('mouseout', handler);
        };
    }, args);
};
/* harmony default export */ var esm_usePageLeave = (usePageLeave);

// CONCATENATED MODULE: ./node_modules/react-use/esm/usePromise.js


var usePromise = function () {
    var refMounted = esm_useRefMounted();
    return Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useCallback"])(function (promise) {
        return new Promise(function (resolve, reject) {
            var onValue = function (value) {
                if (refMounted.current) {
                    resolve(value);
                }
            };
            var onError = function (error) {
                if (refMounted.current) {
                    reject(error);
                }
            };
            promise.then(onValue, onError);
        });
    }, []);
};
/* harmony default export */ var esm_usePromise = (usePromise);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useRaf.js

var useRaf = function (ms, delay) {
    if (ms === void 0) { ms = 1e12; }
    if (delay === void 0) { delay = 0; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(0), elapsed = _a[0], set = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useLayoutEffect"])(function () {
        var raf, timerStop, start;
        var onFrame = function () {
            var time = Math.min(1, (Date.now() - start) / ms);
            set(time);
            loop();
        };
        var loop = function () {
            raf = requestAnimationFrame(onFrame);
        };
        var onStart = function () {
            timerStop = setTimeout(function () {
                cancelAnimationFrame(raf);
                set(1);
            }, ms);
            start = Date.now();
            loop();
        };
        var timerDelay = setTimeout(onStart, delay);
        return function () {
            clearTimeout(timerStop);
            clearTimeout(timerDelay);
            cancelAnimationFrame(raf);
        };
    }, [ms, delay]);
    return elapsed;
};
/* harmony default export */ var esm_useRaf = (useRaf);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useScroll.js

var useScroll = function (ref) {
    if (false) {}
    var frame = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(0);
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({
        x: 0,
        y: 0
    }), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var handler = function () {
            cancelAnimationFrame(frame.current);
            frame.current = requestAnimationFrame(function () {
                if (ref.current) {
                    setState({
                        x: ref.current.scrollLeft,
                        y: ref.current.scrollTop
                    });
                }
            });
        };
        if (ref.current) {
            ref.current.addEventListener('scroll', handler, {
                capture: false,
                passive: true
            });
        }
        return function () {
            if (frame.current) {
                cancelAnimationFrame(frame.current);
            }
            if (ref.current) {
                ref.current.removeEventListener('scroll', handler);
            }
        };
    }, [ref.current]);
    return state;
};
/* harmony default export */ var esm_useScroll = (useScroll);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useSessionStorage.js


var useSessionStorage = function (key, initialValue, raw) {
    if (!isClient) {
        return [initialValue, function () { }];
    }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(function () {
        try {
            var sessionStorageValue = sessionStorage.getItem(key);
            if (typeof sessionStorageValue !== 'string') {
                sessionStorage.setItem(key, raw ? String(initialValue) : JSON.stringify(initialValue));
                return initialValue;
            }
            else {
                return raw ? sessionStorageValue : JSON.parse(sessionStorageValue || 'null');
            }
        }
        catch (_a) {
            // If user is in private mode or has storage restriction
            // sessionStorage can throw. JSON.parse and JSON.stringify
            // cat throw, too.
            return initialValue;
        }
    }), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        try {
            var serializedState = raw ? String(state) : JSON.stringify(state);
            sessionStorage.setItem(key, serializedState);
        }
        catch (_a) {
            // If user is in private mode or has storage restriction
            // sessionStorage can throw. Also JSON.stringify can throw.
        }
    });
    return [state, setState];
};
/* harmony default export */ var esm_useSessionStorage = (useSessionStorage);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useSize.js


var useSize_useState = external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"], useSize_useEffect = external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"], useRef = external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"];
var DRAF = function (callback) { return setTimeout(callback, 35); };
var useSize = function (element, _a) {
    var _b = _a === void 0 ? {} : _a, _c = _b.width, width = _c === void 0 ? Infinity : _c, _d = _b.height, height = _d === void 0 ? Infinity : _d;
    if (!isClient) {
        return [
            typeof element === 'function'
                ? element({ width: width, height: height })
                : element,
            { width: width, height: height }
        ];
    }
    var _e = useSize_useState({ width: width, height: height }), state = _e[0], setState = _e[1];
    if (typeof element === 'function') {
        element = element(state);
    }
    var style = element.props.style || {};
    var ref = useRef(null);
    var window = null;
    var setSize = function () {
        var iframe = ref.current;
        var size = iframe
            ? {
                width: iframe.offsetWidth,
                height: iframe.offsetHeight,
            }
            : { width: width, height: height, };
        setState(size);
    };
    var onWindow = function (window) {
        window.addEventListener('resize', setSize);
        DRAF(setSize);
    };
    useSize_useEffect(function () {
        var iframe = ref.current;
        if (iframe.contentWindow) {
            window = iframe.contentWindow;
            onWindow(window);
        }
        else {
            var onLoad_1 = function () {
                iframe.removeEventListener('load', onLoad_1);
                window = iframe.contentWindow;
                onWindow(window);
            };
            iframe.addEventListener('load', onLoad_1);
        }
        return function () {
            if (window) {
                window.removeEventListener('resize', setSize);
            }
        };
    }, []);
    style.position = 'relative';
    var sized = external_root_React_commonjs2_react_commonjs_react_amd_react_["cloneElement"].apply(external_root_React_commonjs2_react_commonjs_react_amd_react_, [element, { style: style }].concat([
        external_root_React_commonjs2_react_commonjs_react_amd_react_["createElement"]('iframe', {
            ref: ref,
            style: {
                background: 'transparent',
                border: 'none',
                height: '100%',
                left: 0,
                position: 'absolute',
                top: 0,
                width: '100%',
                zIndex: -1
            }
        })
    ].concat(external_root_React_commonjs2_react_commonjs_react_amd_react_["Children"].toArray(element.props.children))));
    return [sized, state];
};
/* harmony default export */ var esm_useSize = (useSize);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useSpeech.js



var useSpeech = function (text, opts) {
    if (opts === void 0) { opts = {}; }
    var _a = esm_useSetState({
        isPlaying: false,
        volume: opts.volume || 1,
    }), state = _a[0], setState = _a[1];
    var uterranceRef = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(null);
    esm_useMount(function () {
        var utterance = new SpeechSynthesisUtterance(text);
        utterance.volume = opts.volume || 1;
        utterance.onstart = function () { return setState({ isPlaying: true }); };
        utterance.onresume = function () { return setState({ isPlaying: true }); };
        utterance.onend = function () { return setState({ isPlaying: false }); };
        utterance.onpause = function () { return setState({ isPlaying: false }); };
        uterranceRef.current = utterance;
        window.speechSynthesis.speak(uterranceRef.current);
    });
    return state;
};
/* harmony default export */ var esm_useSpeech = (useSpeech);

// EXTERNAL MODULE: ./node_modules/rebound/dist/rebound.js
var rebound = __webpack_require__(11);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useSpring.js


var useSpring = function (targetValue, tension, friction) {
    if (targetValue === void 0) { targetValue = 0; }
    if (tension === void 0) { tension = 50; }
    if (friction === void 0) { friction = 3; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(null), spring = _a[0], setSpring = _a[1];
    var _b = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(targetValue), value = _b[0], setValue = _b[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var listener = {
            onSpringUpdate: function (spring) {
                var value = spring.getCurrentValue();
                setValue(value);
            }
        };
        if (!spring) {
            var newSpring = (new rebound["SpringSystem"]()).createSpring(tension, friction);
            newSpring.setCurrentValue(targetValue);
            setSpring(newSpring);
            newSpring.addListener(listener);
            return;
        }
        return function () {
            spring.removeListener(listener);
            setSpring(null);
        };
    }, [tension, friction]);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (spring) {
            spring.setEndValue(targetValue);
        }
    }, [targetValue]);
    return value;
};
/* harmony default export */ var esm_useSpring = (useSpring);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useStartTyping.js

var isFocusedElementEditable = function () {
    var activeElement = document.activeElement, body = document.body;
    if (!activeElement)
        return false;
    // If not element has focus, we assume it is not editable, too.
    if (activeElement === body)
        return false;
    // Assume <input> and <textarea> elements are editable.
    switch (activeElement.tagName) {
        case 'INPUT':
        case 'TEXTAREA':
            return true;
    }
    // Check if any other focused element id editable.
    return activeElement.hasAttribute('contenteditable');
};
var isTypedCharGood = function (_a) {
    var keyCode = _a.keyCode;
    // 0...9
    if ((keyCode >= 48) && (keyCode <= 57))
        return true;
    // a...z
    if ((keyCode >= 65) && (keyCode <= 90))
        return true;
    // All other keys.
    return false;
};
var useStartTyping = function (onStartTyping) {
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useLayoutEffect"])(function () {
        var keydown = function (event) {
            !isFocusedElementEditable() && isTypedCharGood(event) && onStartTyping(event);
        };
        document.addEventListener('keydown', keydown);
        return function () {
            document.removeEventListener('keydown', keydown);
        };
    }, []);
};
/* harmony default export */ var esm_useStartTyping = (useStartTyping);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useUnmount.js

var useUnmount = function (fn) {
    esm_useEffectOnce(function () { return fn; });
};
/* harmony default export */ var esm_useUnmount = (useUnmount);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useThrottle.js


var useThrottle = function (value, ms) {
    if (ms === void 0) { ms = 200; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(value), state = _a[0], setState = _a[1];
    var timeout = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(null);
    var nextValue = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(null);
    var hasNextValue = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(0);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (!timeout.current) {
            setState(value);
            var timeoutCallback_1 = function () {
                if (hasNextValue.current) {
                    hasNextValue.current = false;
                    setState(nextValue.current);
                    timeout.current = setTimeout(timeoutCallback_1, ms);
                }
                else {
                    timeout.current = null;
                }
            };
            timeout.current = setTimeout(timeoutCallback_1, ms);
        }
        else {
            nextValue.current = value;
            hasNextValue.current = true;
        }
    }, [value]);
    esm_useUnmount(function () {
        clearTimeout(timeout.current);
    });
    return state;
};
/* harmony default export */ var esm_useThrottle = (useThrottle);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useThrottleFn.js


var useThrottleFn = function (fn, ms, args) {
    if (ms === void 0) { ms = 200; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(null), state = _a[0], setState = _a[1];
    var timeout = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(null);
    var nextArgs = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(null);
    var hasNextArgs = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(false);
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (!timeout.current) {
            setState(fn.apply(void 0, args));
            var timeoutCallback_1 = function () {
                if (hasNextArgs.current) {
                    hasNextArgs.current = false;
                    setState(fn.apply(void 0, nextArgs.current));
                    timeout.current = setTimeout(timeoutCallback_1, ms);
                }
                else {
                    timeout.current = null;
                }
            };
            timeout.current = setTimeout(timeoutCallback_1, ms);
        }
        else {
            nextArgs.current = args;
            hasNextArgs.current = true;
        }
    }, args);
    esm_useUnmount(function () {
        clearTimeout(timeout.current);
    });
    return state;
};
/* harmony default export */ var esm_useThrottleFn = (useThrottleFn);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useTimeout.js

var useTimeout = function (ms) {
    if (ms === void 0) { ms = 0; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])(false), ready = _a[0], setReady = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var timer = setTimeout(function () {
            setReady(true);
        }, ms);
        return function () {
            clearTimeout(timer);
        };
    }, [ms]);
    return ready;
};
/* harmony default export */ var esm_useTimeout = (useTimeout);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useTitle.js

var useTitle = function (title) {
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        document.title = title;
    }, [title]);
};
/* harmony default export */ var esm_useTitle = (useTitle);

// EXTERNAL MODULE: ./node_modules/ts-easing/lib/index.js
var lib = __webpack_require__(12);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useTween.js


var useTween = function (easingName, ms, delay) {
    if (easingName === void 0) { easingName = 'inCirc'; }
    if (ms === void 0) { ms = 200; }
    if (delay === void 0) { delay = 0; }
    var fn = lib["easing"][easingName];
    var t = esm_useRaf(ms, delay);
    if (false) {}
    return fn(t);
};
/* harmony default export */ var esm_useTween = (useTween);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useVideo.js

var useVideo = util_createHTMLMediaHook('video');
/* harmony default export */ var esm_useVideo = (useVideo);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useWindowScroll.js


var useWindowScroll = function () {
    var frame = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useRef"])(0);
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({
        x: isClient ? window.scrollX : 0,
        y: isClient ? window.scrollY : 0
    }), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        var handler = function () {
            cancelAnimationFrame(frame.current);
            frame.current = requestAnimationFrame(function () {
                setState({
                    x: window.scrollX,
                    y: window.scrollY
                });
            });
        };
        window.addEventListener('scroll', handler, {
            capture: false,
            passive: true
        });
        return function () {
            cancelAnimationFrame(frame.current);
            window.removeEventListener('scroll', handler);
        };
    }, []);
    return state;
};
/* harmony default export */ var esm_useWindowScroll = (useWindowScroll);

// CONCATENATED MODULE: ./node_modules/react-use/esm/useWindowSize.js


var useWindowSize = function (initialWidth, initialHeight) {
    if (initialWidth === void 0) { initialWidth = Infinity; }
    if (initialHeight === void 0) { initialHeight = Infinity; }
    var _a = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])({
        width: isClient ? window.innerWidth : initialWidth,
        height: isClient ? window.innerHeight : initialHeight,
    }), state = _a[0], setState = _a[1];
    Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useEffect"])(function () {
        if (isClient) {
            var handler_1 = function () {
                setState({
                    width: window.innerWidth,
                    height: window.innerHeight
                });
            };
            window.addEventListener('resize', handler_1);
            return function () { return window.removeEventListener('resize', handler_1); };
        }
        else {
            return undefined;
        }
    }, []);
    return state;
};
/* harmony default export */ var esm_useWindowSize = (useWindowSize);

// CONCATENATED MODULE: ./node_modules/react-wait/dist/react-wait.esm.js

var react_wait_esm_i = function(n) {
    return n.length > 0;
  },
  e = function(n, t) {
    return n.includes(t);
  },
  u = function(n, t) {
    return e(n, t) ? n : n.concat([t]);
  },
  c = function(n, t) {
    return n.filter(function(n) {
      return n !== t;
    });
  },
  react_wait_esm_a = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createContext();
function o(n) {
  return Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useContext"])(react_wait_esm_a).waiters.includes(n.on) ? n.fallback : n.children;
}
function react_wait_esm_f(r) {
  var f = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useState"])([]),
    s = f[0],
    g = f[1];
  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
    react_wait_esm_a.Provider,
    {
      value: {
        waiters: s,
        createWaitingContext: function(t) {
          return {
            isWaiting: function() {
              return e(s, t);
            },
            startWaiting: function() {
              return g(u(s, t));
            },
            endWaiting: function() {
              return g(c(s, t));
            },
            Wait: function(r) {
              return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(o, Object.assign({}, { on: t }, r));
            }
          };
        },
        anyWaiting: function() {
          return react_wait_esm_i(s);
        },
        isWaiting: function(n) {
          return e(s, n);
        },
        startWaiting: function(n) {
          g(u(s, n));
        },
        endWaiting: function(n) {
          g(c(s, n));
        }
      }
    },
    r.children
  );
}
function react_wait_esm_s() {
  var n = Object(external_root_React_commonjs2_react_commonjs_react_amd_react_["useContext"])(react_wait_esm_a);
  return Object.assign({}, n, { Wait: o });
}

//# sourceMappingURL=react-wait.esm.js.map

// CONCATENATED MODULE: ./node_modules/react-use/esm/useWait.js

react_wait_esm_s.Waiter = react_wait_esm_f;
/* harmony default export */ var useWait = (react_wait_esm_s);

// CONCATENATED MODULE: ./node_modules/react-use/esm/index.js







































































// EXTERNAL MODULE: ./node_modules/query-string/index.js
var query_string = __webpack_require__(13);

// CONCATENATED MODULE: ./src/DataTable/DataTableContainer.js


var DataTableContainer_this = undefined;

var DataTableContainer_extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; }

function _objectWithoutProperties(obj, keys) { var target = {}; for (var i in obj) { if (keys.indexOf(i) >= 0) continue; if (!Object.prototype.hasOwnProperty.call(obj, i)) continue; target[i] = obj[i]; } return target; }








var DataTableContainer_DataTableContainer = function DataTableContainer(_ref) {
  var endpointURL = _ref.endpointURL,
      limit = _ref.limit,
      authorized = _ref.authorized,
      total = _ref.total,
      sortKeys = _ref.sortKeys,
      elements = _ref.elements,
      dataTableProps = _objectWithoutProperties(_ref, ["endpointURL", "limit", "authorized", "total", "sortKeys", "elements"]);

  var _React$useState = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useState(elements),
      fetchedElements = _React$useState[0],
      setFetchedElements = _React$useState[1];

  var _React$useState2 = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useState({
    search: "",
    sortKey: "title",
    sortComparitor: "asc",
    cursor: 0,
    limit: limit
  }),
      query = _React$useState2[0],
      setQuery = _React$useState2[1];

  var _React$useState3 = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useState(total),
      totalState = _React$useState3[0],
      setTotalState = _React$useState3[1];

  var _React$useState4 = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useState(sortKeys),
      sortKeysState = _React$useState4[0],
      setSortKeysState = _React$useState4[1];

  var _React$useState5 = external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useState(authorized),
      authorizedState = _React$useState5[0],
      setAuthorizedState = _React$useState5[1];

  external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.useEffect(function () {
    setQuery(DataTableContainer_extends({}, query, { limit: limit }));
  }, [limit]);

  var fetchElements = function () {
    var _ref2 = _asyncToGenerator( /*#__PURE__*/regenerator_default.a.mark(function _callee() {
      var url, res, parsed;
      return regenerator_default.a.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              url = endpointURL + "?" + query_string["stringify"](query);


              console.log("Fetching from: " + url);

              _context.prev = 2;
              _context.next = 5;
              return fetch(url);

            case 5:
              res = _context.sent;

              if (res.ok) {
                _context.next = 8;
                break;
              }

              throw new Error("Request failed with status: " + res.status + " (" + res.statusText + ")");

            case 8:
              _context.next = 10;
              return res.json();

            case 10:
              parsed = _context.sent;


              setFetchedElements(parsed.elements);
              setTotalState(parsed.total);
              setSortKeysState(parsed.sortKeys);
              setAuthorizedState(parsed.authorized);
              _context.next = 21;
              break;

            case 17:
              _context.prev = 17;
              _context.t0 = _context["catch"](2);

              alert("There was an error retrieving the search results.");
              console.error(_context.t0);

            case 21:
            case "end":
              return _context.stop();
          }
        }
      }, _callee, DataTableContainer_this, [[2, 17]]);
    }));

    return function fetchElements() {
      return _ref2.apply(this, arguments);
    };
  }();

  esm_useDebounce(function () {
    return void fetchElements();
  }, 300, [endpointURL, query]);

  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(src_DataTable_DataTable, DataTableContainer_extends({
    authorized: authorizedState,
    elements: fetchedElements,
    total: totalState,
    sortKeys: sortKeysState,
    query: query,
    setQuery: setQuery
  }, dataTableProps));
};

DataTableContainer_DataTableContainer.propTypes = {
  authorized: prop_types_default.a.bool,
  endpointURL: prop_types_default.a.string,
  limit: prop_types_default.a.number,
  total: prop_types_default.a.number,
  elements: prop_types_default.a.arrayOf(prop_types_default.a.object)
};

DataTableContainer_DataTableContainer.defaultProps = {
  authorized: false,
  endpointURL: "",
  limit: 10,
  total: 0,
  elements: []
};

/* harmony default export */ var DataTable_DataTableContainer = (DataTableContainer_DataTableContainer);
// CONCATENATED MODULE: ./src/DataTable/index.js


// CONCATENATED MODULE: ./src/DatasetElement/index.js
function DatasetElement_objectWithoutProperties(obj, keys) { var target = {}; for (var i in obj) { if (keys.indexOf(i) >= 0) continue; if (!Object.prototype.hasOwnProperty.call(obj, i)) continue; target[i] = obj[i]; } return target; }




var DatasetElement_DatasetElement = function DatasetElement(props) {
  var authorized = props.authorized,
      element = DatasetElement_objectWithoutProperties(props, ["authorized"]);

  var imagePath = element.imagePath;
  var runOnCbrainEnabled = imagePath + "/run_on_cbrain_green.png";
  var runOnCbrainDisabled = imagePath + "/run_on_cbrain_gray.png";
  var downloadEnabled = imagePath + "/download_green.png";
  var downloadDisabled = imagePath + "/download_gray.png";

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
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "a",
              { style: { color: "inherit" }, href: "dataset?id=" + element.id },
              element.title
            )
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
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "a",
            {
              href: "#",
              style: {
                pointerEvents: element.isPrivate && !authorized ? "none" : "all"
              }
            },
            ">",
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
              alt: "Run On Cbrain",
              className: "run-on-cbrain-button option-icon",
              src: element.isPrivate && !authorized ? runOnCbrainDisabled : runOnCbrainEnabled
            })
          )
        ),
        external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
          "div",
          { className: "dataset-option", style: { position: "relative" } },
          external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
            "a",
            {
              style: {
                pointerEvents: element.isPrivate && !authorized ? "none" : "all"
              },
              href: "download_metadata?dataset=" + element.downloadPath,
              download: true
            },
            element.isPrivate && !authorized && external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
              "div",
              {
                style: {
                  backgroundColor: "white",
                  padding: "5px",
                  border: "solid black",
                  color: "black",
                  borderWidth: "1px",
                  left: "-30px",
                  textAlign: "center",
                  position: "absolute"
                }
              },
              "Please register for access."
            ),
            external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement("img", {
              alt: "Download Metadata",
              className: "download-button  option-icon",
              src: element.isPrivate && !authorized ? downloadDisabled : downloadEnabled
            })
          )
        )
      )
    )
  );
};

DatasetElement_DatasetElement.propTypes = {
  authorized: prop_types_default.a.bool,
  onRunWithCBRAIN: prop_types_default.a.func,
  // element proptypes
  id: prop_types_default.a.string,
  title: prop_types_default.a.string,
  isPrivate: prop_types_default.a.bool,
  thumbnailURL: prop_types_default.a.string,
  imagePath: prop_types_default.a.string,
  downloadPath: prop_types_default.a.string,
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
};

DatasetElement_DatasetElement.defaultProps = {
  imagePath: "",
  downloadPath: ""
};

/* harmony default export */ var src_DatasetElement = (DatasetElement_DatasetElement);
// CONCATENATED MODULE: ./src/PipelineElement/index.js
function PipelineElement_objectWithoutProperties(obj, keys) { var target = {}; for (var i in obj) { if (keys.indexOf(i) >= 0) continue; if (!Object.prototype.hasOwnProperty.call(obj, i)) continue; target[i] = obj[i]; } return target; }




var PipelineElement_PipelineElement = function PipelineElement(props) {
  var authorized = props.authorized,
      element = PipelineElement_objectWithoutProperties(props, ["authorized"]);

  return external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
    "div",
    { className: "search-pipeline" },
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "pipeline-id" },
      external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
        "a",
        { style: { color: "inherit" }, href: element.url },
        element.id
      )
    ),
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "pipeline-title" },
      element.title
    ),
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "pipeline-description" },
      element.description
    ),
    external_root_React_commonjs2_react_commonjs_react_amd_react_default.a.createElement(
      "div",
      { className: "pipeline-downloads" },
      element.downloads
    )
  );
};

PipelineElement_PipelineElement.propTypes = {
  id: prop_types_default.a.string,
  title: prop_types_default.a.string,
  description: prop_types_default.a.string,
  downloads: prop_types_default.a.number,
  name: prop_types_default.a.string,
  commandline: prop_types_default.a.string,
  author: prop_types_default.a.string,
  inputs: prop_types_default.a.arrayOf(prop_types_default.a.object),
  outputfiles: prop_types_default.a.arrayOf(prop_types_default.a.object),
  toolversion: prop_types_default.a.string,
  schemaversion: prop_types_default.a.string,
  containerimage: prop_types_default.a.object,
  tags: prop_types_default.a.object,
  url: prop_types_default.a.string
};

//PipelineElement.defaultProps = {
//  imagePath: "",
//  downloadPath: ""
//};

/* harmony default export */ var src_PipelineElement = (PipelineElement_PipelineElement);
// CONCATENATED MODULE: ./src/index.js
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "DataTable", function() { return src_DataTable_DataTable; });
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "DataTableContainer", function() { return DataTable_DataTableContainer; });
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "DatasetElement", function() { return src_DatasetElement; });
/* concated harmony reexport */__webpack_require__.d(__webpack_exports__, "PipelineElement", function() { return src_PipelineElement; });






/* harmony default export */ var src = __webpack_exports__["default"] = ({
  DataTable: src_DataTable_DataTable,
  DataTableContainer: DataTable_DataTableContainer,
  DatasetElement: src_DatasetElement,
  PipelineElement: src_PipelineElement
});

/***/ })
/******/ ])["default"];
});