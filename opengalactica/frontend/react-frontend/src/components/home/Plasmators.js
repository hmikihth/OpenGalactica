import React, { useEffect, useState } from "react";
import MobileTableCell from "../../components/MobileTableCell";
import { Box, Grid, Typography, Paper } from "@mui/material";

const Plasmators = () => {
  const [plasmatorsData, setPlasmatorsData] = useState([]);
  const [totalPlasmators, setTotalPlasmators] = useState(0);

  useEffect(() => {
    const fetchPlasmatorsData = async () => {
      try {
        const response = await fetch("/api/v1/plasmators/");
        if (response.ok) {
          const data = await response.json();
          setPlasmatorsData(data);
          
          console.log(data);
          
        } else {
          console.error("Failed to fetch plasmators data");
        }
      } catch (error) {
        console.error("Error fetching plasmators data:", error);
      }
    };

    fetchPlasmatorsData();
  }, []);

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
