import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  ToggleButton,
  ToggleButtonGroup,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Grid,
  Button
} from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";
import api from "../../../utils/api";

const DEFAULT_TOP = 5;

const COLORS = [
  "#1976d2", "#388e3c", "#d32f2f", "#f57c00", "#7b1fa2",
  "#0288d1", "#c2185b", "#7cb342", "#fbc02d", "#5d4037"
];

export default function History() {
  const [period, setPeriod] = useState("day"); // "day" or "week"
  const [etype, setEtype] = useState("alliances"); // alliances | sols | planets 
  const [chartData, setChartData] = useState([]); // array of points (x + values for each entity)
  const [seriesNames, setSeriesNames] = useState([]); // names of entities plotted
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(`toplist/history/`, {
          params: { period, type: etype }
        });
        // expected res.data: { timestamps: [..], series: { "Name1":[..], "Name2":[..], ... } }
        const data = res.data;

        // fallback guard if backend returns array of points directly
        if (Array.isArray(data) && data.length && data[0].time !== undefined) {
          // backend provided array of points directly: [{time:..., name1:..., name2:...}, ...]
          setChartData(data);
          // derive series names from keys
          const keys = Object.keys(data[0]).filter(k => k !== "time");
          setSeriesNames(keys);
        } else if (data.timestamps && data.series) {
          // convert { timestamps:[], series: {name: [v1, v2,...], ...} } into array of points
          const points = data.timestamps.map((t, i) => {
            const p = { time: t };
            Object.entries(data.series).forEach(([name, arr]) => {
              p[name] = arr[i] ?? null;
            });
            return p;
          });
          setChartData(points);
          setSeriesNames(Object.keys(data.series));
        } else {
          // fallback sample data if unexpected
          setChartData([]);
          setSeriesNames([]);
          setError("Unexpected data format from server.");
        }
      } catch (err) {
        console.error("fetch history error", err);
        setError(err.message || "Failed to load history");
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [period, etype]);

  const handlePeriodChange = (ev, val) => { if (val) setPeriod(val); };
  const handleEtypeChange = (ev) => setEtype(ev.target.value);

  return (
    <Paper sx={{ p: 2 }}>
      <Grid container spacing={2} alignItems="center" mb={1}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6">History</Typography>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box display="flex" gap={1} justifyContent="flex-end" alignItems="center">
            <ToggleButtonGroup
              size="small"
              value={period}
              exclusive
              onChange={handlePeriodChange}
              aria-label="period"
            >
              <ToggleButton value="day">Last Day</ToggleButton>
              <ToggleButton value="week">Last Week</ToggleButton>
            </ToggleButtonGroup>

            <FormControl size="small" sx={{ minWidth: 140 }}>
              <InputLabel id="etype-label">Entity</InputLabel>
              <Select
                labelId="etype-label"
                value={etype}
                label="Entity"
                onChange={handleEtypeChange}
              >
                <MenuItem value="alliances">Top Alliances</MenuItem>
                <MenuItem value="sols">Top Sols</MenuItem>
                <MenuItem value="planets">Top Planets</MenuItem>
              </Select>
            </FormControl>

            <Button size="small" onClick={() => { setPeriod(period); setEtype(etype); }}>Refresh</Button>
          </Box>
        </Grid>
      </Grid>

      <Box sx={{ height: 340 }}>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="100%">
            <CircularProgress />
          </Box>
        ) : error ? (
          <Box p={2}>
            <Typography color="error">Error: {error}</Typography>
          </Box>
        ) : chartData.length === 0 ? (
          <Box p={2}>
            <Typography>No data available for the chosen filters.</Typography>
          </Box>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend verticalAlign="top" height={36} />
              {seriesNames.map((name, idx) => (
                <Line
                  key={name}
                  dataKey={name}
                  name={name}
                  stroke={COLORS[idx % COLORS.length]}
                  dot={false}
                  strokeWidth={2}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )}
      </Box>
    </Paper>
  );
}
