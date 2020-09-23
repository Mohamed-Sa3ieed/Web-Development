/**
 * 
 * Manipulating the DOM exercise.
 * Exercise programmatically builds navigation,
 * scrolls to anchors from navigation,
 * and highlights section in viewport upon scrolling.
 * 
 * Dependencies: None
 * 
 * JS Version: ES2015/ES6
 * 
 * JS Standard: ESlint
 * 
*/

/**
 * Define Global Variables
 * 
*/


/**
 * End Global Variables
 * Start Helper Functions
 * 
*/



/**
 * End Helper Functions
 * Begin Main Functions
 * 
*/

// build the nav with all the needed scrolling "animation has been made by "
document.addEventListener('DOMContentLoaded', function () {
    const unorderedList = document.getElementById('navbar__list');
    const listFragment = document.createDocumentFragment();
    //loop on all the sections in the document
    const sectionHeaders = document.querySelectorAll('section');
    sectionHeaders.forEach(function (section) {
        const bookmark = document.createElement('li');
        const markTitle = section.getAttribute('data-nav');
        const markref = section.id;
        bookmark.id = `${markref}-mark`;
        bookmark.innerHTML = `<a href="#${markref}" class="menu__link">${markTitle}</a>`;
        listFragment.appendChild(bookmark);
    });
    unorderedList.appendChild(listFragment);
});

// Add class 'active' to section when near top of viewport and also to the nav-bar

/* the used technique is the intersectionObserver 
because it triggers only on each intersection change instead listening for every scroll
main disadvantage is that it could lead to having too many listeners if we have too many sections
which is not the case for a normal landing page*/

/* in case of too many sections it is better to rollback to the normal scroll listener 
and get bounding rect of sections to decide which one is active*/
/* TODO: use the get bounding rect technique later because the scroll listener is added already
 to support top button functionality */

const options = {
    root: null,
    threshold: .5, //to make sure that at least 50% of the section is visible on the screen

}
const sectionsObserver = new IntersectionObserver(function (entries, observer) {
    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('your-active-class');
            const sectionMark = document.getElementById(entry.target.id + '-mark');
            sectionMark.classList.add('menu__link-active');
            // correct the relative url to match the behavior of clicking on the internal links in the nav-bar
            location.hash = '#' + entry.target.id;
        } else {
            entry.target.classList.remove('your-active-class');
            const sectionMark = document.getElementById(entry.target.id + '-mark');
            sectionMark.classList.remove('menu__link-active');
        }

    })
}, options);
const sections = document.querySelectorAll('section');
//Add intersection observation to all the elements
sections.forEach(function (section) {
    sectionsObserver.observe(section);
});



// Scroll to anchor ID using scrollTO event
/* made by adding internal links into the a ref inside the list item of the nav-bar*/


/**
 * End Main Functions
 * Begin Events
 *
*/
// Add hiding effect when the page is idle for 1 second
let hideTimedFunction;
const nav_bar = document.querySelector('nav');
nav_bar.display = 'none'; //to override the default display style
// make the top button and the nav-bar disappears after a specific idle time (without mouse movement)
let stopHideFunction = () => {
    if (typeof hideTimedFunction != 'undefined') {
        clearTimeout(hideTimedFunction);
    }
};
let hidefunction = () => {
    hideTimedFunction = setTimeout(() => {
        nav_bar.style.display = 'none';
        topButton.style.display = 'none';
    }, 1000);
};

/* after revising the requirements the hiding is related only to the mouse scrolling (mouse moving is not included)
    but it should be left as extra feature and to cover only the utilization of the scroll bar scrolling*/
document.addEventListener('mousemove', event => {
    nav_bar.style.display = 'block';
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        topButton.style.display = 'block';
    }
    stopHideFunction();
    hidefunction();
});

/* We will use this section to add scroll to top functionaluty */
const topButton = document.getElementById("topBtn");
document.addEventListener('scroll', function () {
    // measure a percentage to be skipped from the top before the top button appears
    nav_bar.style.display = 'block';
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        topButton.style.display = 'block';
    } else {
        topButton.style.display = 'none';
    }
    // to have the same idle timing out functionality when a scroll occur
    stopHideFunction();
    hidefunction();
});

// make the button clicking navigate to the beginning of the page
topButton.addEventListener('click', function () {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
});