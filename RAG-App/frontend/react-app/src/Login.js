import React, {useState} from "react"; // useState allows for
import './Login.css';

const Login = ({loginAction}) => {
  // username and password start off as empty strings
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const UserAuthentication = () => {
      // hardcoded login credentials
    if (username === "admin" && password === "admin135"){
        loginAction("admin");
    } else if (username === "user" && password === "user246"){
        loginAction("user"); 
    } else {
        alert("Invalid username and/or password");
    }
  };

    return (
    <div className="login-page">
      <div className="login-box">
        <h2>Login</h2>
        
        <input
          type="text"
          placeholder="Username"
          onChange={({target}) => setUsername(target.value)}
        />

        <input
            type = "password"
            placeholder = "Password"
            onChange={({target}) => setPassword(target.value)}
        />

        <button onClick={UserAuthentication}>Login</button>
      </div>
    </div>
  );
}

export default Login;
