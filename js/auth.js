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
      loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Mock Validation
        if (!email || !password) {
          this.showError('Please fill in all fields.');
          return;
        }
        
        // Mock role determination based on email for testing
        let role = 'trainee';
        if (email.includes('trainer')) role = 'trainer';
        if (email.includes('admin')) role = 'admin';
        
        // Create Mock Session
        const userSession = {
          name: email.split('@')[0].split('.').map(n => n.charAt(0).toUpperCase() + n.slice(1)).join(' '),
          email: email,
          role: role
        };
        
        localStorage.setItem('ccai_user', JSON.stringify(userSession));
        
        // Redirect based on role
        if (role === 'admin') {
          window.location.href = 'admin-dashboard.html';
        } else if (role === 'trainer') {
          window.location.href = 'trainer-dashboard.html';
        } else {
          window.location.href = 'trainee-dashboard.html';
        }
      });
    }
  },

  /**
   * Initializes the registration form if it exists
   */
  initRegisterForm: function() {
    const registerForm = document.getElementById('registerForm');
    
    // Toggle additional fields based on role
    const roleSelect = document.getElementById('role');
    if (roleSelect) {
      roleSelect.addEventListener('change', (e) => {
        const traineeFields = document.getElementById('trainee-fields');
        const trainerFields = document.getElementById('trainer-fields');
        
        if (e.target.value === 'trainer') {
          traineeFields.style.display = 'none';
          trainerFields.style.display = 'block';
        } else {
          traineeFields.style.display = 'block';
          trainerFields.style.display = 'none';
        }
      });
    }

    if (registerForm) {
      registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const name = document.getElementById('fullname').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirm = document.getElementById('confirmPassword').value;
        const role = document.getElementById('role').value;
        
        // Mock Validation
        if (password !== confirm) {
          this.showError('Passwords do not match.');
          return;
        }
        
        if (password.length < 8) {
          this.showError('Password must be at least 8 characters.');
          return;
        }
        
        // Create Mock Session
        const userSession = {
          name: name,
          email: email,
          role: role
        };
        
        localStorage.setItem('ccai_user', JSON.stringify(userSession));
        
        // Redirect
        if (role === 'trainer') {
          window.location.href = 'trainer-dashboard.html';
        } else {
          window.location.href = 'trainee-dashboard.html';
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
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('ccai_user');
        window.location.href = 'login.html';
      });
    });
  },

  /**
   * Shows a simple error message (mock implementation)
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
    const isAuthPage = window.location.pathname.includes('login.html') || window.location.pathname.includes('register.html') || window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/');
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
