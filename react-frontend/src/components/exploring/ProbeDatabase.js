import React, { useState, useEffect } from 'react';
import {
  Card, CardContent, Table, TableHead, TableRow, TableCell, TableBody, Typography,
  Button, Select, MenuItem, Dialog, DialogContent, DialogActions
} from '@mui/material';
import api from '../../utils/api';
import { Link } from 'react-router-dom';

const pageSize = 20;

const ProbeDatabase = ({ refreshTrigger }) => {
  const [reports, setReports] = useState([]);
  const [probeType, setProbeType] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);

  const fetchReports = () => {
    let url = `exploring/?page=${page}`;
    if (probeType) url += `&probe_type=${probeType}`;

    api.get(url).then(res => {
      setReports(res.data.results || []);
      setTotalPages(Math.max(1, Math.ceil(res.data.count / pageSize)));
    });
  };

  useEffect(() => {
    fetchReports();
  }, [probeType, page, refreshTrigger]);

  const handleOpenReport = (report) => {
    setSelectedReport(report);
    setOpenDialog(true);
  };

  const formatTimestamp = (report) => {
    const minute = new Date(report.server_time).getMinutes().toString().padStart(2, '0');
    return `${report.round}:${report.turn}:${minute}`;
  };

  const renderPlanetReport = (data) => {
    if (data?.report_name!=="Planet Probe Report") return null;

    return (
      <>
        <Typography variant="subtitle1"><b>Points:</b> {data.points}</Typography>

        {/* Plasmators */}
        <Typography sx={{ mt: 2 }}><b>Plasmators:</b></Typography>
        <Table size="small">
          <TableBody>
            <TableRow>
              {Object.keys(data.plasmators || {}).map(type => (
                <TableCell key={type}><b>{type}</b></TableCell>
              ))}
            </TableRow>
            <TableRow>
              {Object.values(data.plasmators || {}).map((count, idx) => (
                <TableCell key={idx}>{count}</TableCell>
              ))}
            </TableRow>
          </TableBody>
        </Table>

        {/* Resources */}
        <Typography sx={{ mt: 2 }}><b>Resources:</b></Typography>
        <Table size="small">
          <TableBody>
            <TableRow>
              {Object.keys(data.resources || {}).map(res => (
                <TableCell key={res}><b>{res}</b></TableCell>
              ))}
            </TableRow>
            <TableRow>
              {Object.values(data.resources || {}).map((amount, idx) => (
                <TableCell key={idx}>{amount}</TableCell>
              ))}
            </TableRow>
          </TableBody>
        </Table>

        {/* Production */}
        <Typography sx={{ mt: 2 }}><b>Production Capacity:</b></Typography>
        <Table size="small">
          <TableBody>
            <TableRow>
              {Object.keys(data.production_capacity || {}).map(res => (
                <TableCell key={res}><b>{res}</b></TableCell>
              ))}
            </TableRow>
            <TableRow>
              {Object.values(data.production_capacity || {}).map((amount, idx) => (
                <TableCell key={idx}>{amount}</TableCell>
              ))}
            </TableRow>
          </TableBody>
        </Table>

        {/* Other Details */}
        <Typography sx={{ mt: 2 }}><b>Developments:</b> {data.developments}</Typography>
        <Typography><b>Constructions:</b> {data.constructions}</Typography>
        <Typography><b>Ships:</b> {data.ships}</Typography>
        <Typography><b>PDS:</b> {data.pds}</Typography>
      </>
    );
  };

  const renderShipReport = (data) => {
    if (data?.report_name!=="Ship Probe Report" && data?.report_name!=="Defense Probe Report") return null;
    const shipList = Object.values(data.ships || {});

    return (
      <>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Class</TableCell>
              <TableCell>Quantity</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {shipList.map((ship, idx) => (
              <TableRow key={idx}>
                <TableCell>{ship.name}</TableCell>
                <TableCell>{ship.ship_class}</TableCell>
                <TableCell>{ship.quantity}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </>
    );
  };

  const renderMilitaryReport = (data) => {
      if (data?.report_name!=="Military Probe Report") return null;

      const shipList = Object.values(data.ships || {});
      const fleetList = data.fleets || [];

      return (
        <>
          <Typography sx={{ mt: 2 }}><b>Fleets:</b></Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Formation</TableCell>
                <TableCell>Target</TableCell>
                <TableCell>Distance</TableCell>
                <TableCell>Turns</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {fleetList.map((fleet, idx) => (
                <TableRow key={idx}>
                  <TableCell>{fleet.name}</TableCell>
                  <TableCell>{fleet.status}</TableCell>
                  <TableCell>{fleet.formation}</TableCell>
                  <TableCell>{fleet.target || '-'}</TableCell>
                  <TableCell>{fleet.status==="At home"?'-':fleet.distance}</TableCell>
                  <TableCell>{(fleet.status==="Defend"||fleet.status==="Attack")?fleet.turns:'-'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          <Typography sx={{ mt: 2 }}><b>Ships:</b></Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Class</TableCell>
                {fleetList.map((fleet, i) => (
                  <TableCell key={i}>{fleet.name}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {shipList.map((ship, idx) => (
                <TableRow key={idx}>
                  <TableCell>{ship.name}</TableCell>
                  <TableCell>{ship.ship_class}</TableCell>
                  {ship.quantity.map((qty, i) => (
                    <TableCell key={i}>{qty}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      );
  };

const NotifContentFormatter = ({ data }) => {
  if (!data) return null;

  // If the content is a plain string
  if (typeof data === 'string') {
    return <>{data}</>;
  }

  // If the content is an object with a `report` field
  if (typeof data === 'object' && data.report) {
    return <>{data.report}</>;
  }

  // Fallback: stringify the full JSON
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
};


  const renderInformationReport = (data) => {
      if (data?.report_name!=="Information Probe Report") return null;
      if (!data?.notifications?.length) return <Typography>No notifications found.</Typography>;

      return (
        <>
          <Typography variant="h6" sx={{ mt: 2 }}>Information Report</Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Time</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Content</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.notifications.map((notif, idx) => (
                <TableRow key={idx}>
                  <TableCell>{notif.timestamp}</TableCell>
                  <TableCell>{notif.ntype}</TableCell>
                  <TableCell>
                    <NotifContentFormatter data={notif.content} />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      );
  };
  
  return (
    <Card sx={{ my: 2 }}>
      <CardContent>
        <Typography variant="h6" sx={{ mt: 2 }}>Probe Database</Typography>

        <Select
          value={probeType}
          onChange={e => setProbeType(e.target.value)}
          displayEmpty
          sx={{ my: 1 }}
        >
          <MenuItem value="">All Types</MenuItem>
          <MenuItem value="planet">Planet</MenuItem>
          <MenuItem value="ship">Ship</MenuItem>
          <MenuItem value="defense">Defense</MenuItem>
          <MenuItem value="military">Military</MenuItem>
          <MenuItem value="information">Information</MenuItem>
        </Select>

        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Timestamp</TableCell>
              <TableCell>Probe Type</TableCell>
              <TableCell>Alliance</TableCell>
              <TableCell>Planet</TableCell>
              <TableCell>Points</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reports.map(report => (
              <TableRow key={report.id}>
                <TableCell>{formatTimestamp(report)}</TableCell>
                <TableCell>
                  <Button size="small" onClick={() => handleOpenReport(report)}>
                    {report.probe_type}
                  </Button>
                </TableCell>
                <TableCell>#{report.alliance_identifier || '-'}</TableCell>
                <TableCell>{report.target_planet_name} ({report.coordinates})</TableCell>
                <TableCell>{report.points}</TableCell>
                <TableCell>
                  <Button
                    size="small"
                    variant="outlined"
                    component={Link}
                    to={`/fleetControl/?target=${report.coordinates}`}
                  >
                    Attack
                  </Button>
                  <Button
                    size="small"
                    color="secondary"
                    component={Link}
                    to={`/fleet/exploring/?coords=${report.coordinates}`}
                    sx={{ ml: 1 }}
                  >
                    Probing
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <div style={{ marginTop: '10px' }}>
          <Button onClick={() => setPage(page > 1 ? page - 1 : 1)} disabled={page <= 1}>Previous</Button>
          Page {page} / {totalPages}
          <Button onClick={() => setPage(page < totalPages ? page + 1 : totalPages)} disabled={page >= totalPages}>Next</Button>
        </div>

        <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
          <DialogContent>
            {selectedReport?.result_json ? (
              <>
                <Typography variant="h6" gutterBottom>{selectedReport.result_json.report_name}</Typography>

                <Typography variant="subtitle1">
                  <b>Planet:</b> {selectedReport.result_json.name} ({selectedReport.coordinates})
                </Typography>
                
                {renderPlanetReport(selectedReport.result_json)}

                {renderShipReport(selectedReport.result_json)}
                
                {renderMilitaryReport(selectedReport.result_json)}
                
                {renderInformationReport(selectedReport.result_json)}
                
              </>
            ) : (
              <Typography>No report data available.</Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)} variant="contained">Close</Button>
          </DialogActions>
        </Dialog>
      </CardContent>
    </Card>
  );
};

export default ProbeDatabase;
