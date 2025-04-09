import React, { useEffect, useState } from 'react';
import { Box, CircularProgress } from '@mui/material';
import { useTranslation } from 'react-i18next';

import Grid from '@mui/material/Grid2';
import {Typography} from '@mui/material';

import api from '../../../utils/api';


const OperationsBox = () => {
    const { t } = useTranslation();
  
    const [loading, setLoading] = useState(true);
    const [technologyData, setTechnologyData] = useState(null);
    const [fleets, setFleets] = useState([]);

    
    useEffect(() => {
        const fetchFleets = async () => {
            try {
                const response = await api.get('fleets/');
                setFleets(response.data);
            } catch (error) {
                console.error('Error fetching fleet data:', error);
            }
        };
        fetchFleets();
    }, []);
    
    useEffect(() => {
        const fetchTechnology = async () => {
            try {
                const response = await api.get('home-technology');
                setTechnologyData(response.data);
            } catch (error) {
                console.error('Failed to fetch technology data.');
            } finally {
                setLoading(false);
            }
        };

        fetchTechnology();
    }, []);

    if (loading) {
        return (
            <Box sx={{ textAlign: 'center', padding: 2 }}>
                <CircularProgress />
            </Box>
        );
    }
    
    return (
       <Grid container size={12} sx={{ p: 1, m: 1, border: '2px solid black'}}>
       
            <Grid container size={12}>
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {t('Research')}:
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {technologyData.research || ''} {technologyData.research_turns != null ? `(${technologyData.research_turns})` : '-'}
                    </Typography>
                </Grid>
                
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {t('Building')}:
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {technologyData.building || ''} {technologyData.building_turns != null ? `(${technologyData.building_turns})` : '-'}
                    </Typography>
                </Grid>
            </Grid>
            
            
            <Grid container size={12} sx={{ p:1, borderTop: '1px solid black' }}>
            
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {t('Fleet 1')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        {fleets[0].status}
                    </Typography>
                </Grid>
                
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {t('Fleet 2')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        {fleets[1].status}
                    </Typography>
                </Grid>

                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {t('Fleet 3')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        {fleets[2].status}
                    </Typography>
                </Grid>

                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        {t('Fleet 4')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        {fleets[3].status}
                    </Typography>
                </Grid>

            </Grid>

        </Grid>
    );
};

export default OperationsBox;