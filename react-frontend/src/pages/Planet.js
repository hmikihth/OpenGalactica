import React, { useEffect, useState } from "react";
import { Box, Button, Grid, TextField } from "@mui/material";
import api from "../utils/api";
import PlanetProfile from "../components/planet/PlanetProfile";
import EditPlanetProfile from "../components/planet/EditPlanetProfile";

const PlanetPage = () => {
  const [planetData, setPlanetData] = useState(null);
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);
  const [z, setZ] = useState(0);
  const [isOwnPlanet, setIsOwnPlanet] = useState(false);

  const fetchPlanet = async (x, y, z) => {
    try {
      const response = await api.get(`/planet/${x}/${y}/${z}`);
      setPlanetData(response.data);
      setIsOwnPlanet(response.data.is_own);
    } catch (error) {
      console.error("Error fetching planet:", error);
    }
  };

  const handleJump = () => {
    fetchPlanet(x, y, z);
  };

  const handleNext = async () => {
    try {
      const response = await api.get(`/planet/${x}/${y}/${z}/next`);
      const { x: nextX, y: nextY, z: nextZ } = response.data;
      setX(nextX);
      setY(nextY);
      setZ(nextZ);
      fetchPlanet(nextX, nextY, nextZ);
    } catch (error) {
      console.error("Error fetching next planet:", error);
    }
  };

  const handlePrevious = async () => {
    try {
      const response = await api.get(`/planet/${x}/${y}/${z}/previous`);
      const { x: prevX, y: prevY, z: prevZ } = response.data;
      setX(prevX);
      setY(prevY);
      setZ(prevZ);
      fetchPlanet(prevX, prevY, prevZ);
    } catch (error) {
      console.error("Error fetching previous planet:", error);
    }
  };

  useEffect(() => {
    // Optionally fetch the user's own planet as default on mount
    api.get("/planet/me").then((response) => {
      setX(response.data.x);
      setY(response.data.y);
      setZ(response.data.z);
      setPlanetData(response.data);
      setIsOwnPlanet(response.data.is_own);
    });
  }, []);

  return (
    <Box p={2}>
      <Box display="flex" justifyContent="center" mt={2}>
        <Grid container spacing={2} alignItems="center" justifyContent="center">
          <Grid item>
            <Button variant="outlined" onClick={handlePrevious}>
              Previous
            </Button>
          </Grid>
          <Grid item>
            <TextField
              label="X"
              type="number"
              value={x}
              onChange={(e) => setX(Number(e.target.value))}
              size="small"
            />
          </Grid>
          <Grid item>
            <TextField
              label="Y"
              type="number"
              value={y}
              onChange={(e) => setY(Number(e.target.value))}
              size="small"
            />
          </Grid>
          <Grid item>
            <TextField
              label="Z"
              type="number"
              value={z}
              onChange={(e) => setZ(Number(e.target.value))}
              size="small"
            />
          </Grid>
          <Grid item>
            <Button variant="outlined" onClick={handleJump}>
              Jump
            </Button>
          </Grid>
          <Grid item>
            <Button variant="outlined" onClick={handleNext}>
              Next
            </Button>
          </Grid>
        </Grid>
      </Box>

      {planetData && <PlanetProfile data={planetData} />}
      {isOwnPlanet && <EditPlanetProfile data={planetData} />}
    </Box>
  );
};

export default PlanetPage;
