import React from "react";
import { Box, Typography, Grid, Avatar, Link, Tooltip } from "@mui/material";

const speciesIcons = {
  Digitrox: "/icons/digitrox.png", // Replace with the actual path to your icons
  Human: "/icons/human.png",
  Khaduuii: "/icons/khaduuii.png",
  Piraati: "/icons/piraati.png",
  Shin: "/icons/shin.png",
  Zyk: "/icons/zyk.png",
};

const toplists = [
  { name: "Planets", path: "/toplist/planet" },
  { name: "Sols", path: "/toplist/sols" },
  { name: "Alliances", path: "/toplist/alliances" },
  { name: "Species", path: "/toplist/species" },
  { name: "Plasmators", path: "/toplist/plasmators" },
  { name: "XP", path: "/toplist/xp" },
];

const guidelines = [
  { name: "Regulations", path: "/regulations" },
  { name: "Knowledge base", path: "/knowledge-base" },
  { name: "Encyclopedia", path: "/encyclopedia" },
];

const Database = () => {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Database
      </Typography>

      {/* Ship Details Section */}
      <Typography variant="subtitle1" gutterBottom>
        Ship Details:
      </Typography>
      <Grid container justifyContent="center" spacing={2}>
        {Object.entries(speciesIcons).map(([species, iconPath]) => (
          <Grid item key={species}>
            <Tooltip title={species} arrow>
              <Link
                href={`/ship-details/${species.toLowerCase()}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Avatar
                  src={iconPath}
                  alt={species}
                  sx={{
                    width: 32,
                    height: 32,
                    border: "1px solid #ccc",
                  }}
                />
              </Link>
            </Tooltip>
          </Grid>
        ))}
      </Grid>

      {/* Toplists Section */}
      <Typography variant="subtitle1" gutterBottom sx={{ marginTop: 2 }}>
        Toplists:
      </Typography>
      <Grid container spacing={1}>
        {toplists.map((item) => (
          <Grid item xs={6} sm={4} key={item.name}>
            <Link href={item.path} target="_blank" rel="noopener noreferrer">
              {item.name}
            </Link>
          </Grid>
        ))}
      </Grid>

      {/* Guidelines Section */}
      <Typography variant="subtitle1" gutterBottom sx={{ marginTop: 2 }}>
        Guidelines:
      </Typography>
      <Grid container spacing={1}>
        {guidelines.map((item) => (
          <Grid item xs={6} sm={4} key={item.name}>
            <Link href={item.path} target="_blank" rel="noopener noreferrer">
              {item.name}
            </Link>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Database;
