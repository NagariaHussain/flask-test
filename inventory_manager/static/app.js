// Automatically highlight the active
// navigation link
const navLinks = Array.from(document.querySelectorAll("nav a"));

// Iterate over all the navigation links
for (let link of navLinks) {
    // If the link points to current page
    if (link.href === location.href) {
        // Highlight the link using `active-link` class
        link.setAttribute('aria-current', 'page');
        // Make the link point to current page
        link.href = "#";
    }
}