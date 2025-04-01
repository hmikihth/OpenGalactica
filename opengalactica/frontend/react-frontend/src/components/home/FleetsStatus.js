import React, { useEffect, useState } from 'react';
import { Box, Table, TableBody, TableRow, Typography } from '@mui/material';
import MobileTableCell from '../../components/MobileTableCell';

const FleetsStatus = () => {
  const [fleets, setFleets] = useState([]);

  useEffect(() => {
    fetch('/api/v1/fleets')
      .then((response) => response.json())
      .then((data) => setFleets(data))
      .catch((error) => console.error('Error fetching fleet data:', error));
  }, []);

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
