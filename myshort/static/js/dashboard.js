
function updateEmptyMessage() {                                 // FOR DEALING WITH EMPTY MESSAGE
  const cards = document.querySelectorAll('.col').length;
  const msg = document.getElementById('emptyMsg');

  if (cards === 0) {
    msg.classList.remove('d-none');
  } else {
    msg.classList.add('d-none');
  }
}

  updateEmptyMessage();

  document.querySelectorAll('.delete-btn').forEach(btn => {  // adding event listener to delete buttons
    btn.addEventListener('click', async function () {
      const id = this.dataset.id;
      const shortcode = this.dataset.shortcode;
      const card = document.getElementById(id);

      const res = await fetch(`/delete/${shortcode}/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      });

      if (res.ok) {
        card.remove();
        updateEmptyMessage();
      } else {
        alert('Delete failed.');
      }
    });
  });



  document.getElementById('logoutBtn').addEventListener('click', async function(e) {
    e.preventDefault();
    const btn = document.getElementById('logoutBtn');
    btn.disabled = true; // disable immediately
    const response = await fetch('/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCSRFToken()
      }
    });

    const data = await response.json();
    if (response.ok) {
      window.location.href = '/login/';
    } else {
      alert(data.error || 'Logout failed');
              btn.disabled = false; // re-enable on error
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

