import React from "react";
import { Paper, Typography, Box, Button } from "@mui/material";

const SocialMedia = () => (
  <Paper sx={{ p: 2, mb: 3 }}>
    <Typography variant="h6" gutterBottom>
      Social Media
    </Typography>
    <Typography variant="body2" color="text.secondary">
      Follow us on:
    </Typography>
    <Box sx={{ mt: 1 }}>
      <Button variant="outlined" size="small" sx={{ mr: 1 }}>
        Facebook
      </Button>
      <Button variant="outlined" size="small" sx={{ mr: 1 }}>
        Twitter
      </Button>
      <Button variant="outlined" size="small">
        Discord
      </Button>
    </Box>
  </Paper>
);

export default SocialMedia;
