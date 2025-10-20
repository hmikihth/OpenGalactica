import React, { useEffect, useState } from "react";
import MobileTableCell from "../../components/MobileTableCell";
import { Box, Grid, Typography, Paper, CircularProgress } from "@mui/material";

import api from '../../utils/api';

const Ships = () => {
  const [shipsData, setShipsData] = useState([]);
  const [totalShips, setTotalShips] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchShipsData = async () => {
      try {
        const response = await api.get("ships/");
        setShipsData(response.data);

        // Calculate the total number of ships
        const total = response.data.reduce((sum, item) => sum + item.quantity, 0);
        setTotalShips(total);
      } catch (error) {
        console.error("Error fetching ships data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchShipsData();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }
  
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
