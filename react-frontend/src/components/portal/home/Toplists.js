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
} from "@mui/material";
import api from "../../../utils/api";

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
        const [planetRes, solRes, allianceRes, speciesRes, xpRes, plasmatorRes] = await Promise.all([
          api.get("toplist/planet/"),
          api.get("toplist/sol/"),
          api.get("toplist/alliance/"),
          api.get("toplist/species/"),
          api.get("toplist/xp/"),
          api.get("toplist/plasmator/"),
        ]);

        setData({
          planets: planetRes.data.slice(0, 8),
          sols: solRes.data.slice(0, 8),
          alliances: allianceRes.data.slice(0, 8),
          species: speciesRes.data.slice(0, 8),
          xp: xpRes.data.slice(0, 8),
          plasmators: plasmatorRes.data.slice(0, 8),
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

  const renderTable = (title, rows, columns) => (
    <Grid item xs={12} md={6}>
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                {columns.map((col) => (
                  <TableCell key={col}>{col}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.length > 0 ? (
                rows.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{row.name || row.planet_name || "Unknown"}</TableCell>
                    <TableCell align="right">
                      {row.score || row.points || row.total_points || 0}
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
      {renderTable("Planets", data.planets, ["#", "Planet", "Score"])}
      {renderTable("Sols", data.sols, ["#", "Sol", "Score"])}
      {renderTable("Alliances", data.alliances, ["#", "Alliance", "Score"])}
      {renderTable("Species", data.species, ["#", "Species Leader", "Score"])}
      {renderTable("XP", data.xp, ["#", "Player", "XP"])}
      {renderTable("Plasmators", data.plasmators, ["#", "Player", "Plasmators"])}
    </Grid>
  );
};

export default Toplists;
