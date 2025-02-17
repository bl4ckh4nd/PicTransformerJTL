import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [images, setImages] = useState([])
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchImages()
  }, [])

  const fetchImages = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get('/images')
      setImages(response.data)
    } catch (error) {
      setError('Failed to load images. Please try again.')
      console.error('Error fetching images:', error)
    } finally {
      setLoading(false)
    }
  }

  const deleteImage = async (imageName) => {
    try {
      setError(null)
      await axios.delete(`/images/${imageName}`)
      await fetchImages()
    } catch (error) {
      setError('Failed to delete image. Please try again.')
      console.error('Error deleting image:', error)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('image', file)

    setUploading(true)
    setError(null)
    try {
      await axios.post('/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      await fetchImages()
    } catch (error) {
      setError('Failed to upload image. Please try again.')
      console.error('Error uploading image:', error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="App">
      <h1>Coin Image Processor</h1>
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileUpload}
          disabled={uploading}
        />
        {uploading && <p>Uploading...</p>}
        {error && <p className="error">{error}</p>}
      </div>
      <div className="image-list">
        {loading ? (
          <p>Loading images...</p>
        ) : images.length === 0 ? (
          <p>No images available. Upload some images to get started!</p>
        ) : (
          images.map((image) => (
            <div key={image} className="image-item">
              <img src={`/images/${image}`} alt={image} />
              <button onClick={() => deleteImage(image)}>Delete</button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default App