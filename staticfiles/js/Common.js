
window.addEventListener('DOMContentLoaded',()=>{


    const pathname = window.location.pathname;

    
    
    
   const res=pathname.split('/').pop();
    // console.log(res); 
    console.log("Hiiiiiiiisssi");
   console.log(pathname);
   const listitems=document.querySelectorAll('.nav-item.dropdown .dropdown-menu .dropdown-item')


if(pathname==="/about/"){
    document.querySelector('.Aboutus').classList.add('myactive');
}
else if(pathname==="/creditpage/"){
    document.querySelector('.credit-cards').classList.add('myactive');

}
else if(pathname==="/allinsurance/" || pathname==="/lifeinsurance/" || pathname==="/generalinsurance/" || pathname==="/healthinsurance/" ){

    document.querySelector('.insurance').classList.add('myactive');
    listitems.forEach(items=>{
        // console.log(items.getAttribute('href'));
        if(items.getAttribute('href')===pathname){
            items.classList.add('custom-background');

        }
    })

   



}
else if(pathname==="/contact/"){
    document.querySelector('.contactus').classList.add('myactive');
}

else if(pathname==="/dsa/" || pathname==="/franchise/"){
    console.log("working dsa")
    document.querySelector('.partner').classList.add('myactive');
    listitems.forEach(items=>{
        // console.log(items.getAttribute('href'));
        if(items.getAttribute('href')===pathname){
            items.classList.add('custom-background');

        }
    })
}

else if(pathname==="/personalloans/" || pathname==="/educationalloan/" || pathname==="/homeloan/" || pathname==="/gold/" || pathname==="/loanagainstproperty/" ||pathname==="/bussinessLoan/" || pathname==="/carloan/" || pathname==="/usedcarloan/" || pathname==="/newcarloan/"){

    console.log("working lap1")
    document.querySelector('.loans').classList.add('myactive');
    console.log("working lap2")
    // console.log(res);

    
    // console.log(listitems);

    const hrefValues = Array.from(listitems).map(item => item.getAttribute('href'));

    // console.log(hrefValues);

    listitems.forEach(items=>{
       
        // console.log(items.getAttribute('href'));
        if(items.getAttribute('href')===pathname){
            console.log("UIUIUIUI");
            console.log(items.getAttribute('href'));
            items.classList.add('custom-background');

        }
    })

}

else{
    console.log("No name");
}

});