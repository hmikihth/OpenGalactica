// src/components/PlanetProfile.js
import React from 'react';
import {
  Card, CardHeader, CardContent, Grid, Table, TableBody, TableRow, TableCell,
  Typography, Avatar, Box
} from '@mui/material';

const PlanetProfile = ({ data }) => {
  if (!data) return null;

  const {
    name,
    coordinates,
    species,
    sol,
    alliance,
    plasmators,
    xp,
    slogan,
    profile_image
  } = data;

  return (
    <Card sx={{ maxWidth: 800, mx: 'auto', mt: 5 }}>
      <CardHeader title="Planet Profile" />
      <CardContent>
        <Grid container spacing={3}>
          {/* Left Side Table */}
          <Grid item xs={12} md={6}>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell><strong>Name</strong></TableCell>
                  <TableCell>{name} ({coordinates})</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Species</strong></TableCell>
                  <TableCell>{species}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Sol</strong></TableCell>
                  <TableCell>{sol || '—'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Alliance</strong></TableCell>
                  <TableCell>{alliance || '—'}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Plasmators</strong></TableCell>
                  <TableCell>{plasmators}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>XP</strong></TableCell>
                  <TableCell>{xp}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </Grid>

          {/* Right Side Image + Slogan */}
          <Grid item xs={12} md={6}>
            <Box display="flex" flexDirection="column" alignItems="center">
              {profile_image ? (
                <Avatar
                  src={profile_image}
                  variant="square"
                  alt="Planet Profile"
                  sx={{ width: 150, height: 150, mb: 2 }}
                />
              ) : (
                <Avatar
                  variant="square"
                  sx={{ width: 150, height: 150, mb: 2, bgcolor: 'grey.300' }}
                >
                  N/A
                </Avatar>
              )}
              <Typography variant="subtitle1" align="center">
                {slogan || <em>No slogan set</em>}
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default PlanetProfile;
