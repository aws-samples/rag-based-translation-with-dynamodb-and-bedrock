import React from 'react';
import { Layout, Menu, Button } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { 
  TranslationOutlined, 
  FileExcelOutlined, 
  BookOutlined, 
  SettingOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { Bedrock } from '@lobehub/icons';

import { logout } from '../store/slices/authSlice';

const { Header } = Layout;

const AppHeader = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const menuItems = [
    {
      key: '/',
      icon: <TranslationOutlined />,
      label: 'LLM 翻译工具',
    },
    {
      key: '/excel-translate',
      icon: <FileExcelOutlined />,
      label: 'Excel 文件翻译',
    },
  ];

  // Add admin menu items
  if (user && ['admin', 'super-admin'].includes(user.role)) {
    menuItems.push({
      key: '/dictionary',
      icon: <BookOutlined />,
      label: '专词映射表配置',
    });
  }

  // Add super-admin menu items
  if (user && user.role === 'super-admin') {
    menuItems.push({
      key: '/parameters',
      icon: <SettingOutlined />,
      label: '参数配置',
    });
  }

  return (
    <Header style={{ display: 'flex', alignItems: 'center' }}>
      <div style={{ marginRight: '24px', display: 'flex', alignItems: 'center', width: '246px', height: '48px' }}>
        <Bedrock.Combine size={40} style={{ color: 'white' }} />
      </div>
      <Menu
        theme="dark"
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={({ key }) => navigate(key)}
        style={{ flex: 1 }}
      />
      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center' }}>
        <span style={{ color: 'white', marginRight: 16 }}>
          欢迎, {user?.username} ({user?.role})
        </span>
        <Button 
          type="text" 
          icon={<LogoutOutlined />} 
          onClick={handleLogout}
          style={{ color: 'white' }}
        >
          退出
        </Button>
      </div>
    </Header>
  );
};

export default AppHeader;
