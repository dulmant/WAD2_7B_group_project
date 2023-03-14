function deleteQuiz(slug, token) {
    console.log(slug);
    console.log(token);
    if (confirm("Are you sure you want to delete this quiz? \nThis action cannot be undone.")) {
        $.ajax({
            url: '/quizapp/ajax/delete_quiz/' + slug + '/',
            type: 'DELETE',
            headers: {
                'X-CSRFToken': token
            },
            success: function(response) {
                // handle success
                alert("Quiz deleted successfully!");
                // reload the page or update the quiz list
            },
            error: function(xhr, status, error) {
                // handle error
                alert("An error occurred while deleting the quiz.");
            }
        });
    }
}
