/* TODO: Delete this file */

import React from 'react';
import { Drawer } from '@mui/material';

import NavList from './List';

const drawerWidth = 240;
const drawerIconsWidth = 60;
const appBarHeight = 64;
const headerHeight = 180;

const NavDrawer = ({ open, isMobile, theme }) => {

  return (
    <Drawer
      variant="permanent"
      open={open}
      sx={{
        width: open ? drawerWidth : drawerIconsWidth,
        flexShrink: 0,
        position: open ? 'absolute' : 'fixed',
        top: isMobile ? appBarHeight : headerHeight + appBarHeight,
        '& .MuiDrawer-paper': {
          width: open ? drawerWidth : drawerIconsWidth,
          top: isMobile ? appBarHeight : headerHeight + appBarHeight,
          transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          overflowX: 'hidden',
        },
      }}
    >
      <NavList />
    </Drawer>
  );
};

export default NavDrawer;
