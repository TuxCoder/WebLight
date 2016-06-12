(function() {
  'use strict';

  describe('controllers', function(){
    var vm;
    var $log;
    var auth;

    beforeEach(module('frontend'));
    beforeEach(inject(function(_$controller_,_$log_,_auth_) {

      vm = _$controller_('LoginController');
      $log = _$log_;
      auth = _auth_;
    }));

    it('should be registered', function() {
      expect(vm).not.toEqual(null);
    });

    it('should be registered', function() {
      expect(auth).not.toEqual(null);
    });

    it('should be registered', function() {
      expect($log).not.toEqual(null);
    });
  });
})();
