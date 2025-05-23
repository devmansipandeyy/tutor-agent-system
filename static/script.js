// Dark Mode Toggle
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    themeToggle.textContent = body.classList.contains('dark-mode') ? '☀️' : '🌙';
});

// Form Submission with AJAX
const form = document.getElementById('query-form');
const responseSection = document.getElementById('response-section');
const responseText = document.getElementById('response-text');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const queryInput = document.getElementById('query-input').value;

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: queryInput }),
        });
        const data = await response.json();

        if (data.response) {
            responseText.textContent = data.response;
            responseSection.classList.remove('hidden');
            responseSection.style.opacity = '0';
            setTimeout(() => {
                responseSection.style.transition = 'opacity 0.5s ease-in';
                responseSection.style.opacity = '1';
            }, 50);
        } else {
            responseText.textContent = 'Error: ' + data.error;
            responseSection.classList.remove('hidden');
        }
    } catch (error) {
        responseText.textContent = 'Error: Unable to fetch response';
        responseSection.classList.remove('hidden');
    }
});