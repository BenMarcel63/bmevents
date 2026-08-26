/* =========================================
   BM EVENTS
   Main JavaScript
======================================== */


// ================================
// MOBILE NAVIGATION TOGGLE
// ================================


const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

if(menuToggle){

    menuToggle.addEventListener("click",()=>{

        const isOpen = navLinks.classList.toggle("active");
        menuToggle.setAttribute("aria-expanded", String(isOpen));

    });

}



// ================================
// CLOSE MENU AFTER CLICK
// ================================


const navItems = document.querySelectorAll(".nav-links a");


navItems.forEach(item => {


    item.addEventListener("click", () => {


        if (navLinks) navLinks.classList.remove("active");
        if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");


    });


});


// ================================
// NAVBAR SCROLL EFFECT
// ================================


const navbar = document.querySelector(".navbar");


window.addEventListener("scroll", () => {


    if(navbar && window.scrollY > 50){


        navbar.style.background =
        "rgba(15,23,42,0.92)";


        navbar.style.padding =
        "18px 40px";


    }

    else if(navbar){


        navbar.style.background =
        "rgba(15,23,42,0.45)";


        navbar.style.padding =
        "25px 40px";


    }


});

// ================================
// SCROLL REVEAL ANIMATION
// ================================


const revealElements = document.querySelectorAll(
    ".service-card, .stat-card, .vendor-card, .testimonial-card, .about-content, .gallery-grid img"
);


const revealOnScroll = () => {


    revealElements.forEach(element => {


        const position = element.getBoundingClientRect().top;


        const screenHeight = window.innerHeight;



        if(position < screenHeight - 100){


            element.classList.add("show");


        }


    });


};

window.addEventListener(
    "scroll",
    revealOnScroll
);


revealOnScroll();

// FAQ

const faqItems=document.querySelectorAll(".faq-item");

faqItems.forEach(item=>{

const btn=item.querySelector(".faq-question");

if (btn) btn.addEventListener("click",()=>{

item.classList.toggle("active");

});

});

const topBtn = document.getElementById("topBtn");

if(topBtn){

window.addEventListener("scroll",()=>{

    if(window.scrollY > 500){

        topBtn.style.display="block";

    }else{

        topBtn.style.display="none";

    }

});

topBtn.onclick=()=>{

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

};

}

window.addEventListener("load",()=>{

const loader = document.getElementById("loader");

if(loader){

    loader.style.display="none";

}

});

// Favorite Vendor

const favoriteBtn = document.querySelector(".favorite-btn");

if(favoriteBtn){

    favoriteBtn.addEventListener("click",()=>{

        favoriteBtn.innerHTML="❤ Saved";

        favoriteBtn.style.background="#D4AF37";

        favoriteBtn.style.color="#111";

    });
}
// ================================
// LOGOUT BUTTON
// ================================

const logoutBtn = document.getElementById("logoutBtn");


if(logoutBtn){

    logoutBtn.addEventListener("click", function(){

        localStorage.removeItem("vendorLoggedIn");

        window.location.href = "vendor-login.html";

    });

}