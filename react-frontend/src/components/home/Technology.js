import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Table, TableBody, TableRow } from '@mui/material';
import MobileTableCell from '../../components/MobileTableCell';

import api from '../../utils/api';

const Technology = () => {
    const [technologyData, setTechnologyData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTechnology = async () => {
            try {
                const response = await api.get('home-technology');
                setTechnologyData(response.data);
            } catch (err) {
                setError('Failed to fetch technology data.');
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

    if (error) {
        return <Box sx={{ textAlign: 'center', padding: 2, color: 'red' }}>{error}</Box>;
    }

    return (
        <Table>
            <TableBody>
                {/* Research Section */}
                <TableRow>
                    <MobileTableCell sx={{ fontWeight: 'bold', borderBottom: 'none' }}>Research:</MobileTableCell>
                </TableRow>
                <TableRow>
                    <MobileTableCell sx={{ textAlign: 'right' }}>
                        {technologyData.research || ''} {technologyData.research_turns != null ? `(${technologyData.research_turns})` : ''}
                    </MobileTableCell>
                </TableRow>

                {/* Building Section */}
                <TableRow>
                    <MobileTableCell sx={{ fontWeight: 'bold', borderBottom: 'none' }}>Building:</MobileTableCell>
                </TableRow>
                <TableRow>
                    <MobileTableCell sx={{ textAlign: 'right', borderBottom: 'none'  }}>
                        {technologyData.building || ''} {technologyData.building_turns != null ? `(${technologyData.building_turns})` : ''}
                    </MobileTableCell>
                </TableRow>
            </TableBody>
        </Table>
    );
};

export default Technology;
