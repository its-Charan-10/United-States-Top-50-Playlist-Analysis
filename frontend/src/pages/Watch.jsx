import { useParams } from 'react-router-dom'
import VideoPlayer from '../components/VideoPlayer'

const Watch = () => {
  const { id } = useParams()
  
  // Public HLS Test stream
  const demoUrl = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"

  return (
    <div className="h-screen w-screen bg-black fixed inset-0 z-[100]">
      <VideoPlayer 
        src={demoUrl} 
        title={`Watching Video ${id}`} 
      />
    </div>
  )
}

export default Watch
