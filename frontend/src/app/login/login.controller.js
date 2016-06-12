(function () {
  'use strict';

  angular
    .module('frontend')
    .controller('LoginController', LoginController);

  /** @ngInject */
  function LoginController($log, $state, auth) {
    var vm = this;
    vm.form = undefined;
    vm.error = undefined;

    vm.login = login;

    activate();

    function activate() {
      auth.getForm().then(function (data) {
        vm.form = data
      });
    }

    function login() {
      return auth.login(vm.form).then(function () {
        vm.error = undefined;
        $state.go('home');
      }, function (data) {
        vm.error = data.data.error;
      });
    }
  }
})();
