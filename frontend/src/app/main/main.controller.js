(function () {
  'use strict';

  angular
    .module('frontend')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($rootScope, $scope, auth, device) {
    var vm = this;

    activate();
    function activate() {
      if ($rootScope.sidenav != undefined) {
        $rootScope.sidenav.open();
      }
    }
  }

})();
