import Grid from '@mui/material/Grid2';

import PlanetDataBox from './header/PlanetDataBox'
import ResourceBox from './header/ResourceBox'
import OperationsBox from './header/OperationsBox'

const Header = () => {

    return (
        <header className="header">
            <Grid container spacing={0}>
                <Grid container size={4}>
                    <PlanetDataBox />
                </Grid>
                <Grid container size={4}>
                    <ResourceBox />
                </Grid>
                <Grid container size={4}>
                    <OperationsBox />
                </Grid>
            </Grid>
        </header>
    );
};

export default Header;