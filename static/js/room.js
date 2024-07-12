let ws;
$(document).ready(function () {
    $('.room-link').click(function (event) {
        event.preventDefault();
        let roomId = $(this).data('room-id');
        $.ajax({
            url: roomId,
            method: 'GET',
            success: function (data) {
                $('#chat-container').html(data)
            },
            error: function (xhr) {
                if (xhr.status === 403) {
                    alert('error')
                }
            }
        })
    })
})