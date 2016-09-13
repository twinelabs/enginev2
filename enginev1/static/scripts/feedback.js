$(document).ready(function(){

    // =======
    // CHANGE FEEDBACK GROUP
    // =======

    function changeFeedbackGroup(group_number) {
    // On selecting feedback group:

        // 1) hide all others
        $("div.feedbackGroup").each( function(i, elem) {
            elem.style.display = 'none';
        })

        // 2) show selected group
        $("div.feedbackGroup" + group_number).each( function(i, elem) {
            elem.style.display = 'block';
        });
    }

    $('#feedback_group').change( function() {
        group_number = $(this).val();
        changeFeedbackGroup(group_number);
    });

});