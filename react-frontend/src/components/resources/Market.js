import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TextField,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
  Button,
  Snackbar,
  Alert,
} from '@mui/material';
import api from '../../utils/api';

const Market = () => {
  const [marketData, setMarketData] = useState({
    capacity: { metal: 0, crystal: 0, narion: 0 },
    fee: { metal: 0, crystal: 0, narion: 0 },
  });

  const [formData, setFormData] = useState({
    amount: '',
    inputResource: 'metal',
    outputResource: 'crystal',
  });

  const [message, setMessage] = useState({ text: '', severity: 'success' });
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  useEffect(() => {
    const fetchMarketData = async () => {
      try {
        const response = await api.get('market-data');
        setMarketData(response.data);
      } catch (error) {
        console.error('Failed to load market data:', error);
      }
    };

    fetchMarketData();
  }, []);

  const handleChange = (field) => (e) => {
    setFormData((prev) => ({
      ...prev,
      [field]: e.target.value,
    }));
  };

  const handleExchange = async () => {
    try {
      await api.post('exchange', formData);
      setMessage({ text: 'Exchange successful!', severity: 'success' });
    } catch (error) {
      const errMsg =
        error.response?.data?.detail || 'Exchange failed.';
      setMessage({ text: errMsg, severity: 'error' });
    } finally {
      setSnackbarOpen(true);
    }
  };

  return (
    <Box p={2}>
      <Typography variant="h6" gutterBottom>
        Market
      </Typography>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell><strong></strong></TableCell>
            <TableCell><strong>Metal</strong></TableCell>
            <TableCell><strong>Crystal</strong></TableCell>
            <TableCell><strong>Narion</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell><strong>Market Capacity</strong></TableCell>
            <TableCell>{marketData.capacity.metal}</TableCell>
            <TableCell>{marketData.capacity.crystal}</TableCell>
            <TableCell>{marketData.capacity.narion}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell><strong>Exchange Fee (%)</strong></TableCell>
            <TableCell>{marketData.fee.metal}%</TableCell>
            <TableCell>{marketData.fee.crystal}%</TableCell>
            <TableCell>{marketData.fee.narion}%</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      <Box mt={3}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <TextField
              label="Amount"
              type="number"
              value={formData.amount}
              onChange={handleChange('amount')}
              fullWidth
            />
          </Grid>

          <Grid item xs={12} sm={4}>
            <FormControl fullWidth>
              <InputLabel>From</InputLabel>
              <Select
                value={formData.inputResource}
                label="From"
                onChange={handleChange('inputResource')}
              >
                <MenuItem value="metal">Metal</MenuItem>
                <MenuItem value="crystal">Crystal</MenuItem>
                <MenuItem value="narion">Narion</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={4}>
            <FormControl fullWidth>
              <InputLabel>To</InputLabel>
              <Select
                value={formData.outputResource}
                label="To"
                onChange={handleChange('outputResource')}
              >
                <MenuItem value="metal">Metal</MenuItem>
                <MenuItem value="crystal">Crystal</MenuItem>
                <MenuItem value="narion">Narion</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        <Box mt={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleExchange}
            disabled={
              !formData.amount ||
              formData.inputResource === formData.outputResource
            }
          >
            Exchange
          </Button>
        </Box>
      </Box>

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={() => setSnackbarOpen(false)}
      >
        <Alert
          onClose={() => setSnackbarOpen(false)}
          severity={message.severity}
          sx={{ width: '100%' }}
        >
          {message.text}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Market;
