/* global csrftoken:'' */
(function () {
  'use strict';

  angular
    .module('frontend')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log, $http) {
    $http.defaults.headers.post['X-CSRFToken'] = csrftoken;
    $log.debug('runBlock end');
  }

})();
