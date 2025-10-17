import React, { useEffect, useState } from 'react';
import { Typography, Box, CircularProgress, Card, CardContent } from '@mui/material';
import api from '../../utils/api';

const MinistersMessage = () => {
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMinistersMessage = async () => {
      try {
        const response = await api.get('ministers-message');
        setMessage(response.data.ministers_message);
      } catch (err) {
        setError('Failed to load minister\'s message.');
      } finally {
        setLoading(false);
      }
    };

    fetchMinistersMessage();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Box>
      <Typography variant="h6" component="div" gutterBottom>
        Ministers' messages
      </Typography>
      {message ? (
        <Typography>{message}</Typography>
      ) : (
        <Typography>No message from the ministers is available.</Typography>
      )}
    </Box>
  );
};

export default MinistersMessage;
