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
        $(event.currentTarget).toggleClass('active');

        target.find('.sidebar-submenu').toggle();
    });

    var selectedItem;

    if ($('.dataset-table').length > 0) {
        var table = $('.dataset-table').DataTable({
            paging: true,
            pageLength: 25,
            scrollX: true,
            scrollY: true,
            select: 'single',
            lengthMenu: [[10, 25, 250, -1], [10, 25, 250, 'All']],
            buttons: [{
                extend: 'colvis',
                text: 'Select columns',
            }]
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

        $('.row>.col-sm-6:first-of-type', table.table().container()).removeClass('col-sm-6').addClass('col-sm-8');
        $('.row>.col-sm-6', table.table().container()).removeClass('col-sm-6').addClass('col-sm-4');


        table.on('select', function(e, dt, type, indexes) {
            selectedItem = $(table[type](indexes).nodes().to$()[0]);
            table.buttons(1, null).enable();
        });

        table.on('deselect', function(e, dt, type, indexes) {
            selectedItem = null;
            table.buttons(1, null).disable();
        });
    }

    if ($('radio-inline').length > 4) $('.radio-inline')[4].click();

    $('#custom-search').click(function(event) {
        $('#radio-custom').prop('checked', true);
    });

    $('#newcustom').click(function(event) {
        $('#radio-newcustom').prop('checked', true);
    });

    $('#radio-custom, #radio-newcustom').on('change', function(event) {
        // if (this.checked && this.value.indexOf('custom') !== -1)
            // showCustomSearch();
    });

    // sortable('.sortable');

    $('.prefs-checkbox2').click(function(event) {
        var gp = $(this).parent().parent();
        if (this.checked) {
            $('.match-preference-form input[type="radio"]', gp).prop('disabled', true);
            $('.match-custom-options .form-group *', gp).prop('disabled', false);
            $('.match-custom-options .form-group *', gp).removeClass('disabled');
        }
        else {
            $('.match-preference-formf input[type="radio"]', gp).prop('disabled', false);
            $('.match-custom-options .form-group *', gp).prop('disabled', true);
            $('.match-custom-options .form-group *', gp).addClass('disabled');

        }
    });

    $('.prefs-checkbox').click(function(event) {
        var gp = $(this).parent().parent();
        if (this.checked) {
            $('.slider-pref input[type="radio"]', gp).prop('disabled', true);
            $('.additional-prefs .form-group *', gp).prop('disabled', false);
            $('.additional-prefs .form-group *', gp).removeClass('disabled');
        }
        else {
            $('.slider-pref input[type="radio"]', gp).prop('disabled', false);
            $('.additional-prefs .form-group *', gp).prop('disabled', true);
            $('.additional-prefs .form-group *', gp).addClass('disabled');

        }
    });

    $('.slider-pref').click();

    function showCustomSearch() {
        $('input[name="save-custom-search"]').toggleClass('hidden');
        $('.custom-search-options').toggleClass('hidden');
    }

    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

});