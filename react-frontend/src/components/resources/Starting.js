import React, { useState } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Button,
  Paper,
  Snackbar,
  Alert,
} from '@mui/material';
import api from '../../utils/api';

const Starting = () => {
  const [metal, setMetal] = useState(0);
  const [crystal, setCrystal] = useState(0);
  const [narion, setNarion] = useState(0);
  const [metalCost, setMetalCost] = useState(0);
  const [message, setMessage] = useState(null);
  const [severity, setSeverity] = useState('success');

  const handleCounting = async () => {
    try {
      const response = await api.post('plasmator-starting-count', {
        metal,
        crystal,
        narion,
      });
      setMetalCost(response.data.metal_cost);
    } catch (error) {
      setMessage('Failed to calculate cost');
      setSeverity('error');
    }
  };

  const handleStart = async () => {
    try {
      const response = await api.post('plasmator-starting', {
        metal,
        crystal,
        narion,
      });
      const result = response.data.status;

      if (result === 'successful') {
        setMetal(0);
        setCrystal(0);
        setNarion(0);
        setMetalCost(0);
        setSeverity('success');
        setMessage('Starting successful.');
      } else if (result === 'not enough neutral plasmator') {
        setSeverity('warning');
        setMessage('Not enough neutral plasmator.');
      } else if (result === 'not enough metal') {
        setSeverity('warning');
        setMessage('Not enough metal.');
      } else {
        setSeverity('error');
        setMessage('Unknown error occurred.');
      }
    } catch (error) {
      setSeverity('error');
      setMessage('Failed to start.');
    }
  };

  return (
    <Box p={2}>
      <Typography variant="h6" gutterBottom>
        Plasmator Starting
      </Typography>

      <Paper sx={{ mb: 2, overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Metal</TableCell>
              <TableCell>Crystal</TableCell>
              <TableCell>Narion</TableCell>
              <TableCell>Metal Cost</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>
                <TextField
                  size="small"
                  type="number"
                  value={metal}
                  onChange={(e) => setMetal(parseInt(e.target.value || 0))}
                  inputProps={{ min: 0 }}
                  fullWidth
                />
              </TableCell>
              <TableCell>
                <TextField
                  size="small"
                  type="number"
                  value={crystal}
                  onChange={(e) => setCrystal(parseInt(e.target.value || 0))}
                  inputProps={{ min: 0 }}
                  fullWidth
                />
              </TableCell>
              <TableCell>
                <TextField
                  size="small"
                  type="number"
                  value={narion}
                  onChange={(e) => setNarion(parseInt(e.target.value || 0))}
                  inputProps={{ min: 0 }}
                  fullWidth
                />
              </TableCell>
              <TableCell>{metalCost}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>

      <Box display="flex" gap={2}>
        <Button variant="outlined" color="primary" onClick={handleCounting}>
          Counting
        </Button>
        <Button variant="contained" color="secondary" onClick={handleStart}>
          Start
        </Button>
      </Box>

      <Snackbar
        open={!!message}
        autoHideDuration={4000}
        onClose={() => setMessage(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setMessage(null)} severity={severity} variant="filled">
          {message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Starting;
