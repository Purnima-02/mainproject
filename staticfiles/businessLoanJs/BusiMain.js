document.addEventListener('DOMContentLoaded', function () {
    const hasGstCertificateField = document.querySelector('#id_has_gst_certificate');
   
    const maxnumberlength10 = document.querySelectorAll('#id_mobile_number, #id_net_income_per_month,#id_running_emis_amount_per_month,#id_turnover_in_lakhs_per_year,#id_ref_2_person_mobile_number,#id_ref_1_person_mobile_number,#id_required_loan_amount,#id_business_address_pincode,#id_current_address_pincode,#id_aadhar_pincode');
    const panField = document.getElementById('id_pan_card_number');
    const panError = document.getElementById('pan-error');
    const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;

    
    console.log('im hiss9992');

    const toggleGstNumberField = () => {
        if (hasGstCertificateField.value === 'Y') {
            console.log("jiii");
            document.getElementById('div_id_gst_number').style.display = "block";
            document.getElementById('id_gst_number').required = true;
            console.log(document.getElementById('id_gst_number').hasAttribute('required'));
        } else {
            document.getElementById('div_id_gst_number').style.display = "none";
            document.getElementById('id_gst_number').required = false;
            console.log(document.getElementById('id_gst_number').hasAttribute('required'));
        }
    };

    const panCardValidation = () => {
        if (panPattern.test(panField.value)) {
            panError.innerText = '';
        } else {
            panError.innerText = 'Invalid PAN card number';
            panError.style.color = 'red';
        }
    };

    // Only characters in input
    document.querySelectorAll('#id_first_name,#id_last_name,#id_father_name,#id_mother_name').forEach((s) => {
        console.log('firstname');
        s.addEventListener('input', function (e) {
            var value = e.target.value;
            e.target.value = value.replace(/[^A-Za-z]/g, '');
        });
    });

    panField.addEventListener('change', panCardValidation);
    hasGstCertificateField.addEventListener('change', toggleGstNumberField);
    maxnumberlength10.forEach((element) => {
        element.addEventListener('input', (e) => {
            const maxLength = 10;
            const input = e.target;
            console.log(e.target.id);
            if (input.value.length > maxLength) {
                input.value = input.value.slice(0, maxLength);
            }
        });
    });

    // Add the Aadhar length validation correctly
    document.querySelectorAll('#id_aadhar_card_number').forEach((element) => {
        element.addEventListener('input', (e) => {
            const maxLength = 12;
            const input = e.target;
            if (input.value.length > maxLength) {
                input.value = input.value.slice(0, maxLength);
            }
        });
    });

    // Initial check
    toggleGstNumberField();

    document.querySelectorAll('#id_mobile_number,#id_aadhar_card_number,#id_current_address_pincode,#id_aadhar_pincode,#id_running_emis_amount_per_month,#id_net_income_per_month,#id_gst_number,#id_turnover_in_lakhs_per_year,#id_business_address_pincode,#id_required_loan_amount,#id_ref_1_person_mobile_number,#id_ref_2_person_mobile_number').forEach((numbers) => {
        numbers.addEventListener('input', (e) => {
            if (e.target.value <= 0) {
                e.target.value = '';
            }
        });
    });


    document.getElementById('id_date_of_birth').addEventListener('change',(e)=>{
        const datevalue=e.target.value;
        const dateparts=datevalue.split('-');
        const year=dateparts[0];
  
        if(year.length > 4 ){
          dateparts[0]=year.slice(0,4);
          e.target.value=dateparts.join('-');
          
        }
        console.log("hi");
        const currentYear=new Date().getFullYear();
        if(year > currentYear){
          dateparts[0]=currentYear;
          e.target.value=dateparts.join('-');
         
  
        }
        console.log( e.target.value);
  
      });


      // Only characters in input
 document.querySelectorAll('#id_ref1name,#id_ref2name').forEach((item)=>{


    item.addEventListener('input', function (e) {
        var value = e.target.value;
        e.target.value = value.replace(/[^A-Za-z]/g, '');
      });

 });
   // Only characters in input



   document.querySelectorAll('#id_mobile_number,#id_ref1mobilenumber,#id_ref2mobilenumber').forEach((ele)=>{

    ele.addEventListener('input',(e)=>{

        const maxLength = 10;
    const input = e.target;
    console.log(e.target.id);
    if (input.value.length > maxLength) {
        input.value = input.value.slice(0, maxLength);
    }
    if(input.value<0){
        input.value='';
    }
    });

});
    
});
// =================================================================================================







 


// Scores Length
// document.querySelectorAll('#id_TOEFL_score,#id_GRE_score,#id_IELTS_score,#id_Duolingo_score,#id_PTE_score').forEach((id) => {


//     id.addEventListener('input', (e) => {

//         console.log(e.target.id);
//         const maxLEngth = 5;
//         const input = e.target;
//         if (input.value.length > maxLEngth) {
//             input.value = input.value.slice(0, maxLEngth);
//         }

//         if(input.value < 0){
//             input.value='';
//         }

//     });



// });
// Scores Length


// cibilScore Length

// document.querySelector('#id_cibil_score').addEventListener('input', (e) => {

//     const maxLEngth = 3;
//     const input = e.target;
//     if (input.value.length > maxLEngth) {
//         input.value = input.value.slice(0, maxLEngth);
//     }
//     if(input.value<0){
//         input.value='';
//     }

// });
// cibilScore Length

//  salaried CibilScore
// document.querySelector('#id_co_applicant_salaried_cibil_score').addEventListener('input', (e) => {

//     const maxLEngth = 3;
//     const input = e.target;
//     if (input.value.length > maxLEngth) {
//         input.value = input.value.slice(0, maxLEngth);
//     }
//     if(input.value<0){
//         input.value='';
//     }

    

// });
//  salaried CibilScore


// backlogs
// document.querySelector('#id_backlogs').addEventListener('input', (e) => {

//     const maxLEngth = 2;
//     const input = e.target;
//     if (input.value.length > maxLEngth) {
//         input.value = input.value.slice(0, maxLEngth);
//     }
//     if(input.value<0){
//         input.value='';
//     }

    

// });




// document.querySelectorAll('#id_loan_required,#id_co_applicant_salaried_net_pay,#id_co_applicant_salaried_emis,#id_co_pplicant_self_employed_itr_amount,#id_property_market_value,#id_property_govt_value').forEach((id) => {

    
//     id.addEventListener('input', (e) => {

//         console.log("loans")
       
//         console.log(e.target.id);
       
//         const maxLEngth = 10;
//         const input = e.target;
//         if (input.value.length > maxLEngth) {
//             input.value = input.value.slice(0, maxLEngth);
//         }
//         if(input.value < 0){
//             input.value='';
//         }
        

//     });

    

// });

// document.querySelectorAll('#id_co_applicant_self_employed_business_licence,#id_score_card').forEach((item)=>{


//     item.addEventListener('input',(e)=>{


//         const file = e.target.files[0];
    
//         if(file){
    
    
//             if(!file.name.endsWith('.pdf')){
//                 alert("only PDF Files are allowed..");
//                 e.target.value='';
//             }
//         }
        
//     });


// });



// // ==================================================================

// document.addEventListener('DOMContentLoaded', function () {
//     const hasGstCertificateField = document.querySelector('#id_has_gst_certificate');
   
//     const maxnumberlength10 = document.querySelectorAll('#id_mobile_number, #id_net_income_per_month,#id_running_emis_amount_per_month,#id_turnover_in_lakhs_per_year,#id_ref_2_person_mobile_number,#id_ref_1_person_mobile_number,#id_required_loan_amount,#id_business_address_pincode,#id_current_address_pincode,#id_aadhar_pincode');
//     const panField = document.getElementById('id_pan_card_number');
//     const panError = document.getElementById('pan-error');
//     const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;

//     console.log('im hiuuuu');

//     const toggleGstNumberField = () => {
//         if (hasGstCertificateField.value === 'Y') {
//             console.log("jiii");
//             document.getElementById('div_id_gst_number').style.display = "block";
//             document.getElementById('id_gst_number').required = true;
//             console.log(document.getElementById('id_gst_number').hasAttribute('required'));
//         } else {
//             document.getElementById('div_id_gst_number').style.display = "none";
//             document.getElementById('id_gst_number').required = false;
//             console.log(document.getElementById('id_gst_number').hasAttribute('required'));
//         }
//     };

//     const panCardValidation = () => {
//         if (panPattern.test(panField.value)) {
//             panError.innerText = '';
//         } else {
//             panError.innerText = 'Invalid PAN card number';
//             panError.style.color = 'red';
//         }
//     };

//     // Only characters in input
//     document.querySelectorAll('#id_first_name,#id_last_name,#id_father_name,#id_mother_name,#id_ref_1_person_name,#id_ref_2_person_name').forEach((s) => {
//         console.log('firstname');
//         s.addEventListener('input', function (e) {
//             var value = e.target.value;
//             e.target.value = value.replace(/[^A-Za-z]/g, '');
//         });
//     });

//     panField.addEventListener('change', panCardValidation);
//     hasGstCertificateField.addEventListener('change', toggleGstNumberField);
//     maxnumberlength10.forEach((element) => {
//         element.addEventListener('input', (e) => {
//             const maxLength = 10;
//             const input = e.target;
//             console.log(e.target.id);
//             if (input.value.length > maxLength) {
//                 input.value = input.value.slice(0, maxLength);
//             }
//         });
//     });

//     // Add the Aadhar length validation correctly
//     document.querySelectorAll('#id_aadhar_card_number').forEach((element) => {
//         element.addEventListener('input', (e) => {
//             const maxLength = 12;
//             const input = e.target;
//             if (input.value.length > maxLength) {
//                 input.value = input.value.slice(0, maxLength);
//             }
//         });
//     });

//     // Initial check
//     toggleGstNumberField();

//     document.querySelectorAll('#id_mobile_number,#id_aadhar_card_number,#id_current_address_pincode,#id_aadhar_pincode,#id_running_emis_amount_per_month,#id_net_income_per_month,#id_gst_number,#id_turnover_in_lakhs_per_year,#id_business_address_pincode,#id_required_loan_amount,#id_ref_1_person_mobile_number,#id_ref_2_person_mobile_number').forEach((numbers) => {
//         numbers.addEventListener('input', (e) => {
//             if (e.target.value <= 0) {
//                 e.target.value = '';
//             }
//         });
//     });


//     document.querySelectorAll('#id_date_of_birth,#id_business_establishment_date').forEach((item)=>{

//         const today = new Date();
//         const currentYear = today.getFullYear();
//         item.max = `${currentYear}-12-31`;


//         item.addEventListener('change',(e)=>{
//             console.log("date");
//             const datevalue=e.target.value;
//             const dateparts=datevalue.split('-');
//             const year=dateparts[0];
      
//             if(year.length > 4 ){
//               dateparts[0]=year.slice(0,4);
//               e.target.value=dateparts.join('-');
              
//             }
//             console.log("hi");
//             const currentYear=new Date().getFullYear();
//             if(year > currentYear){
//               dateparts[0]=currentYear;
//               e.target.value=dateparts.join('-');
             
      
//             }
//             console.log( e.target.value);
      
//           });

//   });



// });
