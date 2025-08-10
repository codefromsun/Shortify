
  
  const usernameInput = document.getElementById('username');
 usernameInput.focus();
  const passwordInput = document.getElementById('password');
  const loginBtn = document.getElementById('loginBtn');
  loginBtn.disabled = true;

  function validateInputs() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    if(username.length >0 && password.length >= 6){
        loginBtn.disabled = false;
        } else {
        loginBtn.disabled = true;
    }
  }

  usernameInput.addEventListener('input', validateInputs);
  passwordInput.addEventListener('input', validateInputs);

  document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;
     loginBtn.disabled = true; // Disable button to prevent multiple submissions
    const response = await fetch('/auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
     // alert("Login successful!");
       window.location.href = '/dashboard/'; 
    } else {
        alert(data.error || "Login failed.");
          // reset form fields
          usernameInput.value = "";
          passwordInput.value = "";
          validateInputs();
        }
    });


  function getCSRFToken() {
    const name = 'csrftoken=';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name)) {
        return cookie.substring(name.length);
      }
    }
    return '';
  }