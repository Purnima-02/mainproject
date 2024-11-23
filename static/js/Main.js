
document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.Psection2 .nav-item');
    const sections = document.querySelectorAll('section');
    const offset = 50; 

    window.addEventListener('scroll', () => {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - offset) {
                current = section.getAttribute('id');
            }
        });

        navItems.forEach(navItem => {
            navItem.classList.remove('active');
            if (navItem.getAttribute('data-section') === current) {
                navItem.classList.add('active');
            }
        });
   

    


    navItems.forEach(navItem => {
        navItem.addEventListener('click', (event) => {
            event.preventDefault();
            const sectionId = navItem.getAttribute('data-section');
            document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
        });
    });


});


var mainNavBar=document.querySelector('.navbar-section nav');

var subNAvBAr=document.querySelector('.Psection2 nav');
console.log("Main.js");

window.onscroll=()=>{

    //Arrow Mark
    console.log(window.scrollY);
    console.log(window.innerWidth);
    if(window.scrollY >= 300){
        // console.log(window.scrollY)
        document.querySelector('.scroll-to-top').style.display="block";
    }
    else{
        document.querySelector('.scroll-to-top').style.display="none";

    }  

     //Arrow Mark



     const mainNv=mainNavBar.getBoundingClientRect().bottom;
     console.log(mainNv +"mainNv Bottom");
     const subnv=subNAvBAr.getBoundingClientRect().top;

     console.log(subnv + "subnv Top");
     const diff=subnv-mainNv;
     console.log(diff + "difference");

     if(diff<300){
        mainNavBar.style.opacity=0;
     }
     else{
        mainNavBar.style.opacity=1;
     }



   
    
}


document.querySelector('.scroll-to-top').addEventListener('click',function(){

    window.scrollTo({top:0,behavior:"smooth"});
})


// const navLiItem = document.querySelectorAll('.navbar-section .navbar-nav .nav-item');

// navLiItem.forEach(item => {
//     item.addEventListener('click', function () {
      
//         navLiItem.forEach(nav => nav.classList.remove('active'));
       
//         this.classList.add('active');
//     });
// });







});

// document.addEventListener('DOMContentLoaded', function() {
//     var carLoanDropdown = document.getElementById('carLoanDropdown');
//     var carLoanSubmenu = carLoanDropdown.nextElementSibling;

//     carLoanDropdown.addEventListener('click', function(event) {
//         if (window.innerWidth <= 992) { // Adjust this value based on your mobile breakpoint
//             event.preventDefault(); // Prevent the default link behavior
//             carLoanSubmenu.classList.toggle('show'); // Toggle the submenu visibility
//         }
//     });
// });

