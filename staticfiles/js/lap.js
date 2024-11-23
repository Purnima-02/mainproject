document.addEventListener('DOMContentLoaded', function() {
          var firstNameField = document.getElementById('id_first_name');
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
              this.value = value.replace(/[^0-9]/g, '');  // Remove non-alphabetic characters
          });
      });
   
 
  
