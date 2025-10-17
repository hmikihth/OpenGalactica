import React from 'react';
import { Card, CardContent } from '@mui/material';

const CardWrapper = ({ children }) => (
  <Card elevation={3} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
    <CardContent sx={{ flexGrow: 1 }}>
      {children}
    </CardContent>
  </Card>
);

export default CardWrapper;