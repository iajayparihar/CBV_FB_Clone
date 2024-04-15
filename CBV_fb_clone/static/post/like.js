// unlike function
function submitUnLike(post_id){
    $.ajax({
        url: '/post/post/unlike/'+ post_id +'/',
        type: 'GET',
        data: {
        },
        success : function(response){
            if (response.success){
                location.reload();
            }
        } //success close
    })//ajax close
}// submimtLike close



//like function
function submitLike(post_id) {
    $.ajax({
        url: '/post/post/like/' + post_id + '/',
        type: 'GET',
        data: {
            
        },
        success: function(response) {
            if (response.success) {
                location.reload(); // Reload the page if liking is successful
            } else {
                console.error('Like operation failed:', response.message); // Log error if liking fails
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX request failed:', status, error); // Log error if AJAX request fails
        }
    });
}