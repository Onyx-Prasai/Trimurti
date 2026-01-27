import { motion } from 'framer-motion'

const Logo = () => {
  return (
    <motion.svg
      width="40"
      height="40"
      viewBox="0 0 100 100"
      className="pulse-heartbeat"
      animate={{
        scale: [1, 1.1, 1],
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    >
      {/* Nepalese Map Outline (simplified) */}
      <path
        d="M20 30 L30 20 L50 25 L70 20 L80 30 L75 50 L80 70 L70 80 L50 75 L30 80 L20 70 L25 50 Z"
        fill="none"
        stroke="#D32F2F"
        strokeWidth="2"
      />
      
      {/* Blood Drop */}
      <motion.path
        d="M50 35 Q45 40 45 50 Q45 60 50 65 Q55 60 55 50 Q55 40 50 35 Z"
        fill="#D32F2F"
        animate={{
          scale: [1, 1.05, 1],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    </motion.svg>
  )
}

export default Logo

