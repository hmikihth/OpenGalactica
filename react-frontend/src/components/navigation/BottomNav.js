import React, { useState } from 'react';
import { BottomNavigation, BottomNavigationAction, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ScienceIcon from '@mui/icons-material/Science';
import PlanetIcon from '@mui/icons-material/Public';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPersonDigging } from '@fortawesome/free-solid-svg-icons';


const BottomNav = ({ isMobile, handleOpenModal, value = 0, onChange = () => {} }) => {

  return (
    <Paper
      sx={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 1300,
      }}
      elevation={3}
    >
      <BottomNavigation
        value={value}
        onChange={(event, newValue) => onChange(newValue)}
        showLabels
      >
        <BottomNavigationAction label="Home" icon={<HomeIcon />} component={Link} to="/" />
        <BottomNavigationAction label="Resources" icon={<FontAwesomeIcon icon={faPersonDigging} size="lg" />} component={Link} to="/resources" />
        <BottomNavigationAction label="Research" icon={<ScienceIcon />} component={Link} to="/research" />
        <BottomNavigationAction label="Planet" icon={<PlanetIcon />} component={Link} to="/planet" />
        <BottomNavigationAction label="More" icon={<MoreHorizIcon />} onClick={handleOpenModal} />
      </BottomNavigation>


    </Paper>
  );
};

export default BottomNav;
