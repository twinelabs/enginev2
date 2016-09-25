$(document).ready(function(){

    // =======
    // HIDE/SHOW INITIAL
    // =======

    document.getElementById('match_columns').style.display = 'none';
    document.getElementById('match_rules').style.display = 'none';
    document.getElementById('match_create').style.display = 'none';

    // =======
    // ON SELECTING NEW DATA TABLE:
    //
    // - show/hide #match_columns and #match_rules
    // - clear #match_columns
    // - populate columns for selected data table into #match_columns
    // =======

    function getDataTableColumns(data_table_id, onSuccess) {
        $.ajax({
            url: '/match/a/get_data_table_columns',
            data: {
                'data_table_id': data_table_id
            },
            dataType: 'json',
            success: onSuccess
        });
    }

    function populateSelectedColumns(data_table_id, prefix) {
        getDataTableColumns(data_table_id, function(columns_data) {
            var parentDiv = $(document.getElementById('match_columns_select' + prefix));
            for (i = 0; i < columns_data.length; i++) {
                var column = columns_data[i];
                parentDiv.append(
                    $('<div/>', {'class': 'col-md-4'}).append(
                        $('<a/>', {
                            'class': 'btn btn-default match_column_button',
                            'click': function() { clickColumnButton(this) },
                            'data-checked': false,
                            'data-dc-id': column[0]
                        }).append($('<span/>', {text: column[1]}))
                    )
                );
            }
        });
    }

    function changeDataTable(data_table_id, prefix) {
        document.getElementById('match_columns_select' + prefix).innerHTML = '';
        document.getElementById('match_rules').style.display = 'none';
        var tableBodyDiv = $(document.getElementById('match_rules_table_body'));
        tableBodyDiv.innerHTML = '';

        if (data_table_id == "") {
            document.getElementById('match_columns').style.display = 'none';
        } else {
            document.getElementById('match_columns').style.display = 'block';
            populateSelectedColumns(data_table_id, prefix);
        }
    }

    $('#data_table_A').change( function() {
        data_table_id = $(this).val();
        changeDataTable(data_table_id, '_A');
    });

    $('#data_table_B').change( function() {
        data_table_id = $(this).val();
        changeDataTable(data_table_id, '_B');
    });

    // =======
    // ON SELECT/DESELECT COLUMN:
    //
    // - show/hide #match_rules and #match_create
    // - populate/hide rule for selected column into #match_rules
    // =======

    function matchRuleFormDiv(column_data) {
        var stringOptions  = [
            ["binary_diff", "Diverse"],
            ["binary_same", "Similar"]
        ];
        var numericOptions  = [
            ["euclidean_distance", "Max Distance"],
            ["euclidean_distance", "Min Distance"]
        ];

        if (column_data[2] == 'int64') {
            var options = numericOptions;
        } else {
            var options = stringOptions;
        }

        var formDiv = $('<div/>', {'class': 'match-rule-form'})
        for (i = 0; i < options.length; i++) {
            var option = options[i];
            var res = $('<div/>', {
                    'class': 'match-rule-input'
                }
            ).append( $('<input/>', {
                    'type': 'radio',
                    'name': 'match_rule_' + column_data[0],
                    'data-column-id': column_data[0],
                    'value': option[0]
                })
            ).append(
                $('<label/>', { 'for': 'gender-prefs0', 'text': option[1] })
            );
            formDiv.append(res);
        }

        return formDiv
    }

    function matchImportanceFormDiv(column_data) {
        var res = $('<div/>', {
            'class': 'match-importance-form'
        }).append(
            $('<input/>', {
                'type': 'text',
                'name': 'match_importance_' + column_data[0],
                'width': '50',
                'placeholder': '1-5',
                'class': 'match-importance-input',
                'data-column-id': column_data[0]
            }).on('input', function() { changeImportance(this) })
        );
        return res
    }

    function matchWeightDiv(column_data) {
        var res = $('<div/>', {
            'class': 'match-weight'
        }).append(
            $('<span/>', {
                'type': 'text',
                'id': 'match_weight_' + column_data[0],
                'name': 'match_weight_' + column_data[0],
                'class': 'match-weight'
            })
        );
        return res
    }

    function getDataColumn(data_column_id, onSuccess) {
        $.ajax({
            url: '/match/a/get_data_column',
            data: {
                'data_column_id': data_column_id
            },
            dataType: 'json',
            success: onSuccess
        });
    }

    function createColumnRule(data_column_id) {
        getDataColumn(data_column_id, function(column_data) {
            var column_id = column_data[0],
                column_name = column_data[1];

            var tableBodyDiv = $(document.getElementById('match_rules_table_body'));

            tableBodyDiv.append( $('<tr/>', {
                    'id': 'match_rules_table_row_' + column_id,
                    'class': 'match_rules_table_row'
                }).append(
                    $('<td/>').append(
                        $('<h4/>').append( $('<span/>', {text: column_name}) )
                    )
                ).append(
                    $('<td/>').append(
                        matchRuleFormDiv(column_data)
                    )
                ).append(
                    $('<td/>').append(
                        matchImportanceFormDiv(column_data)
                    )
                ).append(
                    $('<td/>').append(
                        matchWeightDiv(column_data)
                    )
                )
            )
        });
    }

    clickColumnButton = function(elem) {
        var button = $(elem);
        var data_column_id = button.data("dc-id");
        var is_checked = button.data("checked");

        if (!is_checked) {
            button.data("checked", true);
            button.removeClass('btn-default').addClass('btn-info');
            createColumnRule(data_column_id);

            document.getElementById('match_rules').style.display = 'block';
            document.getElementById('match_create').style.display = 'block';
        } else {
            button.data("checked", false);
            button.removeClass('btn-info').addClass('btn-default');

            var goneDiv = document.getElementById('match_rules_table_row_' + data_column_id);
            goneDiv.parentNode.removeChild(goneDiv);
        }
    }


    // =======
    // ON CHANGE IMPORTANCE:
    //
    // - recalc weights
    // =======

    changeImportance = function(elem) {

        var sumImportance = 0;

        $('.match-importance-input').each(function(i) {
            sumImportance += +$(this).val();
        });

        $('.match-importance-input').each(function(i) {
            var importance = +$(this).val();
            var weight = importance / sumImportance;
            var weightPct = (weight * 100).toFixed(1) + "%";

            data_column_id = $(this)[0].getAttribute('data-column-id');
            $('#match_weight_' + data_column_id)[0].innerHTML = weightPct;
        });
    }

});