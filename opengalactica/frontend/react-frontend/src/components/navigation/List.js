/* TODO: Delete this file */

import React from 'react';
import { List, ListItem, ListItemText, ListItemButton, ListItemIcon, Collapse } from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import { 
  Home as HomeIcon, 
  Forum as ForumIcon, 
  Notes as NotesIcon, 
  Science as ScienceIcon, 
  Build as BuildIcon,
  DirectionsBoat as FleetIcon,
  Public as PlanetIcon,
  SolarPower as SolIcon,
  Groups as AllianceIcon,
  AttachMoney as CreditsIcon,
  Article as NewsIcon,
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
} from '@mui/icons-material';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPersonDigging , faIndustry, faShuttleSpace, faNoteSticky } from '@fortawesome/free-solid-svg-icons';

function NavList() {
  const [openSections, setOpenSections] = React.useState({});

  const toggleSection = (section) => {
    setOpenSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const sections = [
    { name: 'Home', icon: <HomeIcon /> },
    { 
      name: 'Communication', 
      icon: <ForumIcon />, 
      children: [
        { name: 'News', icon: <NewsIcon /> },
        { name: 'Messages', icon: <MessagesIcon /> },
        { name: 'Forum', icon: <ForumIcon /> },
        { name: 'Notes', icon: <FontAwesomeIcon icon={faNoteSticky} /> },
      ],
    },
    { name: 'Resources', icon: <FontAwesomeIcon icon={faPersonDigging} /> },
    { name: 'Research', icon: <ScienceIcon /> },
    { 
      name: 'Production', 
      icon: <FontAwesomeIcon icon={faIndustry} />, 
      children: [
        { name: 'Ships', icon: <ShipsIcon /> },
        { name: 'PDS', icon: <PDSIcon /> },
        { name: 'Satellites', icon: <SatellitesIcon /> },
      ],
    },
    { 
      name: 'Fleet', 
      icon: <FontAwesomeIcon icon={faShuttleSpace} />, 
      children: [
        { name: 'Control', icon: <FleetIcon /> },
        { name: 'Exploring', icon: <ExploreIcon /> },
      ],
    },
    { name: 'Planet', icon: <PlanetIcon /> },
    { 
      name: 'Sol', 
      icon: <SolIcon />, 
      children: [
        { name: 'Profile', icon: <ProfileIcon /> },
        { name: 'Politics', icon: <DiplomacyIcon /> },
        { name: 'Forum', icon: <ForumIcon /> },
        { name: 'Temp', icon: <ExploreIcon /> },
        { name: 'Status', icon: <StatusIcon /> },
      ],
    },
    { 
      name: 'Alliance', 
      icon: <AllianceIcon />, 
      children: [
        { name: 'Profile', icon: <ProfileIcon /> },
        { name: 'Members', icon: <AllianceIcon /> },
        { name: 'Voting', icon: <DiplomacyIcon /> },
        { name: 'Diplomacy', icon: <DiplomacyIcon /> },
        { name: 'Forum', icon: <ForumIcon /> },
        { name: 'Treasury', icon: <TreasuryIcon /> },
        { name: 'Research', icon: <ScienceIcon /> },
        { name: 'Exploring', icon: <ExploreIcon /> },
        { name: 'Defense', icon: <DefenseIcon /> },
        { name: 'Attack', icon: <FleetIcon /> },
        { name: 'Status', icon: <StatusIcon /> },
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

  return (
    <List>
      {sections.map(({ name, icon, children }) => (
        <React.Fragment key={name}>
          <ListItem disablePadding>
            <ListItemButton onClick={() => children && toggleSection(name)}>
              <ListItemIcon>{icon}</ListItemIcon>
              <ListItemText primary={name} />
              {children && (openSections[name] ? <ExpandLess /> : <ExpandMore />)}
            </ListItemButton>
          </ListItem>
          {children && (
            <Collapse in={openSections[name]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {children.map(({ name: childName, icon: childIcon }) => (
                  <ListItem key={childName} disablePadding>
                    <ListItemButton sx={{ pl: 3 }}>
                      <ListItemIcon>{childIcon}</ListItemIcon>
                      <ListItemText primary={childName} />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          )}
        </React.Fragment>
      ))}
    </List>
  );
}

export default NavList;
