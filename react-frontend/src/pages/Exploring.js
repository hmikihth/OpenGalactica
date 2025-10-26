import React, { useState } from 'react';
import { Container } from '@mui/material';

import { useLocation } from 'react-router-dom';
import ProbeLaunching from '../components/exploring/ProbeLaunching';
import ProbeDatabase from '../components/exploring/ProbeDatabase';

const Exploring = () => {
  const location = useLocation();
  const [refresh, setRefresh] = useState(0);
  
  const params = new URLSearchParams(location.search);
  const coords = params.get('coords');

  const handleProbeLaunched = () => {
    setRefresh(prev => prev + 1);  // Triggers ProbeDatabase reload
  };
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <ProbeLaunching prefillCoords={coords}  onLaunchSuccess={handleProbeLaunched} />
      <ProbeDatabase refreshTrigger={refresh} />
    </Container>  
  );
};

export default Exploring;
