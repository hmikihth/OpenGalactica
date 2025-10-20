import React, { useEffect, useState } from 'react';
import {
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  Box,
  CircularProgress,
} from '@mui/material';
import api from '../../utils/api';

const Storages = () => {
  const [storageCapacity, setStorageCapacity] = useState([]);
  const [storageStatus, setStorageStatus] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [capacityRes, statusRes] = await Promise.all([
          api.get('storage-capacity'),
          api.get('storage-status'),
        ]);

        setStorageCapacity(capacityRes.data);  // Expected to be a list of 3 levels
        setStorageStatus(statusRes.data);      // Expected to be a list with resource types
      } catch (err) {
        console.error('Failed to fetch storage data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box p={2}>
      <Typography variant="h6" gutterBottom>
        Storage Development Levels
      </Typography>
      <Paper sx={{ mb: 4, overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Level</TableCell>
              <TableCell>Research</TableCell>
              <TableCell>Building</TableCell>
              <TableCell>Metal Capacity</TableCell>
              <TableCell>Crystal Capacity</TableCell>
              <TableCell>Narion Capacity</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {storageCapacity.map((row, idx) => (
              <TableRow key={idx}>
                <TableCell>{row.level}</TableCell>
                <TableCell>{row.research}</TableCell>
                <TableCell>{row.building}</TableCell>
                <TableCell>{row.metal_capacity}</TableCell>
                <TableCell>{row.crystal_capacity}</TableCell>
                <TableCell>{row.narion_capacity}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>

      <Typography variant="h6" gutterBottom>
        Storage Status
      </Typography>
      <Paper sx={{ overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Resource Type</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Turns Until Full</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {storageStatus.map((row, idx) => (
              <TableRow key={idx}>
                <TableCell>{row.resource_type}</TableCell>
                <TableCell>{row.status}</TableCell>
                <TableCell>{row.turns_until_full}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
};

export default Storages;
