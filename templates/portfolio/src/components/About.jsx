import React from 'react';
import { motion } from 'framer-motion';

const About = ({ content }) => {
  return (
    <section id="about" className="py-20 bg-dark-200">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center">
            About <span className="gradient-text">Me</span>
          </h2>

          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8 items-center">
              {/* Profile Image Placeholder */}
              <div className="md:col-span-1">
                <div className="w-48 h-48 mx-auto rounded-full bg-gradient-to-br from-primary-500 to-purple-500 p-1">
                  <div className="w-full h-full rounded-full bg-dark-200 flex items-center justify-center">
                    <span className="text-6xl">👤</span>
                  </div>
                </div>
              </div>

              {/* About Content */}
              <div className="md:col-span-2">
                <div className="prose prose-invert max-w-none">
                  {content.split('\n\n').map((paragraph, index) => (
                    <p key={index} className="text-gray-300 mb-4 leading-relaxed">
                      {paragraph}
                    </p>
                  ))}
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-4 mt-8">
                  <div className="text-center p-4 card">
                    <div className="text-3xl font-bold gradient-text">7+</div>
                    <div className="text-sm text-gray-400">Years Experience</div>
                  </div>
                  <div className="text-center p-4 card">
                    <div className="text-3xl font-bold gradient-text">50+</div>
                    <div className="text-sm text-gray-400">Projects Completed</div>
                  </div>
                  <div className="text-center p-4 card">
                    <div className="text-3xl font-bold gradient-text">20+</div>
                    <div className="text-sm text-gray-400">Happy Clients</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default About;
