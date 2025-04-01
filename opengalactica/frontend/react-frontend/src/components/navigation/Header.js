import Grid from '@mui/material/Grid2';

import PlanetDataBox from './header/PlanetDataBox'

const Header = () => {

    return (
        <header className="header">
            <Grid container spacing={0}>
                <Grid container size={3}>
                    <PlanetDataBox />
                </Grid>
                <Grid size={9}>
                XXX
                </Grid>
            </Grid>
        </header>
    );
};

export default Header;