(function () {
  'use strict';

  angular
    .module('frontend')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($state,$scope, auth, device) {
    var vm = this;
    vm.gotoDevice = gotoDevice;
    vm.devices = [];

    activate();

    function activate() {
      auth.updateStatus().then(function (status) {
        if (!status.loggedIn) {
          $state.go('login');
        }
        device.getDevices().then(function (devices) {
          vm.devices = devices;
        });
      });
    }


    function gotoDevice(key) {
        $state.go('device', {key: key});
    }
  }
})();
