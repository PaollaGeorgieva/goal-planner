document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".progress-section");

  cards.forEach((card) => {
    const percentageText = card.querySelector(".percentage");
    const path = card.querySelector("#progress-path");
    const dot = card.querySelector(".progress-dot");

    const goalType     = card.dataset.goalType;
    const total        = parseInt(card.dataset.target, 10);
    const current      = parseInt(card.dataset.current, 10);
    const isCompleted  = card.dataset.isCompleted === 'true';

    let percent = 0;

    if ((goalType === "target" || goalType === "habit") && isCompleted) {
      percent = 100;
    } else {
      if (total > 0) {
        percent = Math.min((current / total) * 100, 100);
      }
    }




    const radius       = 70;
    const cx           = 80;
    const cy           = 80;
    const angle        = (percent / 100) * 360;
    const radians      = ((angle - 90) * Math.PI) / 180;
    const x            = cx + radius * Math.cos(radians);
    const y            = cy + radius * Math.sin(radians);
    const largeArcFlag = percent > 50 ? 1 : 0;
    const d            = `M${cx},${cy - radius} A${radius},${radius} 0 ${largeArcFlag},1 ${x},${y}`;

    path.setAttribute("d", d);
    if (dot) dot.setAttribute("cx", x), dot.setAttribute("cy", y);
    if (percentageText) percentageText.innerHTML = `${Math.round(percent)}<span>%</span>`;
  });
});
