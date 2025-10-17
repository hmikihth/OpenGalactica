import React, { useState, useEffect } from 'react';
import {
  Box, Button, Card, CardContent, CardHeader, Typography,
  TextField, Avatar
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import api from "../../utils/api";
import { getCSRFToken } from "../../utils/csrf";

const MB = 1024 * 1024;
const MAX_IMAGE_SIZE = 10 * MB;

const Input = styled('input')({
  display: 'none',
});

const EditPlanetProfile = ({ data }) => {
  const [slogan, setSlogan] = useState(data?.slogan || '');
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!selectedFile) {
      setPreview(null);
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(selectedFile);
  }, [selectedFile]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (file && file.size > MAX_IMAGE_SIZE) {
      setError('Image size cannot exceed 10 MB.');
      return;
    }

    setError(null);
    setSelectedFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('slogan', slogan);
    if (selectedFile) {
      formData.append('profile_image', selectedFile);
    }

    try {
      const response = await api.post('planet/profile/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCSRFToken(),
        },
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      alert('Profile updated!');
    } catch (err) {
      console.error(err);
      setError('Failed to update profile.');
    }
  };

  return (
    <Card sx={{ maxWidth: 500, mx: 'auto', mt: 5 }}>
      <CardHeader title="Edit Planet Profile" />
      <CardContent>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Slogan"
            fullWidth
            value={slogan}
            onChange={(e) => setSlogan(e.target.value)}
            inputProps={{ maxLength: 256 }}
            helperText={`${slogan.length}/256 characters`}
            margin="normal"
          />

          <Box display="flex" flexDirection="column" alignItems="center" my={2}>
            {preview && (
              <Avatar
                src={preview}
                variant="square"
                alt="Preview"
                sx={{ width: 120, height: 120, mb: 2 }}
              />
            )}

            <label htmlFor="file-upload">
              <Input
                accept="image/*"
                id="file-upload"
                type="file"
                onChange={handleFileChange}
              />
              <Button
                variant="contained"
                component="span"
                startIcon={<CloudUploadIcon />}
              >
                New Profile Image
              </Button>
            </label>
          </Box>

          {error && (
            <Typography color="error" sx={{ mt: 1 }}>{error}</Typography>
          )}

          <Button
            type="submit"
            variant="contained"
            fullWidth
            sx={{ mt: 2 }}
          >
            Modify
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default EditPlanetProfile;
