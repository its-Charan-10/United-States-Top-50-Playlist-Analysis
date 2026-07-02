import { Link } from 'react-router-dom'
import { FaFacebookF, FaInstagram, FaTwitter, FaYoutube } from 'react-icons/fa6'

const Footer = () => {
  const links = [
    ['Audio Description', 'Help Centre', 'Gift Cards', 'Media Centre'],
    ['Investor Relations', 'Jobs', 'Terms of Use', 'Privacy'],
    ['Legal Notices', 'Cookie Preferences', 'Corporate Information', 'Contact Us'],
  ]

  return (
    <footer className="bg-surface-overlay py-16 px-4 md:px-12 border-t border-white/5">
      <div className="max-w-6xl mx-auto">
        <div className="flex gap-6 mb-8">
          <FaFacebookF className="text-white cursor-pointer hover:text-brand transition-colors" size={24} />
          <FaInstagram className="text-white cursor-pointer hover:text-brand transition-colors" size={24} />
          <FaTwitter className="text-white cursor-pointer hover:text-brand transition-colors" size={24} />
          <FaYoutube className="text-white cursor-pointer hover:text-brand transition-colors" size={24} />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-10">
          {links.map((column, idx) => (
            <div key={idx} className="flex flex-col gap-3">
              {column.map((link) => (
                <Link 
                  key={link} 
                  to="#" 
                  className="text-text-muted hover:underline text-sm transition-colors"
                >
                  {link}
                </Link>
              ))}
            </div>
          ))}
        </div>

        <div className="mb-6">
          <button className="border border-text-muted text-text-muted px-4 py-1 text-sm hover:text-white hover:border-white transition-colors">
            Service Code
          </button>
        </div>

        <p className="text-text-muted text-[11px]">
          © 1997-2026 CineStream, Inc.
        </p>
      </div>
    </footer>
  )
}

export default Footer
