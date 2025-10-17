import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from '@mui/material';
import api from '../../utils/api';

const ShipProductionLine = ({ endpoint = 'ship-production/line/' }) => {
  const [lines, setLines] = useState({});

  useEffect(() => {
    api.get(endpoint).then(res => setLines(res.data));
  }, []);

  const turns = Array.from({ length: 16 }, (_, i) => i + 1);

  return (
    <Card sx={{ width: '100%' }}>
      <CardContent>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell><strong>Ship</strong></TableCell>
                {turns.map(turn => (
                  <TableCell key={turn} align="center">{turn}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.entries(lines).map(([name, turnData]) => (
                <TableRow key={name}>
                  <TableCell>{name}</TableCell>
                  {turns.map(turn => (
                    <TableCell key={turn} align="center">
                      {turnData[String(turn)] || ''}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
};

export default ShipProductionLine;
