import React from 'react';
import { AppBar, Toolbar, IconButton, Button } from '@mui/material';
import Grid from '@mui/material/Grid2';
import MenuIcon from '@mui/icons-material/Menu';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import { useNavigate } from 'react-router-dom';

import StatusButtonGroup from './StatusButtonGroup';

import api from '../../utils/api';

import Cookies from 'js-cookie';


const appBarHeight = 64; // Height of the AppBar
const headerHeight = 180; // Height of the Header


const NavAppBar = ({ toggleModal, isMobile, isAuthenticated, setIsAuthenticated }) => {
  const navigate = useNavigate();

  const handleLogout = async (e) => {
    e.preventDefault();
    try {
      await api.post('auth/logout/', {}, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
          },
      });
      setIsAuthenticated(false);
      window.location.href = '/';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleLoginRedirect = () => {
    navigate('/login');
  };

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
        {isMobile ? (
          <div></div>
        ) : (
          <IconButton color="inherit" aria-label="open drawer" edge="start" onClick={toggleModal} sx={{ mr: 2 }}>
            <MenuIcon /> &nbsp; Menu
          </IconButton>
        )}
        <Grid container sx={{ minWidth: '80vw', margin: 'auto' }}>
          <Grid size={10}>
            <StatusButtonGroup />
          </Grid>
          <Grid size={2} display="flex" justifyContent="flex-end" alignItems="center">
            {isAuthenticated ? (
              isMobile ? (
                <IconButton color="error" onClick={handleLogout}>
                  <LogoutIcon />
                </IconButton>
              ) : (
                <Button
                  color="error"
                  variant="contained"
                  startIcon={<LogoutIcon />}
                  onClick={handleLogout}
                >
                  Logout
                </Button>
              )
            ) : (
              isMobile ? (
                <IconButton color="success" onClick={handleLoginRedirect}>
                  <LoginIcon />
                </IconButton>
              ) : (
                <Button
                  color="success"
                  variant="contained"
                  startIcon={<LoginIcon />}
                  onClick={handleLoginRedirect}
                >
                  Login
                </Button>
              )
            )}
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
};

export default NavAppBar;
