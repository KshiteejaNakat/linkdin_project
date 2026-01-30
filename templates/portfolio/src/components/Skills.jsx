import React from 'react';
import { motion } from 'framer-motion';

const Skills = ({ skills }) => {
  const technicalSkills = skills?.technical || [];
  const softSkills = skills?.soft || [];

  const SkillBar = ({ name, level }) => (
    <div className="mb-4">
      <div className="flex justify-between mb-1">
        <span className="text-gray-300">{name}</span>
        <span className="text-primary-500">{level}%</span>
      </div>
      <div className="h-2 bg-dark-100 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-primary-500 to-purple-500 rounded-full"
          initial={{ width: 0 }}
          whileInView={{ width: `${level}%` }}
          transition={{ duration: 1, delay: 0.2 }}
          viewport={{ once: true }}
        />
      </div>
    </div>
  );

  return (
    <section id="skills" className="py-20 bg-dark-300">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center">
            My <span className="gradient-text">Skills</span>
          </h2>

          <div className="grid md:grid-cols-2 gap-12 max-w-4xl mx-auto">
            {/* Technical Skills */}
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-6 text-primary-500">
                Technical Skills
              </h3>
              {technicalSkills.map((skill, index) => (
                <SkillBar 
                  key={index} 
                  name={skill.name} 
                  level={skill.level} 
                />
              ))}
            </div>

            {/* Soft Skills */}
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-6 text-primary-500">
                Soft Skills
              </h3>
              {softSkills.map((skill, index) => (
                <SkillBar 
                  key={index} 
                  name={skill.name} 
                  level={skill.level} 
                />
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Skills;
