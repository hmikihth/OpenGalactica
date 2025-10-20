import React from 'react';
import {
  Modal,
  Box,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Collapse,
  Divider,
} from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPersonDigging , faIndustry, faShuttleSpace, faNoteSticky } from '@fortawesome/free-solid-svg-icons';
import {
  Forum as ForumIcon,
  Science as ScienceIcon,
  DirectionsBoat as FleetIcon,
  Public as PlanetIcon,
  SolarPower as SolIcon,
  Groups as AllianceIcon,
  AttachMoney as CreditsIcon,
  Article as NewsIcon,
  Article as NotificationsIcon,
  Message as MessagesIcon,
  LocalShipping as ShipsIcon,
  Shield as PDSIcon,
  Satellite as SatellitesIcon,
  Explore as ExploreIcon,
  AccountBalance as TreasuryIcon,
  Security as DefenseIcon,
  Gavel as DiplomacyIcon,
  AccountCircle as ProfileIcon,
  Timeline as StatusIcon,
  AddCircle as ExtraIcon,
  History as HistoryIcon,
  Notifications as RemindersIcon,
  Home as HomeIcon
} from '@mui/icons-material';

import NavItem from './NavItem';

const sections = [
  {
    name: 'Communication',
    icon: <ForumIcon />,
    children: [
      { name: 'Notifications', icon: <NotificationsIcon />, url: '/notifications' },
      { name: 'Messages', icon: <MessagesIcon />, url: '/messages' },
      { name: 'Forum', icon: <ForumIcon /> },
      { name: 'Notes', icon: <FontAwesomeIcon icon={faNoteSticky} size="lg" />, url: '/notes' },
    ],
  },
  {
    name: 'Production',
    icon: <FontAwesomeIcon icon={faIndustry} size="lg" />,
    children: [
      { name: 'Ships', icon: <ShipsIcon />, url: '/ships' },
      { name: 'PDS', icon: <PDSIcon />, url: '/pds' },
      { name: 'Satellites', icon: <SatellitesIcon />, url: '/satellites' },
    ],
  },
  {
    name: 'Fleet',
    icon: <FontAwesomeIcon icon={faShuttleSpace} size="lg" />,
    children: [
      { name: 'Control', icon: <FleetIcon />, url: '/fleet/control' },
      { name: 'Exploring', icon: <ExploreIcon />, url: '/fleet/exploring' },
    ],
  },
  {
    name: 'Sol',
    icon: <SolIcon />,
    children: [
      { name: 'Profile', icon: <ProfileIcon />, url: '/sol/profile' },
      { name: 'Politics', icon: <DiplomacyIcon />, url: '/sol/politics' },
      { name: 'Forum', icon: <ForumIcon />, url: '/sol/forum' },
      { name: 'Temp', icon: <ExploreIcon />, url: '/sol/temp' },
      { name: 'Status', icon: <StatusIcon />, url: '/sol/status' },
    ],
  },
  {
    name: 'Alliance',
    icon: <AllianceIcon />,
    children: [
      { name: 'Profile', icon: <ProfileIcon />, url: '/alliance/profile' },
      { name: 'Members', icon: <AllianceIcon />, url: '/alliance/members' },
      { name: 'Voting', icon: <DiplomacyIcon />, url: '/alliance/voting' },
      { name: 'Diplomacy', icon: <DiplomacyIcon />, url: '/alliance/diplomacy' },
      { name: 'Forum', icon: <ForumIcon />, url: '/alliance/forum' },
      { name: 'Treasury', icon: <TreasuryIcon />, url: '/alliance/treasury' },
      { name: 'Research', icon: <ScienceIcon />, url: '/alliance/research' },
      { name: 'Exploring', icon: <ExploreIcon />, url: '/alliance/exploring' },
      { name: 'Defense', icon: <DefenseIcon />, url: '/alliance/defense' },
      { name: 'Attack', icon: <FleetIcon />, url: '/alliance/attack' },
      { name: 'Status', icon: <StatusIcon />, url: '/alliance/status' },
    ],
  },
  { 
    name: 'Credits', 
    icon: <CreditsIcon />, 
    children: [
      { name: 'Info', icon: <NewsIcon /> },
      { name: 'Charge', icon: <CreditsIcon /> },
      { name: 'History', icon: <HistoryIcon /> },
      { name: 'Extra', icon: <ExtraIcon /> },
      { name: 'Alliance Extra', icon: <ExtraIcon /> },
      { name: 'Reminders', icon: <RemindersIcon /> },
  ],
},
];

const MainMenuModal = ({isMobile, isOpen, onClose }) => {
  const [openSections, setOpenSections] = React.useState({});

  const toggleSection = (section) => {
    setOpenSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  return (
    <Modal open={isOpen} onClose={onClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: isMobile ? '80%' : '50%',
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
          borderRadius: 2,
          maxHeight: '80vh',
          overflowY: 'auto',
        }}
      >

        {!isMobile && (
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 2, mb: 2 }}>
            <NavItem url='/' label='Home' icon={<HomeIcon />} />
            <NavItem url='/resources' label='Resources' icon={<FontAwesomeIcon icon={faPersonDigging} size="lg" />} />
            <NavItem url='/research' label='Research' icon={<ScienceIcon />} />
            <NavItem url='/planet' label='Planet' icon={<PlanetIcon />} />
          </Box>
        )}
        
        <List>
        {sections.map(({ name, icon, children }) => (
          <React.Fragment key={name}>
            <Divider />
            <ListItem disablePadding>
              <ListItemButton onClick={() => toggleSection(name)}>
                <ListItemIcon>{icon}</ListItemIcon>
                <Typography>{name}</Typography>
                {openSections[name] ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
            </ListItem>
            <Collapse in={openSections[name]} timeout="auto" unmountOnExit>
              <Box sx={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', 
               gap: 2, mt: 1 }}>
                {children.map(({ name: childName, icon: childIcon, url: childUrl }) => (
                  <NavItem key={childName} url={childUrl} label={childName} icon={childIcon} />
                ))}
              </Box>
            </Collapse>
          </React.Fragment>
        ))}
      </List>
      </Box>
    </Modal>
  );
};

export default MainMenuModal;
