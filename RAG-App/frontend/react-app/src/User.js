import './User.css';

const User = ({ logoutAction }) => {
    return (
        <div className="user-page">
            <div className="user-header">
                <h2>User Dashboard</h2>
                <button className="logout-btn" onClick={logoutAction}>Logout</button>
            </div>

            <div className="user-content">
                <div className="welcome-section">
                    <h3>Welcome to the User Dashboard!</h3>
                    <p>Please use the AI chat box below to answer any questions you have.</p>
                </div>
            </div>
        </div>
    );
};

export default User;