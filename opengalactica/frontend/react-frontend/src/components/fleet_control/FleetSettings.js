import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Typography, TextField, Button, Grid
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const FleetSettings = () => {
  const [fleets, setFleets] = useState([]);
  const [names, setNames] = useState({});

  useEffect(() => {
    api.get('fleet-settings/')
      .then(res => {
        setFleets(res.data);
        const initialNames = {};
        res.data.forEach(f => initialNames[f.id] = f.name);
        setNames(initialNames);
      });
  }, []);

  const handleChange = (fleetId, value) => {
    setNames({ ...names, [fleetId]: value });
  };

  const handleSave = () => {
    api.post('fleet-settings/update-names/', names, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      }
    }).then(() => window.location.reload());
  };

  return (
    <Card sx={{ my: 2, py:2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Fleet Settings</Typography>
        <Grid container spacing={2}>
          {fleets.map(fleet => (
            <Grid item xs={12} md={3} key={fleet.id}>
              <TextField
                label={fleet.name}
                value={names[fleet.id] || ''}
                onChange={e => handleChange(fleet.id, e.target.value)}
                fullWidth
                size="small"
              />
            </Grid>
          ))}
        </Grid>
        <Button
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
          onClick={handleSave}
        >
          Save
        </Button>
      </CardContent>
    </Card>
  );
};

export default FleetSettings;
