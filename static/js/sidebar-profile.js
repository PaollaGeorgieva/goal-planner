
const calendarScript = document.getElementById("calendar-data");
const calendarMap = calendarScript
  ? JSON.parse(calendarScript.textContent)
  : {};


document.querySelectorAll('.sidebar-nav .nav-item:not(.logout)').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();

    document.querySelectorAll('.sidebar-nav .nav-item').forEach(a => a.classList.remove('active'));
    document.querySelectorAll('.content .panel').forEach(p => p.classList.remove('active'));

    link.classList.add('active');
    document.getElementById(link.dataset.target).classList.add('active');
  });
});


function pad(n) {
  return String(n).padStart(2, '0');
}


function generateCalendar(year, month) {
  const calendarGrid = document.getElementById("calendar-grid");
  calendarGrid.innerHTML = "";

  const start = new Date(year, month, 1);
  const end   = new Date(year, month + 1, 0);
  const offset = (start.getDay() + 6) % 7;
  const totalDays = end.getDate();


  for (let i = 0; i < offset; i++) {
    const empty = document.createElement("div");
    empty.classList.add("calendar-day", "empty");
    calendarGrid.appendChild(empty);
  }


  for (let d = 1; d <= totalDays; d++) {
    const cell = document.createElement("div");
    cell.classList.add("calendar-day");
    cell.textContent = d;


    const iso = `${year}-${pad(month + 1)}-${pad(d)}`;


    const statuses = calendarMap[iso] || [];

    if (statuses.includes("completed") && statuses.includes("checked-in")) {
      cell.classList.add("both");
    } else if (statuses.includes("completed")) {
      cell.classList.add("completed");
    } else if (statuses.includes("checked-in")) {
      cell.classList.add("checked-in");
    }

    calendarGrid.appendChild(cell);
  }
}


const today = new Date();
generateCalendar(today.getFullYear(), today.getMonth());

