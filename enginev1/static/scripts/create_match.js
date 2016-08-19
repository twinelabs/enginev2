$(document).ready(function(){

    // =======
    // CHANGE TASK
    // =======

    function clickTaskButton(taskOn) {
    // On clicking Group/Assign buttons:

        // 1) select form input (radio button)
        taskOff = (taskOn == "cluster") ? "assign" : "cluster"

        // 2) change button color
        document.getElementById("task_" + taskOn).checked = true;
        $("#task_" + taskOn + "_button").removeClass('btn-default').addClass('btn-info');
        $("#task_" + taskOff + "_button").removeClass('btn-info').addClass('btn-default');

        // 3) hide/show relevant matching options and columns divs
        document.getElementById("task_" + taskOn + "_options").style.display = 'block';
        document.getElementById("task_" + taskOff + "_options").style.display = 'none';

        document.getElementById("task_" + taskOn + "_columns").style.display = 'block';
        document.getElementById("task_" + taskOff + "_columns").style.display = 'none';
    }

    $('#task_cluster_button').click(function() {
        clickTaskButton("cluster");
    });
    $('#task_assign_button').click(function() {
        clickTaskButton("assign");
    });

    // =======
    // GROUP - CHANGE DATASET
    // =======

    function changeSingleDataSet(data_table_id) {
    // On selecting single data set for GROUP:

        // 1) show columns div (if selection is not blank)
        displayOption = (data_table_id == "") ? 'none' : 'block';
        document.getElementById('task_cluster_columns').style.display = displayOption;

        // 2) show columns for selected data table
        $("div[data-column='none'][data-dt-id='" + data_table_id + "']").each( function(i, elem) {
            elem.style.display = 'block';
        });
        $("div[data-column='none'][data-dt-id!='" + data_table_id + "']").each( function(i, elem) {
            elem.style.display = 'none';
        });
    }

    $('#data_tables_single').change( function() {
        data_table_id = $(this).val();
        changeSingleDataSet(data_table_id);
    });


    // =======
    // GROUP - SELECT COLUMN
    // =======

    function clickColumnButton(dc_id, buttonDiv) {
    // On clicking column buttons:

        // 1) select checkbox
        var rule_row = document.getElementById('cluster_rule_row_' + dc_id);
        var chkbx = document.getElementById('task_cluster_columns_checkbox_' + dc_id);
        chkbx.checked = !chkbx.checked;

        // 2) hide/show matching rule
        if (chkbx.checked) {
            buttonDiv.removeClass('btn-default').addClass('btn-info');
            rule_row.style.display = 'table-row';
        } else {
            buttonDiv.removeClass('btn-info').addClass('btn-default');
            rule_row.style.display = 'none';
        }

        document.getElementById('matching_rules').style.display = 'block';
    }


    $(".task_cluster_column_button").on( 'click', function() {
        var dc_id = $(this).attr("data-dc-id");
        clickColumnButton(dc_id, $(this));
    });

    // =======
    // ASSIGN - CHANGE DATASET(S)
    // =======

    function changeMultipleDataSet(A_or_B, data_table_id) {
    // On selecting either data set for assign:

        // 1) show columns for selected data table
        $("div[data-column='" + A_or_B + "'][data-dt-id='" + data_table_id + "']").each( function(i, elem) {
            elem.style.display = 'inline-block';
        });
        $("div[data-column='" + A_or_B + "'][data-dt-id!='" + data_table_id + "']").each( function(i, elem) {
            elem.style.display = 'none';
        });
    }

    $('#data_tables_multipleA').change( function() {
        document.getElementById('task_assign_columns').style.display = 'block';
        data_table_id = $(this).val();
        changeMultipleDataSet("A", data_table_id);
    });

    $('#data_tables_multipleB').change( function() {
        document.getElementById('task_assign_columns').style.display = 'block';
        data_table_id = $(this).val();
        changeMultipleDataSet("B", data_table_id);
    });

    changeMultipleDataSet("A", "99999");
    changeMultipleDataSet("B", "99999");

});