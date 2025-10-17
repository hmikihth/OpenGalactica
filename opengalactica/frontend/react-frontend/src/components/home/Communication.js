import React, { useEffect, useState } from 'react';
import { Typography, Box, Table, TableBody, TableRow, TableCell, Link, CircularProgress } from '@mui/material';
import api from '../../utils/api';

const Communication = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCommunicationData = async () => {
      try {
        const response = await api.get('communication');
        setData(response.data);
      } catch (err) {
        setError('Failed to load communication data.');
      } finally {
        setLoading(false);
      }
    };

    fetchCommunicationData();
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
        Communication
      </Typography>
      {data ? (
        <Table>
          <TableBody>
            {/* Row for New Events */}
            <TableRow>
              <TableCell>
                <Link href="/notifications" underline="hover" color="inherit">
                  New events
                </Link>
              </TableCell>
              <TableCell align="right">{data.new_events}</TableCell>
            </TableRow>
            {/* Row for New Messages */}
            <TableRow>
              <TableCell sx={{borderBottom: 'none'}}>
                <Link href="/messages" underline="hover" color="inherit">
                  New messages
                </Link>
              </TableCell>
              <TableCell align="right" sx={{borderBottom: 'none'}}>{data.new_messages}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      ) : (
        <Typography>No communication data available.</Typography>
      )}
    </Box>
  );
};

export default Communication;
