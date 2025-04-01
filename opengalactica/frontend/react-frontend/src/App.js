import React, { Component } from 'react';
import { withTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import { BrowserRouter as Router } from 'react-router-dom';
import Button from '@mui/material/Button';

import NavBox from './components/NavBox';
import logo from './logo.svg';
import './App.css';
import i18n from 'i18next';

class App extends Component {
  componentDidMount() {
    document.title = 'OpenGalactica';
  }

  render() {
    const { t } = this.props;

    return (
      <Router>
        <div className="App">
          <Helmet>
            <title>{t('app_title')}</title>
            <meta name="description" content={t('app_description')} />
          </Helmet>
          <NavBox />
{/*
          <Button variant="contained" onClick={() => i18n.changeLanguage('hu')}>Change to Hungarian</Button>
          <Button variant="contained" onClick={() => i18n.changeLanguage('en')}>Change to English</Button>
*/}
        </div>
      </Router>
    );
  }
}

export default withTranslation()(App);
