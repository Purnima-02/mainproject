document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_full_name');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
          });
      });

document.getElementById('id_required_loan_amount').setAttribute('min', '500');

document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_name');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
          });
      });

      document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_state');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^a-zA-Z]/g, '');  // Remove non-alphabetic characters
          });
      });
      document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_contact_no');
          firstNameField.addEventListener('input', function() {
              var value = this.value;
              this.value = value.replace(/[^0-9]/g, '');  // Remove non-alphabetic characters
          });
      });
      
      





