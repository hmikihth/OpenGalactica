// SatelliteProduction.js
import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Table, TableHead, TableRow, TableCell,
  TableBody, TextField, Button, Grid
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const SatelliteProduction = () => {
  const [satellites, setSatellites] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [resources, setResources] = useState({ metal: 0, crystal: 0, narion: 0 });
  const [costs, setCosts] = useState({ metal: 0, crystal: 0, narion: 0, points: 0 });

  useEffect(() => {
    api.get('satellite-production/available').then(res => setSatellites(res.data));
    api.get('planet').then(res => setResources(res.data));
  }, []);

  const handleQuantityChange = (id, val) => {
    const quantity = parseInt(val || 0);
    const updated = { ...quantities, [id]: quantity };
    setQuantities(updated);

    const newCosts = satellites.reduce((acc, sat) => {
      const qty = updated[sat.id] || 0;
      acc.metal += sat.metal * qty;
      acc.crystal += sat.crystal * qty;
      acc.narion += sat.narion * qty;
      acc.points += (sat.metal + sat.crystal + sat.narion) * qty * 0.01;
      return acc;
    }, { metal: 0, crystal: 0, narion: 0, points: 0 });

    setCosts(newCosts);
  };

  const handleProduce = () => {
    const payload = Object.entries(quantities)
      .filter(([_, qty]) => qty > 0)
      .map(([satellite_type, quantity]) => ({ satellite_type, quantity }));

    api.post('satellite-production/produce/', payload, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    }).then(() => window.location.reload());
  };

  return (
    <Card sx={{ my: 2 }}>
      <CardContent>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Metal</TableCell>
              <TableCell>Crystal</TableCell>
              <TableCell>Narion</TableCell>
              <TableCell>Prod. Time</TableCell>
              <TableCell>Qty</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {satellites.map(sat => (
              <TableRow key={sat.id}>
                <TableCell>{sat.name}</TableCell>
                <TableCell>{sat.metal}</TableCell>
                <TableCell>{sat.crystal}</TableCell>
                <TableCell>{sat.narion}</TableCell>
                <TableCell>{sat.production_time}</TableCell>
                <TableCell>
                  <TextField
                    type="number"
                    size="small"
                    value={quantities[sat.id] || ''}
                    onChange={e => handleQuantityChange(sat.id, e.target.value)}
                    inputProps={{ min: 0 }}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Grid container spacing={2} mt={2}>
          <Grid item><Button variant="contained" onClick={handleProduce}>Produce</Button></Grid>
        </Grid>
        <Table sx={{ mt: 2 }}>
          <TableBody>
            <TableRow>
              <TableCell><b>Available</b></TableCell>
              <TableCell>{resources.metal}</TableCell>
              <TableCell>{resources.crystal}</TableCell>
              <TableCell>{resources.narion}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><b>Costs</b></TableCell>
              <TableCell>{costs.metal}</TableCell>
              <TableCell>{costs.crystal}</TableCell>
              <TableCell>{costs.narion}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default SatelliteProduction;