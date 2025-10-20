import React from 'react';
import { Grid } from '@mui/material';
import CardWrapper from '../CardWrapper';

import News from './News';
import Communication from './Communication';
import Database from './Database';
import MinistersMessage from './MinistersMessage';
import AllianceNews from './AllianceNews';
import Voting from './Voting';
import FleetsStatus from './FleetsStatus';
import Technology from './Technology';
import Plasmators from './Plasmators';
import PDS from './PDS';
import Satellites from './Satellites';
import Ships from './Ships';

const mobileSections = [
    { component: <Communication />},
    { component: <News />},
    { component: <AllianceNews />},
    { component: <MinistersMessage />},
    { component: <FleetsStatus />},
    { component: <Technology />},
    { component: <PDS />},
    { component: <Plasmators />},
    { component: <Satellites />},
    { component: <Database />},
    { component: <Ships />},
    { component: <Voting />},
  ];

const MobileGrid = () => (
  <Grid container spacing={3} sx={{ padding: 1 }}>
    {mobileSections.map((section, index) => (
      <Grid key={index} item xs={12} sx={{ display: 'flex' }}>
        <CardWrapper>{section.component}</CardWrapper>
      </Grid>
    ))}
  </Grid>
);

export default MobileGrid;