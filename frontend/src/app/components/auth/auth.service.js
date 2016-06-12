(function () {
  'use strict';

  angular
    .module('frontend')
    .service('auth', auth);

  /** @ngInject */
  function auth($http) {
    var vm = this;
    vm.getForm = getForm;
    vm.login = login;
    vm.updateStatus = updateStatus;
    vm.getStatus = getStatus;
    vm.status = {'loggedIn': false, 'user': null};

    updateStatus();

    function getForm() {
      return $http.get('/api/login').then(function (response) {
        return response.data.form;
      });
    }

    function login(form) {
      return $http.post('/api/login', form).then(function () {
        status.loggedIn = true;
      });
    }

    function updateStatus() {
      return $http.get('/api/user').then(function (resp) {
        vm.status.user = resp.data;
        vm.status.loggedIn = resp.data.user_id != undefined;
        return vm.status;
      });
    }

    function getStatus() {
      return vm.status;
    }
  }

})();
