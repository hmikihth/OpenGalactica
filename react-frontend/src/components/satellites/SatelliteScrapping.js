import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Table, TableHead, TableRow, TableCell,
  TableBody, TextField, Button, Grid, Select, MenuItem
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const SatelliteScrapping = () => {
  const [stock, setStock] = useState([]);
  const [selected, setSelected] = useState('');
  const [quantity, setQuantity] = useState(0);
  const [materials, setMaterials] = useState({ metal: 0, crystal: 0, narion: 0 });

  useEffect(() => {
    api.get('satellite-production/scrappable/').then(res => setStock(res.data));
  }, []);

  useEffect(() => {
    const sat = stock.find(s => s.id === selected);
    if (sat) {
      const q = parseInt(quantity || 0);
      setMaterials({
        metal: sat.metal * q * 0.5,
        crystal: sat.crystal * q * 0.5,
        narion: sat.narion * q * 0.5
      });
    } else {
      setMaterials({ metal: 0, crystal: 0, narion: 0 });
    }
  }, [selected, quantity, stock]);

  const handleScrap = () => {
    api.post('satellite-production/scrap/', { satellite_type: selected, quantity }, {
      headers: { 'X-CSRFToken': getCSRFToken() }
    }).then(() => window.location.reload());
  };

  return (
    <Card sx={{ my: 2 }}>
      <CardContent>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Select
              size="small"
              value={selected}
              onChange={e => setSelected(e.target.value)}
              displayEmpty
            >
              <MenuItem value="" disabled>Select Satellite</MenuItem>
              {stock.map(s => (
                <MenuItem key={s.id} value={s.id}>{s.name} ({s.quantity})</MenuItem>
              ))}
            </Select>
          </Grid>
          <Grid item>
            <TextField
              type="number"
              size="small"
              label="Quantity"
              value={quantity}
              onChange={e => setQuantity(e.target.value)}
              inputProps={{ min: 0 }}
            />
          </Grid>
          <Grid item>
            <Button variant="outlined" onClick={handleScrap}>Scrap</Button>
          </Grid>
        </Grid>
        <Table sx={{ mt: 2 }}>
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

export default SatelliteScrapping;