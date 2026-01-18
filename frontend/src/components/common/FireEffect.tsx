"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface FireEffectProps {
    children: React.ReactNode;
    active?: boolean;
    intensity?: 'low' | 'medium' | 'high';
    className?: string;
}

/**
 * A component that wraps content with a fire/ember glow effect
 * Used to highlight fields with low confidence scores
 */
export default function FireEffect({
    children,
    active = true,
    intensity = 'medium',
    className = ''
}: FireEffectProps) {
    if (!active) {
        return <>{children}</>;
    }

    const intensityConfig = {
        low: {
            glowSize: '10px',
            pulseOpacity: [0.3, 0.5, 0.3],
            duration: 2,
        },
        medium: {
            glowSize: '15px',
            pulseOpacity: [0.4, 0.7, 0.4],
            duration: 1.5,
        },
        high: {
            glowSize: '20px',
            pulseOpacity: [0.5, 0.9, 0.5],
            duration: 1,
        },
    };

    const config = intensityConfig[intensity];

    return (
        <motion.div
            className={`relative ${className}`}
            animate={{
                boxShadow: [
                    `0 0 ${config.glowSize} rgba(255, 100, 50, ${config.pulseOpacity[0]}), 0 0 ${parseInt(config.glowSize) * 2}px rgba(255, 60, 20, ${config.pulseOpacity[0] * 0.5}), inset 0 0 ${parseInt(config.glowSize) / 2}px rgba(255, 150, 50, ${config.pulseOpacity[0] * 0.3})`,
                    `0 0 ${parseInt(config.glowSize) * 1.5}px rgba(255, 120, 50, ${config.pulseOpacity[1]}), 0 0 ${parseInt(config.glowSize) * 3}px rgba(255, 80, 30, ${config.pulseOpacity[1] * 0.5}), inset 0 0 ${parseInt(config.glowSize)}px rgba(255, 180, 80, ${config.pulseOpacity[1] * 0.3})`,
                    `0 0 ${config.glowSize} rgba(255, 100, 50, ${config.pulseOpacity[2]}), 0 0 ${parseInt(config.glowSize) * 2}px rgba(255, 60, 20, ${config.pulseOpacity[2] * 0.5}), inset 0 0 ${parseInt(config.glowSize) / 2}px rgba(255, 150, 50, ${config.pulseOpacity[2] * 0.3})`,
                ],
            }}
            transition={{
                duration: config.duration,
                repeat: Infinity,
                ease: 'easeInOut',
            }}
        >
            {/* Ember particles */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-xl">
                {[...Array(6)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute w-1 h-1 rounded-full"
                        style={{
                            background: `radial-gradient(circle, rgba(255,${150 + i * 20},50,1) 0%, rgba(255,${100 + i * 15},30,0.6) 50%, transparent 100%)`,
                            left: `${15 + i * 14}%`,
                            bottom: '-2px',
                        }}
                        animate={{
                            y: [-2, -20 - Math.random() * 15, -35],
                            x: [0, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 30],
                            opacity: [0, 1, 0],
                            scale: [0.5, 1, 0.3],
                        }}
                        transition={{
                            duration: 1.5 + Math.random() * 0.5,
                            repeat: Infinity,
                            delay: i * 0.2,
                            ease: 'easeOut',
                        }}
                    />
                ))}
            </div>

            {/* Content */}
            <div className="relative z-10">
                {children}
            </div>
        </motion.div>
    );
}
