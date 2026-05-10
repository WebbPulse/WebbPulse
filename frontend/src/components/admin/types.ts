export interface AdminPanelProps {
  className?: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  github_url?: string;
  live_url?: string;
  featured: boolean;
  created_at: string;
}

export interface Experience {
  id: number;
  title: string;
  company: string;
  location: string;
  period: string;
  start_date: string;
  end_date?: string;
  description: string;
  technologies: string[];
  achievements: string[];
  created_at: string;
}

export interface ProjectFormData {
  title: string;
  description: string;
  image: string;
  technologies: string[];
  github_url: string;
  live_url: string;
  featured: boolean;
}

export interface ExperienceFormData {
  title: string;
  company: string;
  location: string;
  period: string;
  start_date: string;
  end_date: string;
  description: string;
  technologies: string[];
  achievements: string[];
}

export interface BlogPostFormData {
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  read_time: string;
  category_id: number | undefined;
  published_at: string | undefined;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  read_time?: string;
  published_at?: string;
  created_at: string;
  updated_at?: string;
  category_id?: number;
  category?: {
    id: number;
    name: string;
    slug: string;
  };
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
}

export interface CategoryFormData {
  name: string;
  slug: string;
  description: string;
}

// Skill
export interface Skill {
  id: number;
  name: string;
  category: 'frontend' | 'backend' | 'devops' | 'other';
  proficiency: number;
  icon?: string;
  order: number;
  created_at: string;
}

export interface SkillFormData {
  name: string;
  category: 'frontend' | 'backend' | 'devops' | 'other';
  proficiency: number;
  icon: string;
  order: number;
}

// Education
export interface Education {
  id: number;
  degree: string;
  school: string;
  location: string;
  period: string;
  start_date: string;
  end_date?: string | null;
  description?: string | null;
  order: number;
  created_at: string;
}

export interface EducationFormData {
  degree: string;
  school: string;
  location: string;
  period: string;
  start_date: string;
  end_date: string;
  description: string;
  order: number;
}

// Certification
export interface Certification {
  id: number;
  name: string;
  issuer: string;
  issued_date: string;
  credential_url?: string | null;
  order: number;
  created_at: string;
}

export interface CertificationFormData {
  name: string;
  issuer: string;
  issued_date: string;
  credential_url: string;
  order: number;
}

// Site Content
export interface AboutValueFormData {
  title: string;
  description: string;
  icon: string;
}

export interface SiteContentFormData {
  hero_title: string;
  hero_subtitle: string;
  hero_description: string;
  about_paragraphs: string[];
  about_values: AboutValueFormData[];
  profile_image_url: string;
  resume_url: string;
  email: string;
  github_url: string;
  linkedin_url: string;
  footer_tagline: string;
}

export type AdminTab =
  | 'projects'
  | 'experience'
  | 'skills'
  | 'education'
  | 'certifications'
  | 'blog'
  | 'categories'
  | 'site-content';
