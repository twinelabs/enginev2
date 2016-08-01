( function(ChartExport) {
  if ( !ChartExport ) {
    ChartExport = window.ChartExport = {};
  }

  ChartExport[ "export" ] = function( chart, config ) {
    var _this = {
      config: {},
      setup: {
        chart: chart,
        hasBlob: false
      },
      defaults: {
        fileName: "ChartExport",
        formats: {
          JPG: {
            mimeType: "image/jpg",
            extension: "jpg"
          },
          PNG: {
            mimeType: "image/png",
            extension: "png"
          },
          SVG: {
            mimeType: "text/xml",
            extension: "svg"
          },
          PDF: {
            mimeType: "application/pdf",
            extension: "pdf"
          },
          CSV: {
            mimeType: "text/plain",
            extension: "csv"
          },
          JSON: {
            mimeType: "text/plain",
            extension: "json"
          }
        },
        pdfMake: {
          images: {},
          pageOrientation: "portrait",
          pageMargins: 40,
          pageOrigin: false,
          pageSize: "A4",
          pageSizes: {
            "4A0": [ 4767.87, 6740.79 ],
            "2A0": [ 3370.39, 4767.87 ],
            "A0": [ 2383.94, 3370.39 ],
            "A1": [ 1683.78, 2383.94 ],
            "A2": [ 1190.55, 1683.78 ],
            "A3": [ 841.89, 1190.55 ],
            "A4": [ 595.28, 841.89 ],
            "A5": [ 419.53, 595.28 ],
            "A6": [ 297.64, 419.53 ],
            "A7": [ 209.76, 297.64 ],
            "A8": [ 147.40, 209.76 ],
            "A9": [ 104.88, 147.40 ],
            "A10": [ 73.70, 104.88 ],
            "B0": [ 2834.65, 4008.19 ],
            "B1": [ 2004.09, 2834.65 ],
            "B2": [ 1417.32, 2004.09 ],
            "B3": [ 1000.63, 1417.32 ],
            "B4": [ 708.66, 1000.63 ],
            "B5": [ 498.90, 708.66 ],
            "B6": [ 354.33, 498.90 ],
            "B7": [ 249.45, 354.33 ],
            "B8": [ 175.75, 249.45 ],
            "B9": [ 124.72, 175.75 ],
            "B10": [ 87.87, 124.72 ],
            "C0": [ 2599.37, 3676.54 ],
            "C1": [ 1836.85, 2599.37 ],
            "C2": [ 1298.27, 1836.85 ],
            "C3": [ 918.43, 1298.27 ],
            "C4": [ 649.13, 918.43 ],
            "C5": [ 459.21, 649.13 ],
            "C6": [ 323.15, 459.21 ],
            "C7": [ 229.61, 323.15 ],
            "C8": [ 161.57, 229.61 ],
            "C9": [ 113.39, 161.57 ],
            "C10": [ 79.37, 113.39 ],
            "RA0": [ 2437.80, 3458.27 ],
            "RA1": [ 1729.13, 2437.80 ],
            "RA2": [ 1218.90, 1729.13 ],
            "RA3": [ 864.57, 1218.90 ],
            "RA4": [ 609.45, 864.57 ],
            "SRA0": [ 2551.18, 3628.35 ],
            "SRA1": [ 1814.17, 2551.18 ],
            "SRA2": [ 1275.59, 1814.17 ],
            "SRA3": [ 907.09, 1275.59 ],
            "SRA4": [ 637.80, 907.09 ],
            "EXECUTIVE": [ 521.86, 756.00 ],
            "FOLIO": [ 612.00, 936.00 ],
            "LEGAL": [ 612.00, 1008.00 ],
            "LETTER": [ 612.00, 792.00 ],
            "TABLOID": [ 792.00, 1224.00 ]
          }
        }
      },

      /**
       * Generates download file;
       */
      download: function( data, type, filename ) {
        // SAVE
        if ( window.saveAs && _this.setup.hasBlob ) {
          var blob = _this.toBlob( {
            data: data,
            type: type
          }, function( data ) {
            saveAs( data, filename );
          } );

          // ERROR
        } else {
          throw new Error( "Unable to create file. Ensure saveAs (FileSaver.js) is supported." );
        }
        return data;
      },

      /**
       * Recursive method to merge the given objects together
       * Overwrite flag replaces the value instead to crawl through
       */
      deepMerge: function( a, b, overwrite ) {
        var i1, v, type = b instanceof Array ? "array" : "object";

        for ( i1 in b ) {
          // PREVENT METHODS
          if ( type == "array" && isNaN( i1 ) ) {
            continue;
          }

          v = b[ i1 ];

          // NEW
          if ( a[ i1 ] == undefined || overwrite ) {
            if ( v instanceof Array ) {
              a[ i1 ] = new Array();
            } else if ( v instanceof Function ) {
              a[ i1 ] = function() {};
            } else if ( v instanceof Date ) {
              a[ i1 ] = new Date();
            } else if ( v instanceof Object ) {
              a[ i1 ] = new Object();
            } else if ( v instanceof Number ) {
              a[ i1 ] = new Number();
            } else if ( v instanceof String ) {
              a[ i1 ] = new String();
            }
          }

          if (
            ( a instanceof Object || a instanceof Array ) &&
            ( v instanceof Object || v instanceof Array ) &&
            !( v instanceof Function || v instanceof Date || _this.isElement( v ) ) &&
            i1 != "chart"
          ) {
            _this.deepMerge( a[ i1 ], v, overwrite );
          } else {
            if ( a instanceof Array && !overwrite ) {
              a.push( v );
            } else {
              a[ i1 ] = v;
            }
          }
        }
        return a;
      },

      /**
       * Checks if given argument is a valid node
       */
      isElement: function( thingy ) {
        return thingy instanceof Object && thingy && thingy.nodeType === 1;
      },

      /**
       * Returns the current canvas
       */
      toCanvas: function( options, callback ) {
        var cfg = _this.deepMerge( {
          // NUFFIN
        }, options || {} );
        var data = _this.setup.canvas;

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Returns an image; by default PNG
       */
      toImage: function( options, callback ) {
        var cfg = _this.deepMerge( {
          format: "png",
          quality: 1,
          multiplier: _this.config.multiplier
        }, options || {} );
        var data = cfg.data;
        var img = document.createElement( "img" );

        if ( !cfg.data ) {
          if ( cfg.lossless || cfg.format == "svg" ) {
            data = _this.toSVG( _this.deepMerge( cfg, {
              getBase64: true
            } ) );
          } else {
            data = _this.toPNG( cfg );
          }
        }

        img.setAttribute( "src", data );

        _this.handleCallback( callback, img, cfg );

        return img;
      },

      /**
       * Generates a blob instance image; returns base64 datastring
       */
      toBlob: function( options, callback ) {
        var cfg = _this.deepMerge( {
          data: "empty",
          type: "text/plain"
        }, options || {} );
        var data;
        var isBase64 = /^data:.+;base64,(.*)$/.exec( cfg.data );

        // GATHER BODY
        if ( isBase64 ) {
          cfg.data = isBase64[ 0 ];
          cfg.type = cfg.data.slice( 5, cfg.data.indexOf( "," ) - 7 );
          cfg.data = _this.toByteArray( {
            data: cfg.data.slice( cfg.data.indexOf( "," ) + 1, cfg.data.length )
          } );
        }

        if ( cfg.getByteArray ) {
          data = cfg.data;
        } else {
          data = new Blob( [ cfg.data ], {
            type: cfg.type
          } );
        }

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates JPG image; returns base64 datastring
       */
      toJPG: function( options, callback ) {
        var cfg = _this.deepMerge( {
          format: "jpeg",
          quality: 1,
          multiplier: _this.config.multiplier
        }, options || {} );
        cfg.format = cfg.format.toLowerCase();

        var svgNode = d3.select(_this.setup.chart.selector + ' svg')
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg")
          .style({
            'background-color': '#fff'
          })
          .node()
        //.parentNode.innerHTML;

        //var xml_string =  new XMLSerializer().serializeToString(svgNode);

        var wrap = document.createElement('div');
        wrap.appendChild(svgNode.cloneNode(true));

        var html = wrap.innerHTML;

        var canvas = document.createElement("canvas"),
          context = canvas.getContext("2d");

        canvas.width = _this.setup.chart.divRealWidth;
        canvas.height = _this.setup.chart.divRealHeight;

        var data;
        var image = new Image;
        image.src =  "data:image/svg+xml;base64," + btoa(html);
        context.drawImage(image, 0, 0, _this.setup.chart.divRealWidth, _this.setup.chart.divRealHeight);
        data = canvas.toDataURL(cfg);

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates PNG image; returns base64 datastring
       */
      toPNG: function( options, callback ) {
        var cfg = _this.deepMerge( {
          format: "png",
          quality: 1,
          multiplier: _this.config.multiplier
        }, options || {} );

        var svgNode = d3.select(_this.setup.chart.selector + ' svg')
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg")
          .style({
            'background-color': '#fff'
          })
          .node()//.parentNode.innerHTML;

        //var xml_string =  new XMLSerializer().serializeToString(svgNode);

        var wrap = document.createElement('div');
        wrap.appendChild(svgNode.cloneNode(true));

        var html = wrap.innerHTML;

        var canvas = document.createElement("canvas"),
          context = canvas.getContext("2d");

        canvas.width = _this.setup.chart.divRealWidth;
        canvas.height = _this.setup.chart.divRealHeight;

        var data;
        var image = new Image;
        image.src =  "data:image/svg+xml;base64," + btoa(html);
        //image.onload = function(){
        //  context.drawImage(image, 0, 0, _this.setup.chart.divRealWidth, _this.setup.chart.divRealHeight);
        //  data = canvas.toDataURL(cfg);
        //
        //  _this.handleCallback( callback, data, cfg );
        //}
        context.drawImage(image, 0, 0, _this.setup.chart.divRealWidth, _this.setup.chart.divRealHeight);
        data = canvas.toDataURL(cfg);

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates SVG image; returns base64 datastring
       */
      toSVG: function( options, callback ) {
        var clipPaths = [];
        var cfg = _this.deepMerge( {
          getBase64: true
        }, options || {} );

        var svgNode = d3.select(_this.setup.chart.selector + ' svg')
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg")
          .style({
            'background-color': '#fff'
          })
          .node();

        var wrap = document.createElement('div');
        wrap.appendChild(svgNode.cloneNode(true));

        var data = wrap.innerHTML;

        if ( cfg.getBase64 ) {
          data = "data:image/svg+xml;base64," + btoa( data );
        }

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates PDF; returns base64 datastring
       */
      toPDF: function( options, callback ) {
        var cfg = _this.deepMerge( _this.deepMerge( {
          multiplier: _this.config.multiplier || 2,
          pageOrigin: _this.config.pageOrigin
        }, _this.config.pdfMake ), options || {}, true );
        var data = new pdfMake.createPdf( cfg );

        // Get image data
        cfg.images.reference = _this.toPNG( cfg );

        // Get page margins; exported from pdfMake
        function getMargins( margin ) {
          if ( typeof margin === 'number' || margin instanceof Number ) {
            margin = {
              left: margin,
              right: margin,
              top: margin,
              bottom: margin
            };
          } else if ( margin instanceof Array ) {
            if ( margin.length === 2 ) {
              margin = {
                left: margin[ 0 ],
                top: margin[ 1 ],
                right: margin[ 0 ],
                bottom: margin[ 1 ]
              };
            } else if ( margin.length === 4 ) {
              margin = {
                left: margin[ 0 ],
                top: margin[ 1 ],
                right: margin[ 2 ],
                bottom: margin[ 3 ]
              };
            } else throw 'Invalid pageMargins definition';
          } else {
            margin = {
              left: _this.defaults.pdfMake.pageMargins,
              top: _this.defaults.pdfMake.pageMargins,
              right: _this.defaults.pdfMake.pageMargins,
              bottom: _this.defaults.pdfMake.pageMargins
            };
          }

          return margin;
        }

        // Get page dimensions
        function getSize( pageSize, pageOrientation ) {
          var pageDimensions = _this.defaults.pdfMake.pageSizes[ String( pageSize ).toUpperCase() ].slice();

          if ( !pageDimensions ) {
            throw new Error( "The given pageSize \"" + pageSize + "\" does not exist!" );
          }

          // Revers in case of landscape
          if ( pageOrientation == "landscape" ) {
            pageDimensions.reverse();
          }

          return pageDimensions;
        }

        // Polyfill default content if none is given
        if ( !cfg.content ) {
          var pageContent = [];
          var pageDimensions = getSize( cfg.pageSize, cfg.pageOrientation );
          var pageMargins = getMargins( cfg.pageMargins );

          pageDimensions[ 0 ] -= ( pageMargins.left + pageMargins.right );
          pageDimensions[ 1 ] -= ( pageMargins.top + pageMargins.bottom );

          if ( cfg.pageOrigin ) {
            pageContent.push( "Saved from: " );
            pageContent.push( window.location.href );
            pageDimensions[ 1 ] -= ( 14.064 * 2 );
          }

          pageContent.push( {
            image: "reference",
            fit: pageDimensions
          } );

          cfg.content = pageContent;
        }

        if ( callback ) {
          data.getDataUrl( ( function( callback ) {
            return function( a ) {
              callback.apply( _this, arguments );
            }
          } )( callback ) );
        }

        return data;
      },

      /**
       * Generates an image; hides all elements on page to trigger native print method
       */
      toPRINT: function( options, callback ) {
        var i1;
        var cfg = _this.deepMerge( {
          delay: 1,
          lossless: false
        }, options || {} );
        var data = _this.toImage( cfg );
        var states = [];
        var items = document.body.childNodes;

        data.setAttribute( "style", "width: 100%; max-height: 100%;" );

        for ( i1 = 0; i1 < items.length; i1++ ) {
          if ( _this.isElement( items[ i1 ] ) ) {
            states[ i1 ] = items[ i1 ].style.display;
            items[ i1 ].style.display = "none";
          }
        }

        document.body.appendChild( data );
        window.print();

        setTimeout( function() {
          for ( i1 = 0; i1 < items.length; i1++ ) {
            if ( _this.isElement( items[ i1 ] ) ) {
              items[ i1 ].style.display = states[ i1 ];
            }
          }
          document.body.removeChild( data );
          _this.handleCallback( callback, data, cfg );
        }, cfg.delay );

        return data;
      },

      /**
       * Generates JSON string
       */
      toJSON: function( options, callback ) {
        var cfg = _this.deepMerge( {
          dateFormat: _this.config.dateFormat || "dateObject",
        }, options || {}, true );
        cfg.data = cfg.data ? cfg.data : _this.getChartData( cfg );
        var data = JSON.stringify( cfg.data, undefined, "\t" );

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates CSV string
       */
      toCSV: function( options, callback ) {
        var row, col;
        var cfg = _this.deepMerge( {
          data: _this.getChartData( options ),
          delimiter: ",",
          quotes: true,
          escape: true,
          withHeader: true
        }, options || {}, true );
        var data = "";
        var cols = [];
        var buffer = [];

        function enchant( value, column ) {

          // WRAP IN QUOTES
          if ( typeof value === "string" ) {
            if ( cfg.escape ) {
              value = value.replace( '"', '""' );
            }
            if ( cfg.quotes ) {
              value = [ '"', value, '"' ].join( "" );
            }
          }

          return value;
        }

        // HEADER
        for ( value in cfg.data[ 0 ] ) {
          buffer.push( enchant( value ) );
          cols.push( value );
        }
        if ( cfg.withHeader ) {
          data += buffer.join( cfg.delimiter ) + "\n";
        }

        // BODY
        for ( row in cfg.data ) {
          buffer = [];
          if ( !isNaN( row ) ) {
            for ( col in cols ) {
              if ( !isNaN( col ) ) {
                var column = cols[ col ];
                var value = cfg.data[ row ][ column ];

                buffer.push( enchant( value, column ) );
              }
            }
            data += buffer.join( cfg.delimiter ) + "\n";
          }
        }

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates an array of arrays
       */
      toArray: function( options, callback ) {
        var row, col;
        var cfg = _this.deepMerge( {
          data: _this.getChartData( options ),
          withHeader: false,
          stringify: true
        }, options || {}, true );
        var data = [];
        var cols = [];

        // HEADER
        for ( col in cfg.data[ 0 ] ) {
          cols.push( col );
        }
        if ( cfg.withHeader ) {
          data.push( cols );
        }

        // BODY
        for ( row in cfg.data ) {
          var buffer = [];
          if ( !isNaN( row ) ) {
            for ( col in cols ) {
              if ( !isNaN( col ) ) {
                var col = cols[ col ];
                var value = cfg.data[ row ][ col ];
                if ( value == null ) {
                  value = "";
                } else if ( cfg.stringify ) {
                  value = String( value );
                } else {
                  value = value;
                }
                buffer.push( value );
              }
            }
            data.push( buffer );
          }
        }

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Generates byte array with given base64 datastring; returns byte array
       */
      toByteArray: function( options, callback ) {
        var cfg = _this.deepMerge( {
          // NUFFIN
        }, options || {} );
        var Arr = ( typeof Uint8Array !== 'undefined' ) ? Uint8Array : Array
        var PLUS = '+'.charCodeAt( 0 )
        var SLASH = '/'.charCodeAt( 0 )
        var NUMBER = '0'.charCodeAt( 0 )
        var LOWER = 'a'.charCodeAt( 0 )
        var UPPER = 'A'.charCodeAt( 0 )
        var data = b64ToByteArray( cfg.data );

        function decode( elt ) {
          var code = elt.charCodeAt( 0 )
          if ( code === PLUS )
            return 62 // '+'
          if ( code === SLASH )
            return 63 // '/'
          if ( code < NUMBER )
            return -1 //no match
          if ( code < NUMBER + 10 )
            return code - NUMBER + 26 + 26
          if ( code < UPPER + 26 )
            return code - UPPER
          if ( code < LOWER + 26 )
            return code - LOWER + 26
        }

        function b64ToByteArray( b64 ) {
          var i, j, l, tmp, placeHolders, arr

          if ( b64.length % 4 > 0 ) {
            throw new Error( 'Invalid string. Length must be a multiple of 4' )
          }

          // THE NUMBER OF EQUAL SIGNS (PLACE HOLDERS)
          // IF THERE ARE TWO PLACEHOLDERS, THAN THE TWO CHARACTERS BEFORE IT
          // REPRESENT ONE BYTE
          // IF THERE IS ONLY ONE, THEN THE THREE CHARACTERS BEFORE IT REPRESENT 2 BYTES
          // THIS IS JUST A CHEAP HACK TO NOT DO INDEXOF TWICE
          var len = b64.length
          placeHolders = '=' === b64.charAt( len - 2 ) ? 2 : '=' === b64.charAt( len - 1 ) ? 1 : 0

          // BASE64 IS 4/3 + UP TO TWO CHARACTERS OF THE ORIGINAL DATA
          arr = new Arr( b64.length * 3 / 4 - placeHolders )

          // IF THERE ARE PLACEHOLDERS, ONLY GET UP TO THE LAST COMPLETE 4 CHARS
          l = placeHolders > 0 ? b64.length - 4 : b64.length

          var L = 0

          function push( v ) {
            arr[ L++ ] = v
          }

          for ( i = 0, j = 0; i < l; i += 4, j += 3 ) {
            tmp = ( decode( b64.charAt( i ) ) << 18 ) | ( decode( b64.charAt( i + 1 ) ) << 12 ) | ( decode( b64.charAt( i + 2 ) ) << 6 ) | decode( b64.charAt( i + 3 ) )
            push( ( tmp & 0xFF0000 ) >> 16 )
            push( ( tmp & 0xFF00 ) >> 8 )
            push( tmp & 0xFF )
          }

          if ( placeHolders === 2 ) {
            tmp = ( decode( b64.charAt( i ) ) << 2 ) | ( decode( b64.charAt( i + 1 ) ) >> 4 )
            push( tmp & 0xFF )
          } else if ( placeHolders === 1 ) {
            tmp = ( decode( b64.charAt( i ) ) << 10 ) | ( decode( b64.charAt( i + 1 ) ) << 4 ) | ( decode( b64.charAt( i + 2 ) ) >> 2 )
            push( ( tmp >> 8 ) & 0xFF )
            push( tmp & 0xFF )
          }

          return arr
        }

        _this.handleCallback( callback, data, cfg );

        return data;
      },

      /**
       * Callback handler; injects additional arguments to callback
       */
      handleCallback: function( callback ) {
        var i1, data = Array();
        if ( callback && callback instanceof Function ) {
          for ( i1 = 0; i1 < arguments.length; i1++ ) {
            if ( i1 > 0 ) {
              data.push( arguments[ i1 ] );
            }
          }
          return callback.apply( _this, data );
        }
      },

      /**
       * Gathers chart data according to its type
       */
      getChartData: function( options ) {
        return options.updateData ? options.updateData(_this.setup.chart.data) : _this.setup.chart.data;
      },

      /**
       * Initiates export instance; merges given config; attaches event listener
       */
      construct: function() {
        // CHECK BLOB CONSTRUCTOR
        try {
          _this.setup.hasBlob = !!new Blob;
        } catch ( e ) {}

        // WORK AROUND TO BYPASS FILESAVER CHECK TRYING TO OPEN THE BLOB URL IN SAFARI BROWSER
        window.safari = window.safari ? window.safari : {};

        // MERGE SETTINGS
        _this.deepMerge( _this.defaults.pdfMake, _this.config, true );
        _this.deepMerge( _this.defaults.pdfMake, _this.config.pdfMake || {}, true );
        _this.deepMerge( _this.libs, _this.config.libs || {}, true );

        // UPDATE CONFIG
        _this.config.pdfMake = _this.defaults.pdfMake;
        _this.config = _this.deepMerge( _this.defaults, _this.config, true );
      }
    }

    // USE GIVEN CONFIG
    if ( config ) {
      _this.config = config;
    } else {
      return;
    }

    // CONSTRUCT INSTANCE
    _this.construct();

    // EXPORT SCOPE
    return _this.deepMerge( this, _this );
  }
} )( window.ChartExport );