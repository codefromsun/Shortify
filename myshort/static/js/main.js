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
                document.getElementById('logoutBtn').addEventListener('click', async function(e) {
    e.preventDefault();
    const response = await fetch('/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken':  getCookie("csrftoken")
      }
    });

    const data = await response.json();
    if (response.ok) {
      window.location.href = '/login/';
    } else {
      alert(data.error || 'Logout failed');
    }
  });

      document.addEventListener("DOMContentLoaded", () => {


        const longUrlInput = document.getElementById("longUrl");
        const shortUrlInput = document.getElementById("shortUrl");
        const shortenBtn = document.getElementById("shortenBtn");
        const copyBtn = document.getElementById("copyBtn");
        const visitBtn = document.getElementById("visitBtn");
        const resetBtn = document.getElementById("resetBtn");

        const shortenSection = document.getElementById("shorten-section");
        const resultSection = document.getElementById("result-section");

        shortenBtn.addEventListener("click", () => {
          const longUrl = longUrlInput.value.trim();

          if (!longUrl) {
            alert("Please enter a valid URL.");
            longUrlInput.focus();
            return;
          }

          fetch("/shorten/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ original_url: longUrl })
          })
          .then(response => {
            if (!response.ok) throw new Error("Server error");
            return response.json();
          })
          .then(data => {

            longUrlResult.value = longUrl; 
            shortUrlInput.value = data.short_url;
            visitBtn.href = data.short_url;

            shortenSection.classList.add("d-none");
            resultSection.classList.remove("d-none");
          })
          .catch(error => {
            console.error("Error:", error);
            longUrlInput.value = "";
            alert("Enter Valid URL!");
            longUrlInput.focus();
          });
        });

        copyBtn.addEventListener("click", () => {
          navigator.clipboard.writeText(shortUrlInput.value)
            .then(() => alert("Short URL copied to clipboard!"))
            .catch(() => alert("Copy failed."));
        });

        resetBtn.addEventListener("click", () => {
          longUrlInput.value = "";
          shortUrlInput.value = "";
          resultSection.classList.add("d-none");
          shortenSection.classList.remove("d-none");
          longUrlInput.focus();
        });


      });