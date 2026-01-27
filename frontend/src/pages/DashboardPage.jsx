import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import axios from 'axios';
import { toast } from 'sonner';
import { Activity, Calendar, Trophy, TrendingUp, Sparkles, LogOut, User, Shield, Moon, Sun } from 'lucide-react';
import { useTheme } from '@/components/ThemeProvider';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const DashboardPage = ({ user: initialUser }) => {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const [user, setUser] = useState(initialUser);
  const [progress, setProgress] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [recommendations, setRecommendations] = useState('');
  const [loadingRec, setLoadingRec] = useState(false);

  useEffect(() => {
    fetchUserData();
    fetchProgress();
    fetchAchievements();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/user/profile`, {
        withCredentials: true,
      });
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user data');
    }
  };

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/workout/progress`, {
        withCredentials: true,
      });
      setProgress(response.data);
    } catch (error) {
      console.error('Failed to fetch progress');
    }
  };

  const fetchAchievements = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/achievements/available`, {
        withCredentials: true,
      });
      setAchievements(response.data);
    } catch (error) {
      console.error('Failed to fetch achievements');
    }
  };

  const fetchAIRecommendations = async () => {
    setLoadingRec(true);
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/ai/recommendations`,
        {},
        { withCredentials: true }
      );
      setRecommendations(response.data.recommendations);
      toast.success('AI recommendations loaded!');
    } catch (error) {
      toast.error('Failed to get AI recommendations');
    } finally {
      setLoadingRec(false);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${BACKEND_URL}/api/auth/logout`, {}, { withCredentials: true });
      toast.success('Logged out successfully');
      navigate('/');
    } catch (error) {
      toast.error('Logout failed');
    }
  };

  const nextDay = progress ? progress.completed_days + 1 : 1;
  const isCompleted = progress && progress.completed_days >= 45;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="glass border-b border-border sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-volt-blue" />
            <h1 className="text-2xl font-heading font-black tracking-tight">FIT & FLEX</h1>
          </div>
          <div className="flex items-center gap-4">
            <Button
              data-testid="theme-toggle-btn"
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </Button>
            {user?.is_admin && (
              <Button
                data-testid="admin-panel-btn"
                variant="outline"
                onClick={() => navigate('/admin')}
              >
                <Shield className="w-4 h-4 mr-2" />
                Admin
              </Button>
            )}
            <Button
              data-testid="profile-btn"
              variant="outline"
              onClick={() => navigate('/profile')}
            >
              <User className="w-4 h-4 mr-2" />
              Profile
            </Button>
            <Button
              data-testid="logout-btn"
              variant="ghost"
              onClick={handleLogout}
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Welcome Section */}
          <div className="mb-12">
            <h2 className="text-4xl md:text-5xl font-heading font-black tracking-tight mb-2">
              Welcome back, {user?.name?.split(' ')[0]}!
            </h2>
            <p className="text-muted-foreground text-lg">
              {user?.fitness_goal} • {user?.selected_sport || 'General Fitness'}
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            <Card data-testid="progress-card" className="card-hover border-border">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Progress</CardTitle>
                <TrendingUp className="w-5 h-5 text-volt-blue" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-heading font-black mb-2">
                  {progress?.completed_days || 0}/45
                </div>
                <Progress value={progress?.progress_percentage || 0} className="mb-2" />
                <p className="text-xs text-muted-foreground">
                  {progress?.progress_percentage?.toFixed(0) || 0}% complete
                </p>
              </CardContent>
            </Card>

            <Card data-testid="streak-card" className="card-hover border-border">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Current Streak</CardTitle>
                <Trophy className="w-5 h-5 text-electric-blaze" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-heading font-black mb-2">
                  {progress?.current_streak || 0} 🔥
                </div>
                <p className="text-xs text-muted-foreground">
                  Best: {progress?.longest_streak || 0} days
                </p>
              </CardContent>
            </Card>

            <Card data-testid="next-workout-card" className="card-hover border-border">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Next Workout</CardTitle>
                <Calendar className="w-5 h-5 text-volt-blue" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-heading font-black mb-2">
                  Day {isCompleted ? 45 : nextDay}
                </div>
                <p className="text-xs text-muted-foreground">
                  {isCompleted ? 'Program completed!' : '30-45 minutes'}
                </p>
              </CardContent>
            </Card>

            <Card data-testid="bmi-card" className="card-hover border-border">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">BMI</CardTitle>
                <Activity className="w-5 h-5 text-volt-blue" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-heading font-black mb-2">
                  {user?.bmi || 'N/A'}
                </div>
                <p className="text-xs text-muted-foreground">
                  {user?.bmi
                    ? user.bmi < 18.5
                      ? 'Underweight'
                      : user.bmi < 25
                      ? 'Normal'
                      : user.bmi < 30
                      ? 'Overweight'
                      : 'Obese'
                    : 'Not set'}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Achievements Section */}
          {achievements.length > 0 && (
            <Card data-testid="achievements-card" className="mb-12 border-border">
              <CardHeader>
                <CardTitle className="font-heading flex items-center gap-2">
                  <Trophy className="w-5 h-5 text-volt-blue" />
                  Achievements
                </CardTitle>
                <CardDescription>Your fitness milestones</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  {achievements.map((achievement) => (
                    <motion.div
                      key={achievement.name}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className={`text-center p-4 rounded-lg border-2 transition-all ${
                        achievement.earned
                          ? 'border-volt-blue bg-volt-blue/10'
                          : 'border-border bg-secondary/50 opacity-50'
                      }`}
                      data-testid={`achievement-${achievement.name.toLowerCase().replace(/\s+/g, '-')}`}
                    >
                      <div className="text-4xl mb-2">{achievement.badge}</div>
                      <p className="font-bold text-xs mb-1">{achievement.name}</p>
                      <p className="text-xs text-muted-foreground mb-2">{achievement.description}</p>
                      {!achievement.earned && (
                        <div className="mt-2">
                          <Progress value={(achievement.progress / achievement.days_required) * 100} className="h-1" />
                          <p className="text-xs text-muted-foreground mt-1">
                            {achievement.progress}/{achievement.days_required}
                          </p>
                        </div>
                      )}
                      {achievement.earned && (
                        <p className="text-xs text-volt-blue font-bold mt-2">✓ Earned</p>
                      )}
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* AI Recommendations */}
          <Card data-testid="ai-recommendations-card" className="mb-12 border-border">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="font-heading flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-volt-blue" />
                    AI Recommendations
                  </CardTitle>
                  <CardDescription>Personalized tips for your fitness journey</CardDescription>
                </div>
                <Button
                  data-testid="get-recommendations-btn"
                  onClick={fetchAIRecommendations}
                  disabled={loadingRec}
                  variant="outline"
                >
                  {loadingRec ? 'Loading...' : 'Get Tips'}
                </Button>
              </div>
            </CardHeader>
            {recommendations && (
              <CardContent>
                <div className="prose prose-sm dark:prose-invert">
                  <p className="text-muted-foreground whitespace-pre-line">{recommendations}</p>
                </div>
              </CardContent>
            )}
          </Card>

          {/* Action Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {isCompleted ? (
              <Card data-testid="completed-card" className="md:col-span-2 border-volt-blue/50 bg-volt-blue/5">
                <CardHeader className="text-center">
                  <Trophy className="w-16 h-16 text-volt-blue mx-auto mb-4" />
                  <CardTitle className="font-heading text-2xl">Congratulations!</CardTitle>
                  <CardDescription>You've completed the 45-day program!</CardDescription>
                </CardHeader>
                <CardContent className="text-center">
                  <Button
                    data-testid="unlock-features-btn"
                    size="lg"
                    className="btn-hover bg-volt-blue hover:bg-volt-blue/90 font-bold"
                  >
                    Unlock More Features (Coming Soon)
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <Card
                data-testid="start-workout-card"
                className="card-hover border-border cursor-pointer"
                onClick={() => navigate(`/workout/day/${nextDay}`)}
              >
                <CardHeader>
                  <CardTitle className="font-heading text-xl">Start Today's Workout</CardTitle>
                  <CardDescription>Day {nextDay} • 30-45 minutes</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    data-testid="start-workout-btn"
                    size="lg"
                    className="w-full btn-hover bg-volt-blue hover:bg-volt-blue/90 font-bold"
                  >
                    Start Workout
                  </Button>
                </CardContent>
              </Card>
            )}

            <Card data-testid="browse-days-card" className="card-hover border-border">
              <CardHeader>
                <CardTitle className="font-heading text-xl">Browse All Days</CardTitle>
                <CardDescription>View your complete 45-day program</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {Array.from({ length: 45 }, (_, i) => i + 1).slice(0, 15).map((day) => (
                    <Button
                      key={day}
                      data-testid={`day-btn-${day}`}
                      variant="outline"
                      size="sm"
                      onClick={() => navigate(`/workout/day/${day}`)}
                      className="w-12 h-12"
                    >
                      {day}
                    </Button>
                  ))}
                  <Button
                    variant="outline"
                    size="sm"
                    className="w-12 h-12"
                  >
                    ...
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default DashboardPage;
