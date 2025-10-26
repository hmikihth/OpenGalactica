import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  useMediaQuery,
} from '@mui/material';

import api from '../../utils/api';

import { useTheme } from '@mui/material/styles';


const groupByTarget = (fleets) => {
  const groups = {};
  for (const fleet of fleets) {
    const target = fleet.target;
    if (!groups[target]) groups[target] = [];
    groups[target].push(fleet);
  }
  return groups;
};

const groupByOwner = (fleets) => {
  const groups = {};
  for (const fleet of fleets) {
    const owner = fleet.owner;
    if (!groups[owner]) groups[owner] = [];
    groups[owner].push(fleet);
  }
  return groups;
};

const calculateGroupTotals = (group) => {
  let attackers = 0;
  let defenders = 0;
  group.forEach((fleet) => {
    if (fleet.role === 'Attackers') attackers += fleet.ships;
    else if (fleet.role === 'Defenders') defenders += fleet.ships;
  });
  return { attackers, defenders };
};

const IncomingTable = ({ title, fleets }) => {
  const grouped = groupByTarget(fleets);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box component={Paper} p={2} mb={4} sx={{ backgroundColor: '#121212' }}>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        {title}
      </Typography>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell sx={{ color: 'white' }}>Species</TableCell>
            <TableCell sx={{ color: 'white' }}>Origin</TableCell>
            <TableCell sx={{ color: 'white' }}>Alliance</TableCell>
            <TableCell sx={{ color: 'white' }}>Points</TableCell>
            <TableCell sx={{ color: 'white' }}>Ships</TableCell>
            <TableCell sx={{ color: 'white' }}>Distance</TableCell>
            <TableCell sx={{ color: 'white' }}>Arrival</TableCell>
            {!isMobile && <TableCell sx={{ color: 'white' }}>Destination</TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(grouped).map(([target, group], index) => {
            const sortedGroup = [...group].sort((a, b) => {
              if (a.role === b.role) return a.owner.localeCompare(b.owner);
              return a.role === 'Attackers' ? -1 : 1;
            });
            const totals = calculateGroupTotals(group);
            return (
              <React.Fragment key={index}>
                {isMobile && (
                  <TableRow>
                    <TableCell colSpan={7} sx={{ color: 'white', fontWeight: 'bold' }}>
                      Destination: {target}
                    </TableCell>
                  </TableRow>
                )}

                {sortedGroup.map((fleet, i) => (
                  <TableRow
                    key={i}
                    sx={{ backgroundColor: fleet.role === 'Attackers' ? '#b71c1c' : '#1b5e20' }}
                  >
                    <TableCell sx={{ color: 'white' }}>{fleet.species}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.owner}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.alliance}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.points}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.ships}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.distance}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.arrival}</TableCell>
                    {!isMobile && <TableCell sx={{ color: 'white' }}>{fleet.target}</TableCell>}
                  </TableRow>
                ))}

                <TableRow>
                  <TableCell colSpan={4} sx={{ color: 'white', fontStyle: 'italic' }}>
                    Total:
                  </TableCell>
                  <TableCell colSpan={4} sx={{ color: 'white', fontStyle: 'italic' }}>
                    {totals.attackers} / {totals.defenders}
                  </TableCell>
                </TableRow>
              </React.Fragment>
            );
          })}
        </TableBody>
      </Table>
    </Box>
  );
};

const OutgoingTable = ({ title, fleets }) => {
  const grouped = groupByOwner(fleets);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box component={Paper} p={2} mb={4} sx={{ backgroundColor: '#121212' }}>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        {title}
      </Typography>

      <Table>
        <TableHead>
          <TableRow>
            {!isMobile && <TableCell sx={{ color: 'white' }}>Origin</TableCell>}
            <TableCell sx={{ color: 'white' }}>Ships</TableCell>
            <TableCell sx={{ color: 'white' }}>Distance</TableCell>
            <TableCell sx={{ color: 'white' }}>Arrival</TableCell>
            <TableCell sx={{ color: 'white' }}>Species</TableCell>
            <TableCell sx={{ color: 'white' }}>Destination</TableCell>
            <TableCell sx={{ color: 'white' }}>Alliance</TableCell>
            <TableCell sx={{ color: 'white' }}>Points</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(grouped).map(([origin, group], index) => {
            const sortedGroup = [...group].sort((a, b) => {
              if (a.role === b.role) return a.target.localeCompare(b.target);
              return a.role === 'Attackers' ? -1 : 1;
            });
            const totals = calculateGroupTotals(group);
            return (
              <React.Fragment key={index}>
                {isMobile && (
                  <TableRow>
                    <TableCell colSpan={7} sx={{ color: 'white', fontWeight: 'bold' }}>
                      Origin: {origin}
                    </TableCell>
                  </TableRow>
                )}

                {sortedGroup.map((fleet, i) => (
                  <TableRow
                    key={i}
                    sx={{ backgroundColor: fleet.role === 'Attackers' ? '#b71c1c' : '#1b5e20' }}
                  >
                    {!isMobile && <TableCell sx={{ color: 'white' }}>{fleet.owner}</TableCell>}
                    <TableCell sx={{ color: 'white' }}>{fleet.ships}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.distance}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.arrival}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.species}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.target}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.alliance}</TableCell>
                    <TableCell sx={{ color: 'white' }}>{fleet.points}</TableCell>
                  </TableRow>
                ))}

                <TableRow>
                  <TableCell colSpan={1} sx={{ color: 'white', fontStyle: 'italic' }}>
                    Total:
                  </TableCell>
                  <TableCell colSpan={7} sx={{ color: 'white', fontStyle: 'italic' }}>
                    {totals.attackers} / {totals.defenders}
                  </TableCell>
                </TableRow>
              </React.Fragment>
            );
          })}
        </TableBody>
      </Table>
    </Box>
  );
};

const SolStatus = () => {
  const [incoming, setIncoming] = useState([]);
  const [outgoing, setOutgoing] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFleets = async () => {
      try {
        const [incRes, outRes] = await Promise.all([
          api.get('sol/incoming/'),
          api.get('sol/outgoing/'),
        ]);
        setIncoming(incRes.data);
        setOutgoing(outRes.data);
      } catch (err) {
        setError('Failed to load sol fleet data.');
      } finally {
        setLoading(false);
      }
    };
    fetchFleets();
  }, []);

  if (loading) {
    return <Typography sx={{ color: 'white' }}>Loading...</Typography>;
  }

  if (error) {
    return <Typography sx={{ color: 'red' }}>{error}</Typography>;
  }

  
  return (
    <Box p={2}>
      <IncomingTable title="Incoming Fleets" fleets={incoming} />
      <OutgoingTable title="Outgoing Fleets" fleets={outgoing} />
    </Box>
  );
};

export default SolStatus;
