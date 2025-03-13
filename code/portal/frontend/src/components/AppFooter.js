import React from 'react';
import { Layout } from 'antd';

const { Footer } = Layout;

const AppFooter = () => {
  return (
    <Footer style={{ textAlign: 'center' }}>
      LLM Translate Tool ©{new Date().getFullYear()} Created with React and FastAPI
    </Footer>
  );
};

export default AppFooter;
