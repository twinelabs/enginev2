$(document).ready(function(){
    var sidebarVisible = true;
    $('.sidebar-close-button').on('click', function(e) {
        sidebarVisible = !sidebarVisible;
        if (sidebarVisible) {
            $('.sidebar-close-button').text('<');
        }
        else {
            $('.sidebar-close-button').text('>');
        }
        $('.sidebar-content').toggleClass('sidebar-hidden');
        $('.sidebar-close-button').toggleClass('sidebar-visible');
        $('.main-content').toggleClass('col-sm-9');
        $('.main-content').toggleClass('col-sm-12');
    });

    $('.sidebar-menu-header').on('click', function(e) {
        $(event.currentTarget).parent().toggleClass('active');
        $(event.currentTarget).parent().find('.sidebar-submenu').toggle();
    });

    var selectedItem;

    var table = $('.dataset-table').DataTable({
        paging:   true,
        scrollX: true,
        scrollY: true,
        select: 'single',
        lengthChange: false,
        buttons: [{
            extend: 'colvis',
            text: 'Select columns',
            className: 'btn btn-default'
        }, {
          text: 'View',
          action: function (e, dt, node, config) {
              // Do stuff
          },
          className: 'btn btn-default view'
        },
        {
            text: 'Edit',
            action: function(e, dt, node, config) {
                // Do stuff
            },
            className: 'btn btn-default edit'
        },
        {
            text: 'Delete',
            action: function(e, dt, node, config) {
                // Do stuff
            },
            className: 'btn btn-default delete'
        }],
        columnDefs: [
            { visible: false, targets: 0 }
        ]
    });
    table.buttons(['.view', '.edit', '.delete']).disable();

    table.buttons().container().prependTo( table.table().container() ) ;

    table.on('select', function(e, dt, type, indexes) {
        selectedItem = $(table[type](indexes).nodes().to$()[0]);
        table.buttons(['.view', '.edit', '.delete']).enable();
    });

    table.on('deselect', function(e, dt, type, indexes) {
        selectedItem = null;
        table.buttons(['.view', '.edit', '.delete']).disable();
    });
});