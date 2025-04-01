import React, { useEffect, useState } from 'react';
import { Typography, Box, Link, CircularProgress } from '@mui/material';
import axios from 'axios';

const News = () => {
  const [news, setNews] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLatestNews = async () => {
      try {
        const response = await axios.get('/api/v1/latest-news');
        setNews(response.data);
      } catch (err) {
        setError('Failed to load the latest news.');
      } finally {
        setLoading(false);
      }
    };

    fetchLatestNews();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Box>
      {news ? (
        <>
          <Typography
            variant="h6"
            gutterBottom
            sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
          >
            <Link href={news.url} underline="hover" color="inherit">
              {news.title}
            </Link>
            <Typography variant="caption" sx={{ color: 'gray' }}>
              {news.timestamp}
            </Typography>
          </Typography>
          <Typography variant="body2" sx={{ marginTop: 1 }}>
            {news.description}
          </Typography>
        </>
      ) : (
        <Typography>No news available at the moment.</Typography>
      )}
    </Box>
  );
};

export default News;
