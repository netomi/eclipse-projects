document$.subscribe(function() {
  var tables = document.querySelectorAll("article table:not([class])")
  tables.forEach(function(table) {
    var filter = new TableFilter(table, {
        base_path: 'https://unpkg.com/tablefilter@0.7.3/dist/tablefilter/'
    });
    filter.init();
  })
})
