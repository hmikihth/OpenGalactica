import React from 'react';
import { Box, CssBaseline, useMediaQuery, useTheme } from '@mui/material';
import { styled } from '@mui/system';
import { Routes, Route } from 'react-router-dom';

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

import Toplist from '../pages/portal/Toplist';
import Encyklopedia from '../pages/portal/Encyklopedia';
import Support from '../pages/portal/Support';


const drawerIconsWidth = 60;
const appBarHeight = 64;
const headerHeight = 180;

const MainContent = styled('main')(({ theme, isMobile, open }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  marginLeft: isMobile ? 0: drawerIconsWidth,
  marginTop: isMobile ? appBarHeight : headerHeight + appBarHeight,
}));

export default function NavBox() {
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
          <Header />
        </Box>
      )}

      {/* Spacing Box for Header */}
      <Box sx={{ height: isMobile ? 0 : headerHeight }} />

      {/* AppBar */}
      <NavAppBar toggleModal={toggleModal} isMobile={isMobile} />

      <MainMenuModal isMobile={isMobile} isOpen={open} onClose={handleCloseModal} />
   
      
      {isMobile ? (
        <BottomNav isMobile={isMobile} handleOpenModal={handleOpenModal} />
      ) : (
        <br />
      )}


      
      {/* Main Content */}
      <MainContent isMobile={isMobile} open={open}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/research" element={<Research />} />
          <Route path="/ships" element={<Ships />} />
          <Route path="/pds" element={<PDS />} />
          <Route path="/satellites" element={<Satellites />} />
          <Route path="/fleet/control" element={<FleetControl />} />
          <Route path="/fleet/exploring" element={<Exploring />} />
          <Route path="/planet" element={<Planet />} />
          <Route path="/messages" element={<Messages />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/notes" element={<Notes />} />
          
          <Route path="/sol/profile" element={<SolProfile />} />
          <Route path="/sol/politics" element={<SolPolitics />} />
          <Route path="/sol/forum" element={<SolForum />} />
          <Route path="/sol/status" element={<SolStatus />} />
          <Route path="/sol/temp" element={<TempSol />} />
          
          <Route path="/alliance/profile" element={<AllianceProfile />} />
          <Route path="/alliance/members" element={<AllianceMembers />} />
          <Route path="/alliance/forum" element={<AllianceForum />} />
          <Route path="/alliance/status" element={<AllianceStatus />} />
          <Route path="/alliance/attack" element={<AllianceAttack />} />
          <Route path="/alliance/defense" element={<AllianceDefense />} />
          <Route path="/alliance/diplomacy" element={<AllianceDiplomacy />} />
          <Route path="/alliance/exploring" element={<AllianceExploring />} />
          <Route path="/alliance/research" element={<AllianceResearch />} />
          <Route path="/alliance/treasury" element={<AllianceTreasury />} />
          <Route path="/alliance/voting" element={<AllianceVoting />} />
          
          <Route path="/credits/info" element={<CreditsInfo />} />
          <Route path="/credits/charge" element={<CreditsCharge />} />
          <Route path="/credits/history" element={<CreditsHistory />} />
          <Route path="/credits/extra" element={<CreditsExtra />} />
          <Route path="/credits/alliance-extra" element={<CreditsAlliance />} />
          <Route path="/credits/reminders" element={<CreditsReminders />} />

          <Route path="/portal/toplist" element={<Toplist />} />
          <Route path="/portal/news" element={<News />} />
          <Route path="/portal/encyklopedia" element={<Encyklopedia />} />
          <Route path="/portal/support" element={<Support />} />

          </Routes>
      </MainContent>
    </Box>
  );
}
