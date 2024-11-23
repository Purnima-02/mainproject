document.addEventListener('DOMContentLoaded', function() {
    console.log("ccc")
          var firstNameField = document.getElementById('id_first_name');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
          });
      });
      document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_ref1_name');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
        });
    });
    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_ref2_name');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_existing_loan_details');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
        });
    });

      document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_aadhar_card_number');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^0-9]/g, '');  // Remove non-alphabetic characters
          });
      });

      document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_mobile_number');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^0-9]{10}/g, '');  // Remove non-alphabetic characters
          });
      });

      document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_ref1_mobile');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^0-9]{10}/g, '');  // Remove non-alphabetic characters
        });
    });


    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_ref2_mobile');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^0-9]{10}/g, '');  // Remove non-alphabetic characters
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_business_type');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            if (value) {
                value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
            }
            this.value = value;
        });
    });
    
    

    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_business_name');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            if (value) {
                value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
            }
            this.value = value;
        });
    });
    
    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_coapplicant_mobile_number');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^0-9]/g, '');  // Remove non-alphabetic characters
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_pan_card_number');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            this.value = value.replace(/[^A-Z0-9]{{10}/g, '');  // Remove non-alphabetic characters
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_co_applicant_first_name');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            if (value) {
                value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
            }
            this.value = value;
        });
    });
    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_co_applicant_last_name');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            if (value) {
                value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
            }
            this.value = value;
        });
    });
 
    document.addEventListener('DOMContentLoaded', function() {
        var firstNameField = document.getElementById('id_co_applicant_occupation');
        firstNameField.addEventListener('input', function() {
            var value = this.value;
            if (value) {
                value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
            }
            this.value = value;
        });
    });
  
