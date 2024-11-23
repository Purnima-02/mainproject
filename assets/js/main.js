
document.addEventListener('DOMContentLoaded',()=>{
    console.log('Dom Loaded');
document.getElementById('id_co_applicant_type').addEventListener('change', function () {
    var salariedFields = document.getElementById('salaried-fields');
    var selfEmployedFields = document.getElementById('self-employed-fields');
    if (this.value == 'SALARIEDEMPLOYEE') {
        salariedFields.style.display = 'block';
        selfEmployedFields.style.display = 'none';
        // Add required attribute to salariedFields
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

        console.log(document.getElementById('id_co_applicant_self_employed_business_licence').hasAttribute('required'));

    } else if (this.value == 'SELFEMPLOYEED') {
        salariedFields.style.display = 'none';
        selfEmployedFields.style.display = 'block';
        // Add required attribute
        document.getElementById('id_co_applicant_self_employed_business_name').required = true;
        document.getElementById('id_co_applicant_self_employed_itr_mandatory').required = true;
        document.getElementById('id_co_pplicant_self_employed_itr_amount').required = true;
        document.getElementById('id_co_applicant_self_employed_business_licence').required = true;
        // Remove required attribute
        document.getElementById('id_co_applicant_parent_name').required = false;
        document.getElementById('id_co_applicant_company_name').required = false;
        document.getElementById('id_co_applicant_salaried_designation').required = false;
        document.getElementById('id_co_applicant_salaried_net_pay').required = false;
        document.getElementById('id_co_applicant_salaried_emis').required = false;
        document.getElementById('id_co_applicant_salaried_cibil_score').required = false;
    } else {
        salariedFields.style.display = 'none';
        selfEmployedFields.style.display = 'none';
        // Remove all required attributes
        document.getElementById('id_co_applicant_parent_name').required = false;
        document.getElementById('id_co_applicant_company_name').required = false;
        document.getElementById('id_co_applicant_salaried_designation').required = false;
        document.getElementById('id_co_applicant_salaried_net_pay').required = false;
        document.getElementById('id_co_applicant_salaried_emis').required = false;
        document.getElementById('id_co_applicant_salaried_cibil_score').required = false;
        document.getElementById('id_co_applicant_self_employed_business_name').required = false;
        document.getElementById('id_co_applicant_self_employed_itr_mandatory').required = false;
        document.getElementById('id_co_pplicant_self_employed_itr_amount').required = false;
        document.getElementById('id_co_applicant_self_employed_business_licence').required = false;
    }
});



document.querySelector('#id_mobile_number').addEventListener('input', (e) => {

    const maxLength = 10;
    const input = e.target;
    console.log(e.target.id);
    if (input.value.length > maxLength) {
        input.value = input.value.slice(0, maxLength);
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
// Scores Length


// cibilScore Length

document.querySelector('#id_cibil_score').addEventListener('input', (e) => {

    const maxLEngth = 3;
    const input = e.target;
    if (input.value.length > maxLEngth) {
        input.value = input.value.slice(0, maxLEngth);
    }

});
// cibilScore Length

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


});



