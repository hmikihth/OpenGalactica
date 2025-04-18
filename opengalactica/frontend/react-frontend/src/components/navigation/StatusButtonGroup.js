import React from 'react';
import { ButtonGroup, useMediaQuery } from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faNewspaper, faEnvelope, faSun } from '@fortawesome/free-solid-svg-icons';
import Diversity3Icon from '@mui/icons-material/Diversity3';
import { useTheme } from '@mui/system';
import StatusButton from './StatusButton';

const StatusButtonGroup = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <ButtonGroup
      variant="contained"
      aria-label="Basic button group"
      sx={{
        width: '90%',
        margin: 'auto',
        display: 'flex',
        gap: 1,
      }}
    >
      <StatusButton
        icon={<FontAwesomeIcon icon={faNewspaper} />}
        label="Notifications"
        color="success"
        isMobile={isMobile}
        href="/notifications"
      />
      <StatusButton
        icon={<FontAwesomeIcon icon={faEnvelope} />}
        label="Messages"
        color="secondary"
        isMobile={isMobile}
        href="/messages"
      />
      <StatusButton
        icon={<FontAwesomeIcon icon={faSun} />}
        label="Sol status"
        color="primary"
        isMobile={isMobile}
        href="/sol/status"
      />
      <StatusButton
        icon={<Diversity3Icon />}
        label="Alliance status"
        color="warning"
        isMobile={isMobile}
        href="/alliance/status"
      />
    </ButtonGroup>
  );
};

export default StatusButtonGroup;
