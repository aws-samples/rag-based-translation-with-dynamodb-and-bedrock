import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const SuperAdminRoute = ({ children }) => {
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (!user || user.role !== 'super-admin') {
    return <Navigate to="/" />;
  }

  return children;
};

export default SuperAdminRoute;
