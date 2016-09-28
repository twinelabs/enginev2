$(document).ready(function(){

    // =======
    // HIDE/SHOW/SET INITIAL
    // =======

    document.getElementById('match_columns').style.display = 'none';
    document.getElementById('match_rules').style.display = 'none';
    document.getElementById('match_create').style.display = 'none';

    var sel_AorB = null,
        sel_id = null,
        colors = ['#a0a0a0', '#b0b0b0', '#c0c0c0', '#d0d0d0'],
        colorIndex = 0;

    function clearPairings() {
        sel_AorB = null;
        sel_id = null;
        colorIndex = 0;
    }

    // =======
    // SHOW DIRECTION HELP
    // =======

    $('#id_direction').change( function() {
        var direction = $(this).val();
        var directionHelp = document.getElementById('direction_help');
        if (direction == "onetomany") {
            directionHelp.innerHTML = "<b>Each</b> element from 1st dataset matched with<br /><b>multiple</b> elements from 2nd dataset.";
        } else {
            directionHelp.innerHTML = "<b>Multiple</b> elements from 1st dataset<br />matched with <b>each</b> element from 2nd dataset.";
        }
    });

    // =======
    // ON SELECTING NEW DATA TABLE:
    //
    // - show/hide #match_columns and #match_rules
    // - populate data_table_name_[A/B] header
    // - clear #match_columns_[A/B]
    // - populate columns for selected data table into #match_columns_[A/B]
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

    function populateSelectedColumns(data_table_id, AorB) {
        getDataTableColumns(data_table_id, function(columns_data) {
            var parentDiv = $(document.getElementById('match_columns_select_' + AorB));
            for (i = 0; i < columns_data.length; i++) {
                var column = columns_data[i];
                parentDiv.append(
                    $('<div/>', {'class': 'col-md-4'}).append(
                        $('<a/>', {
                            'id': 'match_column_button_' + AorB + '_' + column[0],
                            'class': 'btn btn-default match_column_button match_column_button' + AorB,
                            'click': function() { clickColumnButton(this) },
                            'data-pair-id': null,
                            'data-aorb': AorB,
                            'data-dc-id': column[0]
                        }).append($('<span/>', {text: column[1]}))
                    )
                );
            }
        });
    }

    function changeDataTable(elem, AorB) {
        data_table_id = elem.val();
        data_table_name = elem[0].options[elem[0].selectedIndex].innerHTML;

        document.getElementById('match_columns_select_' + AorB).innerHTML = '';
        document.getElementById('match_rules').style.display = 'none';
        var tableBodyDiv = $(document.getElementById('match_rules_table_body'));
        tableBodyDiv.innerHTML = '';

        if (data_table_id == "") {
            document.getElementById('match_columns').style.display = 'none';
        } else {
            document.getElementById('match_columns').style.display = 'block';
            document.getElementById('data_table_name_' + AorB).innerHTML = data_table_name;
            populateSelectedColumns(data_table_id, AorB);
        }
    }

    $('#data_table_A').change( function() {
        changeDataTable($(this), 'A');
    });

    $('#data_table_B').change( function() {
        changeDataTable($(this), 'B');
    });

    // =======
    // ON SELECT/DESELECT COLUMN:
    //
    // - mark as selected/deselected
    // - pair & lock with corresponding column (if selected)
    // - populate/hide rule for selected column into #match_rules
    // - show/hide #match_rules and #match_create
    // =======

    function matchRuleFormDiv(column_data_A, column_data_B, pairID) {
        var stringOptions  = [
            ["equality", "Should be Same"],
            ["inequality", "Should be Different"],
            ["intersect_comma", "Should Overlap (comma-separated)"],
        ];
        var numericOptions  = [
            ["gte", "Greater Than"],
            ["lte", "Less Than"]
        ];

        if (column_data_A[2] == 'int64') {
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
                    'name': 'match_rule_' + pairID,
                    'data-column-id': pairID,
                    'value': option[0]
                })
            ).append(
                $('<label/>', { 'for': 'gender-prefs0', 'text': option[1] })
            );
            formDiv.append(res);
        }

        return formDiv
    }

    function matchImportanceFormDiv(pairID) {
        var res = $('<div/>', {
            'class': 'match-importance-form'
        }).append(
            $('<input/>', {
                'type': 'text',
                'name': 'match_importance_' + pairID,
                'width': '50',
                'placeholder': '1-5',
                'class': 'match-importance-input',
                'pair-id': pairID
            }).on('input', function() { changeImportance(this) })
        );
        return res
    }

    function matchWeightDiv(pairID) {
        var res = $('<div/>', {
            'class': 'match-weight'
        }).append(
            $('<span/>', {
                'type': 'text',
                'id': 'match_weight_' + pairID,
                'name': 'match_weight_' + pairID,
                'class': 'match-weight'
            })
        );
        return res
    }

    function getTwoDataColumns(id_A, id_B, onSuccess) {
        $.ajax({
            url: '/match/a/get_two_data_columns',
            data: {
                'id_A': id_A,
                'id_B': id_B
            },
            dataType: 'json',
            success: onSuccess
        });
    }

    function createPairRule(id_A, id_B) {
        getTwoDataColumns(id_A, id_B, function(column_data_A_B) {
            var column_data_A = column_data_A_B[0],
                column_data_B = column_data_A_B[1];
            var pairID = 'A' + column_data_A[0] + '_B' + column_data_B[0];

            var tableBodyDiv = $(document.getElementById('match_rules_table_body'));

            tableBodyDiv.append( $('<tr/>', {
                    'id': 'match_rules_table_row_' + pairID,
                    'class': 'match_rules_table_row'
                }).append(
                    $('<td/>').append(
                        $('<h4/>').append( $('<span/>', {text: column_data_A[1]}) )
                    )
                ).append(
                    $('<td/>').append(
                        matchRuleFormDiv(column_data_A, column_data_B, pairID)
                    )
                ).append(
                    $('<td/>').append(
                        $('<h4/>').append( $('<span/>', {text: column_data_B[1]}) )
                    )
                ).append(
                    $('<td/>').append(
                        matchImportanceFormDiv(pairID)
                    )
                ).append(
                    $('<td/>').append(
                        matchWeightDiv(pairID)
                    )
                )
            )
        });
    }

    function addPair(c) {
        p1 = $(document.getElementById('match_column_button_' + c['my_AorB'] + '_' + c['my_id']));
        p2 = $(document.getElementById('match_column_button_' + c['pair_AorB'] + '_' + c['pair_id']));

        p1.data('pair-id', c['pair_id']);
        p2.data('pair-id', c['my_id']);
        p1.removeClass('btn-default').addClass('btn-success');
        p2.removeClass('btn-info').addClass('btn-success');

        sel_id = null;
        sel_AorB = null;

        var id_A = (c['my_AorB'] == 'A') ? c['my_id'] : c['pair_id'],
            id_B = (c['my_AorB'] == 'A') ? c['pair_id'] : c['my_id'];
        createPairRule(id_A, id_B);
    }
    
    function groupID(c) {
        if (c['my_AorB']== 'A') {
            return 'A' + c['my_id'] + '_B' + c['pair_id']
        } else {
            return 'A' + c['pair_id'] + '_B' + c['my_id']
        }
    }

    function removePair(c) {
        p1 = $(document.getElementById('match_column_button_' + c['my_AorB'] + '_' + c['my_id']));
        p2 = $(document.getElementById('match_column_button_' + c['pair_AorB'] + '_' + c['pair_id']));
        p1.data('pair-id', null);
        p2.data('pair-id', null);
        p1.removeClass('btn-success').addClass('btn-default');
        p2.removeClass('btn-success').addClass('btn-default');

        var goneDiv = document.getElementById('match_rules_table_row_' + groupID(c));
        goneDiv.parentNode.removeChild(goneDiv);
    }

    function printClickStatus(verbose, c) {
        if (verbose) {
            var s = c['action'] + " - my_id: " + c['my_id'] + ', pair_id: ' + c['pair_id'] + ', my_AorB: ' + c['my_AorB'] + ', pair_AorB: ' + c['pair_AorB'];
            console.log(s);
        }
    }

    clickColumnButton = function(elem) {
        var button = $(elem);
        var c = {
            "my_id": button.data("dc-id"),
            "pair_id": button.data("pair-id"),
            "my_AorB": button.data("aorb"),
            "pair_AorB": (button.data("aorb") == 'A') ? 'B' : 'A',
            "action": "CLICKED"
        }

        var verbose = false;
        printClickStatus(verbose, c)

        // if paired: unpair self and partner
        if (c['pair_id'] != null) {
            c['action'] = "UNPAIR";
            removePair(c);

        // if something selected ...
        } else if (sel_id != null) {

            // ... if it's me: unselect
            if (sel_id == c['my_id']) {
                c['action'] = "UNSELECT";
                sel_id = null;
                sel_AorB = null;
                button.removeClass('btn-info').addClass('btn-default');

            // ... within the same data set: change to me
            } else if (sel_AorB == c['my_AorB']) {
                c['action'] = "CHANGE";

                old = document.getElementById('match_column_button_' + c['my_AorB'] + '_' + sel_id);
                $(old).removeClass('btn-info').addClass('btn-default');
                button.removeClass('btn-default').addClass('btn-info');
                sel_id = c['my_id'];

            // in the other data set: pair
            } else {
                c['action'] = "PAIR";
                c['pair_id'] = sel_id;
                addPair(c);
            }

        // if nothing selected: select
        } else {
            c['action'] = "SELECT";

            sel_id = c['my_id'];
            sel_AorB = c['my_AorB'];
            button.removeClass('btn-default').addClass('btn-info');

            document.getElementById('match_rules').style.display = 'block';
            document.getElementById('match_create').style.display = 'block';
        }

        printClickStatus(verbose, c)
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

            pair_id = $(this)[0].getAttribute('pair-id');
            $('#match_weight_' + pair_id)[0].innerHTML = weightPct;
        });
    }

});