import './Admin.css';

const Admin = ({ logoutAction }) => {
    return (
        <div className="admin-page">
            <h2> Welcome to the Admin page! </h2>
            <button onClick={logoutAction}>Logout</button>
        </div>
    );
};

export default Admin;