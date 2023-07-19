// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault(); // Prevent form from being submitted
  
    // Get the entered email and password
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
  
    // TODO: Add your login authentication logic here
  
    // Clear the form fields
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
  }
  
  // Attach event listener to form submission
  var form = document.getElementById('login-form');
  form.addEventListener('submit', handleSubmit);
  