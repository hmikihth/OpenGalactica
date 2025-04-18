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
  CircularProgress
} from '@mui/material';

const Messages = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [receivedMessages, setReceivedMessages] = useState([]);
  const [sentMessages, setSentMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);
  };

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const [receivedRes, sentRes] = await Promise.all([
          fetch('/api/v1/messages/received/'),
          fetch('/api/v1/messages/sent/'),
        ]);

        const receivedData = await receivedRes.json();
        const sentData = await sentRes.json();

        setReceivedMessages(receivedData);
        setSentMessages(sentData);
      } catch (error) {
        console.error('Failed to fetch messages:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, []);

  const renderTable = (ttype, messages) => (
    <TableContainer component={Paper}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell><strong>Time</strong></TableCell>
            <TableCell><strong>{ttype=='received'?'Sender':'Receiver'}</strong></TableCell>
            <TableCell><strong>Alliance</strong></TableCell>
            <TableCell><strong>Title</strong></TableCell>
            <TableCell><strong>Read</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {messages.map((msg) => (
            <TableRow key={msg.id}>
              <TableCell>{msg.round}:{msg.turn}:{new Date(msg.server_time).getSeconds()}</TableCell>
              <TableCell>{ttype=='received'?msg.sender:msg.receiver}</TableCell>
              <TableCell>{msg.alliance ?? '-'}</TableCell>
              <TableCell>{msg.title}</TableCell>
              <TableCell>{msg.read ? 'Yes' : 'No'}</TableCell>
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
      <Tabs value={tabIndex} onChange={handleTabChange} centered>
        <Tab label="Received" />
        <Tab label="Sent" />
      </Tabs>

      <Box sx={{ mt: 2 }}>
        {tabIndex === 0 && (
          <>
            <Typography variant="h6" gutterBottom>
              Received Messages
            </Typography>
            {renderTable('received', receivedMessages)}
          </>
        )}

        {tabIndex === 1 && (
          <>
            <Typography variant="h6" gutterBottom>
              Sent Messages
            </Typography>
            {renderTable('sent', sentMessages)}
          </>
        )}
      </Box>
    </Box>
  );
};

export default Messages;
