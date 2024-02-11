document.addEventListener('DOMContentLoaded', () => {
    const inputArea = document.querySelector('#inputArea');
    const submitButton = document.querySelector('#submitButton');

    submitButton.addEventListener('click', () => {
        const text = inputArea.value;

        if (text.trim() !== '') {
            sendDataToBackend(text);
        }
    });
});

async function sendDataToBackend(text) {
    try {
        const response = await fetch('/save_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text
            })
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data.message);
        } else {
            console.error('Error sending data to backend');
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}
