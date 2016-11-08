!function(){"use strict";angular.module("frontend",["ngAnimate","ngCookies","ngTouch","ngSanitize","ngMessages","ngAria","ngResource","ui.router","ngMaterial","toastr","ngOrderObjectBy"])}(),function(){"use strict";function n(){function n(n,t,e,o){function i(){e.status.loggedIn?t.getDevices().then(function(n){u.devices=n}):u.devices=[]}function a(t){u.isOpen=!1,n.go("device",{key:t})}function r(){u.isOpen=!0}var u=this;u.gotoDevice=a,u.devices=[],u.isOpen=!0,u.open=r,u.update=i,o.sidenav=u,i()}n.$inject=["$state","device","auth","$rootScope"];var t={restrict:"E",templateUrl:"app/components/sidenav/sidenav.html",controller:n,controllerAs:"vm",bindToController:!0};return t}angular.module("frontend").directive("mySidenav",n)}(),function(){"use strict";function n(n){function t(){return n.get("/api/device").then(function(n){return n.data})}function e(t){return n.get("/api/device/"+t).then(function(n){return n.data})}function o(t){return n.post("/api/device/"+t.name,t).then(function(n){return n.data})}function i(t){return t.animation=null,n.post("/api/device/"+t.name,t).then(function(n){return n.data})}var a=this;a.getDevices=t,a.getDevice=e,a.updateDevice=o,a.offDevice=i}n.$inject=["$http"],angular.module("frontend").service("device",n)}(),function(){"use strict";function n(){function n(n,t){function e(){t.go("login")}var o=this;o.status=n.getStatus(),o.logout=n.logout,o.login=e}n.$inject=["auth","$state"];var t={restrict:"E",templateUrl:"app/components/navbar/navbar.html",scope:{creationDate:"="},controller:n,controllerAs:"vm",bindToController:!0};return t}angular.module("frontend").directive("myNavbar",n)}(),function(){"use strict";function n(n,t,e){function o(){return n.get("/api/login").then(function(n){return n.data.form})}function i(t){return n.post("/api/login",t).then(function(){c.updateStatus()})}function a(){return n.post("/api/logout").then(function(){c.updateStatus(),e.go("home")})}function r(){return n.get("/api/user").then(function(n){c.status.user=n.data;var e=c.status.loggedIn;return c.status.loggedIn=0!=n.data.user_id,e!=c.status.loggedIn&&t.sidenav.update(),c.status})}function u(){return c.status}var c=this;c.getForm=o,c.login=i,c.logout=a,c.updateStatus=r,c.getStatus=u,c.status={loggedIn:!1,user:null},r()}n.$inject=["$http","$rootScope","$state"],angular.module("frontend").service("auth",n)}(),function(){"use strict";function n(n){function t(){return n.get("/api/animation",{cache:!0}).then(function(n){return n.data})}function e(n){return t().then(function(t){var e=null;return angular.forEach(t,function(t){t.name==n&&(e=t)}),e})}var o=this;o.getAnimations=t,o.getAnimation=e}n.$inject=["$http"],angular.module("frontend").service("animations",n)}(),function(){"use strict";function n(n,t,e,o){function i(){void 0!=n.sidenav&&n.sidenav.open()}i()}n.$inject=["$rootScope","$scope","auth","device"],angular.module("frontend").controller("MainController",n)}(),function(){"use strict";function n(n,t,e){function o(){e.getForm().then(function(n){a.form=n})}function i(){return e.login(a.form).then(function(){a.error=void 0,t.go("home")},function(n){a.error=n.data.error})}var a=this;a.form=void 0,a.error=void 0,a.login=i,o()}n.$inject=["$log","$state","auth"],angular.module("frontend").controller("LoginController",n)}(),function(){"use strict";function n(n,t,e){function o(){c.reload(),e.getAnimations().then(function(n){c.animations=n})}function i(){t.getDevice(n.key).then(function(n){c.device=n,c.animation=n.animation.name})}function a(){void 0!=c.device&&t.offDevice(c.device).then(function(n){c.device=n,c.animation=null})}function r(){l++;var n=l;void 0!=c.device&&t.updateDevice(c.device).then(function(t){l==n&&(c.device=t,c.animation=t.animation.name)})}function u(){void 0!=c.device&&e.getAnimation(c.animation).then(function(n){c.device.animation=n,c.update()})}var c=this;c.device=void 0,c.animations=void 0,c.animation=void 0,c.update=r,c.reload=i,c.off=a,c.updateAnimation=u,o();var l=0}n.$inject=["$stateParams","device","animations"],angular.module("frontend").controller("DeviceController",n)}(),function(){"use strict";function n(n,t){t.defaults.headers.post["X-CSRFToken"]=csrftoken,n.debug("runBlock end")}n.$inject=["$log","$http"],angular.module("frontend").run(n)}(),function(){"use strict";function n(n,t){n.state("home",{url:"/",templateUrl:"app/main/main.html",controller:"MainController",controllerAs:"vm"}).state("login",{url:"/login",templateUrl:"app/login/login.html",controller:"LoginController",controllerAs:"vm"}).state("device",{url:"/device/:key",templateUrl:"app/device/device.html",controller:"DeviceController",controllerAs:"vm"}),t.otherwise("/")}n.$inject=["$stateProvider","$urlRouterProvider"],angular.module("frontend").config(n)}(),function(){"use strict";angular.module("frontend")}(),function(){"use strict";function n(n,t){n.debugEnabled(!0),t.allowHtml=!0,t.timeOut=3e3,t.positionClass="toast-top-right",t.preventDuplicates=!0,t.progressBar=!0}n.$inject=["$logProvider","toastrConfig"],angular.module("frontend").config(n)}(),angular.module("frontend").run(["$templateCache",function(n){n.put("app/device/device.html",'<h1>{{ vm.device.name }}</h1><form ng-submit=vm.update()><md-input-container layout=row><md-select ng-change=vm.updateAnimation() ng-model=vm.animation><md-option ng-value=animation.name ng-repeat="animation in vm.animations">{{ animation.name }}</md-option></md-select></md-input-container><md-input-container layout=row ng-repeat="(name,param) in vm.device.animation.params|orderObjectBy:\'key\'"><lable flex=60>{{ name }}<div ng-switch=param.type><input ng-switch-when=float ng-change=vm.update() ng-model=param.value type=number min="{{ param.min }}" max="{{ param.max }}" step="{{ param.step }}"> <input ng-switch-when=color ng-change=vm.update() ng-model=param.value type=color> <input ng-switch-when=boolean ng-change=vm.update() ng-model=param.value type=checkbox><md-slider ng-switch-when=range ng-model=param.value ng-change=vm.update() min="{{ param.min }}" max="{{ param.max }}" step="{{ param.step }}\' ></md-slider>\n                <input ng-switch-default=" ng-change=vm.update() ng-model=param.value type=text></div></lable></md-input-container><div layout=row><md-input-container flex=20><input type=submit value=update></md-input-container><md-input-container layout=row flex=20><input ng-click=vm.off() type=button value=off></md-input-container><md-input-container layout=row flex=20><input ng-click=vm.reload() type=button value=reload></md-input-container></div></form>'),n.put("app/login/login.html","{{ vm.error }}<form ng-submit=vm.login() name=auth><label>Username: <input type=text ng-model=vm.form.login_name name=login_name required></label><label>Password: <input type=password ng-model=vm.form.password name=password required></label><input type=submit value=Login></form>"),n.put("app/main/main.html",""),n.put("app/components/navbar/navbar.html",'<md-toolbar layout=row layout-align="center center"><section flex layout=row layout-align="left center"><md-button href=#/ class=md-raised>Home</md-button></section><div ng-switch=vm.status.loggedIn><div ng-switch-when=true>Hello {{ vm.status.user.login_name }}<md-button ng-click=vm.logout()>Logout</md-button></div><div ng-switch-default><md-button ng-click=vm.login()>login</md-button></div></div></md-toolbar>'),n.put("app/components/sidenav/sidenav.html",'<md-sidenav md-is-locked-open=vm.isOpen class=md-whiteframe-z2><md-list><md-list-item ng-repeat="device in vm.devices"><md-button ng-click=vm.gotoDevice(device.name)>{{device.name}}</md-button></md-list-item></md-list></md-sidenav>')}]);
//# sourceMappingURL=../maps/scripts/app-eb0706511c.js.map
