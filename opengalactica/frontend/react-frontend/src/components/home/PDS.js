import React, { useEffect, useState } from "react";
import MobileTableCell from "../../components/MobileTableCell";
import { Box, Grid, Typography, Paper } from "@mui/material";

const PDS = () => {
  const [pdsData, setPdsData] = useState([]);
  const [totalPDS, setTotalPDS] = useState(0);

  useEffect(() => {
    const fetchPDSData = async () => {
      try {
        const response = await fetch("/api/v1/pds/");
        if (response.ok) {
          const data = await response.json();
          setPdsData(data);

          // Calculate the total number of PDS
          const total = data.reduce((sum, item) => sum + item.quantity, 0);
          setTotalPDS(total);
        } else {
          console.error("Failed to fetch PDS data");
        }
      } catch (error) {
        console.error("Error fetching PDS data:", error);
      }
    };

    fetchPDSData();
  }, []);

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
