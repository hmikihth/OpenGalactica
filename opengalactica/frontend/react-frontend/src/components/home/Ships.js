import React, { useEffect, useState } from "react";
import MobileTableCell from "../../components/MobileTableCell";
import { Box, Grid, Typography, Paper } from "@mui/material";

const Ships = () => {
  const [shipsData, setShipsData] = useState([]);
  const [totalShips, setTotalShips] = useState(0);

  useEffect(() => {
    const fetchShipsData = async () => {
      try {
        const response = await fetch("/api/v1/ships/");
        if (response.ok) {
          const data = await response.json();
          setShipsData(data);

          // Calculate the total number of ships
          const total = data.reduce((sum, item) => sum + item.quantity, 0);
          setTotalShips(total);
        } else {
          console.error("Failed to fetch ships data");
        }
      } catch (error) {
        console.error("Error fetching ships data:", error);
      }
    };

    fetchShipsData();
  }, []);

  return (
    <Box>
      <Typography variant="h6" component="div" gutterBottom>
        Ships ({totalShips})
      </Typography>
      <Grid container spacing={2}>
        {shipsData.map((ship) => (
          <Grid item xs={6} key={ship.id}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>{ship.name}</strong>
              </Typography>
              <Typography variant="body2">{ship.quantity}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Ships;
