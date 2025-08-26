// JavaScript for Travel Booking System

document.addEventListener("DOMContentLoaded", function () {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML =
                    '<span class="loading-spinner"></span> Processing...';
            }
        });
    });

    // Price calculation for booking form
    const calculateTotalPrice = () => {
        const pricePerSeat = parseFloat(
            document.getElementById("price-per-seat")?.value || 0
        );
        const seatsInput = document.getElementById("id_number_of_seats");
        const totalPriceElement = document.getElementById("total-price");

        if (seatsInput && totalPriceElement) {
            const seats = parseInt(seatsInput.value) || 0;
            const total = seats * pricePerSeat;
            totalPriceElement.textContent = `$${total.toFixed(2)}`;
        }
    };

    // Attach event listeners
    const seatsInput = document.getElementById("id_number_of_seats");
    if (seatsInput) {
        seatsInput.addEventListener("input", calculateTotalPrice);
        calculateTotalPrice(); // Initial calculation
    }

    // Search filter enhancements
    const searchForm = document.querySelector('form[method="get"]');
    if (searchForm) {
        const inputs = searchForm.querySelectorAll("input, select");
        inputs.forEach((input) => {
            input.addEventListener("change", function () {
                searchForm.submit();
            });
        });
    }
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(amount);
}

function showToast(message, type = "success") {
    // Simple toast notification implementation
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    new bootstrap.Toast(toast).show();
}
