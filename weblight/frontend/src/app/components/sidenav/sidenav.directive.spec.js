(function() {
  'use strict';

  /**
   * @todo Complete the test
   * This example is not perfect.
   * Test should check if MomentJS have been called
   */
  describe('directive sidebar', function() {
    // var $window;
    var vm;
    var el;

    beforeEach(module('frontend'));
    beforeEach(inject(function($compile, $rootScope) {
      // spyOn(_$window_, 'moment').and.callThrough();
      // $window = _$window_;

      el = angular.element('<my-sidebar></my-sidebar>');

      $compile(el)($rootScope.$new());
      $rootScope.$digest();
      vm = el.isolateScope().vm;
      // ctrl = el.controller('mySidebar');
    }));

    it('should be compiled', function() {
      expect(el.html()).not.toEqual(null);
    });
    it('should be compiled', function() {
      expect(vm).not.toEqual(null);
    });
  });
})();
