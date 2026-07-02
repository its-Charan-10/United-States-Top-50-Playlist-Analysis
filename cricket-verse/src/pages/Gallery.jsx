import React from 'react';
import { motion } from 'framer-motion';
import { Image as ImageIcon } from 'lucide-react';

const galleryImages = [
  { url: 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', title: 'Stadium View' },
  { url: 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', title: 'Bowling Action' },
  { url: 'https://images.unsplash.com/photo-1593341646782-e0b495cff86d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', title: 'Celebration' },
  { url: 'https://images.unsplash.com/photo-1624526267942-ab0f0b080613?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', title: 'The Equipment' },
  { url: 'https://images.unsplash.com/photo-1587280501635-a1976a4a6b25?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', title: 'The Pitch' },
  { url: 'https://images.unsplash.com/photo-1607734834519-d8576ae60ea6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', title: 'Night Match' },
];

export default function Gallery() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
          <ImageIcon className="w-8 h-8 text-cricket-blue" />
          Moments in Cricket
        </h2>

        <div className="columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6">
          {galleryImages.map((image, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.03 }}
              className="relative rounded-2xl overflow-hidden group break-inside-avoid shadow-xl cursor-pointer"
            >
              <img 
                src={image.url} 
                alt={image.title} 
                className="w-full h-auto object-cover"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/0 to-black/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
                <div className="p-6">
                  <h3 className="text-xl font-bold text-white translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                    {image.title}
                  </h3>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
