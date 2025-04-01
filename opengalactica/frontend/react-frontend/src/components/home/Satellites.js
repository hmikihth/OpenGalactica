import React, { useEffect, useState } from "react";
import MobileTableCell from "../../components/MobileTableCell";
import { Box, Grid, Typography, Paper } from "@mui/material";

const Satellites = () => {
  const [satelliteData, setSatelliteData] = useState([]);
  const [totalSatellites, setTotalSatellites] = useState(0);

  useEffect(() => {
    const fetchSatelliteData = async () => {
      try {
        const response = await fetch("/api/v1/satellites/");
        if (response.ok) {
          const data = await response.json();
          setSatelliteData(data);

          // Calculate the total number of satellites
          const total = data.reduce((sum, item) => sum + item.quantity, 0);
          setTotalSatellites(total);
        } else {
          console.error("Failed to fetch satellites data");
        }
      } catch (error) {
        console.error("Error fetching satellites data:", error);
      }
    };

    fetchSatelliteData();
  }, []);

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
