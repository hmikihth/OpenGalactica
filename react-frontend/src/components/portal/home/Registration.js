import React from "react";
import { Paper, Typography, Button } from "@mui/material";

const Registration = () => (
  <Paper sx={{ p: 2, mb: 3 }}>
    <Typography variant="h6" gutterBottom>
      Join the Universe
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
      Register now and start building your planet today.
    </Typography>
    <Button variant="contained" color="primary">
      Register
    </Button>
  </Paper>
);

export default Registration;
