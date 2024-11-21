import React, { useState } from 'react';

const ImageUploader = () => {
  const [image, setImage] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleUpload = () => {
    setUploading(true);
    const formData = new FormData();
    formData.append('image', image);

    fetch(`${backendUrl}/upload`, {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setUploading(false);
      })
      .catch((error) => {
        console.error(error);
        setUploading(false);
      });
  };

};

export default ImageUploader;