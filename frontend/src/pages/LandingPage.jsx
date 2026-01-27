import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Activity, Dumbbell, Target, TrendingUp } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const LandingPage = () => {
  const navigate = useNavigate();

  const handleGoogleLogin = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + '/dashboard';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const handleSignUp = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + '/onboarding';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const handleGuestMode = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/api/auth/guest`, {}, {
        withCredentials: true,
      });
      toast.success('Welcome! Starting as guest');
      navigate('/onboarding', { state: { user: response.data } });
    } catch (error) {
      toast.error('Failed to start guest session');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-obsidian via-background to-obsidian">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Image with Overlay */}
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: 'url(https://images.unsplash.com/photo-1728908053208-b7403ce54b6b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTJ8MHwxfHNlYXJjaHwyfHxhdGhsZXRlJTIwc3ByaW50aW5nJTIwdHJhY2slMjBkYXJrJTIwYWVzdGhldGljfGVufDB8fHx8MTc2OTUzMTg0NXww&ixlib=rb-4.1.0&q=85)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-b from-obsidian/90 via-obsidian/70 to-obsidian"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 container mx-auto px-4 pt-20 pb-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            {/* Logo/Brand */}
            <div className="mb-8 flex justify-center items-center space-x-3">
              <Activity className="w-12 h-12 text-volt-blue" />
              <h1 className="text-6xl md:text-7xl font-heading font-black tracking-tight text-white">
                FIT & FLEX
              </h1>
            </div>

            <p className="text-xl md:text-2xl text-muted-foreground mb-4 leading-relaxed">
              Your 45-Day Journey to Peak Performance
            </p>
            <p className="text-base md:text-lg text-muted-foreground/80 mb-12 max-w-2xl mx-auto">
              Personalized workout plans for every sport. No equipment needed. Start building your fitness today.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <Button
                data-testid="google-signin-btn"
                onClick={handleGoogleLogin}
                size="lg"
                className="btn-hover bg-volt-blue hover:bg-volt-blue/90 text-white font-bold px-8 py-6 text-lg rounded-full"
              >
                Sign In with Google
              </Button>
              <Button
                data-testid="google-signup-btn"
                onClick={handleSignUp}
                size="lg"
                className="btn-hover bg-electric-blaze hover:bg-electric-blaze/90 text-white font-bold px-8 py-6 text-lg rounded-full"
              >
                Sign Up for Free
              </Button>
              <Button
                data-testid="guest-mode-btn"
                onClick={handleGuestMode}
                size="lg"
                variant="outline"
                className="btn-hover border-2 border-white/20 hover:border-volt-blue text-white font-bold px-8 py-6 text-lg rounded-full"
              >
                Try as Guest
              </Button>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
                className="card-hover glass rounded-2xl p-8 border border-white/10"
                data-testid="feature-card-plans"
              >
                <Dumbbell className="w-12 h-12 text-volt-blue mb-4 mx-auto" />
                <h3 className="text-xl font-heading font-bold mb-2 text-white">Sport-Specific Plans</h3>
                <p className="text-muted-foreground text-sm">
                  Tailored exercises for badminton, athletics, basketball, and more
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.6 }}
                className="card-hover glass rounded-2xl p-8 border border-white/10"
                data-testid="feature-card-tracking"
              >
                <Target className="w-12 h-12 text-electric-blaze mb-4 mx-auto" />
                <h3 className="text-xl font-heading font-bold mb-2 text-white">Progress Tracking</h3>
                <p className="text-muted-foreground text-sm">
                  Monitor your journey day by day with detailed insights
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.6 }}
                className="card-hover glass rounded-2xl p-8 border border-white/10"
                data-testid="feature-card-ai"
              >
                <TrendingUp className="w-12 h-12 text-volt-blue mb-4 mx-auto" />
                <h3 className="text-xl font-heading font-bold mb-2 text-white">AI Recommendations</h3>
                <p className="text-muted-foreground text-sm">
                  Get personalized tips based on your fitness profile
                </p>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
