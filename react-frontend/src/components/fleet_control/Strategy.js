import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Typography, Select, MenuItem, Button, Grid
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const formations = ['wedge', 'wall', 'sphere'];

const Strategy = () => {
  const [fleets, setFleets] = useState([]);
  const [formationSettings, setFormationSettings] = useState({});

  useEffect(() => {
    api.get('fleet-strategy/')
      .then(res => {
        setFleets(res.data);
        const initialFormations = {};
        res.data.forEach(f => initialFormations[f.id] = f.formation);
        setFormationSettings(initialFormations);
      });
  }, []);

  const handleChange = (fleetId, value) => {
    setFormationSettings({ ...formationSettings, [fleetId]: value });
  };

  const handleSave = () => {
    api.post('fleet-strategy/update-strategy/', formationSettings, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      }
    }).then(() => window.location.reload());
  };

  return (
    <Card sx={{ my: 2, py:2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Fleet Strategy</Typography>
        <Grid container spacing={2}>
          {fleets.map(fleet => (
            <Grid item xs={12} md={3} key={fleet.id}>
              <Typography variant="body2">{fleet.name}</Typography>
              <Select
                value={formationSettings[fleet.id] || ''}
                onChange={e => handleChange(fleet.id, e.target.value)}
                fullWidth
                size="small"
              >
                {formations.map(form => (
                  <MenuItem key={form} value={form}>{form}</MenuItem>
                ))}
              </Select>
            </Grid>
          ))}
        </Grid>
        <Button
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
          onClick={handleSave}
        >
          Save Formations
        </Button>
      </CardContent>
    </Card>
  );
};

export default Strategy;
