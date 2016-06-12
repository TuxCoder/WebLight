(function () {
  'use strict';

  angular
    .module('frontend')
    .service('device', Device);

  /** @ngInject */
  function Device($http) {
    var vm = this;
    vm.getDevices = getDevices;
    vm.getDevice = getDevice;
    vm.updateDevice = updateDevice;


    function getDevices() {
      return $http.get('/api/device').then(function (resp) {
        return resp.data;
      });
    }

    function getDevice(device_name) {
      return $http.get('/api/device/' + device_name).then(function (resp) {
        return resp.data
      });
    }

    function updateDevice(device) {
      return $http.post('/api/device/' + device.name, device).then(function(resp){
        return resp.data;
      });
    }
  }

})();
