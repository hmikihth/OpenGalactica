import React from "react";
import { Paper, Typography } from "@mui/material";

const History = () => (
  <Paper sx={{ p: 2 }}>
    <Typography variant="h6" gutterBottom>
      Game History
    </Typography>
    <Typography variant="body2" color="text.secondary">
      The OpenGalactica universe began in 2023 as a small experimental project
      and has evolved into a large multiplayer strategy game where every
      player’s decision shapes the galaxy.
    </Typography>
  </Paper>
);

export default History;
