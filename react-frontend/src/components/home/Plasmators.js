import React, { useEffect, useState } from "react";
import { Box, Grid, Typography, Paper, CircularProgress } from "@mui/material";

import api from '../../utils/api';

const Plasmators = () => {
  const [plasmatorsData, setPlasmatorsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlasmatorsData = async () => {
      try {
        const response = await api.get("plasmators/");
        setPlasmatorsData(response.data);
      } catch (e) {
        setError(e);
        console.error("Error fetching plasmators data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPlasmatorsData();
  });

  
  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  
  return (
    <Box>
      <Typography variant="h6" component="div" gutterBottom>
        Plasmators ({plasmatorsData.total_plasmators})
      </Typography>
      <Grid container spacing={2}>
      
          <Grid item xs={6}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>Metal</strong>
              </Typography>
              <Typography variant="body2">{plasmatorsData.metal_plasmator}</Typography>
            </Paper>
          </Grid>
          
          <Grid item xs={6}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>Crystal</strong>
              </Typography>
              <Typography variant="body2">{plasmatorsData.crystal_plasmator}</Typography>
            </Paper>
          </Grid>
          
          <Grid item xs={6}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>Narion</strong>
              </Typography>
              <Typography variant="body2">{plasmatorsData.narion_plasmator}</Typography>
            </Paper>
          </Grid>
          
          <Grid item xs={6}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>Neutral</strong>
              </Typography>
              <Typography variant="body2">{plasmatorsData.neutral_plasmator}</Typography>
            </Paper>
          </Grid>
          
      </Grid>
    </Box>
  );
};

export default Plasmators;
