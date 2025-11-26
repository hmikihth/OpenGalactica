import React, { useEffect, useState } from "react";
import {
  Paper,
  Typography,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Avatar,
} from "@mui/material";
import api from "../../../utils/api";

import SpeciesAvatar from "../../SpeciesAvatar";

const rankColor = (rank) => {
  switch (rank) {
    case 1:
      return "#d4af37";
    case 2:
      return "#c0c0c0";
    case 3:
      return "#cd7f32";
    default:
      return "#888";
  }
};

// Species → Color mapping
const speciesColor = {
  Human: "#3f51b5",      // blue
  Digitrox: "#4caf50",   // green
  Khaduuii: "#ffeb3b",   // yellow
  Shin: "#f44336",       // red
  Zyk: "#a1887f",        // light brown
  Piraati: "#9c27b0",    // purple
};

// Avatar renderer
const renderSpeciesAvatar = (species) => {
  if (!species) return null;

  return (
    <Avatar
      sx={{
        width: 24,
        height: 24,
        fontSize: "0.75rem",
        bgcolor: speciesColor[species] || "#888",
        color: "#fff",
        display: "inline-flex",
        mr: 1,
      }}
    >
      {species[0]}
    </Avatar>
  );
};

const Toplists = () => {
  const [data, setData] = useState({
    planets: [],
    sols: [],
    alliances: [],
    species: [],
    xp: [],
    plasmators: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchToplists = async () => {
      try {
        const [
          planetRes,
          solRes,
          allianceRes,
          speciesRes,
          xpRes,
          plasmatorRes,
        ] = await Promise.all([
          api.get("toplist/planet/"),
          api.get("toplist/sol/"),
          api.get("toplist/alliance/"),
          api.get("toplist/species/"),
          api.get("toplist/xp/"),
          api.get("toplist/plasmator/"),
        ]);

        setData({
          planets: planetRes.data.slice(0, 10),
          sols: solRes.data.slice(0, 10),
          alliances: allianceRes.data.slice(0, 10),
          species: speciesRes.data.slice(0, 10),
          xp: xpRes.data.slice(0, 10),
          plasmators: plasmatorRes.data.slice(0, 10),
        });
      } catch (error) {
        console.error("Error fetching toplists:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchToplists();
  }, []);

  if (loading) return <CircularProgress />;

  const renderTable = (title, rows, fields) => (
    <Grid item xs={12} md={6}>
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>#</TableCell>
                <TableCell>Name</TableCell>
                <TableCell align="right">{fields.label}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.length > 0 ? (
                rows.map((row, idx) => (
                  <TableRow key={idx}>
                    <TableCell
                      sx={{
                        fontWeight: 700,
                        color: rankColor(row.rank),
                      }}
                    >
                      {row.rank}
                    </TableCell>

                    <TableCell sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <SpeciesAvatar species={row.species} />
                      {row.name}
                    </TableCell>

                    <TableCell align="right">
                      {row[fields.key]}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No data
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Grid>
  );

  return (
    <Grid container spacing={2}>
      {renderTable("Planets", data.planets, { key: "points", label: "Score" })}
      {renderTable("Sols", data.sols, { key: "points", label: "Score" })}
      {renderTable("Alliances", data.alliances, { key: "points", label: "Score" })}
      {renderTable("Species Leaders", data.species, { key: "points", label: "Score" })}
      {renderTable("XP Ranking", data.xp, { key: "xp", label: "XP" })}
      {renderTable("Plasmators", data.plasmators, { key: "total_plasmators", label: "Plasmators" })}
    </Grid>
  );
};

export default Toplists;
