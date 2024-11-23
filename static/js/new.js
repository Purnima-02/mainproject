const loanAmountInput = document.getElementById('loan-amount');
const loanAmountSlider = document.getElementById('loan-amount-slider');
const interestRateInput = document.getElementById('interest-rate');
const interestRateSlider = document.getElementById('interest-rate-slider');
const loanTenureInput = document.getElementById('loan-tenure');
const loanTenureSlider = document.getElementById('loan-tenure-slider');

const emiElement = document.getElementById('emi');
const principalAmountElement = document.getElementById('principal-amount');
const interestPayableElement = document.getElementById('interest-payable');
const totalAmountElement = document.getElementById('total-amount');

function calculateEMI() {
    const loanAmount = parseFloat(loanAmountInput.value);
    const interestRate = parseFloat(interestRateInput.value) / 12 / 100;
    const loanTenure = parseFloat(loanTenureInput.value) * 12;

    const emi = loanAmount * interestRate * (Math.pow(1 + interestRate, loanTenure) / (Math.pow(1 + interestRate, loanTenure) - 1));
    const totalAmount = emi * loanTenure;
    const interestPayable = totalAmount - loanAmount;

    emiElement.innerText = emi.toFixed(2);
    principalAmountElement.innerText = loanAmount.toFixed(0);
    interestPayableElement.innerText = interestPayable.toFixed(0);
    totalAmountElement.innerText = totalAmount.toFixed(0);
}

loanAmountInput.addEventListener('input', (e) => {
    loanAmountSlider.value = e.target.value;
    calculateEMI();
});

loanAmountSlider.addEventListener('input', (e) => {
    loanAmountInput.value = e.target.value;
    calculateEMI();
});

interestRateInput.addEventListener('input', (e) => {
    interestRateSlider.value = e.target.value;
    calculateEMI();
});

interestRateSlider.addEventListener('input', (e) => {
    interestRateInput.value = e.target.value;
    calculateEMI();
});

loanTenureInput.addEventListener('input', (e) => {
    loanTenureSlider.value = e.target.value;
    calculateEMI();
});

loanTenureSlider.addEventListener('input', (e) => {
    loanTenureInput.value = e.target.value;
    calculateEMI();
});

calculateEMI();


// Faq's Js 

function toggleAccordion(index) {
    var accordions = document.querySelectorAll('.accordion-content');
    accordions.forEach(function(accordion, i) {
        if (i === index) {
            accordion.style.display = accordion.style.display === 'block' ? 'none' : 'block';
        } else {
            accordion.style.display = 'none';
        }
    });
}