(function () {
  'use strict';

  angular
    .module('frontend')
    .controller('DeviceController', DeviceController);

  /** @ngInject */
  function DeviceController($stateParams, device, animations ) {
    var vm = this;
    vm.device = undefined;
    vm.animations = undefined;
    vm.animation = undefined;
    vm.update = update;
    vm.reload = reload;
    vm.off = off;
    vm.updateAnimation = updateAnimation;

    activate();

    function activate() {
      vm.reload();
      animations.getAnimations().then(function (animations) {
        vm.animations = animations;
      });
    }

    function reload() {
      device.getDevice($stateParams.key).then(function (device) {
        vm.device = device;
          vm.animation = device.animation.name;
      });
    }

    function off() {
      if (vm.device != undefined) {
        device.offDevice(vm.device).then(function (device) {
          vm.device = device;
          vm.animation = null;
        });
      }
    }

    var update_id =0; // prevent from update to old data
    function update() {
      update_id++;
      var current_id =update_id;
      if (vm.device != undefined) {
        device.updateDevice(vm.device).then(function (device) {
          if(update_id==current_id) {
            vm.device = device;
            if (device.animation != null) {
              vm.animation = device.animation.name;
            }
          }
        });
      }
    }

    function updateAnimation() {
      if (vm.device != undefined) {
        animations.getAnimation(vm.animation).then(function(animation){
          vm.device.animation = animation;
          vm.update();
        });
      }
    }


  }


  angular
    .module('frontend')
    .filter('orderByValue', function () {
      function strcmp ( str1, str2 ) {
        // http://kevin.vanzonneveld.net
        // +   original by: Waldo Malqui Silva
        // +      input by: Steve Hilder
        // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
        // +    revised by: gorthaur
        // *     example 1: strcmp( 'waldo', 'owald' );
        // *     returns 1: 1
        // *     example 2: strcmp( 'owald', 'waldo' );
        // *     returns 2: -1

        return ( ( str1 == str2 ) ? 0 : ( ( str1 > str2 ) ? 1 : -1 ) );
      }

      return function (obj) {
        if (obj == undefined) {
          return [];
        }
        var array = [];
        Object.keys(obj).forEach(function (key) {
          // inject key into each object so we can refer to it from the template
          obj[key].name = key;
          array.push(obj[key]);
        });
        // apply a custom sorting function
        array.sort(function (a, b) {
          return strcmp ( a.name, b.name );
        });
        return array;
      };
    });
})();
