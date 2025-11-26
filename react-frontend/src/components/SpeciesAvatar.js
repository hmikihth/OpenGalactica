// src/components/SpeciesAvatar.js
import React from "react";
import { Avatar, Tooltip } from "@mui/material";

const speciesColors = {
  Human: "#3b82f6",       // Blue
  Digitrox: "#22c55e",    // Green
  Khaduuii: "#facc15",    // Yellow
  Shin: "#ef4444",        // Red
  Zyk: "#a16207",         // Light brown
  Piraati: "#a855f7"      // Purple
};

const SpeciesAvatar = ({ species }) => {
  if (!species) return null;

  const initial = species.charAt(0).toUpperCase();
  const bg = speciesColors[species] || "#6b7280"; // fallback gray

  return (
    <Tooltip title={species} placement="top">
      <Avatar
        sx={{
          bgcolor: bg,
          width: 26,
          height: 26,
          fontSize: "0.85rem"
        }}
      >
        {initial}
      </Avatar>
    </Tooltip>
  );
};

export default SpeciesAvatar;
