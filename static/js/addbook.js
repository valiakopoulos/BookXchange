$("#searchBookForm").submit(function (event) {
    // cancels the form submission
    event.preventDefault();
    submitForm();
});

function submitForm() {
    $('#GoSearch').prop('disabled', true);
    $('#bookplacement').empty();
    $('#booksearch').empty().append($('<div>').addClass('loadingAnimation'));
    // Initiate Variables With Form Content
    var isbn = $("#isbn").val();

    var request = $.ajax({
        type: "POST",
        url: "/searchbook",
        data: "isbn=" + isbn
    });

    request.done(function (html) {
        $('#booksearch').html(html);
        $('.addBook').each(function () {
            $(this).click(function () {
                var panel = $('#' + $(this).val());
                $('.addBook', panel).remove();
                $('#bookplacement').html(panel[0].outerHTML);
                $('#booksearch').html('');
                $('#addbook_button').removeAttr('disabled');
                setupDescription();
            });
        });
        setupDescription();
    $('#GoSearch').prop('disabled', false);
    });

    request.fail(function(jqXHR, textStatus) {
        $('#booksearch').empty();
        $('#booksearch').html('Could not find the book!<br />');
        $('#GoSearch').prop('disabled', false);
        //$('#addbook_button').attr('disabled', true);
    });
}

$(function() {
    var oldprice = '';
    $('#price').focus(function() { oldprice = $(this).val(); });
    $('#price').change(function() {
        var num = parseFloat($(this).val());
        if(isNaN(num) || num < 0) {
            $(this).val(oldprice);
        } else {
            $(this).val(num.toFixed(2));
        }
    });
});