import React from 'react';
import { Button } from '@mui/material';

const StatusButton = ({ icon, label, color, isMobile }) => {
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
      }}
    >
      {React.cloneElement(icon, { style: { marginRight: isMobile ? 0 : 8 } })}
      {!isMobile && label}
    </Button>
  );
};

export default StatusButton;
