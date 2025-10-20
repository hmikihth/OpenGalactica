import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, Slider, Typography, Box, TextField
} from '@mui/material';

const SwapShipDialog = ({ open, onClose, maxQuantity, fleets, onSubmit }) => {
  const [quantity, setQuantity] = useState(0);

  useEffect(() => {
    if (open) {
      setQuantity(maxQuantity);
    }
  }, [open, maxQuantity]);

  const handleQuantityChange = (val) => {
    const newVal = Math.max(0, Math.min(maxQuantity, val));
    setQuantity(newVal);
  };

  const handleFleetSelect = (targetFleetId) => {
    if (quantity > 0) {
      onSubmit(quantity, targetFleetId);
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Move Ships</DialogTitle>
      <DialogContent>
        <Typography gutterBottom>Select Quantity:</Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Slider
            value={quantity}
            min={0}
            max={maxQuantity}
            step={1}
            marks
            valueLabelDisplay="auto"
            onChange={(e, val) => handleQuantityChange(val)}
            sx={{ flex: 1 }}
          />
          <TextField
            label="Quantity"
            type="number"
            size="small"
            value={quantity}
            inputProps={{ min: 0, max: maxQuantity }}
            onChange={(e) => handleQuantityChange(parseInt(e.target.value) || 0)}
            sx={{ width: '80px' }}
          />
        </Box>

        <Typography sx={{ mt: 2 }}>Select Target Fleet:</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
          {fleets.map(fleet => (
            <Button
              key={fleet.id}
              variant="contained"
              size="small"
              disabled={quantity === 0}
              onClick={() => handleFleetSelect(fleet.id)}
            >
              {fleet.name}
            </Button>
          ))}
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
};

export default SwapShipDialog;
