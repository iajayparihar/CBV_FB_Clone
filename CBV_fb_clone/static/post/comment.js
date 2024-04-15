
function openModal(id) {
    let modal = document.getElementById("myModal" + id);
    modal.style.display = "block";
}

function closeModal(id) {
    let modal = document.getElementById("myModal" + id);
    modal.style.display = "none";
}

function submitComment(post_id) {
    let commentText = $('#comment' + post_id).val(); // post_id is string ==> `$('#comment1')`
    $.ajax({
        url: '/post/post/comment/' + post_id + '/',
        type: 'POST',
        data: {
            'comment': commentText,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // CSRF token from form
        },
        success: function(response) {
            console.log(response);
            if (response.success) {
                closeModal(post_id); // closing the comment modal
                location.reload(); // reload the page
            } else {
                alert('Error adding comment: ' + response.message);
            }
        },
    });
}
