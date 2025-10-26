import React, { useEffect, useState } from "react";
import { Box, Grid, Typography, Paper, CircularProgress } from "@mui/material";

import api from '../../utils/api';

const Satellites = () => {
  const [satelliteData, setSatelliteData] = useState([]);
  const [totalSatellites, setTotalSatellites] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSatelliteData = async () => {
      try {
        const response = await api.get("satellites/");
        setSatelliteData(response.data);

        // Calculate the total number of satellites
        const total = response.data.reduce((sum, item) => sum + item.quantity, 0);
        setTotalSatellites(total);
      } catch (e) {
        setError(e);
        console.error("Error fetching satellites data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSatelliteData();
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
        Satellites ({totalSatellites})
      </Typography>
      <Grid container spacing={2}>
        {satelliteData.map((satellite) => (
          <Grid item xs={6} key={satellite.id}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>{satellite.name}</strong>
              </Typography>
              <Typography variant="body2">{satellite.quantity}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Satellites;
