import React from 'react';
import { Container, Card, CardHeader, CardContent} from '@mui/material';

import SatelliteProduction from '../components/satellites/SatelliteProduction';
import SatelliteProductionLine from '../components/satellites/SatelliteProductionLine';
import SatelliteScrapping from '../components/satellites/SatelliteScrapping';


const Satellites = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Production */}
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Satellite Production" />
        <CardContent>
          <SatelliteProduction />
        </CardContent>
      </Card>

      {/* Production Line */}
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Production Line" />
        <CardContent>
          <SatelliteProductionLine />
        </CardContent>
      </Card>

      {/* Scrapping */}
      <Card>
        <CardHeader title="Satellite Scrapping" />
        <CardContent>
          <SatelliteScrapping />
        </CardContent>
      </Card>
    </Container>
  );
};

export default Satellites;
