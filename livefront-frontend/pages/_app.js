import '../styles/globals.css'
import { FiHelpCircle } from 'react-icons/fi'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <button
        onClick={() => window.open('/documentation.html', '_blank')}
        style={{
          position: 'fixed',
          top: '1rem',
          right: '1rem',
          zIndex: 1000,
          background: '#ceca14',
          border: 'none',
          borderRadius: '50%',
          width: '2.5rem',
          height: '2.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
        }}
        aria-label="View documentation"
        title="View documentation"
      >
        <FiHelpCircle size={24} color="#333" />
      </button>
      <Component {...pageProps} />
    </>
  )
}

export default MyApp