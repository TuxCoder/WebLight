(function () {
  'use strict';

  angular
    .module('frontend')
    .service('auth', auth);

  /** @ngInject */
  function auth($http,$rootScope) {
    var vm = this;
    vm.getForm = getForm;
    vm.login = login;
    vm.logout = logout;
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
        vm.updateStatus()
      });
    }

    function logout() {
      return $http.post('/api/logout').then(function () {
        vm.updateStatus()
      });
    }

    function updateStatus() {
      return $http.get('/api/user').then(function (resp) {
        vm.status.user = resp.data;
        var loggedIn =vm.status.loggedIn;
        vm.status.loggedIn = resp.data.user_id != 0;
        if(loggedIn != vm.status.loggedIn) {
          $rootScope.sidenav.update();
        }
        return vm.status;
      });
    }

    function getStatus() {
      return vm.status;
    }
  }

})();
