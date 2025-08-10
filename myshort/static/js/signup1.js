        document.addEventListener("DOMContentLoaded", () => {
          const usernameInput = document.getElementById("username");
          const password1Input = document.getElementById("password1");
          const password2Input = document.getElementById("password2");
          const btn = document.getElementById("btn");
          usernameInput.focus();

    function validateForm() {
      const username = usernameInput.value.trim();
      const password1 = password1Input.value;
      const password2 = password2Input.value;

      if (username && password1 === password2 && password1.length >= 6) {
        btn.disabled = false;
      } else {
        btn.disabled = true;
      }
    }

    // Initialize as disabled
    btn.disabled = true;

    // Real-time validation
    [usernameInput, password1Input, password2Input].forEach(input => {
      input.addEventListener("input", validateForm);
    });

    btn.addEventListener("click", async () => {
      const username = usernameInput.value.trim();
      const password = password1Input.value;
      btn.disabled = true; // Disable button to prevent multiple submissions

      try {
        const response = await fetch("/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
         // alert("User registered successfully!");
          window.location.href = "/dashboard/"; 
        } else {
          alert(data.error || "Registration failed.");
          // reset form fields
          usernameInput.value = "";
          password1Input.value = "";
          password2Input.value = "";
          usernameInput.focus();

        }
      } catch (err) {
        console.error("Error:", err);
        alert("Something went wrong. Try again.");
      }
    });

    // CSRF Helper
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });