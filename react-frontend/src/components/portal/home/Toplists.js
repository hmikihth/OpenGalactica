import React from "react";
import { Paper, Typography } from "@mui/material";

const Toplists = () => (
  <Paper sx={{ p: 2, mb: 3 }}>
    <Typography variant="h6" gutterBottom>
      Toplists
    </Typography>
    <Typography variant="body2" color="text.secondary">
      - Planet: Vega Prime (1,234,567 pts) <br />
      - Alliance: Star Lords (12,345,678 pts) <br />
      - Sol: Solis (98,765,432 pts)
    </Typography>
  </Paper>
);

export default Toplists;
