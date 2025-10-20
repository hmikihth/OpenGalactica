import React from 'react';
import { useMediaQuery, useTheme } from '@mui/material';
import DesktopGrid from '../components/home/DesktopGrid';
import MobileGrid from '../components/home/MobileGrid';

const Home = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return <>{isMobile ? <MobileGrid /> : <DesktopGrid />}</>;
};

export default Home;