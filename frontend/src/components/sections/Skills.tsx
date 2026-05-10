import React from 'react';
import { GradientText } from '../common';
import { useSkills, useInViewReveal } from '../../hooks';
import type { Skill, SkillCategory } from '../../services/api';

const CATEGORY_META: Record<
  SkillCategory,
  { label: string; accent: string; glow: string; bar: string }
> = {
  frontend: {
    label: 'Frontend',
    accent: 'text-accent-cyan-400',
    glow: 'hover:shadow-glow-cyan',
    bar: 'from-accent-cyan-500 to-accent-cyan-300',
  },
  backend: {
    label: 'Backend',
    accent: 'text-accent-violet-400',
    glow: 'hover:shadow-glow-violet',
    bar: 'from-accent-violet-500 to-accent-violet-300',
  },
  devops: {
    label: 'DevOps & Infrastructure',
    accent: 'text-accent-fuchsia-400',
    glow: 'hover:shadow-glow-fuchsia',
    bar: 'from-accent-fuchsia-500 to-accent-fuchsia-300',
  },
  other: {
    label: 'Other',
    accent: 'text-surface-200',
    glow: 'hover:shadow-glow-soft',
    bar: 'from-accent-cyan-400 via-accent-violet-400 to-accent-fuchsia-400',
  },
};

const CATEGORY_ORDER: SkillCategory[] = [
  'frontend',
  'backend',
  'devops',
  'other',
];

const SkillCard: React.FC<{ skill: Skill; index: number }> = ({
  skill,
  index,
}) => {
  const meta = CATEGORY_META[skill.category];
  const { ref, isInView } = useInViewReveal<HTMLDivElement>({ threshold: 0.2 });

  return (
    <div
      ref={ref}
      style={{ animationDelay: `${(index % 8) * 60}ms` }}
      className={`group relative surface-glass rounded-2xl p-5 transition-all duration-500 hover:-translate-y-1 ${meta.glow} ${isInView ? 'animate-fade-in-up' : 'opacity-0'}`}
    >
      <div className="flex items-start justify-between">
        <span className="text-3xl" aria-hidden="true">
          {skill.icon ?? '💻'}
        </span>
        <span className={`text-xs font-medium ${meta.accent}`}>
          {skill.proficiency}%
        </span>
      </div>
      <h4 className="mt-4 font-display font-semibold text-surface-50 text-base">
        {skill.name}
      </h4>
      <div className="mt-3 h-1 w-full rounded-full bg-surface-800 overflow-hidden">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${meta.bar} transition-[width] duration-1000 ease-out`}
          style={{ width: isInView ? `${skill.proficiency}%` : '0%' }}
        />
      </div>
    </div>
  );
};

const SkillSkeletonCard: React.FC = () => (
  <div className="surface-glass rounded-2xl p-5 animate-pulse">
    <div className="flex items-center justify-between">
      <div className="w-8 h-8 bg-surface-800 rounded" />
      <div className="w-8 h-3 bg-surface-800 rounded" />
    </div>
    <div className="mt-4 h-4 bg-surface-800 rounded w-2/3" />
    <div className="mt-3 h-1 bg-surface-800 rounded w-full" />
  </div>
);

export const Skills: React.FC = () => {
  const { data, loading, error } = useSkills();
  const { ref, isInView } = useInViewReveal<HTMLDivElement>({
    threshold: 0.05,
  });

  const grouped = (data ?? []).reduce<Record<SkillCategory, Skill[]>>(
    (acc, skill) => {
      (acc[skill.category] = acc[skill.category] || []).push(skill);
      return acc;
    },
    { frontend: [], backend: [], devops: [], other: [] }
  );

  return (
    <section
      id="skills"
      className="relative py-24 sm:py-32 overflow-hidden bg-surface-950"
    >
      <div className="absolute inset-0 bg-mesh-1 opacity-40 pointer-events-none" />
      <div
        ref={ref}
        className={`relative z-10 max-w-7xl mx-auto px-6 sm:px-8 ${isInView ? 'animate-fade-in' : 'opacity-0'}`}
      >
        <div className="text-center mb-16 max-w-2xl mx-auto">
          <span className="inline-block text-xs uppercase tracking-[0.2em] text-accent-violet-400 mb-4">
            Skills
          </span>
          <h2 className="font-display text-4xl sm:text-5xl font-bold text-surface-50 mb-4">
            Tools I <GradientText as="span">work with</GradientText>
          </h2>
          <p className="text-surface-300 text-lg">
            A snapshot of my current toolkit across frontend, backend, infra,
            and the rest.
          </p>
        </div>

        {loading && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <SkillSkeletonCard key={i} />
            ))}
          </div>
        )}

        {error && !loading && (
          <p className="text-center text-surface-400">
            Couldn't load skills right now.
          </p>
        )}

        {!loading && !error && (
          <div className="space-y-14">
            {CATEGORY_ORDER.map(cat => {
              const skills = grouped[cat];
              if (!skills || skills.length === 0) return null;
              const meta = CATEGORY_META[cat];
              return (
                <div key={cat}>
                  <div className="flex items-center gap-3 mb-6">
                    <span
                      className={`text-xs uppercase tracking-[0.2em] font-medium ${meta.accent}`}
                    >
                      {meta.label}
                    </span>
                    <span className="flex-1 h-px bg-gradient-to-r from-surface-700 to-transparent" />
                    <span className="text-xs text-surface-500">
                      {skills.length}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {skills.map((skill, idx) => (
                      <SkillCard key={skill.id} skill={skill} index={idx} />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
};
