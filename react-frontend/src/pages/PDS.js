import React from 'react';
import { Container, Card, CardHeader, CardContent, Box } from '@mui/material';

import ShipProduction from '../components/ships/ShipProduction';
import ShipProductionLine from '../components/ships/ShipProductionLine';
import ShipScrapping from '../components/ships/ShipScrapping';

const PDS = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Production */}
      <Card sx={{ mb: 4 }}>
        <CardHeader title="PDS Production" />
        <CardContent>
          <ShipProduction endpoint="ship-production/pds-available" />
        </CardContent>
      </Card>

      {/* Production Line */}
      <Card sx={{ mb: 4 }}>
        <CardHeader title="PDS production Line" />
        <CardContent>
          <ShipProductionLine endpoint="ship-production/pds-line" />
        </CardContent>
      </Card>

      {/* Scrapping */}
      <Card>
        <CardHeader title="PDS Scrapping" />
        <CardContent>
          <ShipScrapping endpoint="ship-scrap/pds-owned" />
        </CardContent>
      </Card>
    </Container>
  );
};

export default PDS;
