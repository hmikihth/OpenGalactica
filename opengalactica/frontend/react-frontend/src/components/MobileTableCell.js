import React from 'react';
import { TableCell } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

const MobileTableCell = ({ children, sx }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <TableCell sx={{ fontSize: isMobile ? '0.4rem' : '1rem', ...sx }}>
      {children}
    </TableCell>
  );
};

export default MobileTableCell;
