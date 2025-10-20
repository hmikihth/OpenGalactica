import React, { useEffect, useState } from "react";
import MobileTableCell from "../../components/MobileTableCell";
import { Box, Grid, Typography, Paper, CircularProgress } from "@mui/material";
import api from '../../utils/api';

const PDS = () => {
  const [pdsData, setPdsData] = useState([]);
  const [totalPDS, setTotalPDS] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPDSData = async () => {
      try {
        const response = await api.get("pds/");
        setPdsData(response.data);

        // Calculate the total number of PDS
        const total = response.data.reduce((sum, item) => sum + item.quantity, 0);
        setTotalPDS(total);
      } catch (error) {
        console.error("Error fetching PDS data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPDSData();
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
        PDS ({totalPDS})
      </Typography>
      <Grid container spacing={2}>
        {pdsData.map((pds) => (
          <Grid item xs={6} key={pds.id}>
            <Paper variant="outlined" sx={{ padding: 1 }}>
              <Typography variant="body1">
                <strong>{pds.name}</strong>
              </Typography>
              <Typography variant="body2">{pds.quantity}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default PDS;
