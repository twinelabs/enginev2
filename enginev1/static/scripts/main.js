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
        $('.main-content').toggleClass('col-sm-10');
        $('.main-content').toggleClass('col-sm-12');
        $('.main-content').toggleClass('col-sm-offset-2');
    });

    $('.sidebar-menu-header').on('click', function(event) {
        var target = $(event.currentTarget).parent();
        target.toggleClass('active');
        target.find('.sidebar-submenu').toggle();
    });

    var selectedItem;

    if ($('.dataset-table').length > 0) {
        var table = $('.dataset-table').DataTable({
            paging: true,
            scrollX: true,
            scrollY: true,
            select: 'single',
            lengthMenu: [[10, 25, 250, -1], [10, 25, 250, 'All']],
            buttons: [{
                extend: 'colvis',
                text: 'Select columns',
            }],
            columnDefs: [
                { visible: false, targets: 0 }
            ]
        });
        new $.fn.dataTable.Buttons(table, {
            buttons: [{
                text: 'View',
                action: function(e, dt, node, config) {
                    // Do stuff
                },
            },
                {
                    text: 'Edit',
                    action: function(e, dt, node, config) {
                        // Do stuff
                    },
                },
                {
                    text: 'Delete',
                    action: function(e, dt, node, config) {
                        // Do stuff
                    },
                    className: 'btn-danger'
                }]
        });
        table.buttons(1, null).disable();

        $('.row>.col-sm-6:first-of-type', table.table().container()).prepend(table.buttons(0, null).container());
        $('.row>.col-sm-6>.dt-buttons', table.table().container()).after(table.buttons(1, null).container());

        table.on('select', function(e, dt, type, indexes) {
            selectedItem = $(table[type](indexes).nodes().to$()[0]);
            table.buttons(1, null).enable();
        });

        table.on('deselect', function(e, dt, type, indexes) {
            selectedItem = null;
            table.buttons(1, null).disable();
        });
    }

    $('.radio-inline')[0].click();

    $('#custom-search').click(function(event) {
        $('#radio-custom').prop('checked', true);
    });

    $('#newcustom').click(function(event) {
        $('#radio-newcustom').prop('checked', true);
    });

    $('#radio-custom, #radio-newcustom').on('change', function(event) {
        console.log(this.checked);
        console.log(this.value);
        if (this.checked && this.value.indexOf('custom') !== -1)
            showCustomSearch();
    });

    function showCustomSearch() {
        $('input[name="save-custom-search"]').toggleClass('hidden');
        $('.custom-search-options').toggleClass('hidden');
    }
});