import React, { useState } from 'react';

import axios from 'axios';
import { TextField, Button, Typography, Box, Alert } from '@mui/material';

import api from '../utils/api';

const Login = ({ onLoginSuccess = () => {} }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    await api.get('auth/csrf/', {
      withCredentials: true,
    });
    try {
      await api.post('auth/login/', {
        username,
        password,
      }, {
        withCredentials: true,  // Important: to send the session cookie!
      });
      onLoginSuccess(); // Parent component can refresh data or navigate
      window.location.href = '/';
    } catch (err) {
      console.error(err);
      setError('Invalid username or password.');
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleLogin}
      sx={{
        maxWidth: 400,
        margin: 'auto',
        marginTop: 8,
        padding: 4,
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        boxShadow: 3,
        borderRadius: 2,
      }}
    >
      <Typography variant="h5" component="h1" align="center">
        Login
      </Typography>

      <TextField
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />

      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      {error && <Alert severity="error">{error}</Alert>}

      <Button type="submit" variant="contained" color="primary">
        Login
      </Button>
    </Box>
  );
};

export default Login;
