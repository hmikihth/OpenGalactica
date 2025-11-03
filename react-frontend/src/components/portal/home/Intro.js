import React from "react";
import { Paper, Typography } from "@mui/material";

const Intro = () => (
  <Paper sx={{ p: 3, mb: 3 }}>
    <Typography variant="h4" gutterBottom>
      Welcome to OpenGalactica
    </Typography>
    <Typography variant="body1">
      Explore the vastness of space, form alliances, and conquer galaxies. Join
      thousands of players in the OpenGalactica universe.
    </Typography>
  </Paper>
);

export default Intro;
