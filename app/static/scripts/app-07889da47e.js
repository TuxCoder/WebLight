!function(){"use strict";angular.module("frontend",["ngAnimate","ngCookies","ngTouch","ngSanitize","ngMessages","ngAria","ngResource","ui.router","ngMaterial","toastr"])}(),function(){"use strict";function t(){function t(t){var n=this;n.status=t.getStatus()}t.$inject=["auth"];var n={restrict:"E",templateUrl:"app/components/navbar/navbar.html",scope:{creationDate:"="},controller:t,controllerAs:"vm",bindToController:!0};return n}angular.module("frontend").directive("myNavbar",t)}(),function(){"use strict";function t(t){function n(){return t.get("/api/device").then(function(t){return t.data})}function e(n){return t.get("/api/device/"+n).then(function(t){return t.data})}function o(n){return t.post("/api/device/"+n.name,n).then(function(t){return t.data})}var i=this;i.getDevices=n,i.getDevice=e,i.updateDevice=o}t.$inject=["$http"],angular.module("frontend").service("device",t)}(),function(){"use strict";function t(t){function n(){return t.get("/api/login").then(function(t){return t.data.form})}function e(n){return t.post("/api/login",n).then(function(){status.loggedIn=!0})}function o(){return t.get("/api/user").then(function(t){return a.status.user=t.data,a.status.loggedIn=void 0!=t.data.user_id,a.status})}function i(){return a.status}var a=this;a.getForm=n,a.login=e,a.updateStatus=o,a.getStatus=i,a.status={loggedIn:!1,user:null},o()}t.$inject=["$http"],angular.module("frontend").service("auth",t)}(),function(){"use strict";function t(t){function n(){return t.get("/api/animation",{cache:!0}).then(function(t){return t.data})}function e(t){return n().then(function(n){var e=null;return angular.forEach(n,function(n){n.name==t&&(e=n)}),e})}var o=this;o.getAnimations=n,o.getAnimation=e}t.$inject=["$http"],angular.module("frontend").service("animations",t)}(),function(){"use strict";function t(t,n,e){function o(){e.getForm().then(function(t){a.form=t})}function i(){return e.login(a.form).then(function(){a.error=void 0,n.go("home")},function(t){a.error=t.data.error})}var a=this;a.form=void 0,a.error=void 0,a.login=i,o()}t.$inject=["$log","$state","auth"],angular.module("frontend").controller("LoginController",t)}(),function(){"use strict";function t(t,n,e,o){function i(){e.updateStatus().then(function(n){n.loggedIn||t.go("login"),o.getDevices().then(function(t){r.devices=t})})}function a(n){t.go("device",{key:n})}var r=this;r.gotoDevice=a,r.devices=[],i()}t.$inject=["$state","$scope","auth","device"],angular.module("frontend").controller("MainController",t)}(),function(){"use strict";function t(t,n,e){function o(){n.getDevice(t.key).then(function(t){r.device=t,r.animation=t.animation.name}),e.getAnimations().then(function(t){r.animations=t})}function i(){void 0!=r.device&&n.updateDevice(r.device).then(function(t){r.device=t,r.animation=t.animation.name})}function a(){void 0!=r.device&&e.getAnimation(r.animation).then(function(t){r.device.animation=t})}var r=this;r.device=void 0,r.animations=void 0,r.animation=void 0,r.update=i,r.updateAnimation=a,o()}t.$inject=["$stateParams","device","animations"],angular.module("frontend").controller("DeviceController",t)}(),function(){"use strict";function t(t,n){n.defaults.headers.post["X-CSRFToken"]=csrftoken,t.debug("runBlock end")}t.$inject=["$log","$http"],angular.module("frontend").run(t)}(),function(){"use strict";function t(t,n){t.state("home",{url:"/",templateUrl:"app/main/main.html",controller:"MainController",controllerAs:"vm"}).state("login",{url:"/login",templateUrl:"app/login/login.html",controller:"LoginController",controllerAs:"vm"}).state("device",{url:"/device/:key",templateUrl:"app/device/device.html",controller:"DeviceController",controllerAs:"vm"}),n.otherwise("/")}t.$inject=["$stateProvider","$urlRouterProvider"],angular.module("frontend").config(t)}(),function(){"use strict";angular.module("frontend")}(),function(){"use strict";function t(t,n){t.debugEnabled(!0),n.allowHtml=!0,n.timeOut=3e3,n.positionClass="toast-top-right",n.preventDuplicates=!0,n.progressBar=!0}t.$inject=["$logProvider","toastrConfig"],angular.module("frontend").config(t)}(),angular.module("frontend").run(["$templateCache",function(t){t.put("app/device/device.html",'<div layout=vertical layout-fill><md-content><h1>{{ vm.device.name }}</h1><select ng-change=vm.updateAnimation() ng-model=vm.animation><option ng-repeat="animation in vm.animations" value="{{ animation.name }}">{{ animation.name }}</option></select><lable ng-repeat="(name,param) in vm.device.animation.params">{{ name }} <input ng-model=param.value type="{{ param.type }}" min="{{ param.min }}" max="{{ param.max }}" step="{{ param.step }}"></lable><button ng-click=vm.update()>update</button></md-content></div>'),t.put("app/main/main.html",'<div layout=vertical layout-fill><md-content><div ng-repeat="device in vm.devices"><button ng-click=vm.gotoDevice(device.name)>{{device.name}}</button></div></md-content></div>'),t.put("app/login/login.html","<div layout=vertical layout-fill><md-content>{{ vm.error }}<form ng-submit=vm.login() name=auth><label>Username: <input type=text ng-model=vm.form.login_name name=login_name required></label><label>Password: <input type=password ng-model=vm.form.password name=password required></label><input type=submit value=Login></form></md-content></div>"),t.put("app/components/navbar/navbar.html",'<md-toolbar layout=row layout-align="center center"><section flex layout=row layout-align="left center"><md-button href=# class=md-raised>Home</md-button><md-button href=# class=md-raised>About</md-button><md-button href=# class=md-raised>Contact</md-button></section><div ng-switch=vm.status.loggedIn><div ng-switch-when=true>Hello {{ vm.status.user.login_name }}</div><div ng-switch-default>login</div></div></md-toolbar>')}]);
//# sourceMappingURL=../maps/scripts/app-07889da47e.js.map
