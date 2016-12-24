(function() {
  'use strict';

  angular
    .module('frontend')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'vm'
      })
      .state('login', {
        url: "/login",
        templateUrl: "app/login/login.html",
        controller: 'LoginController',
        controllerAs: 'vm'
      })
      .state('device', {
        url: "/device/:key",
        templateUrl: "app/device/device.html",
        controller: 'DeviceController',
        controllerAs: 'vm'
      });

    $urlRouterProvider.otherwise('/');
  }

})();
