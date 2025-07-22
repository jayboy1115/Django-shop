import axios from "axios"
import jwtDecode from "jwt-decode"

// Use environment variable for API base URL with fallback
export const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

const api = axios.create({
    baseURL: BASE_URL
})

// Request interceptor for adding auth token and handling token expiration
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access");
        if (token) {
            try {
                const decoded = jwtDecode(token);
                const expiry_date = decoded.exp;
                const current_time = Date.now() / 1000;
                
                if (expiry_date > current_time) {
                    config.headers.Authorization = `Bearer ${token}`;
                } else {
                    // Token expired, attempt to use refresh token
                    const refreshToken = localStorage.getItem("refresh");
                    if (refreshToken) {
                        // We'll handle refresh in a separate function
                        // For now, just remove the expired token
                        localStorage.removeItem("access");
                    }
                }
            } catch (error) {
                console.error("Token decode error:", error);
                localStorage.removeItem("access");
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for handling common errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const originalRequest = error.config;
        
        // Handle 401 Unauthorized errors
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            // Could implement token refresh logic here
            // For now, redirect to login if unauthorized
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        
        return Promise.reject(error);
    }
)


export default api



