import React, { useState, useEffect } from 'react';
import { Card, CardContent, TextField, Button, MenuItem, Typography } from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const probeTypes = [
  { value: 'planet', label: 'Planet Probe' },
  { value: 'ship', label: 'Ship Probe' },
  { value: 'defense', label: 'Defense Probe' },
  { value: 'military', label: 'Military Probe' },
  { value: 'information', label: 'Information Probe' },
];

const ProbeLaunching = ({ prefillCoords, onLaunchSuccess }) => {
  const [probeType, setProbeType] = useState('planet');
  const [quantity, setQuantity] = useState(0);
  const [targetCoordinates, setTargetCoordinates] = useState({ x: '', y: '', z: '' });

  const handleLaunch = () => {
    if (!targetCoordinates.x || !targetCoordinates.y || !targetCoordinates.z || !probeType || quantity <= 0) return;

    api.post('exploring/launch_probe/', {
      probe_type: probeType,
      quantity: quantity,
      x: targetCoordinates.x,
      y: targetCoordinates.y,
      z: targetCoordinates.z,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      }
    }).then(() => {
      onLaunchSuccess();
      alert('Probes launched!');
    });
  };

  useEffect(() => {
    if (prefillCoords) {
        const c = prefillCoords.split(':');
        setTargetCoordinates({x:c[0], y:c[1],z:c[2]});
    }
  }, [prefillCoords]);

  return (
    <Card sx={{ my: 2 }}>
      <CardContent>
        <Typography variant="h6">Launch Probe</Typography>

        <TextField
          select
          label="Probe Type"
          value={probeType}
          onChange={e => setProbeType(e.target.value)}
          sx={{ m: 1 }}
        >
          {probeTypes.map((type) => (
            <MenuItem key={type.value} value={type.value}>
              {type.label}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="X"
          type="number"
          value={targetCoordinates.x}
          onChange={e => setTargetCoordinates({...targetCoordinates, x: e.target.value})}
          sx={{ m: 1, width:'80px', maxWidth:'10vw' }}
        />
        <TextField
          label="Y"
          type="number"
          value={targetCoordinates.y}
          onChange={e => setTargetCoordinates({...targetCoordinates, y: e.target.value})}
          sx={{ m: 1, width:'80px', maxWidth:'10vw' }}
        />
        <TextField
          label="Z"
          type="number"
          value={targetCoordinates.z}
          onChange={e => setTargetCoordinates({...targetCoordinates, z: e.target.value})}
          sx={{ m: 1, width:'80px', maxWidth:'10vw' }}
        />


        <TextField
          type="number"
          label="Quantity"
          value={quantity}
          onChange={e => setQuantity(parseInt(e.target.value) || 0)}
          sx={{ mx:3, my: 1, width:'200px', maxWidth:'10vw' }}
        />

        <Button
          variant="contained"
          onClick={handleLaunch}
          disabled={quantity <= 0}
          sx={{ my: 2 }}
        >
          Launch
        </Button>
      </CardContent>
    </Card>
  );
};

export default ProbeLaunching;

