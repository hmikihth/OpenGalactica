import React from "react";
import { Paper, Typography, Grid } from "@mui/material";

const ScoreChanges = () => (
  <Paper sx={{ p: 3, mt: 3 }}>
    <Typography variant="h5" gutterBottom>
      Recent Score Changes
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={12} md={6}>
        <Typography variant="body2" color="text.secondary">
          Planet Vega Prime gained 12,000 points.
        </Typography>
      </Grid>
      <Grid item xs={12} md={6}>
        <Typography variant="body2" color="text.secondary">
          Alliance Star Lords lost 3,200 points.
        </Typography>
      </Grid>
    </Grid>
  </Paper>
);

export default ScoreChanges;
