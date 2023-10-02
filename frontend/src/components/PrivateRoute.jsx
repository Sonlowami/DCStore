// PrivateRoute component to protect routes that require authentication
import React from "react";
import { Route, Navigate } from "react-router-dom";
import AuthService from "../lib/helpers/authService";
import { Outlet } from "react-router-dom";

const PrivateRoute = () => {
    const auth = AuthService.isAuthenticated();

    // If authorized, return an outlet that will render child elements
    // If not, return element that will navigate to login page
    return auth ? <Outlet /> : <Navigate to="/login" />;
}


export default PrivateRoute;
