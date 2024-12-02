document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const dateField = document.querySelector("input[name='date_time']");

    form.addEventListener("submit", function (event) {
        const currentDate = new Date();
        const enteredDate = new Date(dateField.value);

        if (enteredDate > currentDate) {
            event.preventDefault(); // Prevent form submission
            toastr.error("Future dates are not allowed!");
        }
    });
});
