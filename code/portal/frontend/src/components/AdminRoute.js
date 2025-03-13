import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const AdminRoute = ({ children }) => {
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (!user || !['admin', 'super-admin'].includes(user.role)) {
    return <Navigate to="/" />;
  }

  return children;
};

export default AdminRoute;
