(() => {
    const form = document.querySelector("[data-seat-map-form]");
    if (!form) {
        return;
    }

    const summary = form.querySelector("[data-seat-summary]");
    const emptyState = summary.querySelector("[data-summary-empty]");
    const details = summary.querySelector("[data-summary-details]");
    const outputs = {
        seat: summary.querySelector("[data-summary-seat]"),
        cabinClass: summary.querySelector("[data-summary-class]"),
        seatType: summary.querySelector("[data-summary-type]"),
        baseFare: summary.querySelector("[data-summary-base]"),
        estimatedFee: summary.querySelector("[data-summary-fee]"),
        estimatedTotal: summary.querySelector("[data-summary-total]"),
    };

    function updateSummary(input) {
        if (!input) {
            emptyState.hidden = false;
            details.hidden = true;
            return;
        }

        outputs.seat.textContent = input.dataset.seatNumber;
        outputs.cabinClass.textContent = input.dataset.cabinClass;
        outputs.seatType.textContent = input.dataset.seatType;
        outputs.baseFare.textContent = input.dataset.baseFare;
        outputs.estimatedFee.textContent = input.dataset.estimatedFee;
        outputs.estimatedTotal.textContent = input.dataset.estimatedTotal;
        emptyState.hidden = true;
        details.hidden = false;
    }

    form.addEventListener("change", (event) => {
        if (event.target.matches('input[name="seat"]')) {
            updateSummary(event.target);
        }
    });

    updateSummary(form.querySelector('input[name="seat"]:checked'));
})();
