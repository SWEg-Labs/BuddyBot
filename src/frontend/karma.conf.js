module.exports = function (config) {
    config.set({
      basePath: '',
      frameworks: ['jasmine', '@angular-devkit/build-angular'],
      plugins: [
        require('karma-jasmine'),
        require('karma-chrome-launcher'),
        require('karma-jasmine-html-reporter'),
        require('karma-coverage')
      ],
      client: {
        clearContext: false // lascia il browser aperto dopo i test
      },
      coverageReporter: {
        type: 'html',
        dir: 'coverage/',
        check: {
          global: {
            statements: 75,
            branches: 75,
            functions: 75,
            lines: 75
          }
        }
      },
      reporters: ['progress', 'kjhtml'],
      port: 9876,
      colors: true,
      logLevel: config.LOG_INFO,
      autoWatch: true,
      browsers: ['Chrome'],
      singleRun: false,
      restartOnFileChange: true
    });
  };
  