$(document).ready(function () {
    $(".like-form").submit(function (event) {
        event.preventDefault();
        var form = $(this);
        var post_id = form.data('post-id');
        var likeButton = form.find('.like-btn');

        console.log('Submitting like form for post ID:', post_id);

        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            dataType: "json",
            data: form.serialize(),
            success: function (data) {
                console.log('Success! Received data:', data);

                // Actualiza el número de likes en la interfaz
                $("#likes-count-" + post_id).text(data.likes_count);

                // Cambia el color del botón
                if (likeButton.hasClass('liked')) {
                    likeButton.removeClass('liked');
                    console.log('Removing liked class');
                } else {
                    likeButton.addClass('liked');
                    console.log('Adding liked class');
                }
            },
            error: function (error) {
                console.error('Error during AJAX request:', error);
            }
        });
    });
});
