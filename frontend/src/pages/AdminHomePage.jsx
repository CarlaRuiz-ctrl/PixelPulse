import React, { useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import LoadingSpinner from "../components/LoadingSpinner";
import { Button } from "primereact/button";
import UsersDashboard from "../components/UsersDashboard";
import UserUpdateForm from "../components/UserUpdateForm";
import OrdersDashboard from "../components/OrdersDashboard";
import { Dialog } from "primereact/dialog";
import { ConfirmDialog } from "primereact/confirmdialog";

const AdminHomePage = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = React.useState(true);
    const [users, setUsers] = React.useState(null);
    const [orders, setOrders] = React.useState(null);
    const [selectedUser, setSelectedUser] = React.useState(null);
    const [showUpdateForm, setShowUpdateForm] = React.useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);

    const getAllUsers = async () => {
        try {
            const response = await axios.get("/api/admin/users");
            closeAllTables("users");
            setUsers(response.data);
            setLoading(false);
        } catch (error) {
            console.error(error);
        }
    };

    const deleteUser = async (userId) => {
        try {
            await axios.delete(`/api/admin/users/delete/${userId}`);
            getAllUsers();
        } catch (error) {
            console.error(error);
        }
    };

    const getAllOrders = async () => {
        try {
            const response = await axios.get("/api/admin/orders");
            closeAllTables("orders");
            setOrders(response.data);
            setLoading(false);
        } catch (error) {
            console.error(error);
        }
    };

    const closeAllTables = (currentTable) => {
        if (currentTable === "users") {
            setOrders(null);
        } else if (currentTable === "orders") {
            setUsers(null);
        }
    };

    useEffect(() => {
        const checkUser = async () => {
            try {
                await axios.get("/api/auth/userType");
            } catch (error) {
                navigate("/unauthorized");
            } finally {
                setLoading(false);
            }
        };
        checkUser();
    }, []);

    return (
        <div id="adminPageContainer">
            <div className="controlButtons">
                <Button onClick={() => getAllUsers()}>Get All Users</Button>
                <Button onClick={() => getAllOrders()}>Get All Orders</Button>
            </div>
            <h1>Admin Home Page</h1>
            {loading && <LoadingSpinner />}
            {users && (
                <UsersDashboard
                    users={users}
                    setSelectedUser={setSelectedUser}
                    setShowUpdateForm={setShowUpdateForm}
                    setShowDeleteDialog={setShowDeleteDialog}
                />
            )}
            {orders && <OrdersDashboard orders={orders} />}
            <Dialog
                header="Update User"
                visible={showUpdateForm}
                style={{ width: "50vw" }}
                onHide={() => setShowUpdateForm(false)}
            >
                {selectedUser && (
                    <UserUpdateForm
                        user={selectedUser}
                        setShowUpdateForm={setShowUpdateForm}
                        getAllUsers={getAllUsers}
                    />
                )}
            </Dialog>
            <ConfirmDialog
                header="Delete User"
                visible={showDeleteDialog}
                onHide={() => setShowDeleteDialog(false)}
                message="Are you sure you want to delete this user?"
                accept={() => {
                    setShowDeleteDialog(false);
                    deleteUser(selectedUser.user_id);
                }}
            ></ConfirmDialog>
        </div>
    );
};

export default AdminHomePage;
