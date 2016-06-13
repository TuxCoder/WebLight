(function () {
  'use strict';

  angular
    .module('frontend')
    .directive('mySidenav', MySidenav);

  /** @ngInject */
  function MySidenav() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/sidenav/sidenav.html',
      controller: SidenavController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    /** @ngInject */
    function SidenavController($state, device, $rootScope) {
      var vm = this;
      vm.gotoDevice = gotoDevice;
      vm.devices = [];
      vm.isOpen = true;
      vm.open = open;
      $rootScope.sidenav = vm;

      activate();

      function activate() {
        device.getDevices().then(function (devices) {
          vm.devices = devices;
        });
      }


      function gotoDevice(key) {
        vm.isOpen = false;
        $state.go('device', {key: key});
      }

      function open() {
        vm.isOpen = true;
      }
    }
  }

})();
