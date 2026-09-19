/**
 * CAPACITY CONNECT AI - Authentication
 */

const Auth = {
  /**
   * Initializes the login form if it exists on the page
   */
  initLoginForm: function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (!email || !password) {
          this.showError('Please fill in all fields.');
          return;
        }

        try {
          const formData = new URLSearchParams();
          formData.append('username', email);
          formData.append('password', password);

          const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
          });

          if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Login failed');
          }

          const tokenData = await response.json();
          localStorage.setItem('capacity_access_token', tokenData.access_token);
          localStorage.setItem('capacity_refresh_token', tokenData.refresh_token);

          const user = await window.api.get('/auth/me', { token: tokenData.access_token });
          localStorage.setItem('capacity_user', JSON.stringify(user));


          if (user.role === 'ADMIN') {
            window.location.href = 'admin-dashboard.html';
          } else if (user.role === 'TRAINER') {
            window.location.href = 'trainer-dashboard.html';
          } else {
            window.location.href = 'trainee-dashboard.html';
          }
        } catch (error) {
          this.showError(error.message || 'Authentication failed');
        }
      });
    }
  },

  /**
   * Initializes the registration form if it exists
   */
  initRegisterForm: function() {
    const registerForm = document.getElementById('registerForm');
    const roleSelect = document.getElementById('role');

    if (roleSelect) {
      roleSelect.addEventListener('change', (e) => {
        const traineeFields = document.getElementById('trainee-fields');
        const trainerFields = document.getElementById('trainer-fields');

        if (e.target.value === 'TRAINER') {
          traineeFields.style.display = 'none';
          trainerFields.style.display = 'block';
        } else {
          traineeFields.style.display = 'block';
          trainerFields.style.display = 'none';
        }
      });
    }

    if (registerForm) {
      registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('fullname').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirm = document.getElementById('confirmPassword').value;
        let role = document.getElementById('role').value;

        if (role === 'trainer') role = 'TRAINER';
        else if (role === 'trainee') role = 'TRAINEE';

        if (password !== confirm) {
          this.showError('Passwords do not match.');
          return;
        }

        if (password.length < 8) {
          this.showError('Password must be at least 8 characters.');
          return;
        }

        try {
          await window.api.post('/auth/register', {
            name: name,
            email: email,
            password: password,
            role: role
          });

          // Trainers require admin approval before login.
          if (role === 'TRAINER') {
            this.showError('Trainer registration submitted successfully. Your account is pending admin approval. You can log in after your account is approved.');
            return;
          }

          // Trainees can log in immediately after registration.
          const formData = new URLSearchParams();
          formData.append('username', email);
          formData.append('password', password);

          const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
          });

          if (!response.ok) throw new Error('Auto-login failed');

          const tokenData = await response.json();
          localStorage.setItem('capacity_access_token', tokenData.access_token);
          localStorage.setItem('capacity_refresh_token', tokenData.refresh_token);

          try {
            const user = await window.api.get('/auth/me');
            localStorage.setItem('capacity_user', JSON.stringify(user));
          } catch(e) {
            console.warn("Could not fetch user profile immediately after registration", e);
          }

          window.location.href = 'trainee-dashboard.html';
        } catch (error) {
          this.showError(error.message || 'Registration failed');
        }
      });
    }
  },


  /**
   * Initializes logout buttons
   */
  initLogout: function() {
    const logoutBtns = document.querySelectorAll('.logout-btn');

    logoutBtns.forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();

        try {
          await window.api.post('/auth/logout', {});
        } catch (e) {
          console.error('Logout error', e);
        }

        localStorage.removeItem('capacity_access_token');
        localStorage.removeItem('capacity_refresh_token');
        localStorage.removeItem('capacity_user');
        window.location.href = 'login.html';
      });
    });
  },

  /**
   * Shows a simple error message
   */
  showError: function(msg) {
    const errorEl = document.getElementById('auth-error');

    if (errorEl) {
      errorEl.textContent = msg;
      errorEl.style.display = 'block';
    } else {
      alert(msg);
    }
  },

  /**
   * Enforces that a user is logged in for protected routes
   */
  requireAuth: function() {
    const isAuthPage =
      window.location.pathname.includes('login.html') ||
      window.location.pathname.includes('register.html') ||
      window.location.pathname.includes('index.html') ||
      window.location.pathname.endsWith('/');

    const storedUser = localStorage.getItem('ccai_user');

    if (!storedUser && !isAuthPage) {
      window.location.href = 'login.html';
    }
  }
};

// Initialize on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  Auth.initLoginForm();
  Auth.initRegisterForm();
  Auth.initLogout();

  // Note: For this demonstration phase, we won't strictly enforce requireAuth()
  // on every page load to allow easy testing without getting locked out.
  // Uncomment below for strict routing:
  // Auth.requireAuth();
});