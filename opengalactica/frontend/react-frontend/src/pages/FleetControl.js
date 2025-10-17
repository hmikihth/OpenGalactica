import React from 'react';
import { Container } from '@mui/material';

import FleetSettings from "../components/fleet_control/FleetSettings";
import Strategy from "../components/fleet_control/Strategy";
import FleetControl from "../components/fleet_control/FleetControl";
import FcFleets from "../components/fleet_control/Fleets";

const FleetControlPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <FcFleets />
      <FleetControl />
      <Strategy />
      <FleetSettings />
    </Container>  
  );
};

export default FleetControlPage;
