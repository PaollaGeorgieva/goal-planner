document.addEventListener("DOMContentLoaded", function () {
    const habitFields = document.getElementById("habit-fields");
    const targetFields = document.getElementById("target-fields");
    const typeRadios = document.querySelectorAll('input[name="goal_type"]');
    const currentGoalType = document.getElementById("current_goal_type");
    const endDateInput = document.getElementById("id_end_date");

    function toggleFields() {
        let selectedType;


        if (currentGoalType) {

            selectedType = currentGoalType.value;
        } else {

            selectedType = document.querySelector('input[name="goal_type"]:checked')?.value || 'target';
        }

        if (endDateInput) {
            endDateInput.disabled = selectedType === "habit";
        }

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


    toggleFields();
});