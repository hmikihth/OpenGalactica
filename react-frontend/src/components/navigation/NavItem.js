import React from 'react';
import { Box, Typography } from '@mui/material';

const NavItem = ({ url, label, icon, onClick }) => {
  const handleRedirect = () => {
    if (onClick) onClick(); // Optional: Call any additional logic before redirecting
    window.location.href = url; // Redirect to the specified URL
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        cursor: 'pointer',
        m: 1,
      }}
      onClick={handleRedirect}
    >
      {React.cloneElement(icon, { fontSize: 'medium' })} {/* Render the icon with specified fontSize */}
      <Typography variant="body2">{label}</Typography>
    </Box>
  );
};

export default NavItem;
