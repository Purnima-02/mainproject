document.addEventListener('DOMContentLoaded',()=>{


    console.log("content Loaded");
   

    // document.querySelectorAll('input,select,textarea').forEach(e=>{

        
    //     e.setAttribute('readonly',true);
    // })

    document.querySelector('#id_mobile_number').addEventListener('input', (e) => {

        const maxLength = 10;
        const input = e.target;
        console.log(e.target.id);
        if (input.value.length > maxLength) {
            input.value = input.value.slice(0, maxLength);
        }
    
    
    });


    // Only characters in input
    document.getElementById('id_student_name').addEventListener('input', function (e) {
        var value = e.target.value;
        e.target.value = value.replace(/[^A-Za-z]/g, '');
      });
       // Only characters in input
    

    const co_Applicant_type=document.getElementById('id_co_applicant_type').value;
    console.log(co_Applicant_type);

//    console.log(document.getElementById('id_score_card').hasAttribute('required'));

    const doc=document.getElementById('id_score_card').addEventListener('change',(e)=>{
    
        const verify=e.target.files[0].name;
        if(!verify.endsWith('pdf')){
            e.target.value='';

        }
    });

    // Scores Length
document.querySelectorAll('#id_TOEFL_score,#id_GRE_score,#id_IELTS_score,#id_Duolingo_score,#id_PTE_score').forEach((id) => {


    id.addEventListener('input', (e) => {

        console.log(e.target.id);
        const maxLEngth = 5;
        const input = e.target;
        if (input.value.length > maxLEngth) {
            input.value = input.value.slice(0, maxLEngth);
        }

    });

});

// cibilScore Length

document.querySelector('#id_cibil_score').addEventListener('input', (e) => {

    const maxLEngth = 3;
    const input = e.target;
    if (input.value.length > maxLEngth) {
        input.value = input.value.slice(0, maxLEngth);
    }

});

//  salaried CibilScore
document.querySelector('#id_co_applicant_salaried_cibil_score').addEventListener('input', (e) => {

    const maxLEngth = 3;
    const input = e.target;
    if (input.value.length > maxLEngth) {
        input.value = input.value.slice(0, maxLEngth);
    }

});

//  salaried CibilScore

document.querySelectorAll('#id_loan_required,#id_co_applicant_salaried_net_pay,#id_co_applicant_salaried_emis,#id_co_pplicant_self_employed_itr_amount,#id_property_market_value,#id_property_govt_value').forEach((id) => {

    id.addEventListener('input', (e) => {

        console.log(e.target.id);
        const maxLEngth = 10;
        const input = e.target;
        if (input.value.length > maxLEngth) {
            input.value = input.value.slice(0, maxLEngth);
        }

    });

});


    if(co_Applicant_type==="SALARIEDEMPLOYEE"){

        document.getElementById('salaried-fields').style.display="block";
        document.getElementById('self-employed-fields').style.display="none";

        document.getElementById('id_co_applicant_parent_name').required = true;
        document.getElementById('id_co_applicant_company_name').required = true;
        document.getElementById('id_co_applicant_salaried_designation').required = true;
        document.getElementById('id_co_applicant_salaried_net_pay').required = true;
        document.getElementById('id_co_applicant_salaried_emis').required = true;
        document.getElementById('id_co_applicant_salaried_cibil_score').required = true;

         // Remove required attribute
         document.getElementById('id_co_applicant_self_employed_business_name').required = false;
         document.getElementById('id_co_applicant_self_employed_itr_mandatory').required = false;
         document.getElementById('id_co_pplicant_self_employed_itr_amount').required = false;
         document.getElementById('id_co_applicant_self_employed_business_licence').required = false;
 
         console.log( document.getElementById('id_co_applicant_parent_name').hasAttribute('required'));
    }

    else{
        document.getElementById('salaried-fields').style.display="none";
        document.getElementById('self-employed-fields').style.display="block";

        

    }

    

    console.log("uuuu")


});