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
    function SidenavController($state, device,auth, $rootScope) {
      var vm = this;
      vm.gotoDevice = gotoDevice;
      vm.devices = [];
      vm.isOpen = true;
      vm.open = open;
      vm.update = update;
      $rootScope.sidenav = vm;

      update();

      function update() {
        if(auth.status.loggedIn) {
          device.getDevices().then(function (devices) {
            vm.devices = devices;
          });
        }else {
          vm.devices=[];
        }
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
