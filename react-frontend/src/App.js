import React, { useState, useEffect } from 'react';
import { withTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { BrowserRouter as Router } from 'react-router-dom';
import { Typography, CircularProgress } from '@mui/material';

import NavBox from './components/NavBox';
import './App.css';

import api from './utils/api';

const App = ({ t }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authChecked, setAuthChecked] = useState(false);
  
  useEffect(() => {
    document.title = 'OpenGalactica';
    const checkAuthStatus = async () => {
      try {
        const response = await api.get('auth/status/', { withCredentials: true });
        setIsAuthenticated(response.data.is_authenticated);
      } catch (error) {
        console.error('Failed to check auth status:', error);
        setIsAuthenticated(false);
      } finally {
        setAuthChecked(true); // ✅ Mark as checked
      }
    };

    checkAuthStatus();
  }, []);

  if (!authChecked) {
    return <Typography>Loading...<CircularProgress /></Typography>;
  }
  
  return (
    <Router>
      <div className="App">
        <Helmet>
          <script type="text/javascript" id="hs-script-loader" async defer src="//js.hs-scripts.com/43861621.js"></script>
          <title>{t('app_title')}</title>
          <meta name="description" content={t('app_description')} />
        </Helmet>
        <NavBox isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
      </div>
    </Router>
  );
};

export default withTranslation()(App);
