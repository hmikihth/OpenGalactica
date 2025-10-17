import React from 'react';
import { Button } from '@mui/material';

const StatusButton = ({ icon, label, color, isMobile, href }) => {
  return (
    <Button
      color={color}
      sx={{
        flex: 1,
        display: 'flex',
        flexDirection: isMobile ? 'column' : 'row',
        alignItems: 'center',
        justifyContent: isMobile ? 'center' : 'flex-start',
        textAlign: isMobile ? 'center' : 'left',
        fontSize: '0.7em',
      }}
      href={href}
    >
      {React.cloneElement(icon, { style: { marginRight: isMobile ? 0 : 8 } })}
      {!isMobile && label}
    </Button>
  );
};

export default StatusButton;
