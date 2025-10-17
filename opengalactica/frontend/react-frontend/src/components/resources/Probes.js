import React, { useEffect, useState } from 'react';
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
  CircularProgress,
  Snackbar,
  Alert,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const Probes = () => {
  const [launchable, setLaunchable] = useState(null);
  const [launchAmount, setLaunchAmount] = useState('');
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const navigate = useNavigate();

  const fetchProbes = async () => {
    try {
      const response = await api.get('resource-production/plasmator-probes/');
      setLaunchable(response.data[0].quantity);
    } catch (error) {
      console.error('Failed to fetch probe data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProbes();
  }, []);

  const handleLaunch = async () => {
    if (!launchAmount || launchAmount <= 0) {
      setSnackbar({ open: true, message: 'Please enter a valid amount.', severity: 'warning' });
      return;
    }

    try {
      const response = await api.post('resource-production/launch/', {
        quantity: parseInt(launchAmount, 10)}, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
      });

      setSnackbar({
        open: true,
        message: `Successfully launched ${launchAmount} probe(s). Found ${response.data.new_plasmators} new plasmator(s).`,
        severity: 'success',
      });

      setLaunchAmount('');
      fetchProbes(); // refresh available probes
    } catch (error) {
      console.error('Failed to launch probes:', error);
      setSnackbar({
        open: true,
        message: 'Failed to launch probes.',
        severity: 'error',
      });
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Box p={2}>
      <Typography variant="h6" gutterBottom>
        Launch Plasmator Probes
      </Typography>

      <Paper sx={{ mb: 2, overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Launchable Probes</TableCell>
              <TableCell>Amount to Launch</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>{launchable}</TableCell>
              <TableCell>
                <TextField
                  size="small"
                  type="number"
                  value={launchAmount}
                  onChange={(e) => setLaunchAmount(e.target.value)}
                  inputProps={{ min: 0, max: launchable }}
                  fullWidth
                />
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>

      <Box display="flex" gap={2}>
        <Button variant="outlined" color="primary" onClick={() => navigate('/satellites')}>
          Produce
        </Button>
        <Button
          variant="contained"
          color="secondary"
          disabled={launchable <= 0}
          onClick={handleLaunch}
        >
          Launch
        </Button>
      </Box>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Probes;
