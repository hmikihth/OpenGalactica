import React from 'react';
import { AppBar, Toolbar, IconButton, Button } from '@mui/material';
import Grid from '@mui/material/Grid2';
import MenuIcon from '@mui/icons-material/Menu';
import LogoutIcon from '@mui/icons-material/Logout';

import StatusButtonGroup from './StatusButtonGroup';
import StatusButton from './StatusButton';

const appBarHeight = 64; // Height of the AppBar
const headerHeight = 180; // Height of the Header

const NavAppBar = ({ toggleModal, isMobile }) => {
  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        top: isMobile ? 0 : headerHeight,
        height: appBarHeight,
        bgcolor: '#333333',
      }}
    >
      <Toolbar>
        {isMobile ? ( <div></div>) : (
            <IconButton color="inherit" aria-label="open drawer" edge="start" onClick={toggleModal} sx={{ mr: 2 }}>
              <MenuIcon /> &nbsp; Menu
            </IconButton>
        )}
        <Grid container sx={{ minWidth: '80vw', margin: 'auto' }}>
          <Grid size={10}>
            <StatusButtonGroup />
          </Grid>
          <Grid size={2}>
          
              <StatusButton
                icon={<LogoutIcon />}
                label="Logout"
                color="error"
                isMobile={isMobile}
              />

          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
};

export default NavAppBar;
