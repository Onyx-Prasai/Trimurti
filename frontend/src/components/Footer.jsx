import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaHeart } from 'react-icons/fa';

const Footer = () => {
  return (
    <motion.footer
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-gray-800 text-white py-10"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About This Product */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-red-500">About This Product</h3>
            <p className="text-gray-400 text-sm">
              Blood Hub Nepal is a comprehensive platform dedicated to connecting blood donors
              with recipients, managing blood requests, and promoting a healthy lifestyle
              through features like AI Health predictions and reward programs.
            </p>
          </div>

          {/* Features */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-red-500">Features</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/find-blood" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Find Blood Donors
                </Link>
              </li>
              <li>
                <Link to="/blood-prediction" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Blood Donation Prediction
                </Link>
              </li>
              <li>
                <Link to="/ai-health" className="text-gray-400 hover:text-white transition-colors text-sm">
                  AI Health Assistance
                </Link>
              </li>
              <li>
                <Link to="/points" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Rewards Program
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-red-500">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/settings/help" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Help & FAQ
                </Link>
              </li>
              <li>
                <Link to="/settings/legal" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <a href="mailto:support@bloodhubnepal.com" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Contact Us
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-10 pt-8 text-center text-gray-500 text-sm">
          <p className="flex items-center justify-center">
            Made with <FaHeart className="mx-1 text-red-500" /> by Trimurti &copy; {new Date().getFullYear()}
          </p>
          <p className="mt-2">All rights reserved.</p>
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;
