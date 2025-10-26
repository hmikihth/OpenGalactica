import React from 'react';
import { Container, Card } from '@mui/material';

import Market from '../components/resources/Market';
import Probes from '../components/resources/Probes';
import Production from '../components/resources/Production';
import Sending from '../components/resources/Sending';
import Starting from '../components/resources/Starting';
import Storages from '../components/resources/Storages';


const sections = [
    { component: <Production />},
    { component: <Storages />},
    { component: <Probes />},
    { component: <Starting />},
    { component: <Sending />},
    { component: <Market />},
  ];
  
  
const Resources = () => (
<Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>

    {sections.map((section, index) => (
      <Card sx={{ mb: 4 }}>
        {section.component}
      </Card>
    ))}
</Container>

);

export default Resources;
