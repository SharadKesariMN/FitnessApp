import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import axios from 'axios';
import { toast } from 'sonner';
import { Activity, Dumbbell, Heart, Trophy } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const SPORTS_LIST = [
  'Badminton',
  'Athletics',
  'Basketball',
  'Soccer',
  'Tennis',
  'Swimming',
  'Volleyball',
  'Cricket',
  'Running',
  'Cycling',
];

const PurposeSelectionPage = () => {
  const navigate = useNavigate();
  const [fitnessGoal, setFitnessGoal] = useState('');
  const [selectedSport, setSelectedSport] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!fitnessGoal) {
      toast.error('Please select a fitness goal');
      return;
    }

    if (fitnessGoal === 'Sports' && !selectedSport) {
      toast.error('Please select a sport');
      return;
    }

    setLoading(true);

    try {
      await axios.put(
        `${BACKEND_URL}/api/user/fitness-goal`,
        {
          fitness_goal: fitnessGoal,
          selected_sport: fitnessGoal === 'Sports' ? selectedSport : null,
        },
        { withCredentials: true }
      );

      const planResponse = await axios.post(
        `${BACKEND_URL}/api/workout/generate-plan`,
        {},
        { withCredentials: true }
      );

      toast.success('Your 45-day plan is ready!');
      navigate('/dashboard');
    } catch (error) {
      toast.error('Failed to create workout plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background py-12 px-4">
      <div className="container max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-center mb-12">
            <Activity className="w-12 h-12 text-volt-blue mx-auto mb-4" />
            <h1 className="text-4xl md:text-5xl font-heading font-black tracking-tight mb-3">
              Choose Your Path
            </h1>
            <p className="text-muted-foreground text-lg">
              Select your fitness purpose for a customized 45-day program
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <Card
              data-testid="purpose-card-hobby"
              onClick={() => setFitnessGoal('Hobby')}
              className={`cursor-pointer card-hover transition-all ${
                fitnessGoal === 'Hobby'
                  ? 'border-volt-blue border-2 shadow-lg shadow-volt-blue/20'
                  : 'border-border hover:border-volt-blue/50'
              }`}
            >
              <CardHeader className="text-center">
                <Heart className="w-12 h-12 text-volt-blue mx-auto mb-3" />
                <CardTitle className="font-heading">Hobby</CardTitle>
                <CardDescription>Beginner to Intermediate</CardDescription>
              </CardHeader>
              <CardContent className="text-center text-sm text-muted-foreground">
                <p>Easy fitness plan for casual wellness</p>
                <p className="mt-2 text-xs">30-45 min/day • 45 days</p>
              </CardContent>
            </Card>

            <Card
              data-testid="purpose-card-fitness"
              onClick={() => setFitnessGoal('Fitness')}
              className={`cursor-pointer card-hover transition-all ${
                fitnessGoal === 'Fitness'
                  ? 'border-volt-blue border-2 shadow-lg shadow-volt-blue/20'
                  : 'border-border hover:border-volt-blue/50'
              }`}
            >
              <CardHeader className="text-center">
                <Dumbbell className="w-12 h-12 text-electric-blaze mx-auto mb-3" />
                <CardTitle className="font-heading">Fitness</CardTitle>
                <CardDescription>Intermediate to Advanced</CardDescription>
              </CardHeader>
              <CardContent className="text-center text-sm text-muted-foreground">
                <p>Intensive training for serious gains</p>
                <p className="mt-2 text-xs">30-45 min/day • 45 days</p>
              </CardContent>
            </Card>

            <Card
              data-testid="purpose-card-sports"
              onClick={() => setFitnessGoal('Sports')}
              className={`cursor-pointer card-hover transition-all ${
                fitnessGoal === 'Sports'
                  ? 'border-volt-blue border-2 shadow-lg shadow-volt-blue/20'
                  : 'border-border hover:border-volt-blue/50'
              }`}
            >
              <CardHeader className="text-center">
                <Trophy className="w-12 h-12 text-volt-blue mx-auto mb-3" />
                <CardTitle className="font-heading">Sports</CardTitle>
                <CardDescription>Sport-Specific Training</CardDescription>
              </CardHeader>
              <CardContent className="text-center text-sm text-muted-foreground">
                <p>Tailored exercises for your sport</p>
                <p className="mt-2 text-xs">30-45 min/day • 45 days</p>
              </CardContent>
            </Card>
          </div>

          {fitnessGoal === 'Sports' && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              transition={{ duration: 0.3 }}
              className="mb-8"
            >
              <Card data-testid="sport-selection-card" className="border-border">
                <CardHeader>
                  <CardTitle className="font-heading">Select Your Sport</CardTitle>
                  <CardDescription>Choose the sport you want to train for</CardDescription>
                </CardHeader>
                <CardContent>
                  <Select value={selectedSport} onValueChange={setSelectedSport}>
                    <SelectTrigger data-testid="sport-select-trigger" className="w-full">
                      <SelectValue placeholder="Choose a sport" />
                    </SelectTrigger>
                    <SelectContent>
                      {SPORTS_LIST.map((sport) => (
                        <SelectItem key={sport} value={sport} data-testid={`sport-option-${sport.toLowerCase()}`}>
                          {sport}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </CardContent>
              </Card>
            </motion.div>
          )}

          <div className="text-center">
            <Button
              data-testid="generate-plan-btn"
              onClick={handleSubmit}
              disabled={loading || !fitnessGoal || (fitnessGoal === 'Sports' && !selectedSport)}
              size="lg"
              className="btn-hover bg-volt-blue hover:bg-volt-blue/90 font-bold px-12 py-6 text-lg"
            >
              {loading ? 'Creating Your Plan...' : 'Generate My 45-Day Plan'}
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PurposeSelectionPage;
