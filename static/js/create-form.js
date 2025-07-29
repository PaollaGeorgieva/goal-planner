
document.addEventListener("DOMContentLoaded", function () {
    const habitFields = document.getElementById("habit-fields");
    const targetFields = document.getElementById("target-fields");
    const typeRadios = document.querySelectorAll('input[name="goal_type"]');

    function toggleFields() {
    const selectedType = document.querySelector('input[name="goal_type"]:checked').value;
    if (selectedType === "habit") {
        habitFields.classList.remove("hidden");
        targetFields.classList.add("hidden");
    } else {
        targetFields.classList.remove("hidden");
        habitFields.classList.add("hidden");
    }
    }

    typeRadios.forEach(radio => {
    radio.addEventListener("change", toggleFields);
    });

    toggleFields(); // On load
});
