$("#deactivateListing").submit(function (event) {
    // cancels the form submission
    event.preventDefault();

    submitForm(document.activeElement.id);
});

function submitForm(id) {
    var panel = $('#' + id).closest('.book');
    panel.append($('<div>').addClass('block').append($('<div>').addClass('loadingAnimation')));
    var request = $.ajax({
        type: "POST",
        url: "/deactivate",
        data: "listing_id=" + id
    });

    request.done(function (html) {
        $('#' + id).html(html);
        panel.slideUp(500, function() { panel.remove(); });
    });

    request.fail(function(jqXHR, textStatus) {
        $('#' + id).html('Failed to deactivate!');
    });
}

$("#banUser").submit(function (event) {
    // cancels the form submission
    event.preventDefault();
    banUser(document.activeElement.id);
});

function banUser(id) {
    var panel = $('#' + id).closest('.panel');
    panel.append($('<div>').addClass('block').append($('<div>').addClass('loadingAnimation')));
    var request = $.ajax({
        type: "POST",
        url: "/banuser",
        data: "user_id=" + id
    });

    request.done(function (html) {
        $('#' + id).html(html);
        $('.block', panel).remove();
    });

    request.fail(function (jqXHR, textStatus) {
        $('#' + id).html('Failed to ban!');
    });
}