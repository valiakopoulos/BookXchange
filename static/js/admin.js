$("#deactivateListing").submit(function (event) {
    // cancels the form submission
    event.preventDefault();
    submitForm(document.activeElement.id);
});

function submitForm(id) {
    var request = $.ajax({
        type: "POST",
        url: "/deactivate",
        data: "listing_id=" + id
    });

    request.done(function (html) {
        $('#' + id).html(html);
    });

    request.fail(function(jqXHR, textStatus) {
        $('#' + id).html('Failed to deactivate!');
    });
}