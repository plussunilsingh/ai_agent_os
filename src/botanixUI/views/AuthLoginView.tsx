import React from 'react';
import { Form, Button, Input } from 'antd';
import styled from 'styled-components';
import { useHistory } from 'react-router-dom';

const HighContrastText = styled.span`
  color: white;
`;

interface AuthLoginViewProps {}

const AuthLoginView: React.FC<AuthLoginViewProps> = () => {
  const history = useHistory();

  const onFinish = (values: any) => {
    console.log('Received values of form: ', values);
    // Here you would handle the authentication logic, e.g., call an API to authenticate user
    history.push('/dashboard');
  };

  return (
    <Form
      name="basic"
      initialValues={{ remember: true }}
      onFinish={onFinish}
      style={{
        width: '100%',
        maxWidth: 460,
        margin: '30px auto',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      }}
    >
      <Form.Item
        label={<HighContrastText>Email</HighContrastText>}
        name="email"
        rules={[{ required: true, message: 'Please input your email!' }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label={<HighContrastText>Password</HighContrastText>}
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" block style={{ marginTop: 16 }}>
          Log In
        </Button>
      </Form.Item>
    </Form>
  );
};

export default AuthLoginView;

This `AuthLoginView.tsx` component is designed for a high-contrast text styling, using styled-components to ensure the text color stands out against any background. The form uses Ant Design's components for a consistent and modern UI look. The form handles basic validation and submission logic, including navigation after successful authentication.