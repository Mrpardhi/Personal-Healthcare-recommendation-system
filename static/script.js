// Wait for the DOM to fully load before running scripts
document.addEventListener("DOMContentLoaded", function() {

    // Get the form and add a submit event listener
    const form = document.querySelector("form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();  // Prevent the form from submitting the default way

        // Get form values
        const age = document.getElementById("age").value;
        const gender = document.getElementById("gender").value;
        const hemoglobin = document.getElementById("hemoglobin").value;
        const wbc = document.getElementById("wbc").value;
        const rbc = document.getElementById("rbc").value;
        const bloodSugar = document.getElementById("blood_sugar").value;

        // Basic validation: check if all fields are filled in
        if (age && gender && hemoglobin && wbc && rbc && bloodSugar) {
            // You can submit the form using JavaScript if needed
            form.submit();

            // Simulate form submission and show a message
            showSuccessMessage("Form submitted successfully!");
        } else {
            showErrorMessage("Please fill in all the required fields.");
        }
    });

    // Function to show success messages
    function showSuccessMessage(message) {
        const successMessage = document.createElement("div");
        successMessage.className = "alert success";
        successMessage.innerText = message;
        document.body.prepend(successMessage);

        // Auto-hide the success message after 3 seconds
        setTimeout(function() {
            successMessage.remove();
        }, 3000);
    }

    // Function to show error messages
    function showErrorMessage(message) {
        const errorMessage = document.createElement("div");
        errorMessage.className = "alert error";
        errorMessage.innerText = message;
        document.body.prepend(errorMessage);

        // Auto-hide the error message after 3 seconds
        setTimeout(function() {
            errorMessage.remove();
        }, 3000);
    }
});
