import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGem, faCube, faFire, faCoins, faMeteor } from "@fortawesome/free-solid-svg-icons";

import Grid from '@mui/material/Grid2';
import {Typography} from '@mui/material';

import NumberWithSpaces from '../../NumberWithSpaces'
        
import api from '../../../utils/api';

const ResourceBox = () => {
    const { t } = useTranslation();
    const [planetData, setPlanetData] = useState(null);

    useEffect(() => {
        const fetchPlanetData = async () => {
            try {
                const response = await api.get('planet/');
                setPlanetData(response.data);
            } catch (error) {
                console.error('Error fetching planet data:', error);
            }
        };
        fetchPlanetData();
    }, []);

    if (!planetData) return <div>{t('loading')}</div>;

    return (
       <Grid container size={12} sx={{ p: 1, m: 1, border: '2px solid black'}}>
            
            <Grid container size={6} sx={{ p:1 }}>
            
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        <FontAwesomeIcon icon={faCube} />
                        &nbsp;
                        {t('metal')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.metal} />
                    </Typography>
                </Grid>

                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faGem} />
                        &nbsp;
                        {t('crystal')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.crystal} />
                    </Typography>
                </Grid>
                
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faFire} />
                        &nbsp;
                        {t('narion')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.narion} />
                    </Typography>
                </Grid>
                
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faCoins} />
                        &nbsp;
                        {t('credits')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.credit} />
                    </Typography>
                </Grid>

            </Grid>

            <Grid container size={6} sx={{ p:1, borderLeft: '1px solid black'}}>

                <Grid size={9}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        <FontAwesomeIcon icon={faCube} />
                        &nbsp;
                        {t('Metal plasmator')}: 
                    </Typography>
                </Grid>
                <Grid size={3}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.metal_plasmator} />
                    </Typography>
                </Grid>

                <Grid size={9}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faGem} />
                        &nbsp;
                        {t('Crystal plasmator')}: 
                    </Typography>
                </Grid>
                <Grid size={3}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.crystal_plasmator} />
                    </Typography>
                </Grid>
                
                <Grid size={9}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faFire} />
                        &nbsp;
                        {t('Narion plasmator')}: 
                    </Typography>
                </Grid>
                <Grid size={3}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.narion_plasmator} />
                    </Typography>
                </Grid>
 
                <Grid size={9}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faMeteor} />
                        &nbsp;
                        {t('Neutral plasmator')}: 
                    </Typography>
                </Grid>
                <Grid size={3}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>   
                        <NumberWithSpaces number={planetData.neutral_plasmator} />
                    </Typography>
                </Grid>
            </Grid>
            
        </Grid>
    );
};

export default ResourceBox;