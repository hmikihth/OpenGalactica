import React from "react";
import { Paper, Typography } from "@mui/material";

const News = () => (
  <Paper sx={{ p: 2 }}>
    <Typography variant="h6" gutterBottom>
      Latest News
    </Typography>
    <Typography variant="body2" color="text.secondary">
      - Galaxy expansion update coming soon! <br />
      - New probe mechanics introduced. <br />
      - Server maintenance scheduled for Sunday.
    </Typography>
  </Paper>
);

export default News;
