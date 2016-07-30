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
});