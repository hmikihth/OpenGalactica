import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  CircularProgress,
  Tooltip,
} from '@mui/material';
import api from '../utils/api';

const techTypes = [
  'fleet',
  'engine',
  'planet',
  'pds',
  'probes',
  'resource',
  'advanced',
];

const techTypeLabels = {
  fleet: 'Fleet',
  engine: 'Engine',
  planet: 'Planet',
  pds: 'PDS',
  probes: 'Probes',
  resource: 'Resource',
  advanced: 'Advanced Tech',
};

const Research = () => {
  const [techTree, setTechTree] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTree = async () => {
      try {
        const response = await api.get('research-tree');
        setTechTree(response.data);
      } catch (error) {
        console.error('Failed to fetch research tree:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTree();
  }, []);

  const handleAction = async (techId, action) => {
    try {
      await api.post(`research-${action}`, { id: techId });
      const response = await api.get('research-tree');
      setTechTree(response.data);
    } catch (error) {
      console.error(`${action} failed:`, error);
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Box p={2}>
      <Typography variant="h5" gutterBottom>
        Technology Research Tree
      </Typography>
      <Grid container spacing={2}>
        {techTypes.map((type) => (
          <Grid item xs={12} md={3} key={type}>
            <Typography variant="h6" gutterBottom>
              {techTypeLabels[type]}
            </Typography>
            {techTree[type]?.map((tech) => (
              <Card key={tech.id} variant="outlined" sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="subtitle1">{tech.name}</Typography>
                  <Typography variant="body2">Cost: {tech.cost.metal} M / {tech.cost.crystal} C / {tech.cost.narion} N</Typography>
                  <Typography variant="body2">Time: {tech.development_time} turns</Typography>
                  {tech.requirements.length > 0 && (
                    <Typography variant="body2">
                      Requires: {tech.requirements.join(', ')}
                    </Typography>
                  )}
                </CardContent>
                <CardActions>
                  {tech.status === 'done' ? (
                    <Typography color="success.main">Done</Typography>
                  ) : tech.status === 'active' ? (
                    <Typography color="warning.main">{tech.remaining_turns} turns left</Typography>
                  ) : tech.status === 'available' ? (
                    <Button
                      size="small"
                      variant="contained"
                      onClick={() => handleAction(tech.id, tech.type)}
                    >
                      {tech.type === 'building' ? 'Build' : 'Research'}
                    </Button>
                  ) : (
                    <Tooltip title="Requirements not met">
                      <span>
                        <Button size="small" variant="outlined" disabled>
                          {tech.type === 'building' ? 'Build' : 'Research'}
                        </Button>
                      </span>
                    </Tooltip>
                  )}
                </CardActions>
              </Card>
            ))}
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Research;
