import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Grid,
  Typography,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Snackbar,
  Alert,
} from '@mui/material';
import api from '../../utils/api';

const Sending = () => {
  const [resources, setResources] = useState({ metal: 0, crystal: 0, narion: 0 });
  const [neighbours, setNeighbours] = useState([]);
  const [selectedTarget, setSelectedTarget] = useState('');
  const [sendAmount, setSendAmount] = useState({ metal: '', crystal: '', narion: '' });
  const [fees, setFees] = useState({ metal: 0, crystal: 0, narion: 0 });
  const [message, setMessage] = useState({ text: '', severity: 'success' });
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('resources');
        setResources(res.data);
        const solRes = await api.get('sol-planets');
        setNeighbours(solRes.data);
      } catch (error) {
        console.error('Failed to load data:', error);
      }
    };
    fetchData();
  }, []);

  const handleChange = (field) => (e) => {
    setSendAmount((prev) => ({
      ...prev,
      [field]: e.target.value,
    }));
  };

  const handleCountFees = async () => {
    try {
      const response = await api.post('resource-sending-count', {
        ...sendAmount,
        target: selectedTarget,
      });
      setFees(response.data);
    } catch (error) {
      console.error('Error counting fees:', error);
      setMessage({ text: 'Failed to count fees.', severity: 'error' });
      setSnackbarOpen(true);
    }
  };

  const handleSend = async () => {
    try {
      await api.post('resource-sending', {
        ...sendAmount,
        target: selectedTarget,
      });
      setMessage({ text: 'Resources sent successfully!', severity: 'success' });
      setSendAmount({ metal: '', crystal: '', narion: '' });
      setFees({ metal: 0, crystal: 0, narion: 0 });
    } catch (error) {
      const errMsg =
        error.response?.data?.detail || 'Failed to send resources.';
      setMessage({ text: errMsg, severity: 'error' });
    } finally {
      setSnackbarOpen(true);
    }
  };

  return (
    <Box p={2}>
      <Typography variant="h6" gutterBottom>
        Send Resources
      </Typography>

      {/* Current Resources */}
      <Grid container spacing={2} alignItems="center" sx={{ mb: 1 }}>
        <Grid item xs={12} sm={3}>
          <Typography><strong>Metal:</strong> {resources.metal}</Typography>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Typography><strong>Crystal:</strong> {resources.crystal}</Typography>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Typography><strong>Narion:</strong> {resources.narion}</Typography>
        </Grid>
      </Grid>

      {/* Inputs + Target Select */}
      <Grid container spacing={2}>
        <Grid item xs={12} sm={3}>
          <TextField
            fullWidth
            label="Send Metal"
            type="number"
            value={sendAmount.metal}
            onChange={handleChange('metal')}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <TextField
            fullWidth
            label="Send Crystal"
            type="number"
            value={sendAmount.crystal}
            onChange={handleChange('crystal')}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <TextField
            fullWidth
            label="Send Narion"
            type="number"
            value={sendAmount.narion}
            onChange={handleChange('narion')}
            inputProps={{ min: 0 }}
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <FormControl fullWidth>
            <InputLabel>Target Planet</InputLabel>
            <Select
              value={selectedTarget}
              label="Target Planet"
              onChange={(e) => setSelectedTarget(e.target.value)}
            >
              {neighbours.map((planet) => (
                <MenuItem key={planet.id} value={planet.id}>
                  {planet.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {/* Transaction Fees */}
      <Grid container spacing={2} mt={1}>
        <Grid item xs={12} sm={3}>
          <Typography>Metal Fee: {fees.metal}</Typography>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Typography>Crystal Fee: {fees.crystal}</Typography>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Typography>Narion Fee: {fees.narion}</Typography>
        </Grid>
      </Grid>

      {/* Buttons */}
      <Box mt={2} display="flex" gap={2}>
        <Button variant="contained" color="primary" onClick={handleCountFees}>
          Count Fees
        </Button>
        <Button
          variant="contained"
          color="success"
          onClick={handleSend}
          disabled={!selectedTarget}
        >
          Send
        </Button>
      </Box>

      {/* Snackbar */}
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

export default Sending;
