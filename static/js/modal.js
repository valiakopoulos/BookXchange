$('#exampleModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data('whatever'); // Extract info from data-* attributes
    var listing_id = button.data('listing');
    var user_id = button.data('user-id');
    var title = button.data('booktitle');
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this);
    modal.find('.modal-title').text('New message to ' + recipient);
    modal.find('.modal-body input[name=listing_id]').val(listing_id);
    modal.find('.modal-body input[name=user_id]').val(user_id);
    modal.find('.book-title').text(title);
});

function sendEmail() {
    var modal = $('#exampleModal');
    var lid = modal.find('.modal-body input[name=listing_id]').val();
    var uid = modal.find('.modal-body input[name=user_id]').val();
    var message = modal.find('.modal-body textarea').val();
    var request = $.ajax({
        type: "POST",
        url: "/sendemail",
        data: { 'listing_id': lid, 'user_id': uid, 'message': message }
    });

    request.done(function () {
        $('#exampleModal').modal('hide');
    });
    request.fail(function () {
        $('#exampleModal').modal('hide');
    });
}
