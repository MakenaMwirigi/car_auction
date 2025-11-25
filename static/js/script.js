document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".car-card");

    cards.forEach(card => {
        const carId = card.dataset.carId;
        const endTime = new Date(card.dataset.endTime).getTime();
        const timerEl = card.querySelector(`#timer-${carId}`);

        // Countdown Timer
        const timerInterval = setInterval(() => {
            const now = new Date().getTime();
            const distance = endTime - now;

            if (distance <= 0) {
                clearInterval(timerInterval);
                timerEl.innerHTML = "Bidding Closed";
                card.querySelector("form").style.display = "none";
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            timerEl.innerHTML = `Time left: ${days}d ${hours}h ${minutes}m ${seconds}s`;
        }, 1000);

        // Fetch current bids
        const updateBids = () => {
            fetch(`/bids/${carId}`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById(`bidders-${carId}`).textContent = data.num_bidders;
                    document.getElementById(`highest-${carId}`).textContent = data.highest_bid.toLocaleString();
                });
        };
        updateBids();
        setInterval(updateBids, 5000);

        // Submit bid form
        const form = card.querySelector(".bid-form");
        form.addEventListener("submit", e => {
            e.preventDefault();
            const formData = new FormData(form);
            fetch("/bid", { method: "POST", body: formData })
                .then(res => res.json())
                .then(data => {
                    const msg = card.querySelector(".message");
                    if (data.error) {
                        msg.textContent = data.error;
                        msg.style.color = "red";
                    } else {
                        msg.textContent = "Bid placed successfully!";
                        msg.style.color = "green";
                        form.reset();
                        updateBids();
                    }
                });
        });
    });
});
