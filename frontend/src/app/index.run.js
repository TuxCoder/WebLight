(function () {
  'use strict';

  angular
    .module('frontend')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log, $http, $interval) {
    $log.debug('runBlock end');

    function UpdateCsrf() {
      $http.get('/csrf.js', {cache: false}).then(function (resp) {
        $http.defaults.headers.post['X-CSRFToken'] = resp.data.csrftoken;
      });
    }

    $interval(UpdateCsrf, 60*5*1000); // each 5 min
    UpdateCsrf();
  }

})();
