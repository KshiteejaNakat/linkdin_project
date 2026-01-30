import React from 'react';
import { motion } from 'framer-motion';
import { Briefcase, Calendar, MapPin } from 'lucide-react';

const Experience = ({ experiences }) => {
  const experienceList = experiences || [];

  return (
    <section id="experience" className="py-20 bg-dark-200">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center">
            Work <span className="gradient-text">Experience</span>
          </h2>

          <div className="max-w-3xl mx-auto">
            {/* Timeline */}
            <div className="relative">
              {/* Timeline Line */}
              <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary-500 to-purple-500" />

              {experienceList.map((exp, index) => (
                <motion.div
                  key={index}
                  className={`relative flex flex-col md:flex-row gap-8 mb-12 ${
                    index % 2 === 0 ? 'md:flex-row-reverse' : ''
                  }`}
                  initial={{ opacity: 0, x: index % 2 === 0 ? 50 : -50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  {/* Timeline Dot */}
                  <div className="absolute left-4 md:left-1/2 w-4 h-4 bg-primary-500 rounded-full transform -translate-x-1/2 border-4 border-dark-200" />

                  {/* Content */}
                  <div className={`w-full md:w-1/2 ${index % 2 === 0 ? 'md:pr-12' : 'md:pl-12'} pl-10 md:pl-0`}>
                    <div className="card p-6">
                      <div className="flex items-center gap-2 text-primary-500 mb-2">
                        <Briefcase size={18} />
                        <span className="font-semibold">{exp.company}</span>
                      </div>
                      
                      <h3 className="text-xl font-bold text-white mb-2">
                        {exp.role}
                      </h3>

                      <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-4">
                        <span className="flex items-center gap-1">
                          <Calendar size={14} />
                          {exp.duration}
                        </span>
                        {exp.location && (
                          <span className="flex items-center gap-1">
                            <MapPin size={14} />
                            {exp.location}
                          </span>
                        )}
                      </div>

                      <p className="text-gray-300 mb-4">
                        {exp.description || exp.optimized}
                      </p>

                      {/* Keywords/Technologies */}
                      {exp.technologies && (
                        <div className="flex flex-wrap gap-2">
                          {exp.technologies.map((tech, i) => (
                            <span
                              key={i}
                              className="px-2 py-1 text-xs bg-primary-500/20 text-primary-400 rounded"
                            >
                              {tech}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Spacer for alternating layout */}
                  <div className="hidden md:block w-1/2" />
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Experience;
