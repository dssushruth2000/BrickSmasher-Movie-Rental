async function createAccount() {
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const email = document.getElementById("email").value;

    const response = await fetch(accountCreationURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ first_name: firstName, last_name: lastName, email: email })
    });

    const result = await response.json();
    document.getElementById("message").innerText = result.message || result.error;
}
