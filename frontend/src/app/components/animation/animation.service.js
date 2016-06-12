(function () {
  'use strict';

  angular
    .module('frontend')
    .service('animations', Animations);

  /** @ngInject */
  function Animations($http) {
    var vm = this;
    vm.getAnimations = getAnimations;
    vm.getAnimation = getAnimation;


    function getAnimations() {
      return $http.get('/api/animation', {cache: true}).then(function (resp) {
        return resp.data;
      });
    }

    function getAnimation(key) {
      return getAnimations().then(function (animations) {
        var found= null
        angular.forEach(animations, function (v) {
          if (v.name == key) {
            found= v;
          }
        });
        return found;
      });
    }
  }

})();
