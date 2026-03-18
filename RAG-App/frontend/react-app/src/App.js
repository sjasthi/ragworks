import React, {useState} from "react";
import './App.css';
import Login from "./Login"
import Chat from "./Chat"
import Admin from "./Admin"
import User from "./User"

const App = () => {
  const [role, setRole] = useState(null); // role starts off set to null

  // successful login sets the userRole to "admin" or "user"
  const LoginSuccess = (userRole) => {
    setRole(userRole);
  }
  
  // resets the role to null when user logs out
  const Logout = () => {
    setRole(null);
  }

  /* when not role, LoginSuccess is passed as loginAction prop to update role
    after credentials are verified */
  if (!role) {
    return <Login loginAction={LoginSuccess} />;
  }

  // shows admin screen and ai chat when admin successfully logs in
  if (role === "admin"){
    return (
      <div>
        <Admin logoutAction={Logout} />
      </div>
    );
  }

  // shows user screen and ai chat when admin succesfully logs in
  if (role === "user"){
    return (
      <div>
        <User logoutAction={Logout} />
        <Chat />
      </div>
    );
  }
};

export default App;
