import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import axios from 'axios';
import { Activity, ArrowLeft, User, Mail, Calendar, Ruler, Weight, Target } from 'lucide-react';
import { useTheme } from '@/components/ThemeProvider';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const ProfilePage = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/user/profile`, {
        withCredentials: true,
      });
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch profile');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-volt-blue"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="glass border-b border-border sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Button
            data-testid="back-to-dashboard-btn"
            variant="ghost"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Dashboard
          </Button>
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-volt-blue" />
            <h1 className="text-2xl font-heading font-black tracking-tight">Profile</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container max-w-4xl mx-auto px-4 py-12">
        <div className="space-y-6">
          {/* User Info Card */}
          <Card data-testid="user-info-card" className="border-border">
            <CardHeader>
              <div className="flex items-center gap-4">
                {user?.picture ? (
                  <img
                    src={user.picture}
                    alt={user.name}
                    className="w-20 h-20 rounded-full"
                  />
                ) : (
                  <div className="w-20 h-20 rounded-full bg-volt-blue/20 flex items-center justify-center">
                    <User className="w-10 h-10 text-volt-blue" />
                  </div>
                )}
                <div>
                  <CardTitle className="font-heading text-2xl">{user?.name}</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    <Mail className="w-4 h-4" />
                    {user?.email}
                  </CardDescription>
                  {user?.is_guest && (
                    <Badge variant="outline" className="mt-2">Guest User</Badge>
                  )}
                </div>
              </div>
            </CardHeader>
          </Card>

          {/* Physical Stats */}
          <Card data-testid="physical-stats-card" className="border-border">
            <CardHeader>
              <CardTitle className="font-heading">Physical Stats</CardTitle>
              <CardDescription>Your health metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <Ruler className="w-4 h-4 text-volt-blue" />
                    Height
                  </div>
                  <p className="text-2xl font-heading font-bold">
                    {user?.height ? `${user.height} cm` : 'Not set'}
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <Weight className="w-4 h-4 text-volt-blue" />
                    Weight
                  </div>
                  <p className="text-2xl font-heading font-bold">
                    {user?.weight ? `${user.weight} kg` : 'Not set'}
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <Calendar className="w-4 h-4 text-volt-blue" />
                    Age
                  </div>
                  <p className="text-2xl font-heading font-bold">
                    {user?.age || 'Not set'}
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <Target className="w-4 h-4 text-volt-blue" />
                    BMI
                  </div>
                  <p className="text-2xl font-heading font-bold">
                    {user?.bmi || 'Not set'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Fitness Goals */}
          <Card data-testid="fitness-goals-card" className="border-border">
            <CardHeader>
              <CardTitle className="font-heading">Fitness Goals</CardTitle>
              <CardDescription>Your selected fitness path</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Goal Type</p>
                <Badge className="bg-volt-blue text-white text-base px-4 py-1">
                  {user?.fitness_goal || 'Not set'}
                </Badge>
              </div>
              {user?.selected_sport && (
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Selected Sport</p>
                  <Badge className="bg-electric-blaze text-white text-base px-4 py-1">
                    {user.selected_sport}
                  </Badge>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Account Type */}
          <Card data-testid="account-type-card" className="border-border">
            <CardHeader>
              <CardTitle className="font-heading">Account Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Account Type</span>
                <Badge variant="outline">
                  {user?.is_guest ? 'Guest' : 'Registered'}
                </Badge>
              </div>
              {user?.is_admin && (
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Role</span>
                  <Badge className="bg-electric-blaze text-white">Admin</Badge>
                </div>
              )}
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Theme</span>
                <Badge variant="outline">{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default ProfilePage;
