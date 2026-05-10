import React from 'react';
import type { BaseComponentProps } from '../../types';
import type { Experience as ExperienceType } from '../../services/api';
import { useExperience } from '../../hooks/useApiData';

export type ExperienceProps = BaseComponentProps;

export const Experience: React.FC<ExperienceProps> = ({ className = '' }) => {
  const { data: experienceData, loading, error } = useExperience();

  // Show loading state
  if (loading) {
    return (
      <section
        id="experience"
        className={`py-20 bg-white dark:bg-gray-900 ${className}`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-300">
              Loading experience...
            </p>
          </div>
        </div>
      </section>
    );
  }

  // Show error state
  if (error) {
    return (
      <section
        id="experience"
        className={`py-20 bg-white dark:bg-gray-900 ${className}`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-red-600 dark:text-red-400">
              Error loading experience: {error}
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section
      id="experience"
      className={`py-20 bg-white dark:bg-gray-900 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Experience
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            My professional journey and the impact I've made along the way
          </p>
        </div>

        {/* Timeline */}
        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 h-full w-0.5 bg-gray-200 dark:bg-gray-700"></div>

          {/* Experience Items */}
          <div className="space-y-12">
            {experienceData?.map((item, index) => (
              <ExperienceItem key={item.id} item={item} index={index} />
            ))}
          </div>
        </div>

        {/* Education Section */}
        <div className="mt-20">
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            Education
          </h3>
          <div className="grid md:grid-cols-2 gap-8">
            {educationData.map(education => (
              <div
                key={education.id}
                className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h4 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {education.degree}
                    </h4>
                    <p className="text-gray-600 dark:text-gray-300">
                      {education.institution}
                    </p>
                  </div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {education.period}
                  </span>
                </div>
                <p className="text-gray-700 dark:text-gray-300 mb-3">
                  {education.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Certifications */}
        <div className="mt-20">
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            Certifications
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            {certificationsData.map(cert => (
              <div
                key={cert.id}
                className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 text-center hover:shadow-md transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🏆</span>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {cert.name}
                </h4>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-3">
                  {cert.issuer}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {cert.date}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

const ExperienceItem: React.FC<{ item: ExperienceType; index: number }> = ({
  item,
  index,
}) => {
  const isEven = index % 2 === 0;

  return (
    <div
      className={`relative flex items-center ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'}`}
    >
      {/* Timeline Dot */}
      <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-4 h-4 bg-blue-500 rounded-full border-4 border-white dark:border-gray-900"></div>

      {/* Content */}
      <div
        className={`ml-12 md:ml-0 md:w-5/12 ${isEven ? 'md:mr-auto md:pr-8' : 'md:ml-auto md:pl-8'}`}
      >
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 hover:shadow-md transition-shadow duration-200">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                {item.title}
              </h3>
              <p className="text-blue-600 dark:text-blue-400 font-medium">
                {item.company}
              </p>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                {item.location}
              </p>
            </div>
            <span className="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap">
              {item.period}
            </span>
          </div>

          <p className="text-gray-700 dark:text-gray-300 mb-4">
            {item.description}
          </p>

          {/* Technologies */}
          <div className="flex flex-wrap gap-2 mb-4">
            {item.technologies.map(tech => (
              <span
                key={tech}
                className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
              >
                {tech}
              </span>
            ))}
          </div>

          {/* Achievements */}
          <ul className="space-y-2">
            {item.achievements.map((achievement, idx) => (
              <li
                key={idx}
                className="text-sm text-gray-600 dark:text-gray-300 flex items-start"
              >
                <span className="text-blue-500 mr-2 mt-1">•</span>
                {achievement}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

// Education data

// Education data
const educationData = [
  {
    id: '1',
    degree:
      'Bachelor of Science in Information Networking and Telecommunications',
    institution: 'Fort Hays State University',
    period: 'August 2018 - May 2022',
    description:
      'Focused on networking, telecommunications, and information systems. Served as President of the Advanced Technology Student Organization.',
  },
];

// Certifications data
const certificationsData = [
  {
    id: '1',
    name: 'AWS Certified Cloud Practitioner',
    issuer: 'Amazon Web Services',
    date: '2023',
  },
  {
    id: '2',
    name: 'CCNA: Switching, Routing, and Wireless Essentials',
    issuer: 'Cisco',
    date: '2022',
  },
  {
    id: '3',
    name: 'CCNA: Enterprise Networking, Security, and Automation',
    issuer: 'Cisco',
    date: '2022',
  },
  {
    id: '4',
    name: 'Microsoft Certified: Azure Fundamentals',
    issuer: 'Microsoft',
    date: '2022',
  },
];
