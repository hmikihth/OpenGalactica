import React from "react";
import { Grid, Box } from "@mui/material";

import Intro from "../../components/portal/home/Intro";
import SocialMedia from "../../components/portal/home/SocialMedia";
import News from "../../components/portal/home/News";
import Registration from "../../components/portal/home/Registration";
import Toplists from "../../components/portal/home/Toplists";
import History from "../../components/portal/home/History";
import ScoreChanges from "../../components/portal/home/ScoreChanges";

const PortalHome = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Intro />

      <Grid container spacing={3}>
        {/* Left Column */}
        <Grid item xs={12} md={4}>
          <SocialMedia />
          <News />
        </Grid>

        {/* Right Column */}
        <Grid item xs={12} md={8}>
          <Registration />
          <Toplists />
          <History />
        </Grid>
      </Grid>

      <ScoreChanges />
    </Box>
  );
};

export default PortalHome;
