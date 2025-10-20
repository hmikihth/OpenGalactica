import React, { useEffect, useState } from 'react';

import {
  Box,
  Tab,
  Tabs,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
} from '@mui/material';

import NotifContentFormatter from './NotifContentFormatter';

import api from '../utils/api';


const tabLabels = ['All', 'War', 'Probe', 'Research', 'Building', 'Production', 'News'];

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [tabIndex, setTabIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('notifications/').then(res => {
      setNotifications(res.data.results || []);
    }).finally(() => setLoading(false));
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);
  };

  const getFilteredNotifications = () => {
    const selectedType = tabLabels[tabIndex];
    if (selectedType === 'All') return notifications;
    return notifications.filter((n) => n.ntype === selectedType);
  };

  const renderTable = (data) => (
    <TableContainer component={Paper}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell><strong>Type</strong></TableCell>
            <TableCell><strong>Content</strong></TableCell>
            <TableCell><strong>Read</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((notif) => (
            <TableRow key={notif.id}>
              <TableCell>{notif.round}:{notif.turn}:{new Date(notif.server_time).getSeconds()}</TableCell>
              <TableCell>{notif.ntype}</TableCell>
              <TableCell>
                <NotifContentFormatter ntype={notif.ntype} content={notif.content} />
              </TableCell>
              <TableCell>{notif.read ? 'Yes' : 'No'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Tabs value={tabIndex} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
        {tabLabels.map((label, index) => (
          <Tab key={index} label={label} />
        ))}
      </Tabs>

      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          {tabLabels[tabIndex]} Notifications
        </Typography>
        {renderTable(getFilteredNotifications())}
      </Box>
    </Box>
  );
};

export default Notifications;
