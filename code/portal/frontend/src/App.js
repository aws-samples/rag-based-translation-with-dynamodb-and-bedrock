import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Layout, Spin } from 'antd';

import { fetchUserInfo } from './store/slices/authSlice';
import PrivateRoute from './components/PrivateRoute';
import AdminRoute from './components/AdminRoute';
import SuperAdminRoute from './components/SuperAdminRoute';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import ExcelTranslatePage from './pages/ExcelTranslatePage';
import DictionaryManagementPage from './pages/DictionaryManagementPage';
import ParameterStorePage from './pages/ParameterStorePage';
import AppHeader from './components/AppHeader';
import AppFooter from './components/AppFooter';

const { Content } = Layout;

function App() {
  const dispatch = useDispatch();
  const { isAuthenticated, loading } = useSelector((state) => state.auth);

  useEffect(() => {
    if (isAuthenticated) {
      dispatch(fetchUserInfo());
    }
  }, [dispatch, isAuthenticated]);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <Layout className="app-container">
      {isAuthenticated && <AppHeader />}
      <Content className="content-container">
        <Routes>
          <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} />
          <Route path="/" element={<PrivateRoute><HomePage /></PrivateRoute>} />
          <Route path="/excel-translate" element={<PrivateRoute><ExcelTranslatePage /></PrivateRoute>} />
          <Route path="/dictionary" element={<AdminRoute><DictionaryManagementPage /></AdminRoute>} />
          <Route path="/parameters" element={<SuperAdminRoute><ParameterStorePage /></SuperAdminRoute>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Content>
      {isAuthenticated && <AppFooter />}
    </Layout>
  );
}

export default App;
