// frontend/components/ShipScrapping.js

import React, { useState, useEffect } from 'react';
import {
  Card, CardContent, Typography, Grid, Button,
  TextField, Select, MenuItem, Table, TableHead, TableRow, TableCell, TableBody
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const ShipScrapping = ({ endpoint = 'ship-scrap/owned' }) => {
  const [ships, setShips] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [materials, setMaterials] = useState({ metal: 0, crystal: 0, narion: 0 });

  useEffect(() => {
    api.get(endpoint).then(res => setShips(res.data));
  }, []);

  const selectedShip = ships.find(ship => ship.ship_model === selectedId);
  console.log(selectedShip);

  useEffect(() => {
    if (selectedShip && quantity > 0) {
      const metal = Math.floor(selectedShip.metal * quantity * 0.5);
      const crystal = Math.floor(selectedShip.crystal * quantity * 0.5);
      const narion = Math.floor(selectedShip.narion * quantity * 0.5);
      setMaterials({ metal, crystal, narion });
    } else {
      setMaterials({ metal: 0, crystal: 0, narion: 0 });
    }
  }, [selectedShip, quantity]);

  const handleScrap = () => {
    api.post('ship-scrap/scrap/', { ship_model: selectedId, quantity }, {
      headers: { 'X-CSRFToken': getCSRFToken() }
    })
      .then(() => window.location.reload())
      .catch(err => alert(err.response?.data?.detail || 'Error during scrapping'));
  };

  return (
    <Card sx={{ width: '100%', my: 2 }}>
      <CardContent>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Select value={selectedId} onChange={e => setSelectedId(e.target.value)} displayEmpty>
              <MenuItem value="" disabled>Select unit</MenuItem>
              {ships.map(ship => (
                <MenuItem key={ship.id} value={ship.ship_model}>
                  {ship.ship_model_name} (You have: {ship.quantity})
                </MenuItem>
              ))}
            </Select>
          </Grid>
          <Grid item>
            <TextField
              type="number"
              label="Quantity"
              value={quantity}
              onChange={e => setQuantity(parseInt(e.target.value) || '')}
              inputProps={{ min: 1, max: selectedShip?.quantity || undefined }}
              size="small"
            />
          </Grid>
          <Grid item>
            <Button variant="contained" color="error" onClick={handleScrap} disabled={!selectedId || !quantity}>
              Scrap
            </Button>
          </Grid>
        </Grid>

        <Table sx={{ mt: 3 }}>
          <TableHead>
            <TableRow>
              <TableCell>Metal</TableCell>
              <TableCell>Crystal</TableCell>
              <TableCell>Narion</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>{materials.metal}</TableCell>
              <TableCell>{materials.crystal}</TableCell>
              <TableCell>{materials.narion}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default ShipScrapping;
