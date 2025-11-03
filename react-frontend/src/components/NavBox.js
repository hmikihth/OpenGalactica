import React from 'react';
import { Box, CssBaseline, useMediaQuery, useTheme } from '@mui/material';
import { styled } from '@mui/system';
import { Routes, Route } from 'react-router-dom';

import protectedRoute from './navigation/ProtectedRoute';

import Header from './navigation/Header';
import NavAppBar from './navigation/AppBar';
import BottomNav from './navigation/BottomNav';
import MainMenuModal from './navigation/MainMenuModal';

// Import all page components
import Home from '../pages/Home';
import Resources from '../pages/Resources';
import Research from '../pages/Research';
import Ships from '../pages/Ships';
import PDS from '../pages/PDS';
import Satellites from '../pages/Satellites';
import FleetControl from '../pages/FleetControl';
import Exploring from '../pages/Exploring';
import Planet from '../pages/Planet';
import Messages from '../pages/Messages';
import News from '../pages/News';
import Notifications from '../pages/Notifications';
import Notes from '../pages/Notes';
import Login from '../pages/Login';


import SolProfile from '../pages/sol/Profile';
import SolPolitics from '../pages/sol/Politics';
import SolForum from '../pages/sol/Forum';
import SolStatus from '../pages/sol/Status';
import TempSol from '../pages/sol/Temp';

import AllianceProfile from '../pages/alliance/Profile';
import AllianceMembers from '../pages/alliance/Members';
import AllianceForum from '../pages/alliance/Forum';
import AllianceStatus from '../pages/alliance/Status';
import AllianceVoting from '../pages/alliance/Voting';
import AllianceAttack from '../pages/alliance/Attack';
import AllianceDefense from '../pages/alliance/Defense';
import AllianceDiplomacy from '../pages/alliance/Diplomacy';
import AllianceExploring from '../pages/alliance/Exploring';
import AllianceResearch from '../pages/alliance/Research';
import AllianceTreasury from '../pages/alliance/Treasury';

import CreditsInfo from '../pages/credits/Info';
import CreditsCharge from '../pages/credits/Charge';
import CreditsHistory from '../pages/credits/History';
import CreditsExtra from '../pages/credits/Extra';
import CreditsAlliance from '../pages/credits/Alliance';
import CreditsReminders from '../pages/credits/Reminders';

import PortalHome from '../pages/portal/PortalHome';
import Toplist from '../pages/portal/Toplist';
import Encyklopedia from '../pages/portal/Encyklopedia';
import Support from '../pages/portal/Support';


const appBarHeight = 64;
const headerHeight = 180;

const MainContent = styled('main')(({ theme, isMobile, open }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  marginTop: isMobile ? appBarHeight : headerHeight + appBarHeight,
}));

export default function NavBox({ isAuthenticated, setIsAuthenticated }) {
  const [open, setOpen] = React.useState(false);

  const handleOpenModal = () => setOpen(true);
  const handleCloseModal = () => setOpen(false);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const toggleModal = () => {
    setOpen(!open);
  };
  
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      {/* Top Header Section */}
      {!isMobile && (
        <Box
          sx={{
            width: '100%',
            position: 'fixed',
            top: 0,
            height: headerHeight,
            zIndex: (theme) => theme.zIndex.appBar - 1,
            bgcolor: '#888888',
          }}
        >
          {isAuthenticated && (
          <Header />
          )}
        </Box>
      )}

      {/* Spacing Box for Header */}
      <Box sx={{ height: isMobile ? 0 : headerHeight }} />

      {/* AppBar */}
      <NavAppBar 
        toggleModal={toggleModal} 
        isMobile={isMobile}   
        isAuthenticated={isAuthenticated} 
        setIsAuthenticated={setIsAuthenticated} 
      />

      {isAuthenticated && (
      <MainMenuModal isMobile={isMobile} isOpen={open} onClose={handleCloseModal} />
      )}
      
      {isMobile & isAuthenticated ? (
        <BottomNav isMobile={isMobile} handleOpenModal={handleOpenModal} />
      ) : (
        <br />
      )}


      
      {/* Main Content */}
      <MainContent isMobile={isMobile} open={open} sx={{p:0}}>
        <Routes>
            
            {/* PUBLIC ROUTES */}

            <Route
              path="/login"
              element={<Login onLoginSuccess={() => setIsAuthenticated(true)} />}
            />
                        
            <Route path="/portal/" element={<PortalHome />} />
            <Route path="/portal/toplist" element={<Toplist />} />
            <Route path="/portal/news" element={<News />} />
            <Route path="/portal/encyklopedia" element={<Encyklopedia />} />
            <Route path="/portal/support" element={<Support />} />

            
            {/* PROTECTED ROUTES */}
       
            {protectedRoute("/", <Home />, isAuthenticated)}

            {protectedRoute("/resources", <Resources />, isAuthenticated)}
            {protectedRoute("/research", <Research />, isAuthenticated)}
            {protectedRoute("/ships", <Ships />, isAuthenticated)}
            {protectedRoute("/pds", <PDS />, isAuthenticated)}
            {protectedRoute("/satellites", <Satellites />, isAuthenticated)}
            {protectedRoute("/fleet/control", <FleetControl />, isAuthenticated)}
            {protectedRoute("/fleet/exploring", <Exploring />, isAuthenticated)}
            {protectedRoute("/planet", <Planet />, isAuthenticated)}
            {protectedRoute("/messages", <Messages />, isAuthenticated)}
            {protectedRoute("/notifications", <Notifications />, isAuthenticated)}
            {protectedRoute("/notes", <Notes />, isAuthenticated)}
          
            {protectedRoute("/sol/profile", <SolProfile />, isAuthenticated)}
            {protectedRoute("/sol/politics", <SolPolitics />, isAuthenticated)}
            {protectedRoute("/sol/forum", <SolForum />, isAuthenticated)}
            {protectedRoute("/sol/status", <SolStatus />, isAuthenticated)}
            {protectedRoute("/sol/temp", <TempSol />, isAuthenticated)}
          
            {protectedRoute("/alliance/profile", <AllianceProfile />, isAuthenticated)}
            {protectedRoute("/alliance/members", <AllianceMembers />, isAuthenticated)}
            {protectedRoute("/alliance/forum", <AllianceForum />, isAuthenticated)}
            {protectedRoute("/alliance/status", <AllianceStatus />, isAuthenticated)}
            {protectedRoute("/alliance/attack", <AllianceAttack />, isAuthenticated)}
            {protectedRoute("/alliance/defense", <AllianceDefense />, isAuthenticated)}
            {protectedRoute("/alliance/diplomacy", <AllianceDiplomacy />, isAuthenticated)}
            {protectedRoute("/alliance/exploring", <AllianceExploring />, isAuthenticated)}
            {protectedRoute("/alliance/research", <AllianceResearch />, isAuthenticated)}
            {protectedRoute("/alliance/treasury", <AllianceTreasury />, isAuthenticated)}
            {protectedRoute("/alliance/voting", <AllianceVoting />, isAuthenticated)}
          
            {protectedRoute("/credits/info", <CreditsInfo />, isAuthenticated)}
            {protectedRoute("/credits/charge", <CreditsCharge />, isAuthenticated)}
            {protectedRoute("/credits/history", <CreditsHistory />, isAuthenticated)}
            {protectedRoute("/credits/extra", <CreditsExtra />, isAuthenticated)}
            {protectedRoute("/credits/alliance-extra", <CreditsAlliance />, isAuthenticated)}
            {protectedRoute("/credits/reminders", <CreditsReminders />, isAuthenticated)}

          </Routes>
      </MainContent>
    </Box>
  );
}
