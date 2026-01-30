import React from 'react';
import { motion } from 'framer-motion';
import { ArrowDown, Github, Linkedin, Mail } from 'lucide-react';

const Hero = ({ name, title, tagline }) => {
  return (
    <section className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-dark-300 via-dark-200 to-primary-700/20" />
      
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="container relative z-10 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <p className="text-primary-500 text-lg mb-4">Hello, I'm</p>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="gradient-text">{name}</span>
          </h1>
          
          <h2 className="text-2xl md:text-3xl text-gray-300 mb-6">
            {title}
          </h2>
          
          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8">
            {tagline}
          </p>

          <div className="flex justify-center gap-4 mb-12">
            <a href="#contact" className="btn-primary">
              Get In Touch
            </a>
            <a 
              href="#projects" 
              className="px-6 py-3 border border-primary-500 text-primary-500 rounded-lg hover:bg-primary-500/10 transition-all"
            >
              View Projects
            </a>
          </div>

          <div className="flex justify-center gap-6">
            <a href="#" className="text-gray-400 hover:text-primary-500 transition-colors">
              <Github size={24} />
            </a>
            <a href="#" className="text-gray-400 hover:text-primary-500 transition-colors">
              <Linkedin size={24} />
            </a>
            <a href="#" className="text-gray-400 hover:text-primary-500 transition-colors">
              <Mail size={24} />
            </a>
          </div>
        </motion.div>

        {/* Scroll Indicator */}
        <motion.div
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
          animate={{ y: [0, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
        >
          <ArrowDown className="text-gray-500" size={24} />
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
