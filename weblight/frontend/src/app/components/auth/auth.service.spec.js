(function() {
  'use strict';

  describe('service auth', function() {
    var vm;
    var auth;
    var $http;

    beforeEach(module('frontend'));
    beforeEach(inject(function(_$controler_, _auth_,_$http_) {
      vm=_$controler_;
      auth = _auth_;
      $http =_$http_;
    }));

    it('should be registered', function() {
      expect(vm).not.toEqual(null);
    });

    it('should be registered', function() {
      expect(auth).not.toEqual(null);
    });

    describe('getForm function', function() {
      it('should exist', function() {
        expect(auth.getForm).not.toEqual(null);
      });
    });
    describe('isLoggedIn function', function() {
      it('should exist', function() {
        expect(auth.isLoggedIn).not.toEqual(null);
      });
    });

    it('should be registered', function() {
      expect($http).not.toEqual(null);
    });
  });
})();
