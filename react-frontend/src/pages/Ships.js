// src/pages/Ships.js
import React from 'react';
import { Container, Card, CardHeader, CardContent } from '@mui/material';

import ShipProduction from "../components/ships/ShipProduction";
import ShipProductionLine from "../components/ships/ShipProductionLine";
import ShipScrapping from "../components/ships/ShipScrapping";


const Ships = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Production */}
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Ship Production" />
        <CardContent>
          <ShipProduction />
        </CardContent>
      </Card>

      {/* Production Line */}
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Production Line" />
        <CardContent>
          <ShipProductionLine />
        </CardContent>
      </Card>

      {/* Scrapping */}
      <Card>
        <CardHeader title="Ship Scrapping" />
        <CardContent>
          <ShipScrapping />
        </CardContent>
      </Card>
    </Container>
  );
};

export default Ships;
