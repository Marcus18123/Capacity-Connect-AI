const API_BASE_URL = "http://localhost:8000/api/v1";

const api = {
    getHeaders() {
        const token = localStorage.getItem('capacity_access_token');
        return {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        };
    },

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const token = options.token || localStorage.getItem('capacity_access_token');

        if (!token && endpoint === '/auth/me') {
            return null;
        }

        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(options.headers || {})
        };
        
        try {
            const response = await fetch(url, { ...options, headers });
            
            if (response.status === 401) {
                localStorage.removeItem('capacity_access_token');
                localStorage.removeItem('capacity_refresh_token');
                localStorage.removeItem('capacity_user');
                if (!window.location.pathname.includes('login.html') && !window.location.pathname.includes('register.html')) {
                    window.location.href = 'login.html';
                }
                throw new Error("Unauthorized");
            }
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP Error ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`API Request failed for ${endpoint}:`, error);
            throw error;
        }
    },

    get(endpoint, options = {}) {
        return this.request(endpoint, { method: 'GET', ...options });
    },

    post(endpoint, body, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body),
            ...options
        });
    },


    put(endpoint, body) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body)
        });
    },

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
};

window.api = api;
