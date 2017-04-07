$("#searchBookForm").submit(function (event) {
    // cancels the form submission
    event.preventDefault();
    submitForm();
});

function submitForm() {
    // Initiate Variables With Form Content
    var isbn = $("#isbn").val();

    var request = $.ajax({
        type: "POST",
        url: "/searchbook",
        data: "isbn=" + isbn
    });

    request.done(function (html) {
        $('#bookplacement').html(html);
        $('#addbook_button').removeAttr('disabled');
    });

    request.fail(function(jqXHR, textStatus) {
        $('#bookplacement').html('Could not find the book!<br />');
        $('#addbook_button').attr('disabled', true);
    });
}