import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGlobe, faCirclePlus, faChartSimple, faRectangleList, faStar } from "@fortawesome/free-solid-svg-icons";

import Grid from '@mui/material/Grid2';
import {Typography} from '@mui/material';

import NumberWithSpaces from '../../NumberWithSpaces'

import api from '../../../utils/api';

const PlanetDataBox = () => {
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
            PROFILE IMAGE
            </Grid>

            <Grid container size={6} sx={{ p:1, borderLeft: '1px solid black'}}>    
    
                <Grid size={12}>
                    <Typography align='center' sx={{ fontSize:'0.8em', fontWeight:'bold' }} >
                        {planetData.name} 
                    </Typography>
                </Grid>
                <Grid size={12} sx={{ paddingBottom:'0.8em' }}>
                    <Typography align='center' sx={{ fontSize:'0.8em', fontWeight:'bold' }} >
                        <FontAwesomeIcon icon={faGlobe} />
                        &nbsp;
                        ( {planetData.coordinates} )
                    </Typography>
                </Grid>
    
                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }} >
                        <FontAwesomeIcon icon={faCirclePlus} />
                        &nbsp;
                        {t('points')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <NumberWithSpaces number={planetData.points} />
                    </Typography>
                </Grid>

                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faRectangleList} />
                        &nbsp;
                        {t('top')}#: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        ---
                    </Typography>
                </Grid>



                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faChartSimple} />
                        &nbsp;
                        {t('xp')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>   
                        <NumberWithSpaces number={planetData.xp} />
                    </Typography>
                </Grid>

                <Grid size={6}>
                    <Typography align='left' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        <FontAwesomeIcon icon={faStar} />
                        &nbsp;
                        {t('rank')}: 
                    </Typography>
                </Grid>
                <Grid size={6}>
                    <Typography align='right' sx={{ fontSize:'0.7em', fontWeight:'bold' }}>
                        {t(planetData.rank)}
                    </Typography>
                </Grid>
                
            </Grid>
            
        </Grid>
    );
};

export default PlanetDataBox;