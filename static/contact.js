document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting traditionally

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    // Send form data to the backend
    fetch("/submit_contact", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name, email: email, message: message }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").style.display = "block";
        document.getElementById("response").innerText = data.message;
        document.getElementById("contactForm").reset(); // Reset form after submission
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
