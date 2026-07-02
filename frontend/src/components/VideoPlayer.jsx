import { useEffect, useRef, useState } from 'react'
import Hls from 'hls.js'
import { Play, Pause, RotateCcw, RotateCw, Volume2, VolumeX, Maximize, Settings, SkipForward } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const VideoPlayer = ({ src, title }) => {
  const videoRef = useRef(null)
  const containerRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [progress, setProgress] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const [showControls, setShowControls] = useState(true)
  const [duration, setDuration] = useState(0)
  
  let controlsTimeout

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    if (Hls.isSupported()) {
      const hls = new Hls()
      hls.loadSource(src)
      hls.attachMedia(video)
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = src
    }

    const handleTimeUpdate = () => setProgress((video.currentTime / video.duration) * 100)
    const handleLoadedMetadata = () => setDuration(video.duration)
    
    video.addEventListener('timeupdate', handleTimeUpdate)
    video.addEventListener('loadedmetadata', handleLoadedMetadata)

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate)
      video.removeEventListener('loadedmetadata', handleLoadedMetadata)
    }
  }, [src])

  const togglePlay = () => {
    if (videoRef.current.paused) {
      videoRef.current.play()
      setIsPlaying(true)
    } else {
      videoRef.current.pause()
      setIsPlaying(false)
    }
  }

  const handleSeek = (e) => {
    const pos = (e.nativeEvent.offsetX / e.currentTarget.offsetWidth)
    videoRef.current.currentTime = pos * videoRef.current.duration
  }

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen()
    } else {
      document.exitFullscreen()
    }
  }

  const handleMouseMove = () => {
    setShowControls(true)
    clearTimeout(controlsTimeout)
    controlsTimeout = setTimeout(() => {
      if (isPlaying) setShowControls(false)
    }, 3000)
  }

  return (
    <div 
      ref={containerRef}
      className="relative w-full h-screen bg-black flex items-center justify-center overflow-hidden group cursor-none"
      onMouseMove={handleMouseMove}
      style={{ cursor: showControls ? 'default' : 'none' }}
    >
      <video 
        ref={videoRef}
        className="w-full h-full"
        onClick={togglePlay}
        playsInline
      />

      {/* Controls Overlay */}
      <AnimatePresence>
        {showControls && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/40 flex flex-col justify-between p-8"
          >
            {/* Top Bar */}
            <div className="flex items-center gap-4">
              <button onClick={() => window.history.back()} className="text-white hover:text-brand transition-colors">
                <RotateCcw className="-scale-x-100" />
              </button>
              <h1 className="text-xl font-bold">{title}</h1>
            </div>

            {/* Middle Play/Pause Visual */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
               {/* Visual feedback could go here */}
            </div>

            {/* Bottom Bar */}
            <div className="flex flex-col gap-4">
              {/* Progress Bar */}
              <div 
                className="relative h-1.5 w-full bg-white/20 cursor-pointer group/progress"
                onClick={handleSeek}
              >
                <div 
                  className="absolute h-full bg-brand" 
                  style={{ width: `${progress}%` }} 
                />
                <div 
                  className="absolute h-4 w-4 bg-brand rounded-full top-1/2 -translate-y-1/2 -translate-x-1/2 opacity-0 group-hover/progress:opacity-100 transition-opacity"
                  style={{ left: `${progress}%` }}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-6">
                  <button onClick={togglePlay} className="hover:scale-110 transition-transform">
                    {isPlaying ? <Pause size={32} fill="white" /> : <Play size={32} fill="white" />}
                  </button>
                  <button onClick={() => videoRef.current.currentTime -= 10} className="hover:scale-110 transition-transform">
                    <RotateCcw size={24} />
                  </button>
                  <button onClick={() => videoRef.current.currentTime += 10} className="hover:scale-110 transition-transform">
                    <RotateCw size={24} />
                  </button>
                  <div className="flex items-center gap-2 group/volume">
                    <button onClick={() => setIsMuted(!isMuted)}>
                      {isMuted ? <VolumeX /> : <Volume2 />}
                    </button>
                    <input 
                      type="range" 
                      min="0" max="1" step="0.1" 
                      className="w-0 group-hover/volume:w-24 transition-all accent-brand"
                      onChange={(e) => setVolume(e.target.value)}
                    />
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  <button className="hover:rotate-45 transition-transform"><Settings /></button>
                  <button onClick={toggleFullscreen}><Maximize /></button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default VideoPlayer
