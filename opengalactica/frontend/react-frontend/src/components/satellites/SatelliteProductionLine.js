// SatelliteProduction.js
import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Table, TableHead, TableRow, TableCell, TableContainer,
  TableBody, TextField, Button, Grid, Select, MenuItem
} from '@mui/material';
import api from '../../utils/api';
import { getCSRFToken } from '../../utils/csrf';

const SatelliteProductionLine = () => {
  const [lines, setLines] = useState([]);

  useEffect(() => {
    api.get('satellite-production/line/').then(res => {
      const obj = res.data;
      if (obj && typeof obj === 'object' && !Array.isArray(obj) && Object.keys(obj).length > 0) {
        setLines(obj);
      } else {
        setLines({});
      }
  
    });
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

export default SatelliteProductionLine;