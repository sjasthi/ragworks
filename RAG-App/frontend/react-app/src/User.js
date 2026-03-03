import './User.css';

const User = ({ logoutAction }) => {
    return (
        <div>
            <h2> Welcome to the End User page </h2>
            <button onClick={logoutAction}>Logout</button>
        </div>
    );
};

export default User;