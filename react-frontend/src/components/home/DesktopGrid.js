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

const DesktopGrid = () => {
  const oneColumnSections = [
    { component: <Communication /> },
    { component: <MinistersMessage /> },
    { component: <Technology /> },
    { component: <Plasmators /> },
    { component: <Database /> },
    { component: <Voting /> },
  ];

  const twoColumnSections = [
    { component: <News /> },
    { component: <AllianceNews /> },
    { component: <FleetsStatus />, size: 2 },
    { component: <PDS />, size: 2 },
    { component: <Satellites />, size: 2 },
    { component: <Ships />, size: 2 }
  ];

  return (
    <Grid container spacing={3} sx={{ padding: 1, display: 'flex' }}>
      <Grid item xs={12} md={4}>
        <Grid container spacing={3} sx={{display: 'flex', flexDirection: 'column'}}>
          {oneColumnSections.map((section, index) => (
            <Grid key={index} item xs={12} sx={{ display: 'flex' }}>
              <CardWrapper>{section.component}</CardWrapper>
            </Grid>
          ))}
        </Grid>
      </Grid>
      <Grid item xs={12} md={8}>
        <Grid container spacing={3} sx={{display: 'flex', flexWrap: 'wrap'}}>
          {twoColumnSections.map((section, index) => (
            <Grid key={index} item xs={12} sm={section.size === 2 ? 12 : 6} md={section.size === 2 ? 12 : 6} sx={{ display: 'flex' }}> {/*Added size check*/}
              <CardWrapper>{section.component}</CardWrapper>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Grid>
  );
};

export default DesktopGrid;