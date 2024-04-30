
function updateOpenModal(id) {
    let modal = document.getElementById("updateMyModal" + id);
    modal.style.display = "block";
}

function updateCloseModal(id) {
    let modal = document.getElementById("updateMyModal" + id);
    modal.style.display = "none";
}

function updateComment(postId) {
    let comment = $('#updateComment' + postId).val();
    let commentId = $('#commentId' + postId).text();
    $.ajax({
        type: 'POST',
        url: '/update_comment/',
        data: {
            "cmt_id": commentId,
            'comment': comment,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            console.log(response);
            if (response.success) {
                closeModal(postId); // closing the comment modal
                location.reload(); // reload the page
            } else {
                alert('Error adding comment: ' + response.message);
            }
        },
    });
}

function deleteCmt(cmt_id){
    $.ajax({
        type: 'POST',
        url: '/delete_comment/',
        data: {
            "cmt_id": cmt_id,
        },
        success: function(response) {
            if (response.success) {
                location.reload(); // reload the page
            } else {
                alert('Error adding comment: ');
            }
        },
    });
    
}