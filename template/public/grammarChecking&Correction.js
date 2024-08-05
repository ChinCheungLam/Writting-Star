document.getElementById('check-grammar-button').addEventListener('click', function() {
    const textInput = document.getElementById('text-input').value;
    const correctionContent = document.getElementById('correction-content');

    console.log('Text input:', textInput); // Log the input text

    fetch('/correct-grammar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ paragraph: textInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response data:', data); // Log the response data
        if (data.correction) {
            correctionContent.innerHTML = `<p>${data.correction}</p>`;
        } else {
            correctionContent.innerHTML = '<p>Error in grammar correction.</p>';
        }
    })
    .catch(error => {
        correctionContent.innerHTML = '<p>Error in grammar correction.</p>';
        console.error('Error:', error);
    });
});
