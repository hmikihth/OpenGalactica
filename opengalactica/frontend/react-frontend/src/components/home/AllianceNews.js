import React, { useEffect, useState } from 'react';
import { Typography, Box, CircularProgress, Card, CardContent } from '@mui/material';
import axios from 'axios';

const AllianceNews = () => {
  const [news, setNews] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllianceNews = async () => {
      try {
        const response = await axios.get('/api/v1/alliance-news');
        setNews(response.data.news);
      } catch (err) {
        setError('Failed to load alliance news.');
      } finally {
        setLoading(false);
      }
    };

    fetchAllianceNews();
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
        Alliance News
      </Typography>
      {news ? (
        <Typography>
          {news}
        </Typography>
      ) : (
        <Typography>No alliance news available.</Typography>
      )}
    </Box>
  );
};

export default AllianceNews;
