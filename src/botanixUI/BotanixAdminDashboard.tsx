import React, { useState } from 'react';
import { Button, Modal, Input, Form, Typography, Space, ConfigProvider } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const BotanixAdminDashboard = () => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [users, setUsers] = useState([]);
  const [userInput, setUserInput] = useState({ name: '', email: '' });

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setUserInput({ name: '', email: '' });
  };

  const createUser = () => {
    if (userInput.name && userInput.email) {
      setUsers([...users, userInput]);
      handleCancel();
    }
  };

  const toggleHighContrastText = () => {
    document.body.classList.toggle('high-contrast');
  };

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#007BFF',
          colorBgBase: isDark() ? '#121212' : '#ffffff',
          colorTextBase: isDark() ? 'white' : 'black',
        },
      }}
    >
      <div className="high-contrast" style={{ cursor: 'pointer', padding: 16 }} onClick={toggleHighContrastText}>
        Toggle High Contrast
      </div>
      <Typography.Title level={2}>Botanix Admin Dashboard</Typography.Title>

      {/* User List */}
      <ul>
        {users.map((user, index) => (
          <li key={index}>{`${user.name} - ${user.email}`}</li>
        ))}
      </ul>

      {/* User Creation Modal */}
      <Modal
        title="Create New User"
        open={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Form layout="vertical">
          <Form.Item label="Name" name="name">
            <Input value={userInput.name} onChange={(e) => setUserInput({ ...userInput, name: e.target.value })} />
          </Form.Item>
          <Form.Item label="Email" name="email">
            <Input value={userInput.email} onChange={(e) => setUserInput({ ...userInput, email: e.target.value })} />
          </Form.Item>
        </Form>
        <Space style={{ float: 'right' }}>
          <Button onClick={handleCancel}>Cancel</Button>
          <Button type="primary" onClick={createUser}>
            Create
          </Button>
        </Space>
      </Modal>

      {/* AI Task Planner Widget */}
      <div className="ai-task-planner">
        <Typography.Title level={3}>AI Task Planner</Typography.Title>
        <p>Here you can plan and manage tasks for your team.</p>
      </div>
    </ConfigProvider>
  );
};

const isDark = () => window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

export default BotanixAdminDashboard;