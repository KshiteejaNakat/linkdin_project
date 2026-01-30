import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Github, Folder } from 'lucide-react';

const Projects = ({ projects }) => {
  const projectList = projects || [];

  return (
    <section id="projects" className="py-20 bg-dark-300">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center">
            Featured <span className="gradient-text">Projects</span>
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {projectList.map((project, index) => (
              <motion.div
                key={index}
                className="card p-6 flex flex-col h-full"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -5 }}
              >
                {/* Project Icon */}
                <div className="mb-4">
                  <div className="w-12 h-12 rounded-lg bg-primary-500/20 flex items-center justify-center">
                    <Folder className="text-primary-500" size={24} />
                  </div>
                </div>

                {/* Project Title */}
                <h3 className="text-xl font-bold text-white mb-2">
                  {project.name}
                </h3>

                {/* Project Description */}
                <p className="text-gray-400 mb-4 flex-grow">
                  {project.description}
                </p>

                {/* Technologies */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {(project.tech || project.technologies || []).map((tech, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 text-xs bg-dark-100 text-gray-300 rounded"
                    >
                      {tech}
                    </span>
                  ))}
                </div>

                {/* Links */}
                <div className="flex gap-4">
                  {project.github && (
                    <a
                      href={project.github}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 hover:text-primary-500 transition-colors"
                    >
                      <Github size={20} />
                    </a>
                  )}
                  {project.link && (
                    <a
                      href={project.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 hover:text-primary-500 transition-colors"
                    >
                      <ExternalLink size={20} />
                    </a>
                  )}
                </div>
              </motion.div>
            ))}
          </div>

          {/* View More Button */}
          <div className="text-center mt-12">
            <a
              href="#"
              className="inline-flex items-center gap-2 text-primary-500 hover:text-primary-400 transition-colors"
            >
              View All Projects
              <ExternalLink size={18} />
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Projects;
