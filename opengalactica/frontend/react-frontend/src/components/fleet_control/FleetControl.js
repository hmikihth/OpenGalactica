import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  TextField, Button, Select, MenuItem
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const FleetControl = () => {
  const [fleets, setFleets] = useState([]);
  const [taskInputs, setTaskInputs] = useState({});

  useEffect(() => {
    api.get('fleet-control/').then(res => setFleets(res.data));
  }, []);

  const handleInputChange = (fleetId, field, value) => {
    setTaskInputs(prev => ({
      ...prev,
      [fleetId]: {
        ...(prev[fleetId] || {}),
        [field]: value
      }
    }));
  };

  const sendTask = (fleet) => {
    const input = taskInputs[fleet.id] || {};
    const payload = {
      action: input.action,
      x: input.x,
      y: input.y,
      z: input.z,
    };
    api.post(`fleet-control/${fleet.id}/task/`, payload, {
      headers: { 'X-CSRFToken': getCSRFToken() }
    }).then(() => window.location.reload());
  };

  const recallFleet = (fleetId) => {
    api.post(`fleet-control/${fleetId}/callback/`, {}, {
      headers: { 'X-CSRFToken': getCSRFToken() }
    }).then(() => window.location.reload());
  };

  return (
    <Card sx={{ my: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Fleet Control</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Fleet</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Task</TableCell>
              <TableCell>X</TableCell>
              <TableCell>Y</TableCell>
              <TableCell>Z</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {fleets.map(fleet => (
              <TableRow key={fleet.id}>
                <TableCell>{fleet.name}</TableCell>
                <TableCell>{fleet.status_display}</TableCell>
                <TableCell>
                  {!["move","return"].includes(fleet.task) ? (
                    <Select
                      size="small"
                      value={(taskInputs[fleet.id]?.action) || ''}
                      onChange={e => handleInputChange(fleet.id, 'action', e.target.value)}
                      displayEmpty
                    >
                      <MenuItem value="" disabled>Set Task</MenuItem>
                      <MenuItem value="attack1">Attack - 1 turn</MenuItem>
                      <MenuItem value="attack2">Attack - 2 turns</MenuItem>
                      <MenuItem value="attack3">Attack - 3 turns</MenuItem>
                      <MenuItem value="defend1">Defend - 1  turn</MenuItem>
                      <MenuItem value="defend2">Defend - 2  turns</MenuItem>
                      <MenuItem value="defend3">Defend - 3  turns</MenuItem>
                      <MenuItem value="defend4">Defend - 4  turns</MenuItem>
                      <MenuItem value="defend5">Defend - 5  turns</MenuItem>
                      <MenuItem value="defend6">Defend - 6  turns</MenuItem>
                    </Select>
                  ) : (
                    <Typography>{fleet.task_display}</Typography>
                  )}
                </TableCell>
                <TableCell>
                  {!["move","return"].includes(fleet.task) ? (
                  <TextField
                    sx={{minWidth:"50px", maxWidth:"5vw"}}
                    size="small"
                    type="number"
                    value={taskInputs[fleet.id]?.x || ''}
                    onChange={e => handleInputChange(fleet.id, 'x', e.target.value)}
                  />
                  ) : (
                    <Typography>{fleet.x}</Typography>
                  )}
                </TableCell>
                <TableCell>
                  {!["move","return"].includes(fleet.task) ? (
                  <TextField
                    sx={{minWidth:"50px", maxWidth:"5vw"}}
                    size="small"
                    type="number"
                    value={taskInputs[fleet.id]?.y || ''}
                    onChange={e => handleInputChange(fleet.id, 'y', e.target.value)}
                  />
                  ) : (
                    <Typography>{fleet.y}</Typography>
                  )}
                </TableCell>
                <TableCell>
                  {!["move","return"].includes(fleet.task) ? (
                  <TextField
                    sx={{minWidth:"50px", maxWidth:"5vw"}}
                    size="small"
                    type="number"
                    value={taskInputs[fleet.id]?.z || ''}
                    onChange={e => handleInputChange(fleet.id, 'z', e.target.value)}
                  />
                  ) : (
                    <Typography>{fleet.z}</Typography>
                  )}
                </TableCell>
                <TableCell>
                  {["move","return"].includes(fleet.task) ? (
                    fleet.task==="move" ? (
                        <Button variant="outlined" size="small" onClick={() => recallFleet(fleet.id)}>
                          Recall
                        </Button>
                    ) : (
                        <Typography>-</Typography>
                    )
                  ) : (
                    <Button variant="contained" size="small" onClick={() => sendTask(fleet)}>
                      Send
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default FleetControl;
