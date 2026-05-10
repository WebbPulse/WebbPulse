import { useEffect, useState } from 'react';
import { useReducedMotion } from './useReducedMotion';

/**
 * Returns the current vertical scroll offset multiplied by `speed`.
 * Use as a translateY value for a subtle parallax effect.
 * Disabled (returns 0) under prefers-reduced-motion.
 */
export function useScrollParallax(speed: number = 0.2): number {
  const reducedMotion = useReducedMotion();
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    if (reducedMotion) {
      setOffset(0);
      return;
    }
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        setOffset(window.scrollY * speed);
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => {
      window.removeEventListener('scroll', onScroll);
      cancelAnimationFrame(raf);
    };
  }, [speed, reducedMotion]);

  return offset;
}
