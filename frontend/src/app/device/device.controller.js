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
    vm.updateAnimation = updateAnimation;

    activate();

    function activate() {
      device.getDevice($stateParams.key).then(function (device) {
        vm.device = device;
          vm.animation = device.animation.name;
      });
      animations.getAnimations().then(function (animations) {
        vm.animations = animations;
      });
    }

    function update() {
      if (vm.device != undefined) {
        device.updateDevice(vm.device).then(function (device) {
          vm.device = device;
          vm.animation = device.animation.name;
        });
      }
    }

    function updateAnimation() {
      if (vm.device != undefined) {
        animations.getAnimation(vm.animation).then(function(animation){
          vm.device.animation = animation;
        });
      }
    }
  }
})();
