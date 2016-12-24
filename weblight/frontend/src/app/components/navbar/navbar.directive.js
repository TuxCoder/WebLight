(function() {
  'use strict';

  angular
    .module('frontend')
    .directive('myNavbar', myNavbar);

  /** @ngInject */
  function myNavbar() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/navbar/navbar.html',
      scope: {
          creationDate: '='
      },
      controller: NavbarController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    /** @ngInject */
    function NavbarController(auth,$state) {
      var vm = this;
      vm.status= auth.getStatus();
      vm.logout = auth.logout;
      vm.login = login;

      function login(){
        $state.go('login')
      }
    }
  }

})();
