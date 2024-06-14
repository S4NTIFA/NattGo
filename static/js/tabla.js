document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll('.table tbody tr');
    rows.forEach(row => {
        const cantidadEntregada = parseInt(row.children[4].textContent);
        if (cantidadEntregada < 10) {
            row.style.borderBottomColor = 'red';
        } else {
            row.style.borderBottomColor = 'green';
        }
    });
});
