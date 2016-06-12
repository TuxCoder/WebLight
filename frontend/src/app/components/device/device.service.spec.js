(function() {
  'use strict';

  describe('service auth', function() {
    var vm;
    var $http;

    beforeEach(module('frontend'));
    beforeEach(inject(function(_$controler_, _$http_) {
      vm=_$controler_;
      $http =_$http_;
    }));

    it('should be registered', function() {
      expect(vm).not.toEqual(null);
    });

    it('should be registered', function() {
      expect($http).not.toEqual(null);
    });
  });
})();
