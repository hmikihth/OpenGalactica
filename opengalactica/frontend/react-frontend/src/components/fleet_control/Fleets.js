import React, { useEffect, useState } from 'react';
import { Card, CardContent, Table, TableHead, TableRow, TableCell, TableBody, Typography, Button } from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

import SwapShipDialog from './SwapShipDialog';


const FcFleets = () => {
  const [ships, setShips] = useState([]);
  const [fleets, setFleets] = useState([]);
  const [fuelCosts, setFuelCosts] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  const [maxQuantity, setMaxQuantity] = useState(null);
  
  useEffect(() => {
    api.get('fleet-control/fleet-list/').then(res => setFleets(res.data));
    api.get('fleet-control/ships/').then(res => setShips(res.data));
    api.get('fleet-control/fuel-costs/').then(res => setFuelCosts(res.data));
  }, []);

  const openSwapDialog = (fleetId, max_quantity, ship) => {
    setSelected({ fleetId, ship });
    setMaxQuantity(max_quantity);
    setDialogOpen(true);
  };

  const handleTransfer = (quantity, targetFleetId) => {
    api.post('fleet-control/swap-ship/', {
      source_fleet_id: selected.fleetId,
      target_fleet_id: targetFleetId,
      ship_model_id: selected.ship.id,
      quantity: quantity,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      }
    }).then(() => {
      api.get('fleet-control/ships/').then(res => setShips(res.data));
      api.get('fleet-control/fuel-costs/').then(res => setFuelCosts(res.data));
    });
    setDialogOpen(false);
  };
  
  return (
    <>
      <Card sx={{ my: 2 }}>
        <CardContent>
          <Typography variant="h6">Fleets</Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Ship Name</TableCell>
                <TableCell>Class</TableCell>
                <TableCell>#1</TableCell>
                <TableCell>#2</TableCell>
                <TableCell>#3</TableCell>
                <TableCell>Base</TableCell>
                <TableCell>Fleet 1</TableCell>
                <TableCell>Fleet 2</TableCell>
                <TableCell>Fleet 3</TableCell>
                <TableCell>Fleet 4</TableCell>
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
                  <TableCell>
                      <Button
                        size="small"
                        onClick={() => openSwapDialog(ship.base_id, ship.base, { ...ship, id: ship.id })}
                        disabled={ship.base <= 0}
                      >
                        {ship.base}
                      </Button>
                  </TableCell>
                  <TableCell>
                      <Button
                        size="small"
                        onClick={() => openSwapDialog(ship.fleet1_id, ship.fleet1, { ...ship, id: ship.id })}
                        disabled={ship.fleet1 <= 0}
                      >
                        {ship.fleet1}
                      </Button>
                  </TableCell>
                  <TableCell>
                      <Button
                        size="small"
                        onClick={() => openSwapDialog(ship.fleet2_id, ship.fleet2, { ...ship, id: ship.id })}
                        disabled={ship.fleet2 <= 0}
                      >
                        {ship.fleet2}
                      </Button>
                  </TableCell>
                  <TableCell>
                      <Button
                        size="small"
                        onClick={() => openSwapDialog(ship.fleet3_id, ship.fleet3, { ...ship, id: ship.id })}
                        disabled={ship.fleet3 <= 0}
                      >
                        {ship.fleet3}
                      </Button>
                  </TableCell>
                  <TableCell>
                      <Button
                        size="small"
                        onClick={() => openSwapDialog(ship.fleet4_id, ship.fleet4, { ...ship, id: ship.id })}
                        disabled={ship.fleet4 <= 0}
                      >
                        {ship.fleet4}
                      </Button>
                  </TableCell>
                </TableRow>
              ))}
              {fuelCosts.map(row => (
                <TableRow key={row.name}>
                  <TableCell></TableCell>
                  <TableCell colSpan="2">{row.name}</TableCell>
                  <TableCell colSpan="2">
                    Fuel cost <br/>
                    Distance
                  </TableCell>
                  <TableCell>
                    - <br/> -
                  </TableCell>
                  <TableCell>
                    {row.fleet1_fuel || '-'} <br/>
                    {row.fleet1_distance || '-'}
                  </TableCell>
                  <TableCell>
                    {row.fleet2_fuel || '-'} <br/>
                    {row.fleet2_distance || '-'}
                  </TableCell>
                  <TableCell>
                    {row.fleet3_fuel || '-'} <br/>
                    {row.fleet3_distance || '-'}
                  </TableCell>
                  <TableCell>
                    {row.fleet4_fuel || '-'} <br/>
                    {row.fleet4_distance || '-'}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {selected && (
        <SwapShipDialog
          open={dialogOpen}
          onClose={() => setDialogOpen(false)}
          maxQuantity={maxQuantity}
          fleets={fleets}
          onSubmit={handleTransfer}
        />
      )}
      
    </>
  );
};

export default FcFleets;