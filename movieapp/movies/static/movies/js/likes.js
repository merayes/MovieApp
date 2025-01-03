function initializeLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const commentId = this.dataset.commentId;
            const csrfToken = this.dataset.csrf;
            
            try {
                const response = await fetch(`/comments/${commentId}/toggle-like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin'
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                if (data.success) {
                    // Update button text and like count
                    const likeText = data.liked ? 'Unlike ' : 'Like ';
                    const countSpan = document.createElement('span');
                    countSpan.className = 'like-count';
                    countSpan.textContent = data.like_count;
                    
                    this.textContent = likeText;
                    this.appendChild(countSpan);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while processing your request.');
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', initializeLikeButtons);