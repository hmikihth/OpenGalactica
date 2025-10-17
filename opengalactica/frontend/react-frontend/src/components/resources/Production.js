import React, { useEffect, useState } from 'react';
import { Typography, Table, TableHead, TableRow, TableCell, TableBody, Paper, TableContainer } from '@mui/material';
import api from '../../utils/api';

const Production = () => {
  const [productionData, setProductionData] = useState(null);

  useEffect(() => {
    const fetchProduction = async () => {
      try {
        const response = await api.get('resource-production');
        setProductionData(response.data);
      } catch (error) {
        console.error('Failed to fetch production data:', error);
      }
    };

    fetchProduction();
  }, []);

  const columns = ['Type', 'Plasmators', 'Plasmator Income', 'Planet Income', 'Minister', 'Tax', 'Net Income', 'Gross Income'];

  const formatRow = (key, data) => (
    <TableRow key={key}>
      <TableCell>{data.resource_type || key}</TableCell>
      <TableCell>{data.amount}</TableCell>
      <TableCell>{data.plasmator_income}</TableCell>
      <TableCell>{data.planet_income}</TableCell>
      <TableCell>{data.minister}</TableCell>
      <TableCell>{data.tax}</TableCell>
      <TableCell>{data.net_income}</TableCell>
      <TableCell>{data.gross_income}</TableCell>
    </TableRow>
  );

  return (
    <>
      <Typography variant="h6" gutterBottom>
        Production
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={col}>{col}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {productionData &&
              ['metal', 'crystal', 'narion', 'neutral'].map((resource) =>
                formatRow(resource, productionData[resource])
              )}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

export default Production;
