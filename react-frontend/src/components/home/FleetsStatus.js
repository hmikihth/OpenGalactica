import React, { useEffect, useState } from 'react';
import { Box, Table, TableBody, TableRow, Typography, CircularProgress } from '@mui/material';
import MobileTableCell from '../../components/MobileTableCell';

import api from '../../utils/api';

const FleetsStatus = () => {
  const [fleets, setFleets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {

    const fetchFleets = async () => {
      try {
        const response = await api.get('fleets');
        setFleets(response.data);
      } catch (err) {
        setError('Error fetching fleet data.');
      } finally {
        setLoading(false);
      }
    };

    fetchFleets();    
  
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }
  
  return (
    <Box sx={{ overflowX: 'auto' }}>
      <Typography variant="h6" component="div" gutterBottom>
        Fleets status
      </Typography>
      <Table>
        <TableBody>
          {fleets.map((fleet, index) => (
            <TableRow
              key={index}
              sx={{
                backgroundColor: fleet.active ? 'inherit' : 'grey.300',
              }}
            >
              <MobileTableCell>{fleet.name}</MobileTableCell>
              <MobileTableCell>{fleet.task}</MobileTableCell>
              <MobileTableCell>{fleet.status}</MobileTableCell>
              <MobileTableCell>{fleet.target}</MobileTableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
};

export default FleetsStatus;
