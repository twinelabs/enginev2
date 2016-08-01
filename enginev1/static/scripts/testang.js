app = angular.module('example.app.static', []);

app.controller ('AppController', ['$scope', '$http', function($scope, $http) {

    var _ = $scope;

    _.tables = [
        { "name": "T1", "id": 1 },
        { "name": "T2", "id": 2 }
    ];

    _.selectedTable = _.tables[0];

    _.views = [
    {
      id: 0,
      name: 'Summary'
    },
    {
      id: 1,
      name: 'Charts'
    },
    {
      id: 2,
      name: 'Statistics'
    }
  ];
  _.selectedView = _.views[1];

}]);