document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector(".cards");

    // Duplicate cards for seamless looping
    const cards = Array.from(track.children);
    cards.forEach(card => {
        const clone = card.cloneNode(true);
        track.appendChild(clone);
    });

    let scrollSpeed = 0.5; // px per frame
    let position = 0;

    function animate() {
        position -= scrollSpeed;

        // Reset once half the track is scrolled
        if (Math.abs(position) >= track.scrollWidth / 2) {
            position = 0;
        }

        track.style.transform = `translateX(${position}px)`;
        requestAnimationFrame(animate);
    }

    animate();
});


let paused = false;

track.addEventListener("mouseenter", () => paused = true);
track.addEventListener("mouseleave", () => paused = false);

function animate() {
    if (!paused) {
        position -= scrollSpeed;
        if (Math.abs(position) >= track.scrollWidth / 2) {
            position = 0;
        }
        track.style.transform = `translateX(${position}px)`;
    }
    requestAnimationFrame(animate);
}
