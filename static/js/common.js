function setupDescription() {
    $('.book .info .description').each(function() {
        if($(this).height() > 100) {
            $(this).addClass('scrollshadow');
            $(this).click(function() {
                $(this).toggleClass('scrollshadow');
            });
        }
   });
}

function removeBook(bookId, e) {
    var panel = $(e).closest('.book');
    panel.append($('<div>').addClass('block').append($('<div>').addClass('loadingAnimation')));
    var request = $.ajax({
        type: "POST",
        url: "/removebook",
        data: "book_id=" + bookId
    });

    request.done(function (html) {
        panel.slideUp(500, function() { panel.remove(); });
    });

    request.fail(function (jqXHR, textStatus) {
        $('.block', panel).remove();
        alert('Failed to removed book');
    });
}

$("#searchTheBooks").submit(function (event) {
    // cancels the form submission
    event.preventDefault();
    console.log('hey');
});


$(function() {
   setupDescription();
});