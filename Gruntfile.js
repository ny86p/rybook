module.exports = function (grunt) {
    var path = require('path');

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
  "sass": {
    "dist": {
      "files": [
        {
          "expand": true,
          "src": [
            "**/*.{scss, sass}",
            "!node_modules/**/*.{scss, sass}"
          ],
          "ext": ".css"
        }
      ]
    }
  },
  "slim": {
    "dist": {
      "files": [
        {
          "expand": true,
          "src": [
            "**/*.slim",
            "!node_modules/**/*.slim"
          ],
          "ext": ".html"
        }
      ]
    }
  },
  "watch": {
    "sass": {
      "files": [
        "**/*.scss",
        "!node_modules/**/*.scss"
      ],
      "tasks": [
        "sass"
      ]
    },
    "slim": {
      "files": [
        "**/*.slim",
        "!node_modules/**/*.slim"
      ],
      "tasks": [
        "slim"
      ]
    },
    "all": {
      "files": [
        "**/*",
        "!node_modules/**/*"
      ],
      "tasks": [
        "noop"
      ],
      "options": {
        "cwd": "./",
        "spawn": false,
        "event": [
          "added"
        ]
      }
    }
  }
});

    grunt.registerTask('default', ['watch']);

    // Handle new files with that have a new, supported preprocessor
    grunt.event.on('watch', function(action, filepath) {
      if (action !== 'added') return;

      var ext = path.extname(filepath);

      // Ignore directories
      if (! ext) return;

      // This is a special message that's parsed by Mule
      // to determine if support for an additional preprocessor is necessary
      // Note: this allows us to avoid controlling grunt manually within Mule
      console.log('EXTADDED:' + ext);
    });

    // For watching entire directories but allowing
    // the grunt.event binding to take care of it
    grunt.registerTask('noop', function () {});
  }