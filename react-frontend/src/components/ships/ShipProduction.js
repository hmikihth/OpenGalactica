import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Button,
  Grid
} from '@mui/material';
import api from "../../utils/api";
import { getCSRFToken } from "../../utils/csrf";

const ShipProduction = ({ endpoint = 'ship-production/available' }) => {
  const [ships, setShips] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [resources, setResources] = useState({ metal: 0, crystal: 0, narion: 0 });
  const [costs, setCosts] = useState({ metal: 0, crystal: 0, narion: 0, points: 0 });

  useEffect(() => {
    api.get(endpoint).then(res => setShips(res.data));
    api.get('planet').then(res => setResources(res.data));
  },[]);

  const handleQuantityChange = (shipId, value) => {
    const q = parseInt(value || 0);
    const newQuantities = { ...quantities, [shipId]: q };
    setQuantities(newQuantities);

    const newCosts = ships.reduce(
      (acc, ship) => {
        const quantity = newQuantities[ship.id] || 0;
        acc.metal += ship.metal * quantity;
        acc.crystal += ship.crystal * quantity;
        acc.narion += ship.narion * quantity;
        acc.points += parseInt((ship.metal + ship.crystal + ship.narion) * quantity * 0.1);
        return acc;
      },
      { metal: 0, crystal: 0, narion: 0, points: 0 }
    );
    setCosts(newCosts);
  };

  const handleProduce = () => {
      const payload = Object.entries(quantities)
        .filter(([_, qty]) => qty > 0)
        .map(([ship_model, quantity]) => ({
          ship_model: parseInt(ship_model),
          quantity,
        }));

      api.post('ship-production/produce/', payload, {
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
      })
        .then(() => window.location.reload())
        .catch(err => alert(err.response?.data?.detail || 'Error producing ships'));
  };

  return (
    <Card sx={{ width: '100%' }}>
      <CardContent>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Ship</TableCell>
                <TableCell>Class</TableCell>
                <TableCell>Target 1</TableCell>
                <TableCell>Target 2</TableCell>
                <TableCell>Target 3</TableCell>
                <TableCell>Metal</TableCell>
                <TableCell>Crystal</TableCell>
                <TableCell>Narion</TableCell>
                <TableCell>Production Time</TableCell>
                <TableCell>Produced</TableCell>
                <TableCell>To Produce</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {ships.map(ship => (
                <TableRow key={ship.id}>
                  <TableCell>{ship.name}</TableCell>
                  <TableCell>{ship.ship_class}</TableCell>
                  <TableCell>{ship.target1}</TableCell>
                  <TableCell>{ship.target2}</TableCell>
                  <TableCell>{ship.target3}</TableCell>
                  <TableCell>{ship.metal}</TableCell>
                  <TableCell>{ship.crystal}</TableCell>
                  <TableCell>{ship.narion}</TableCell>
                  <TableCell>{ship.production_time}</TableCell>
                  <TableCell>{ship.produced || 0}</TableCell>
                  <TableCell>
                    <TextField
                      type="number"
                      value={quantities[ship.id] || ''}
                      onChange={e => handleQuantityChange(ship.id, e.target.value)}
                      inputProps={{ min: 0 }}
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Grid container spacing={2} mt={2}>
          <Grid item>
            <Button variant="contained" color="primary" onClick={handleProduce}>Produce</Button>
          </Grid>
        </Grid>

        <Table sx={{ mt: 4 }}>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              <TableCell>Metal</TableCell>
              <TableCell>Crystal</TableCell>
              <TableCell>Narion</TableCell>
              <TableCell>Points</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell><b>Available</b></TableCell>
              <TableCell>{resources.metal}</TableCell>
              <TableCell>{resources.crystal}</TableCell>
              <TableCell>{resources.narion}</TableCell>
              <TableCell></TableCell>
            </TableRow>
            <TableRow>
              <TableCell><b>Costs</b></TableCell>
              <TableCell>{costs.metal}</TableCell>
              <TableCell>{costs.crystal}</TableCell>
              <TableCell>{costs.narion}</TableCell>
              <TableCell>{costs.points}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default ShipProduction;
