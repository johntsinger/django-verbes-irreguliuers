// dataTables configuration
$(document).ready(function () {
    $('#example').DataTable({
        scrollY: '45em',
        scrollX: true,
        scrollCollapse: true,
        paging: false,
        bFilter: true,
        bInfo: false,
        language: {
            zeroRecords: 'Aucune donnée à afficher',
            search: 'Rechercher : ',
        },
    });
    // Adding #button-group to #example_filter div
    $('#example_filter').append($('#button-group'));
});

// Functions that set action for each button of button-group
$('#success').on('click', function () {
    // Remove active class for the other buttons
    $('#unsuccess').removeClass('active')
    $('#not-done').removeClass('active')
    $.fn.dataTable.ext.search.pop()

    // Make the button switchable and add a filter function
    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $.fn.dataTable.ext.search.pop()
    } else {
        $(this).addClass('active');
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var table = $('#example').DataTable();
                return $(table.row(dataIndex).node()).hasClass('success');
            }
        );
    };
    // Display results
    var table = $('#example').DataTable();
    table.draw();
});

$('#unsuccess').on('click', function () {
    $('#success').removeClass('active')
    $('#not-done').removeClass('active')
    $.fn.dataTable.ext.search.pop()

    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $.fn.dataTable.ext.search.pop()
    } else {
        $(this).addClass('active');
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var table = $('#example').DataTable();
                return $(table.row(dataIndex).node()).hasClass('unsuccess');
            }
        );
    };
    var table = $('#example').DataTable();
    table.draw();
});

$('#not-done').on('click', function () {
    $('#success').removeClass('active')
    $('#unsuccess').removeClass('active')
    $.fn.dataTable.ext.search.pop()

    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $.fn.dataTable.ext.search.pop()
    } else {
        $(this).addClass('active');
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var table = $('#example').DataTable();
                return !$(table.row(dataIndex).node()).hasClass('unsuccess') && !$(table.row(dataIndex).node()).hasClass('success');
            }
        );
    };
    var table = $('#example').DataTable();
    table.draw();
});