
function toggleDisplayNoneBlockById(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
      x.style.display = "block";
  } else {
      x.style.display = "none";
  }
  return id;
}
function toggleNav() {
  document.getElementById("sidebar--primary").classList.toggle("left-sidebar-show");
  toggleDisplayNoneBlockById("closebtn");
}


document.addEventListener('DOMContentLoaded', function(){ 
  
  // grab the sections (targets) and menu_links (triggers)
  // for menu items to apply active link styles to
  const sections = document.querySelectorAll(".template__section");
  const menu_links = document.querySelectorAll(".template__nav-item a");
  
  // functions to add and remove the active class from links as appropriate
  const makeActive = (link) => menu_links[link].classList.add("active");
  const removeActive = (link) => menu_links[link].classList.remove("active");
  const removeAllActive = () => [...Array(sections.length).keys()].forEach((link) => removeActive(link));
  
  // change the active link a bit above the actual section
  // this way it will change as you're approaching the section rather
  // than waiting until the section has passed the top of the screen
  const sectionMargin = 200;
  
  // keep track of the currently active link
  // use this so as not to change the active link over and over
  // as the user scrolls but rather only change when it becomes
  // necessary because the user is in a new section of the page
  let currentActive = 0;

  // listen for scroll events
  window.addEventListener("scroll", () => {
    
    // check in reverse order so we find the last section
    // that's present - checking in non-reverse order would
    // report true for all sections up to and including
    // the section currently in view
    //
    // Data in play:
    // window.scrollY    - is the current vertical position of the window
    // sections          - is a list of the dom nodes of the sections of the page
    //                     [...sections] turns this into an array so we can
    //                     use array options like reverse() and findIndex()
    // section.offsetTop - is the vertical offset of the section from the top of the page
    // 
    // basically this lets us compare each section (by offsetTop) against the
    // viewport's current position (by window.scrollY) to figure out what section
    // the user is currently viewing
    const current = sections.length - [...sections].reverse().findIndex((section) => window.scrollY >= section.offsetTop - sectionMargin ) - 1

    // only if the section has changed
    // remove active class from all menu links
    // and then apply it to the link for the current section
    if (current !== currentActive) {
      removeAllActive();
      currentActive = current;
      makeActive(current);
    }
  });
}, false);



/*function toggleLight() {
  var r = document.querySelector(':root');
  r.style.setProperty('--primary-bg-color', 'white');
}*/
/*function toggleLight() {
   document.body.classList.toggle("dark-mode");
   document.h1.classList.toggle("dark-mode");
   document.p.classList.toggle("dark-mode");
   document.ul.classList.toggle("dark-mode");
}*/

//localStorage.setItem("theme", "dark");
function toggleTheme() {
  // to get user setting (can only be dark or light or null)
  // window.matchMedia("(prefers-color-scheme: dark)")
    let button = document.getElementById("light-button");
    let css = document.getElementById('css_theme');
    let css0 = grass + 'assets/css/colors_default.css';
    let css1 = grass + 'assets/css/colors_light.css';
    let css2 = grass + 'assets/css/colors_dark.css';
    let current_css = css.getAttribute("href")
         if (current_css == css0) {css.setAttribute('href', css1);localStorage.setItem("theme", "1");button.setAttribute('title','switch to dark theme')} 
    else if (current_css == css1) {css.setAttribute('href', css2);localStorage.setItem("theme", "2");button.setAttribute('title','switch to default theme')} 
    else if (current_css == css2) {css.setAttribute('href', css0);localStorage.setItem("theme", "0");button.setAttribute('title','switch to light theme')} 
    else {css.setAttribute('href', css0)}
    let button_display = button.style.display;
    button.disabled = true;
    button.style.display = "none";
    setTimeout(function() {
        button.disabled = false;
        button.style.display = button_display;
    }, 100); // 100 millisecond delay   
    
}

window.onload = function() {
  let css = document.getElementById('css_theme');
    let css0 = grass + 'assets/css/colors_default.css';
    let css1 = grass + 'assets/css/colors_light.css';
    let css2 = grass + 'assets/css/colors_dark.css';
  switch (localStorage.getItem("theme")) {
      case "0":
          css.setAttribute('href', css0)
          break;
      case "1":
          css.setAttribute('href', css1)
          break;
      case "2":
          css.setAttribute('href', css2)
          break;
   }

};