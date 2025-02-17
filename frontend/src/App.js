// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

function App() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      const response = await axios.get('/images');
      setImages(response.data);
    } catch (error) {
      console.error("Error fetching images:", error);
    }
  };

  const deleteImage = async (imageName) => {
    try {
      await axios.delete(`/images/${imageName}`);
      fetchImages(); // Refresh image list after deletion
    } catch (error) {
      console.error("Error deleting image:", error);
    }
  };

  return (
    <div className="App">
      <h1>Coin Image Processor</h1>
      <div className="image-list">
        {images.map(image => (
          <div key={image} className="image-item">
            <img src={`/output_images/${image}`} alt={image} />
            <button onClick={() => deleteImage(image)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;