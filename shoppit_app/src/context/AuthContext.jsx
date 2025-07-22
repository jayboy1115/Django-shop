import { createContext, useEffect, useState } from "react";
import jwtDecode from "jwt-decode";
import api from "../api";

export const AuthContext = createContext({
  isAuthenticated: false,
  username: "",
  setIsAuthenticated: () => {},
  get_username: () => {},
  logout: () => {}
});

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");

  const handleAuth = () => {
    const token = localStorage.getItem("access");
    if (!token) {
      setIsAuthenticated(false);
      return false;
    }

    try {
      const decoded = jwtDecode(token);
      const isExpired = decoded.exp < Date.now() / 1000;
      
      if (isExpired) {
        localStorage.removeItem("access");
        setIsAuthenticated(false);
        return false;
      }

      setIsAuthenticated(true);
      return true;
    } catch (error) {
      console.error("Token decode error:", error);
      localStorage.removeItem("access");
      setIsAuthenticated(false);
      return false;
    }
  };

  const get_username = async () => {
    if (!isAuthenticated) return;
    
    try {
      const response = await api.get("get_username");
      setUsername(response.data.username);
    } catch (err) {
      console.error("Failed to get username:", {
        status: err.response?.status,
        message: err.message
      });
      if (err.response?.status === 401) {
        logout();
      }
    }
  };

  const logout = () => {
    localStorage.removeItem("access");
    setIsAuthenticated(false);
    setUsername("");
  };

  useEffect(() => {
    const authValid = handleAuth();
    if (authValid) {
      get_username();
    }
  }, []);

  const authValue = {
    isAuthenticated,
    username,
    setIsAuthenticated,
    get_username,
    logout
  };

  return (
    <AuthContext.Provider value={authValue}>
      {children}
    </AuthContext.Provider>
  );
}