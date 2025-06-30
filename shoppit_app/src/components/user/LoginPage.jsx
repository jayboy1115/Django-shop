import { useContext, useState } from "react"
import "./LoginPage.css"
import Error from "../ui/Error"
import api from "../../api"
import { useLocation, useNavigate, Link } from "react-router-dom"
import { AuthContext } from "../../context/AuthContext"

const LoginPage = () => {
    const {setIsAuthenticated, get_username} = useContext(AuthContext)
    const location = useLocation()
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
 

    const userInfo = {username, password}

    function handleSubmit(e){
        e.preventDefault()
        setLoading(true)

        api.post("token/", userInfo)
        .then(res => {
            console.log(res.data)
            localStorage.setItem("access", res.data.access)
            localStorage.setItem("refresh", res.data.refresh)
            setUsername("")
            setPassword("")
            setLoading(false)
            setIsAuthenticated(true)
            get_username()
            setError("")

            const from = location?.state?.from.pathname || "/";
            navigate(from, {replace:true});
        })
        .catch(err => {
            console.log(err.message)
            setError(err.message)
            setLoading(false)
        })
    }

  return (
    <div className="login-container my-5">
        <div className="login-card shadow">
            {error && <Error error={error} />}
            <h2 className="login-title">Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input 
                        type="username" 
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="form-control" 
                        id="email" 
                        placeholder="Username" 
                        required 
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input 
                        type="password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="form-control" 
                        id="password" 
                        placeholder="Password" 
                        required 
                    />
                </div>
                <button 
                    type="submit" 
                    className="btn btn-primary w-100" 
                    disabled={loading}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>
            <div className="login-footer mt-2">
                <p className="mb-0">No account? <Link to="/signup">Sign up</Link></p>
            </div>
        </div>
    </div>
  )
}

export default LoginPage;